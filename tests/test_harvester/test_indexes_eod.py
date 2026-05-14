"""Tests for indexes_eod (uses date objects)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.indexes_eod import build_indexes_eod
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["^GSPC"])
    m.cached_client = MagicMock()
    m.cached_client.indexes = MagicMock()
    m.cached_client.indexes.historical_price_eod_full = AsyncMock(return_value=[])
    return m


class TestIndexesEod:
    @pytest.mark.asyncio
    async def test_uses_date_objects(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_indexes_eod(cfg, manager)
        await h.run_cycle()
        call = manager.cached_client.indexes.historical_price_eod_full.await_args_list[0]
        assert isinstance(call.args[1], date)
        assert isinstance(call.args[2], date)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "indexes_eod" in _REGISTRY
