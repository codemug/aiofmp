"""Tests for the harvester state store."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "harvester.sqlite")
    s.initialize()
    return s


class TestSchema:
    def test_initialize_idempotent(self, tmp_path: Path) -> None:
        path = tmp_path / "harvester.sqlite"
        StateStore(path).initialize()
        StateStore(path).initialize()  # must not error
        assert path.exists()


class TestCategoryRuns:
    def test_record_run_lifecycle(self, store: StateStore) -> None:
        started = datetime.now(UTC)
        store.record_run_start("statements", started)
        store.record_run_finish(
            "statements",
            started,
            status=RunStatus.OK,
            items_attempted=10,
            items_succeeded=10,
            bytes_estimate=1024,
        )
        latest = store.get_latest_run("statements")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert latest.items_attempted == 10
        assert latest.items_succeeded == 10
        assert latest.bytes_estimate == 1024

    def test_get_latest_run_none(self, store: StateStore) -> None:
        assert store.get_latest_run("never_ran") is None


class TestCheckpoints:
    def test_upsert_and_get(self, store: StateStore) -> None:
        store.set_checkpoint("statements", "AAPL", "2024-12-31")
        assert store.get_checkpoint("statements", "AAPL") == "2024-12-31"
        store.set_checkpoint("statements", "AAPL", "2025-01-15")
        assert store.get_checkpoint("statements", "AAPL") == "2025-01-15"

    def test_missing_checkpoint(self, store: StateStore) -> None:
        assert store.get_checkpoint("statements", "MSFT") is None


class TestSymbolCatalog:
    def test_upsert_and_list(self, store: StateStore) -> None:
        store.upsert_symbol("financial_symbols", "AAPL", {"name": "Apple"})
        store.upsert_symbol("financial_symbols", "MSFT", {"name": "Microsoft"})
        symbols = store.list_symbols("financial_symbols")
        assert set(symbols) == {"AAPL", "MSFT"}

    def test_replace_universe(self, store: StateStore) -> None:
        store.upsert_symbol("commodities", "GCUSD", {})
        store.replace_universe("commodities", [("CLUSD", {}), ("SIUSD", {})])
        assert set(store.list_symbols("commodities")) == {"CLUSD", "SIUSD"}

    def test_refresh_timestamp(self, store: StateStore) -> None:
        assert store.get_last_refresh("indexes") is None
        ts = datetime.now(UTC)
        store.set_last_refresh("indexes", ts)
        got = store.get_last_refresh("indexes")
        assert got is not None
        assert abs((got - ts).total_seconds()) < 1


class TestBandwidthLedger:
    def test_add_and_get(self, store: StateStore) -> None:
        store.add_bytes("2026-05", "statements", 1024)
        store.add_bytes("2026-05", "statements", 2048)
        store.add_bytes("2026-05", "news", 512)
        store.add_bytes("2026-04", "statements", 9999)
        assert store.get_month_bytes("2026-05") == 1024 + 2048 + 512
        assert store.get_category_month_bytes("2026-05", "statements") == 3072
        assert store.get_month_bytes("2026-04") == 9999
