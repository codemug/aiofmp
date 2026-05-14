"""Tests for the harvester budget tracker."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from aiofmp.base import FMPBudgetError, current_harvest_category
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig
from aiofmp.harvester.state import StateStore

GB = 1024 ** 3


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def test_record_bytes_attributes_to_current_category(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    token = current_harvest_category.set("statements")
    try:
        tracker.record_bytes(category=current_harvest_category.get(), byte_count=1024)
    finally:
        current_harvest_category.reset(token)
    month = datetime.now(UTC).strftime("%Y-%m")
    assert store.get_category_month_bytes(month, "statements") == 1024


def test_record_bytes_none_category_attributed_to_user(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    tracker.record_bytes(category=None, byte_count=512)
    month = datetime.now(UTC).strftime("%Y-%m")
    assert store.get_category_month_bytes(month, "user") == 512


def test_is_paused_below_soft_cap(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig(monthly_soft_cap_gb=18))
    assert tracker.is_paused("statements") is False


def test_is_paused_at_soft_cap(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=1 * GB)
    assert tracker.is_paused("statements") is True


def test_is_paused_warn_only(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2, soft_cap_behavior="warn_only")
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=1 * GB)
    assert tracker.is_paused("statements") is False  # warn only — never pauses


def test_check_hard_cap_raises(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=2 * GB)
    with pytest.raises(FMPBudgetError, match="hard cap"):
        tracker.check_hard_cap("statements")


def test_check_hard_cap_only_for_harvester_categories(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="user", byte_count=2 * GB)
    # No exception even though hard cap is breached, because category is 'user'
    tracker.check_hard_cap(None)


def test_month_key_format(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    key = tracker.current_month_key()
    assert len(key) == 7 and key[4] == "-"
