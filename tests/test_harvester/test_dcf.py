"""Tests for dcf category (P4 snapshot overwrite)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.dcf import build_dcf
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest_asyncio.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.config.plan = "premium"  # avoid plan-aware paywall filters in unit tests
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.fmp_client = MagicMock()
    m.fmp_client.dcf = MagicMock()
    m.fmp_client.dcf.dcf_valuation = AsyncMock(
        return_value=[{"symbol": "AAPL", "dcf": 147.27}]
    )
    m.fmp_client.dcf.levered_dcf = AsyncMock(
        return_value=[{"symbol": "AAPL", "dcf": 150.10}]
    )
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestDcf:
    @pytest.mark.asyncio
    async def test_default_endpoints(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_dcf(cfg, manager)
        outcome = await h.run_cycle()
        # 2 symbols * 2 endpoints
        assert outcome.items_attempted == 4
        manager.catalog.symbols.assert_awaited_with("financial_symbols")

        ss = SnapshotStore(manager.cached_client.storage)
        row = await ss.read("discounted-cash-flow", "AAPL")
        assert row is not None
        assert row["dcf"] == 147.27
        row2 = await ss.read("levered-discounted-cash-flow", "AAPL")
        assert row2 is not None
        assert row2["dcf"] == 150.10

    @pytest.mark.asyncio
    async def test_custom_include(self, manager) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"include": ["dcf_valuation"]}
        )
        h = build_dcf(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        manager.fmp_client.dcf.levered_dcf.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_unknown_include_raises(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"include": ["bogus"]})
        with pytest.raises(ValueError, match="bogus"):
            build_dcf(cfg, manager)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "dcf" in _REGISTRY
