"""Tests for GapFillHarvester (DRY base for P3 categories)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


@pytest.fixture
def catalog() -> MagicMock:
    cat = MagicMock()
    cat.symbols = AsyncMock(return_value=["AAPL", "MSFT", "GOOGL"])
    return cat


@pytest.fixture
def cached_client() -> MagicMock:
    """A fake CachedClient that records each call and returns canned data."""
    cc = MagicMock()
    cc.chart = MagicMock()
    cc.chart.historical_price_full = AsyncMock(return_value=[{"date": "2025-01-15", "close": 100}])
    cc.chart.historical_price_light = AsyncMock(return_value=[{"date": "2025-01-15", "close": 100}])
    return cc


def make_harvester(
    *,
    store: StateStore,
    catalog: MagicMock,
    cached_client: MagicMock,
    extra: dict[str, Any] | None = None,
    targets: list[GapFillTarget] | None = None,
) -> GapFillHarvester:
    cfg = CategoryConfig(enabled=True, interval="1d", extra=extra or {})
    budget = BudgetTracker(store, BudgetConfig())
    retry = RetryConfig()

    if targets is None:
        targets = [
            GapFillTarget(
                category_attr="chart",
                method_name="historical_price_full",
                use_date_obj=False,
            )
        ]

    return GapFillHarvester(
        name="test_gap",
        config=cfg,
        state=store,
        budget=budget,
        retry=retry,
        symbol_catalog=catalog,
        symbol_universe="actively_trading",
        cached_client=cached_client,
        targets=targets,
        backfill_seconds=10 * 86400,  # 10 days
    )


class TestGapFillHarvester:
    @pytest.mark.asyncio
    async def test_iterates_symbols_and_calls_target(self, store, catalog, cached_client) -> None:
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 3
        assert outcome.items_succeeded == 3
        assert cached_client.chart.historical_price_full.await_count == 3

    @pytest.mark.asyncio
    async def test_uses_string_dates(self, store, catalog, cached_client) -> None:
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        await h.run_cycle()
        first_call = cached_client.chart.historical_price_full.await_args_list[0]
        # called as historical_price_full(symbol, from_date, to_date)
        assert isinstance(first_call.args[0], str)
        assert isinstance(first_call.args[1], str)
        assert isinstance(first_call.args[2], str)

    @pytest.mark.asyncio
    async def test_uses_date_objects_when_configured(self, store, catalog, cached_client) -> None:
        cached_client.indexes = MagicMock()
        cached_client.indexes.historical_price_eod_full = AsyncMock(return_value=[])
        targets = [
            GapFillTarget(
                category_attr="indexes",
                method_name="historical_price_eod_full",
                use_date_obj=True,
            )
        ]
        h = make_harvester(
            store=store, catalog=catalog, cached_client=cached_client, targets=targets
        )
        await h.run_cycle()
        first_call = cached_client.indexes.historical_price_eod_full.await_args_list[0]
        assert isinstance(first_call.args[1], date)
        assert isinstance(first_call.args[2], date)

    @pytest.mark.asyncio
    async def test_per_symbol_error_does_not_kill_cycle(self, store, catalog, cached_client) -> None:
        cached_client.chart.historical_price_full = AsyncMock(
            side_effect=[
                [{"date": "2025-01-15"}],
                RuntimeError("symbol explodes"),
                [{"date": "2025-01-15"}],
            ]
        )
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.PARTIAL
        assert outcome.items_attempted == 3
        assert outcome.items_succeeded == 2

    @pytest.mark.asyncio
    async def test_multiple_variants(self, store, catalog, cached_client) -> None:
        targets = [
            GapFillTarget(category_attr="chart", method_name="historical_price_full", use_date_obj=False),
            GapFillTarget(category_attr="chart", method_name="historical_price_light", use_date_obj=False),
        ]
        h = make_harvester(
            store=store, catalog=catalog, cached_client=cached_client, targets=targets,
        )
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 6  # 3 symbols * 2 variants
        assert cached_client.chart.historical_price_full.await_count == 3
        assert cached_client.chart.historical_price_light.await_count == 3

    @pytest.mark.asyncio
    async def test_empty_universe_is_ok(self, store, cached_client) -> None:
        empty_catalog = MagicMock()
        empty_catalog.symbols = AsyncMock(return_value=[])
        h = make_harvester(store=store, catalog=empty_catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0
