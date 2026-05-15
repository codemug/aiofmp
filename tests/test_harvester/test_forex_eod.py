"""Tests for forex_eod."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.forex_eod import build_forex_eod
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
    m.catalog.symbols = AsyncMock(return_value=["EURUSD"])
    m.cached_client = MagicMock()
    m.cached_client.forex = MagicMock()
    m.cached_client.forex.historical_price_full = AsyncMock(return_value=[])
    return m


class TestForexEod:
    @pytest.mark.asyncio
    async def test_iterates_pairs(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_forex_eod(cfg, manager)
        outcome = await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("forex_pairs")
        assert outcome.items_attempted == 1

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "forex_eod" in _REGISTRY
