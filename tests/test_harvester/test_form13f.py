"""Tests for form13f category (P2 global walk, per-CIK shard)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.form13f import build_form13f
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _filing(cik: str, d: str) -> dict[str, Any]:
    return {"cik": cik, "acceptedDate": d, "name": "TestFund"}


@pytest_asyncio.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.fmp_client = MagicMock()
    m.fmp_client.form13f = MagicMock()
    m.fmp_client.form13f.latest_filings = AsyncMock()
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestForm13F:
    @pytest.mark.asyncio
    async def test_walks_until_empty(self, manager) -> None:
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01"), _filing("0001067900", "2026-05-01")],
            [_filing("0001067983", "2026-04-28")],
            [],
        ]
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"max_pages": 10, "page_size": 2}
        )
        h = build_form13f(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 3
        assert manager.fmp_client.form13f.latest_filings.await_count == 3

    @pytest.mark.asyncio
    async def test_stops_at_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("form13f", "global", "2026-04-29")
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01")],
            [
                _filing("0001067900", "2026-04-20")
            ],  # < checkpoint -> stop after this page
            [_filing("0001067", "2020-01-01")],
        ]
        cfg = CategoryConfig(
            enabled=True, interval="24h", extra={"page_size": 1, "max_pages": 5}
        )
        h = build_form13f(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.form13f.latest_filings.await_count == 2

    @pytest.mark.asyncio
    async def test_shards_by_cik(self, manager) -> None:
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01"), _filing("0001067900", "2026-05-01")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_form13f(cfg, manager)
        await h.run_cycle()
        berkshire = await manager.cached_client.storage.read(
            ("institutional-ownership/latest", "0001067983")
        )
        other = await manager.cached_client.storage.read(
            ("institutional-ownership/latest", "0001067900")
        )
        global_rows = await manager.cached_client.storage.read(
            ("institutional-ownership/latest", "_global")
        )
        assert len(berkshire) == 1
        assert len(other) == 1
        assert len(global_rows) == 2

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "form13f" in _REGISTRY


class TestForm13FPartialPersist:
    @pytest.mark.asyncio
    async def test_mid_walk_failure_persists_earlier_pages(self, manager) -> None:
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01")],
            RuntimeError("blip"),
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"max_pages": 5, "page_size": 1})
        h = build_form13f(cfg, manager)
        outcome = await h.run_cycle()
        berk = await manager.cached_client.storage.read(("institutional-ownership/latest", "0001067983"))
        assert len(berk) == 1
        assert outcome.status == RunStatus.PARTIAL
