"""Tests for SnapshotStore (P4 snapshot-overwrite pattern)."""

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage


@pytest_asyncio.fixture
async def storage(tmp_path: Path) -> ParquetStorage:
    s = ParquetStorage(tmp_path)
    await s.initialize()
    return s


class TestSnapshotStore:
    @pytest.mark.asyncio
    async def test_write_and_read_single_row(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("discounted-cash-flow", "AAPL", {"symbol": "AAPL", "dcf": 147.27, "Stock Price": 231.79})
        row = await ss.read("discounted-cash-flow", "AAPL")
        assert row is not None
        assert row["symbol"] == "AAPL"
        assert row["dcf"] == 147.27

    @pytest.mark.asyncio
    async def test_write_overwrites_previous(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("ratings-snapshot", "AAPL", {"symbol": "AAPL", "rating": "A-", "score": 4})
        await ss.write("ratings-snapshot", "AAPL", {"symbol": "AAPL", "rating": "A", "score": 5})
        row = await ss.read("ratings-snapshot", "AAPL")
        assert row is not None
        assert row["rating"] == "A"
        assert row["score"] == 5

    @pytest.mark.asyncio
    async def test_read_missing_returns_none(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        assert await ss.read("ratings-snapshot", "ZZZ") is None

    @pytest.mark.asyncio
    async def test_write_empty_dict_skipped(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("ratings-snapshot", "AAPL", {})
        assert await ss.read("ratings-snapshot", "AAPL") is None

    @pytest.mark.asyncio
    async def test_list_entities(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("discounted-cash-flow", "AAPL", {"x": 1})
        await ss.write("discounted-cash-flow", "MSFT", {"x": 2})
        await ss.write("levered-discounted-cash-flow", "AAPL", {"x": 3})
        entities = await ss.list_entities("discounted-cash-flow")
        assert set(entities) == {"AAPL", "MSFT"}
        entities2 = await ss.list_entities("levered-discounted-cash-flow")
        assert set(entities2) == {"AAPL"}
