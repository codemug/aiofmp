"""Tests for commodities_eod."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.commodities_eod import build_commodities_eod
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["GCUSD", "CLUSD"])
    m.cached_client = MagicMock()
    m.cached_client.commodity = MagicMock()
    m.cached_client.commodity.historical_price_full = AsyncMock(return_value=[])
    return m


class TestCommoditiesEod:
    @pytest.mark.asyncio
    async def test_iterates_commodities(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_commodities_eod(cfg, manager)
        outcome = await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("commodities")
        assert outcome.items_attempted == 2
        assert manager.cached_client.commodity.historical_price_full.await_count == 2

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "commodities_eod" in _REGISTRY
