"""Parquet file storage backend for the cached client."""

import json
import logging
import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from .base import StorageBackend, StoredRangeMetadata

logger = logging.getLogger(__name__)

#: Largest integer that round-trips exactly through IEEE 754 double precision
#: (the type pyarrow falls back to for mixed int+float or int+null columns).
#: pyarrow raises `Integer value N is outside the range exactly representable
#: by a IEEE 754 double precision value` for any int with magnitude above this.
_SAFE_INT_FOR_DOUBLE = 2**53


def _sanitize_records_for_parquet(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Pre-process records so ``pa.Table.from_pylist`` accepts them.

    Three classes of FMP-side data hazards are handled:

    1. **Ints outside the float64-safe range** (``|x| > 2^53``).
       ``pa.Table.from_pylist`` infers ``double`` for any numeric column
       that includes a float or None. float64 only represents integers
       exactly up to 2^53. Any such column gets stringified across all
       rows so pyarrow stores it as a string column instead.

    2. **Mixed string + numeric across rows** in the same column.
       This happens on **append**: a previous batch sanitized a column
       to string (because of an unsafe int), the row got written to
       parquet as string, then a fresh batch arrives with only normal
       ints in that field. The merged record list has both strings and
       ints, pyarrow infers string from the first non-null value, then
       raises ``Expected bytes, got a 'int' object`` on the next row.
       Detect this directly and stringify the whole column for
       consistency.

    3. **Empty struct (dict with no keys)**.
       Some FMP endpoints (e.g. ``revenue_geographic_segmentation``)
       return ``{"data": {}}`` for symbols with no breakdown. pyarrow
       infers a struct type from the dict but has no fields to write,
       raising ``Cannot write struct type 'X' with no child field to
       Parquet``. Replace empty dicts with ``None`` so pyarrow can
       still infer the struct shape from non-empty rows.

    The original source list is never mutated. When no transformation
    is needed (the common case), the input list is returned unchanged.
    """
    if not records:
        return records

    type_set: dict[str, set[type]] = {}
    has_unsafe_int: dict[str, bool] = {}
    has_empty_dict: dict[str, bool] = {}

    for r in records:
        for k, v in r.items():
            if v is None:
                continue
            type_set.setdefault(k, set()).add(type(v))
            if (
                isinstance(v, int)
                and not isinstance(v, bool)
                and abs(v) > _SAFE_INT_FOR_DOUBLE
            ):
                has_unsafe_int[k] = True
            if isinstance(v, dict) and not v:
                has_empty_dict[k] = True

    bad_columns: set[str] = set()
    for col, types in type_set.items():
        if has_unsafe_int.get(col):
            bad_columns.add(col)
            continue
        # Mixed string + numeric (int and/or float, ignoring bool) → stringify.
        has_str = str in types
        has_num = int in types or float in types
        if has_str and has_num:
            bad_columns.add(col)

    if not bad_columns and not has_empty_dict:
        return records

    if bad_columns:
        logger.debug(
            "ParquetStorage: stringifying %d column(s): %s",
            len(bad_columns),
            sorted(bad_columns),
        )
    if has_empty_dict:
        logger.debug(
            "ParquetStorage: nulling empty-dict values in %d column(s): %s",
            len(has_empty_dict),
            sorted(has_empty_dict),
        )

    sanitized: list[dict[str, Any]] = []
    for r in records:
        new_r = dict(r)
        for col in bad_columns:
            if col in new_r and new_r[col] is not None:
                new_r[col] = str(new_r[col])
        for col in has_empty_dict:
            if col in new_r and isinstance(new_r[col], dict) and not new_r[col]:
                new_r[col] = None
        sanitized.append(new_r)
    return sanitized


def _key_to_path(base_dir: Path, key: tuple[str, ...]) -> Path:
    """Convert a storage key tuple to a filesystem directory path.

    Forward slashes in key parts are replaced with double underscores.
    Keys with no entity parts use a '_global' subdirectory.
    """
    parts: list[str] = []
    for part in key:
        sanitized = str(part).replace("/", "__").replace("\\", "__")
        parts.append(sanitized)
    if len(parts) == 1:
        parts.append("_global")
    return base_dir / "cachedclient_data" / Path(*parts)


class ParquetStorage(StorageBackend):
    """Local Parquet file storage backend.

    Stores one Parquet file + metadata sidecar per (endpoint, entity) key.

    Directory layout::

        {base_dir}/cachedclient_data/
          historical-price-eod__full/
            AAPL/
              data.parquet
              metadata.json
    """

    def __init__(self, base_dir: str | Path) -> None:
        self._base_dir = Path(base_dir)

    async def initialize(self) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)

    async def close(self) -> None:
        pass  # No resources to clean up for local files

    def _data_path(self, key: tuple[str, ...]) -> Path:
        return _key_to_path(self._base_dir, key) / "data.parquet"

    def _meta_path(self, key: tuple[str, ...]) -> Path:
        return _key_to_path(self._base_dir, key) / "metadata.json"

    async def get_stored_range(
        self, key: tuple[str, ...]
    ) -> StoredRangeMetadata | None:
        meta_path = self._meta_path(key)
        if not meta_path.exists():
            return None
        try:
            meta_dict = json.loads(meta_path.read_text())
            return StoredRangeMetadata(
                min_date=date.fromisoformat(meta_dict["min_date"]),
                max_date=date.fromisoformat(meta_dict["max_date"]),
                record_count=meta_dict["record_count"],
                last_updated=date.fromisoformat(meta_dict["last_updated"]),
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning("Failed to read metadata for key %s: %s", key, e)
            return None

    async def read(
        self,
        key: tuple[str, ...],
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        data_path = self._data_path(key)
        if not data_path.exists():
            return []

        # Guard against zero-byte parquet files left by an interrupted/failed
        # write (e.g. a 429 mid-flush, or a process kill between pq.write_table
        # and fsync). Treat them as "nothing stored" so subsequent harvest
        # cycles can re-populate, and clean up the stale file.
        try:
            if data_path.stat().st_size == 0:
                logger.warning(
                    "ParquetStorage: removing 0-byte parquet at %s (likely interrupted write)",
                    data_path,
                )
                data_path.unlink(missing_ok=True)
                return []
        except OSError as e:
            logger.warning("ParquetStorage: stat failed for %s: %s", data_path, e)
            return []

        try:
            table = pq.read_table(data_path)
        except Exception as e:
            # Last-resort guard for any other corruption (truncated trailer,
            # malformed footer). Same treatment: drop the file and refetch.
            logger.warning(
                "ParquetStorage: failed to read %s (%s); removing and refetching",
                data_path,
                e,
            )
            data_path.unlink(missing_ok=True)
            return []
        rows = table.to_pylist()

        if from_date is not None or to_date is not None:
            # Determine the date field from metadata
            meta_path = self._meta_path(key)
            date_field = "date"
            if meta_path.exists():
                try:
                    meta_dict = json.loads(meta_path.read_text())
                    date_field = meta_dict.get("date_field", "date")
                except (json.JSONDecodeError, KeyError):
                    pass
            rows = _filter_by_date(rows, date_field, from_date, to_date)

        return rows

    async def write(
        self,
        key: tuple[str, ...],
        records: list[dict[str, Any]],
        date_field: str = "date",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        if not records:
            return

        data_path = self._data_path(key)
        data_path.parent.mkdir(parents=True, exist_ok=True)

        safe_records = _sanitize_records_for_parquet(records)
        table = pa.Table.from_pylist(safe_records)

        # Write to a sibling .tmp file first, then atomically rename. This
        # prevents the cache from ever observing a half-written or 0-byte
        # parquet — a previous bug where mid-flush interruption left the
        # final path corrupted and subsequent reads errored out.
        tmp_path = data_path.with_suffix(data_path.suffix + ".tmp")
        try:
            pq.write_table(table, tmp_path, compression="snappy")
            tmp_path.replace(data_path)
        finally:
            # If write_table raised before replace, clean up the partial tmp.
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass

        _write_metadata(self._meta_path(key), records, date_field)

    async def append(
        self,
        key: tuple[str, ...],
        records: list[dict[str, Any]],
        date_field: str = "date",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        if not records:
            return

        existing = await self.read(key)

        # Deduplicate by date field
        seen_dates = {r.get(date_field) for r in existing}
        new_records = [r for r in records if r.get(date_field) not in seen_dates]

        merged = existing + new_records
        await self.write(key, merged, date_field, date_format)

    async def delete(self, key: tuple[str, ...]) -> None:
        dir_path = _key_to_path(self._base_dir, key)
        if dir_path.exists():
            shutil.rmtree(dir_path)

    async def list_keys(
        self, prefix: tuple[str, ...] | None = None
    ) -> list[tuple[str, ...]]:
        data_root = self._base_dir / "cachedclient_data"
        if not data_root.exists():
            return []

        keys: list[tuple[str, ...]] = []
        for parquet_path in data_root.rglob("data.parquet"):
            # Convert path back to key tuple
            rel = parquet_path.parent.relative_to(data_root)
            parts = list(rel.parts)
            # Reverse sanitization: double underscores back to forward slashes
            restored = []
            for p in parts:
                if p == "_global":
                    continue
                restored.append(p.replace("__", "/"))
            key = tuple(restored)
            if prefix is not None and not key[: len(prefix)] == prefix:
                continue
            keys.append(key)

        return keys


def _filter_by_date(
    rows: list[dict[str, Any]],
    date_field: str,
    from_date: date | None,
    to_date: date | None,
) -> list[dict[str, Any]]:
    """Filter rows by date range using the specified date field."""
    filtered: list[dict[str, Any]] = []
    for r in rows:
        d = r.get(date_field)
        if d is None:
            filtered.append(r)
            continue
        try:
            row_date = date.fromisoformat(str(d)[:10])
        except (ValueError, TypeError):
            filtered.append(r)
            continue
        if from_date and row_date < from_date:
            continue
        if to_date and row_date > to_date:
            continue
        filtered.append(r)
    return filtered


def _write_metadata(
    meta_path: Path,
    records: list[dict[str, Any]],
    date_field: str,
) -> None:
    """Write a metadata.json sidecar file."""
    dates: list[date] = []
    for r in records:
        d = r.get(date_field)
        if d is not None:
            try:
                parsed = date.fromisoformat(str(d)[:10])
                dates.append(parsed)
            except (ValueError, TypeError):
                continue

    if not dates:
        return

    meta = {
        "min_date": min(dates).isoformat(),
        "max_date": max(dates).isoformat(),
        "record_count": len(records),
        "last_updated": date.today().isoformat(),
        "date_field": date_field,
    }
    meta_path.write_text(json.dumps(meta, indent=2))
