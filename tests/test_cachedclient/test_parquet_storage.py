"""Tests for the Parquet storage backend."""

from datetime import date
from pathlib import Path

import pytest

from aiofmp.cachedclient.storage.parquet import ParquetStorage, _key_to_path


@pytest.fixture
def storage(tmp_path: Path) -> ParquetStorage:
    return ParquetStorage(base_dir=tmp_path)


@pytest.fixture
def sample_records() -> list[dict]:
    return [
        {"date": "2024-01-02", "symbol": "AAPL", "close": 185.64, "volume": 82488800},
        {"date": "2024-01-03", "symbol": "AAPL", "close": 184.25, "volume": 58414500},
        {"date": "2024-01-04", "symbol": "AAPL", "close": 181.91, "volume": 71983600},
        {"date": "2024-01-05", "symbol": "AAPL", "close": 181.18, "volume": 62303300},
    ]


class TestKeyToPath:
    def test_simple_key(self, tmp_path: Path):
        path = _key_to_path(tmp_path, ("income-statement", "AAPL", "annual"))
        assert (
            path
            == tmp_path / "cachedclient_data" / "income-statement" / "AAPL" / "annual"
        )

    def test_key_with_slashes(self, tmp_path: Path):
        path = _key_to_path(tmp_path, ("historical-price-eod/full", "AAPL"))
        assert (
            path
            == tmp_path / "cachedclient_data" / "historical-price-eod__full" / "AAPL"
        )

    def test_single_part_key_uses_global(self, tmp_path: Path):
        path = _key_to_path(tmp_path, ("treasury-rates",))
        assert path == tmp_path / "cachedclient_data" / "treasury-rates" / "_global"


class TestParquetStorageWriteAndRead:
    @pytest.mark.asyncio
    async def test_write_and_read(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("historical-price-eod/full", "AAPL")
        await storage.write(key, sample_records)

        result = await storage.read(key)
        assert len(result) == 4
        assert result[0]["symbol"] == "AAPL"

    @pytest.mark.asyncio
    async def test_read_nonexistent_key(self, storage: ParquetStorage):
        await storage.initialize()
        result = await storage.read(("nonexistent", "KEY"))
        assert result == []

    @pytest.mark.asyncio
    async def test_write_empty_records(self, storage: ParquetStorage):
        await storage.initialize()
        key = ("test", "empty")
        await storage.write(key, [])
        result = await storage.read(key)
        assert result == []

    @pytest.mark.asyncio
    async def test_read_with_date_filter(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("historical-price-eod/full", "AAPL")
        await storage.write(key, sample_records)

        result = await storage.read(
            key, from_date=date(2024, 1, 3), to_date=date(2024, 1, 4)
        )
        assert len(result) == 2
        dates = [r["date"] for r in result]
        assert "2024-01-03" in dates
        assert "2024-01-04" in dates

    @pytest.mark.asyncio
    async def test_read_with_from_date_only(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("test", "AAPL")
        await storage.write(key, sample_records)

        result = await storage.read(key, from_date=date(2024, 1, 4))
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_read_with_to_date_only(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("test", "AAPL")
        await storage.write(key, sample_records)

        result = await storage.read(key, to_date=date(2024, 1, 3))
        assert len(result) == 2


class TestParquetStorageMetadata:
    @pytest.mark.asyncio
    async def test_get_stored_range(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("historical-price-eod/full", "AAPL")
        await storage.write(key, sample_records)

        meta = await storage.get_stored_range(key)
        assert meta is not None
        assert meta.min_date == date(2024, 1, 2)
        assert meta.max_date == date(2024, 1, 5)
        assert meta.record_count == 4

    @pytest.mark.asyncio
    async def test_get_stored_range_nonexistent(self, storage: ParquetStorage):
        await storage.initialize()
        meta = await storage.get_stored_range(("nonexistent", "KEY"))
        assert meta is None


class TestParquetStorageAppend:
    @pytest.mark.asyncio
    async def test_append_new_records(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("test", "AAPL")
        await storage.write(key, sample_records[:2])

        new_records = [
            {
                "date": "2024-01-08",
                "symbol": "AAPL",
                "close": 185.56,
                "volume": 59144200,
            },
        ]
        await storage.append(key, new_records)

        result = await storage.read(key)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_append_deduplicates(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        key = ("test", "AAPL")
        await storage.write(key, sample_records[:2])

        # Append with one overlapping and one new
        overlap_and_new = [
            sample_records[1],  # duplicate
            {
                "date": "2024-01-08",
                "symbol": "AAPL",
                "close": 185.56,
                "volume": 59144200,
            },
        ]
        await storage.append(key, overlap_and_new)

        result = await storage.read(key)
        assert len(result) == 3  # 2 original + 1 new (duplicate skipped)

    @pytest.mark.asyncio
    async def test_append_to_nonexistent_key(self, storage: ParquetStorage):
        await storage.initialize()
        key = ("test", "NEW")
        records = [{"date": "2024-01-02", "value": 100}]
        await storage.append(key, records)

        result = await storage.read(key)
        assert len(result) == 1


class TestParquetStorageDelete:
    @pytest.mark.asyncio
    async def test_delete(self, storage: ParquetStorage, sample_records: list[dict]):
        await storage.initialize()
        key = ("test", "AAPL")
        await storage.write(key, sample_records)
        assert len(await storage.read(key)) == 4

        await storage.delete(key)
        assert await storage.read(key) == []
        assert await storage.get_stored_range(key) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, storage: ParquetStorage):
        await storage.initialize()
        await storage.delete(("nonexistent", "KEY"))


class TestParquetStorageListKeys:
    @pytest.mark.asyncio
    async def test_list_keys(self, storage: ParquetStorage, sample_records: list[dict]):
        await storage.initialize()
        await storage.write(("endpoint-a", "SYM1"), sample_records)
        await storage.write(("endpoint-a", "SYM2"), sample_records)
        await storage.write(("endpoint-b", "SYM1"), sample_records)

        keys = await storage.list_keys()
        assert len(keys) == 3

    @pytest.mark.asyncio
    async def test_list_keys_with_prefix(
        self, storage: ParquetStorage, sample_records: list[dict]
    ):
        await storage.initialize()
        await storage.write(("endpoint-a", "SYM1"), sample_records)
        await storage.write(("endpoint-a", "SYM2"), sample_records)
        await storage.write(("endpoint-b", "SYM1"), sample_records)

        keys = await storage.list_keys(prefix=("endpoint-a",))
        assert len(keys) == 2

    @pytest.mark.asyncio
    async def test_list_keys_empty(self, storage: ParquetStorage):
        await storage.initialize()
        keys = await storage.list_keys()
        assert keys == []


class TestSanitizeRecordsForParquet:
    """Stringify columns containing ints > 2^53 to avoid pyarrow IEEE 754 errors."""

    def _sanitize(self, records):
        from aiofmp.cachedclient.storage.parquet import _sanitize_records_for_parquet

        return _sanitize_records_for_parquet(records)

    def test_records_without_unsafe_ints_pass_through(self):
        records = [
            {"date": "2024-01-02", "close": 185.64, "volume": 82488800},
            {"date": "2024-01-03", "close": 184.25, "volume": 58414500},
        ]
        # Identity: no copy, no mutation.
        assert self._sanitize(records) is records

    def test_int_exactly_at_safe_boundary_unchanged(self):
        # 2**53 is the largest exactly-representable double-precision int.
        safe = 2**53
        records = [{"x": safe}, {"x": safe - 1}]
        assert self._sanitize(records) is records

    def test_int_above_safe_range_stringifies_whole_column(self):
        records = [
            {"symbol": "BINI", "marketCap": 10124999524352000, "close": 1.23},
            {"symbol": "AAPL", "marketCap": 3000000000000, "close": 200.0},
        ]
        out = self._sanitize(records)
        # marketCap column was stringified across ALL rows (consistent type).
        assert out[0]["marketCap"] == "10124999524352000"
        assert out[1]["marketCap"] == "3000000000000"
        # Other columns untouched.
        assert out[0]["symbol"] == "BINI"
        assert out[0]["close"] == 1.23
        # Source records weren't mutated.
        assert records[0]["marketCap"] == 10124999524352000

    def test_large_negative_int_also_triggers(self):
        records = [{"growth": -18557253521126760}, {"growth": -1.5}]
        out = self._sanitize(records)
        assert out[0]["growth"] == "-18557253521126760"
        assert out[1]["growth"] == "-1.5"  # float coerced to str too for consistency

    def test_none_values_stay_none(self):
        records = [
            {"x": 10000000000000000000, "y": None},  # x > 2^53
            {"x": None, "y": None},
        ]
        out = self._sanitize(records)
        assert out[0]["x"] == "10000000000000000000"
        assert out[1]["x"] is None  # None stays None, not stringified
        assert out[0]["y"] is None
        assert out[1]["y"] is None

    def test_bool_not_treated_as_int(self):
        # bool is a subclass of int in Python; the sanitizer must not stringify it
        # when no other value in the column trips the threshold.
        records = [{"flag": True}, {"flag": False}]
        assert self._sanitize(records) is records

    def test_empty_input(self):
        assert self._sanitize([]) == []

    @pytest.mark.asyncio
    async def test_write_succeeds_with_oversized_int(self, storage: ParquetStorage):
        """End-to-end: a record FMP-style with a huge int can be written + read back."""
        await storage.initialize()
        # The shape mirrors a real failure: one row has a huge int, another row
        # has a float in the same column. Without sanitization, pyarrow would
        # infer double and reject the huge int.
        records = [
            {
                "symbol": "BINI",
                "date": "2026-04-30",
                "marketCap": 10124999524352000,
                "growthRevenue": 0.05,
            },
            {
                "symbol": "BINI",
                "date": "2026-04-29",
                "marketCap": 9000000000000.5,  # float — forces pyarrow to pick double
                "growthRevenue": 0.04,
            },
        ]
        await storage.write(("test-endpoint", "BINI"), records)
        read_back = await storage.read(("test-endpoint", "BINI"))
        assert len(read_back) == 2
        # marketCap is now a string column (precision preserved).
        assert read_back[0]["marketCap"] == "10124999524352000"
        # The float row got stringified too for type consistency.
        assert read_back[1]["marketCap"] == "9000000000000.5"

    def test_mixed_str_and_int_column_stringifies(self):
        # Reproduces the "Expected bytes, got a 'int' object" failure mode:
        # a previous batch sanitized the column (stored as str), a new batch
        # arrives with a normal int. Without intervention, pyarrow infers
        # string from the first row and chokes on row 2.
        records = [
            {"date": "2026-04-30", "marketCap": "10124999524352000"},
            {"date": "2026-04-29", "marketCap": 9_000_000},
        ]
        out = self._sanitize(records)
        assert out[0]["marketCap"] == "10124999524352000"
        assert out[1]["marketCap"] == "9000000"

    def test_mixed_str_and_float_column_stringifies(self):
        records = [
            {"close": "1.234"},
            {"close": 5.67},
        ]
        out = self._sanitize(records)
        assert out[0]["close"] == "1.234"
        assert out[1]["close"] == "5.67"

    def test_mixed_int_and_float_column_unchanged_when_all_safe(self):
        # int + float together without any unsafe int → pyarrow can handle it
        # as double. No stringification needed.
        records = [{"x": 5}, {"x": 5.5}]
        assert self._sanitize(records) is records

    def test_empty_dict_value_nulled_out(self):
        # FMP's revenue_geographic_segmentation returns {"data": {}} for
        # symbols with no breakdown. pyarrow can't write a struct with no
        # fields; replace empties with None so the column infers from
        # non-empty rows.
        records = [
            {"symbol": "COSM", "data": {}},
            {"symbol": "AAPL", "data": {"US": 100, "EU": 50}},
        ]
        out = self._sanitize(records)
        assert out[0]["data"] is None
        assert out[1]["data"] == {"US": 100, "EU": 50}
        # Source unchanged.
        assert records[0]["data"] == {}

    def test_all_empty_dicts_all_nulled(self):
        records = [
            {"symbol": "AAA", "data": {}},
            {"symbol": "BBB", "data": {}},
        ]
        out = self._sanitize(records)
        assert out[0]["data"] is None
        assert out[1]["data"] is None

    def test_populated_dict_unchanged(self):
        records = [{"data": {"a": 1}}]
        assert self._sanitize(records) is records

    @pytest.mark.asyncio
    async def test_write_succeeds_with_mixed_str_and_int_column(
        self, storage: ParquetStorage
    ):
        """Reproduces the live ARHVF/BINI failure: a write where rows have
        both pre-stringified values and new numeric values in the same
        column. Without the sanitizer extension, pyarrow raises
        'Expected bytes, got a 'int' object'."""
        await storage.initialize()
        records = [
            {"symbol": "X", "date": "2026-01-02", "marketCap": "99999999999999999"},
            {"symbol": "X", "date": "2026-01-03", "marketCap": 1000},
            {"symbol": "X", "date": "2026-01-04", "marketCap": 2000.5},
        ]
        await storage.write(("chart-eod", "X"), records)
        read = await storage.read(("chart-eod", "X"))
        assert len(read) == 3
        assert {r["marketCap"] for r in read} == {
            "99999999999999999",
            "1000",
            "2000.5",
        }

    @pytest.mark.asyncio
    async def test_write_succeeds_with_empty_struct_column(
        self, storage: ParquetStorage
    ):
        """Reproduces the COSM/revenue_geographic_segmentation failure."""
        await storage.initialize()
        records = [
            {"symbol": "COSM", "date": "2026-01-02", "data": {}},
            {"symbol": "COSM", "date": "2026-01-03", "data": {"US": 100}},
        ]
        await storage.write(("seg", "COSM"), records)
        read = await storage.read(("seg", "COSM"))
        assert len(read) == 2
        # Empty struct is now stored as None
        empties = [r for r in read if r["data"] is None]
        assert len(empties) == 1


class TestFiveHundredRetry:
    @pytest.mark.asyncio
    async def test_5xx_then_ok_retries(self) -> None:
        """A transient FMPServerError is retried transparently by _make_request."""
        from unittest.mock import AsyncMock, MagicMock, patch

        from aiofmp.base import FMPBaseClient, FMPServerError

        client = FMPBaseClient(api_key="test", max_retries=2, retry_delay=0.001)
        # Bypass session check
        client._session = MagicMock()
        # First call: _handle_response raises FMPServerError. Second: returns data.
        call_count = {"n": 0}

        async def fake_handle(response):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise FMPServerError("Server error: 502")
            return [{"ok": True}]

        client._handle_response = fake_handle
        # Fake session context manager
        async_cm = MagicMock()
        async_cm.__aenter__ = AsyncMock(return_value=MagicMock())
        async_cm.__aexit__ = AsyncMock(return_value=None)
        client._session.get = MagicMock(return_value=async_cm)

        # Patch sleep so the 2s delay doesn't actually run
        with patch("asyncio.sleep", new=AsyncMock(return_value=None)):
            result = await client._make_request("anywhere")
        assert result == [{"ok": True}]
        assert call_count["n"] == 2  # one fail, one success
