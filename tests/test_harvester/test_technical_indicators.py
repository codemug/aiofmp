"""Tests for the technical_indicators category."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.technical_indicators import build_technical_indicators
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.config.plan = "premium"  # avoid plan-aware paywall filters in unit tests
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.cached_client = MagicMock()
    ti = MagicMock()
    ti.simple_moving_average = AsyncMock(return_value=[])
    ti.relative_strength_index = AsyncMock(return_value=[])
    m.cached_client.technical_indicators = ti
    return m


class TestTechnicalIndicators:
    @pytest.mark.asyncio
    async def test_empty_indicators_is_ok(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"indicators": []})
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0

    @pytest.mark.asyncio
    async def test_one_indicator_two_symbols(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={
                "indicators": [
                    {
                        "method": "simple_moving_average",
                        "period_length": 20,
                        "timeframe": "1day",
                    }
                ],
            },
        )
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert (
            manager.cached_client.technical_indicators.simple_moving_average.await_count
            == 2
        )
        first = manager.cached_client.technical_indicators.simple_moving_average.await_args_list[
            0
        ]
        assert first.args[0] in ("AAPL", "MSFT")  # symbol
        assert first.args[1] == 20  # period_length
        assert first.args[2] == "1day"  # timeframe
        assert isinstance(first.args[3], date)  # from_date
        assert isinstance(first.args[4], date)  # to_date

    @pytest.mark.asyncio
    async def test_multiple_indicators(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={
                "indicators": [
                    {
                        "method": "simple_moving_average",
                        "period_length": 20,
                        "timeframe": "1day",
                    },
                    {
                        "method": "relative_strength_index",
                        "period_length": 14,
                        "timeframe": "1day",
                    },
                ],
            },
        )
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 4  # 2 symbols * 2 indicators

    @pytest.mark.asyncio
    async def test_unknown_method_raises_at_build(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={
                "indicators": [
                    {"method": "moonshot", "period_length": 1, "timeframe": "1day"}
                ]
            },
        )
        with pytest.raises(ValueError, match="moonshot"):
            build_technical_indicators(cfg, manager)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "technical_indicators" in _REGISTRY
