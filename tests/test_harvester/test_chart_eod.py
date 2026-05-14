"""Tests for chart_eod category."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.categories.chart_eod import build_chart_eod
from aiofmp.harvester.config import CategoryConfig


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    """A fake manager exposing the attributes a category factory consumes."""
    from aiofmp.harvester.budget import BudgetTracker
    from aiofmp.harvester.config import BudgetConfig, RetryConfig
    from aiofmp.harvester.state import StateStore

    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL"])
    m.cached_client = MagicMock()
    m.cached_client.chart = MagicMock()
    m.cached_client.chart.historical_price_full = AsyncMock(return_value=[{"date": "2025-01-15"}])
    m.cached_client.chart.historical_price_light = AsyncMock(return_value=[])
    return m


class TestChartEod:
    @pytest.mark.asyncio
    async def test_default_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"backfill_years": 5})
        h = build_chart_eod(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 1  # 1 symbol * 1 default variant
        manager.cached_client.chart.historical_price_full.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_multiple_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"variants": ["historical_price_full", "historical_price_light"]},
        )
        h = build_chart_eod(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        manager.cached_client.chart.historical_price_full.assert_awaited_once()
        manager.cached_client.chart.historical_price_light.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_custom_symbol_universe(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"symbol_universe": "financial_symbols"},
        )
        h = build_chart_eod(cfg, manager)
        await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("financial_symbols")

    @pytest.mark.asyncio
    async def test_registers_at_import(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "chart_eod" in _REGISTRY
