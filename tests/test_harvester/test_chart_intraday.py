"""Tests for chart_intraday and its sister intraday categories."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


def _fake_manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["X"])
    m.cached_client = MagicMock()
    # Set up every (category, method) the tests touch:
    for cat in ("chart", "commodity", "forex", "indexes"):
        c = MagicMock()
        for method in ("intraday_1min", "intraday_5min", "intraday_15min", "intraday_30min",
                       "intraday_1hour", "intraday_4hour"):
            setattr(c, method, AsyncMock(return_value=[]))
        setattr(m.cached_client, cat, c)
    return m


class TestChartIntradayFamily:
    @pytest.mark.asyncio
    async def test_chart_intraday_default_timeframe(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_chart_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.cached_client.chart.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_chart_intraday_multiple_timeframes(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={"timeframes": ["1hour", "5min"]})
        h = build_chart_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.cached_client.chart.intraday_1hour.assert_awaited_once()
        mgr.cached_client.chart.intraday_5min.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_chart_intraday_invalid_timeframe_raises(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={"timeframes": ["weekly"]})
        with pytest.raises(ValueError, match="weekly"):
            build_chart_intraday(cfg, mgr)

    @pytest.mark.asyncio
    async def test_commodities_intraday(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.commodities_intraday import build_commodities_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["GCUSD"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_commodities_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("commodities")
        mgr.cached_client.commodity.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_forex_intraday(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.forex_intraday import build_forex_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["EURUSD"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_forex_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("forex_pairs")
        mgr.cached_client.forex.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_indexes_intraday_uses_date_obj(self, tmp_path: Path) -> None:
        from datetime import date
        from aiofmp.harvester.categories.indexes_intraday import build_indexes_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["^GSPC"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_indexes_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("indexes")
        first_call = mgr.cached_client.indexes.intraday_1hour.await_args_list[0]
        assert isinstance(first_call.args[1], date)
        assert isinstance(first_call.args[2], date)
