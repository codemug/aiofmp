"""Tests for analyst_estimates category (P2 per-symbol page walk)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.analyst_estimates import build_analyst_estimates
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _row(d: str) -> dict[str, Any]:
    return {"symbol": "AAPL", "date": d, "revenueAvg": 100}


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
    m.fmp_client.analyst.financial_estimates = AsyncMock()

    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestAnalystEstimates:
    @pytest.mark.asyncio
    async def test_first_run_walks_until_max_backfill(self, manager) -> None:
        today = date.today()
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row((today - timedelta(days=400)).isoformat())],
            [_row((today - timedelta(days=800)).isoformat())],
            [
                _row((today - timedelta(days=1200)).isoformat())
            ],  # > 3y backfill -> stop after this
            [],  # safety
        ]
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={
                "estimate_periods": ["annual"],
                "max_backfill_years": 3,
                "page_size": 1,
            },
        )
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()

        assert outcome.status == RunStatus.OK
        # 3 pages walked (oldest = 1200d > 3*365 = 1095, so we stop after that page)
        assert manager.fmp_client.analyst.financial_estimates.await_count == 3
        ckpt = manager.state.get_checkpoint("analyst_estimates", "AAPL/annual")
        assert ckpt is not None

    @pytest.mark.asyncio
    async def test_subsequent_run_walks_until_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("analyst_estimates", "AAPL/annual", "2024-06-01")
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2024-12-31"), _row("2024-09-30")],
            [_row("2024-07-31"), _row("2024-04-30")],  # 2024-04-30 < 2024-06-01 -> stop
        ]
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={
                "estimate_periods": ["annual"],
                "max_backfill_years": 3,
                "page_size": 2,
            },
        )
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()
        assert manager.fmp_client.analyst.financial_estimates.await_count == 2
        assert outcome.status == RunStatus.OK

    @pytest.mark.asyncio
    async def test_empty_page_stops_walk(self, manager) -> None:
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2025-01-01")],
            [],
        ]
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"estimate_periods": ["annual"]}
        )
        h = build_analyst_estimates(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.analyst.financial_estimates.await_count == 2

    @pytest.mark.asyncio
    async def test_writes_to_storage_at_expected_key(self, manager) -> None:
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2025-12-31")],
            [],
        ]
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"estimate_periods": ["annual"]}
        )
        h = build_analyst_estimates(cfg, manager)
        await h.run_cycle()
        records = await manager.cached_client.storage.read(
            ("analyst-estimates", "AAPL", "annual")
        )
        assert len(records) >= 1
        assert records[0]["date"] == "2025-12-31"

    @pytest.mark.asyncio
    async def test_per_symbol_error_does_not_stop_cycle(self, manager) -> None:
        manager.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])

        async def side_effect(symbol, period, page=0, limit=100):
            if symbol == "MSFT":
                raise RuntimeError("blown")
            return [_row("2025-12-31")] if page == 0 else []

        manager.fmp_client.analyst.financial_estimates = AsyncMock(
            side_effect=side_effect
        )
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"estimate_periods": ["annual"]}
        )
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert outcome.items_succeeded == 1
        assert outcome.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "analyst_estimates" in _REGISTRY
