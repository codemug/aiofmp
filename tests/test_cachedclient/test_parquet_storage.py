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
