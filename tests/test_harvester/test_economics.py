"""Tests for the economics category."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.economics import build_economics
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
    m.config.plan = "premium"  # avoid plan-aware paywall filters in unit tests
    m.cached_client = MagicMock()
    m.cached_client.economics = MagicMock()
    m.cached_client.economics.treasury_rates = AsyncMock(return_value=[])
    m.cached_client.economics.economic_indicators = AsyncMock(return_value=[])
    return m


class TestEconomics:
    @pytest.mark.asyncio
    async def test_default_indicators(self, manager: MagicMock) -> None:
        from aiofmp.harvester.plan import VALID_ECONOMIC_INDICATORS

        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_economics(cfg, manager)
        outcome = await h.run_cycle()
        # 1 treasury_rates call + N default indicators (FMP's actual names).
        n = len(VALID_ECONOMIC_INDICATORS)
        assert outcome.items_attempted == 1 + n
        manager.cached_client.economics.treasury_rates.assert_awaited_once()
        assert manager.cached_client.economics.economic_indicators.await_count == n

    @pytest.mark.asyncio
    async def test_custom_indicators(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"indicators": ["GDP", "CPI"], "backfill_years": 3},
        )
        h = build_economics(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 3  # treasury + 2 indicators
        names_called = [
            c.args[0]
            for c in manager.cached_client.economics.economic_indicators.await_args_list
        ]
        assert set(names_called) == {"GDP", "CPI"}

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "economics" in _REGISTRY
