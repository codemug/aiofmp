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

        table = pq.read_table(data_path)
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

        table = pa.Table.from_pylist(records)
        pq.write_table(table, data_path, compression="snappy")

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
