"""Tests for analyst_snapshots category (P4 snapshot overwrite)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.analyst_snapshots import build_analyst_snapshots
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest_asyncio.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL"])
    m.fmp_client = MagicMock()
    m.fmp_client.analyst = MagicMock()
    m.fmp_client.analyst.ratings_snapshot = AsyncMock(
        return_value=[{"symbol": "AAPL", "rating": "A-"}]
    )
    m.fmp_client.analyst.price_target_consensus = AsyncMock(
        return_value=[{"symbol": "AAPL", "targetConsensus": 250}]
    )
    m.fmp_client.analyst.price_target_summary = AsyncMock(
        return_value=[{"symbol": "AAPL"}]
    )
    m.fmp_client.analyst.stock_grades_summary = AsyncMock(
        return_value=[{"symbol": "AAPL", "consensus": "Buy"}]
    )
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestAnalystSnapshots:
    @pytest.mark.asyncio
    async def test_default_endpoints(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        # 1 symbol * 4 default endpoints
        assert outcome.items_attempted == 4

        ss = SnapshotStore(manager.cached_client.storage)
        row = await ss.read("ratings-snapshot", "AAPL")
        assert row is not None
        assert row["rating"] == "A-"

    @pytest.mark.asyncio
    async def test_custom_endpoint_list(self, manager) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"include": ["ratings_snapshot"]}
        )
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 1
        manager.fmp_client.analyst.price_target_consensus.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_empty_response_skips_write(self, manager) -> None:
        manager.fmp_client.analyst.ratings_snapshot = AsyncMock(return_value=[])
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"include": ["ratings_snapshot"]}
        )
        h = build_analyst_snapshots(cfg, manager)
        await h.run_cycle()
        ss = SnapshotStore(manager.cached_client.storage)
        assert await ss.read("ratings-snapshot", "AAPL") is None

    @pytest.mark.asyncio
    async def test_per_endpoint_error_does_not_kill_cycle(self, manager) -> None:
        manager.fmp_client.analyst.ratings_snapshot = AsyncMock(
            side_effect=RuntimeError("boom")
        )
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"include": ["ratings_snapshot", "price_target_consensus"]},
        )
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert outcome.items_succeeded == 1
        assert outcome.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "analyst_snapshots" in _REGISTRY
