"""Tests for the statements category (P1)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.statements import (
    LIMIT_ONLY_ENDPOINTS,
    PERIOD_AND_LIMIT_ENDPOINTS,
    PERIOD_ONLY_ENDPOINTS,
    build_statements,
)
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _wire_statement_methods(stmts: MagicMock) -> None:
    for m in PERIOD_AND_LIMIT_ENDPOINTS + LIMIT_ONLY_ENDPOINTS + PERIOD_ONLY_ENDPOINTS:
        setattr(stmts, m, AsyncMock(return_value=[]))


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    # Tests use Premium so quarterly is allowed (matches the period lists below).
    m.config.plan = "premium"
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.cached_client = MagicMock()
    m.cached_client.calendar = MagicMock()
    m.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
    m.cached_client.statements = MagicMock()
    _wire_statement_methods(m.cached_client.statements)
    return m


def _expected_calls_per_symbol(periods: list[str]) -> int:
    # 10 period+limit endpoints × len(periods)
    n = len(PERIOD_AND_LIMIT_ENDPOINTS) * len(periods)
    # 1 limit-only endpoint
    n += len(LIMIT_ONLY_ENDPOINTS)
    # 2 period-only endpoints × len(periods)
    n += len(PERIOD_ONLY_ENDPOINTS) * len(periods)
    return n


class TestStatementsFirstRun:
    @pytest.mark.asyncio
    async def test_first_run_uses_initial_limit_and_full_universe(
        self, manager: MagicMock
    ) -> None:
        """With no checkpoint set, first run iterates the financial_symbols universe with initial_limit."""
        cfg = CategoryConfig(
            enabled=True,
            interval="6h",
            extra={
                "periods": ["annual", "quarter"],
                "initial_limit": 40,
                "incremental_limit": 2,
            },
        )
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        manager.catalog.symbols.assert_awaited_with("financial_symbols")
        expected = _expected_calls_per_symbol(["annual", "quarter"]) * 2  # 2 symbols
        assert outcome.items_attempted == expected
        # Verify limit=40 was passed to a period+limit endpoint
        first = manager.cached_client.statements.income_statement.await_args_list[0]
        assert first.kwargs.get("limit") == 40

    @pytest.mark.asyncio
    async def test_first_run_sets_checkpoint(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        await h.run_cycle()
        ckpt = manager.state.get_checkpoint("statements", "global")
        assert ckpt is not None
        # Looks like a date string YYYY-MM-DD
        assert len(ckpt) == 10 and ckpt[4] == "-"


class TestStatementsIncremental:
    @pytest.mark.asyncio
    async def test_uses_earnings_calendar_when_checkpoint_exists(
        self, manager: MagicMock
    ) -> None:
        manager.state.set_checkpoint("statements", "global", "2026-04-01")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(
            return_value=[
                {"symbol": "AAPL", "date": "2026-04-25"},
                {"symbol": "AAPL", "date": "2026-04-26"},  # duplicate symbol
                {"symbol": "TSLA", "date": "2026-04-28"},
            ]
        )
        cfg = CategoryConfig(
            enabled=True,
            interval="6h",
            extra={
                "periods": ["annual"],
                "incremental_limit": 2,
            },
        )
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        manager.cached_client.calendar.earnings_calendar.assert_awaited_once()
        # 2 unique symbols (AAPL, TSLA)
        expected = _expected_calls_per_symbol(["annual"]) * 2
        assert outcome.items_attempted == expected
        # Verify limit=2 was used
        first = manager.cached_client.statements.income_statement.await_args_list[0]
        assert first.kwargs.get("limit") == 2

    @pytest.mark.asyncio
    async def test_no_filings_in_window_is_noop(self, manager: MagicMock) -> None:
        manager.state.set_checkpoint("statements", "global", "2026-04-01")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0
        manager.cached_client.statements.income_statement.assert_not_awaited()


class TestStatementsSafetyNet:
    @pytest.mark.asyncio
    async def test_safety_net_triggers_after_interval(self, manager: MagicMock) -> None:
        # set an old "last safety-net" checkpoint
        manager.state.set_checkpoint(
            "statements_safetynet",
            "global",
            (datetime.now(UTC) - timedelta(days=40)).date().isoformat(),
        )
        manager.state.set_checkpoint("statements", "global", "2026-05-10")
        cfg = CategoryConfig(
            enabled=True,
            interval="6h",
            extra={
                "periods": ["annual"],
                "safety_net_interval": "30d",
            },
        )
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        # Safety-net ran: should have iterated full universe (2 symbols)
        expected = _expected_calls_per_symbol(["annual"]) * 2
        assert outcome.items_attempted == expected
        # New safety-net checkpoint should be today
        new_ckpt = manager.state.get_checkpoint("statements_safetynet", "global")
        from datetime import date

        assert new_ckpt == date.today().isoformat()

    @pytest.mark.asyncio
    async def test_safety_net_skipped_when_recent(self, manager: MagicMock) -> None:
        manager.state.set_checkpoint(
            "statements_safetynet",
            "global",
            (datetime.now(UTC) - timedelta(days=5)).date().isoformat(),
        )
        manager.state.set_checkpoint("statements", "global", "2026-05-10")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()
        # No safety net, no filings discovered → 0 attempted
        assert outcome.items_attempted == 0


class TestStatementsSafetyNetSeeding:
    @pytest.mark.asyncio
    async def test_first_run_seeds_safetynet_checkpoint(
        self, manager: MagicMock
    ) -> None:
        """After a first incremental run, the statements_safetynet checkpoint must be set
        so the 30-day timer starts."""
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        # No checkpoints set; this is the first run.
        await h.run_cycle()
        sn = manager.state.get_checkpoint("statements_safetynet", "global")
        assert sn is not None  # safety-net timer started

    @pytest.mark.asyncio
    async def test_safetynet_run_uses_separate_category_row(
        self, manager: MagicMock
    ) -> None:
        """When the safety-net fires, the category_runs row is under 'statements_safetynet'."""
        manager.state.set_checkpoint(
            "statements_safetynet",
            "global",
            (datetime.now(UTC) - timedelta(days=40)).date().isoformat(),
        )
        manager.state.set_checkpoint("statements", "global", "2026-05-10")
        cfg = CategoryConfig(
            enabled=True,
            interval="6h",
            extra={
                "periods": ["annual"],
                "safety_net_interval": "30d",
            },
        )
        h = build_statements(cfg, manager)
        await h._run_once_and_record()

        sn_run = manager.state.get_latest_run("statements_safetynet")
        assert sn_run is not None
        assert sn_run.status in (RunStatus.OK, RunStatus.PARTIAL)
        assert sn_run.items_attempted > 0


class TestRegistration:
    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "statements" in _REGISTRY
