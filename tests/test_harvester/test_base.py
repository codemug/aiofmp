"""Tests for the CategoryHarvester abstract base class."""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from aiofmp.base import FMPBudgetError, FMPRateLimitError, current_harvest_category
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    RetryConfig,
    RetryPolicy,
)
from aiofmp.harvester.state import RunStatus, StateStore


class FakeCategory(CategoryHarvester):
    """Minimal concrete subclass for testing the base class."""

    def __init__(self, name, config, store, budget, retry, *, behavior="ok"):
        super().__init__(name, config, store, budget, retry)
        self.behavior = behavior
        self.run_count = 0
        self.items = 0

    async def run_cycle(self) -> RunOutcome:
        self.run_count += 1
        if self.behavior == "ok":
            self.items += 3
            return RunOutcome(status=RunStatus.OK, items_attempted=3, items_succeeded=3)
        if self.behavior == "raise":
            raise RuntimeError("boom")
        if self.behavior == "429_then_ok":
            if self.run_count == 1:
                raise FMPRateLimitError("rl")
            return RunOutcome(status=RunStatus.OK, items_attempted=1, items_succeeded=1)
        if self.behavior == "always_429":
            raise FMPRateLimitError("rl")
        if self.behavior == "budget":
            raise FMPBudgetError("hard cap")
        raise AssertionError(f"unknown behavior {self.behavior!r}")


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def _make(store: StateStore, behavior: str = "ok"):
    config = CategoryConfig(enabled=True, interval="1s", extra={})
    budget = BudgetTracker(store, BudgetConfig())
    retry = RetryConfig(
        on_429=RetryPolicy(backoff_seconds=[0, 0], max_attempts=2),
        on_5xx=RetryPolicy(backoff_seconds=[0], max_attempts=1),
    )
    return FakeCategory("fake", config, store, budget, retry, behavior=behavior)


class TestCategoryHarvester:
    @pytest.mark.asyncio
    async def test_ok_run_records_state(self, store: StateStore) -> None:
        h = _make(store, "ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert latest.items_attempted == 3
        assert latest.items_succeeded == 3
        assert h.run_count == 1

    @pytest.mark.asyncio
    async def test_exception_marks_error(self, store: StateStore) -> None:
        h = _make(store, "raise")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.ERROR
        assert latest.error is not None and "boom" in latest.error

    @pytest.mark.asyncio
    async def test_429_then_ok_retries(self, store: StateStore) -> None:
        h = _make(store, "429_then_ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert h.run_count == 2

    @pytest.mark.asyncio
    async def test_always_429_marks_partial(self, store: StateStore) -> None:
        h = _make(store, "always_429")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_budget_error_marks_partial(self, store: StateStore) -> None:
        h = _make(store, "budget")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_sets_contextvar_during_cycle(self, store: StateStore) -> None:
        seen: list[str | None] = []

        class CaptureCategory(FakeCategory):
            async def run_cycle(self) -> RunOutcome:
                seen.append(current_harvest_category.get())
                return RunOutcome(status=RunStatus.OK)

        config = CategoryConfig(enabled=True, interval="1s", extra={})
        budget = BudgetTracker(store, BudgetConfig())
        retry = RetryConfig()
        h = CaptureCategory("fake", config, store, budget, retry)
        await h._run_once_and_record()
        assert seen == ["fake"]
        assert current_harvest_category.get() is None

    @pytest.mark.asyncio
    async def test_paused_category_skips_run(self, store: StateStore) -> None:
        cfg = CategoryConfig(enabled=True, interval="1s", extra={})
        budget_cfg = BudgetConfig(monthly_soft_cap_gb=0, monthly_hard_cap_gb=1)
        budget = BudgetTracker(store, budget_cfg)
        budget.record_bytes("fake", 1)
        retry = RetryConfig()
        h = FakeCategory("fake", cfg, store, budget, retry, behavior="ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PAUSED_FOR_BUDGET
        assert h.run_count == 0

    @pytest.mark.asyncio
    async def test_run_forever_respects_stop_event(self, store: StateStore) -> None:
        h = _make(store, "ok")
        stop_event = asyncio.Event()
        task = asyncio.create_task(h.run_forever(stop_event))
        await asyncio.sleep(0.05)
        stop_event.set()
        await asyncio.wait_for(task, timeout=2.0)
        assert h.run_count >= 1
