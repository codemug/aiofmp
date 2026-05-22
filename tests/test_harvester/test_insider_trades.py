"""Tests for insider_trades category (P2 global walk, per-symbol shard)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.insider_trades import build_insider_trades
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _trade(symbol: str, d: str) -> dict[str, Any]:
    return {"symbol": symbol, "filingDate": d, "transactionType": "P-Purchase"}


@pytest_asyncio.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.config.plan = "premium"  # avoid plan-aware paywall filters in unit tests
    m.fmp_client = MagicMock()
    m.fmp_client.insider_trades = MagicMock()
    m.fmp_client.insider_trades.latest_insider_trades = AsyncMock()
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestInsiderTrades:
    @pytest.mark.asyncio
    async def test_first_run_walks_until_max_pages(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-01"), _trade("MSFT", "2026-05-01")],
            [_trade("AAPL", "2026-04-25"), _trade("GOOGL", "2026-04-24")],
            [],  # stops the walk
        ]
        cfg = CategoryConfig(
            enabled=True,
            interval="6h",
            extra={
                "max_pages": 10,
                "page_size": 2,
            },
        )
        h = build_insider_trades(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 3

    @pytest.mark.asyncio
    async def test_subsequent_run_stops_at_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("insider_trades", "global", "2026-04-30")
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-02")],
            [_trade("MSFT", "2026-04-25")],  # < checkpoint -> stop after this page
            [_trade("X", "2020-01-01")],
        ]
        cfg = CategoryConfig(
            enabled=True, interval="6h", extra={"page_size": 1, "max_pages": 10}
        )
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 2

    @pytest.mark.asyncio
    async def test_shards_by_symbol(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-01"), _trade("MSFT", "2026-05-01")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="6h", extra={})
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        aapl_rows = await manager.cached_client.storage.read(
            ("insider-trading/latest", "AAPL")
        )
        msft_rows = await manager.cached_client.storage.read(
            ("insider-trading/latest", "MSFT")
        )
        global_rows = await manager.cached_client.storage.read(
            ("insider-trading/latest", "_global")
        )
        assert any(r["symbol"] == "AAPL" for r in aapl_rows)
        assert any(r["symbol"] == "MSFT" for r in msft_rows)
        assert len(global_rows) == 2

    @pytest.mark.asyncio
    async def test_max_pages_safety(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.return_value = [
            _trade("AAPL", "2026-05-01")
        ]
        cfg = CategoryConfig(
            enabled=True, interval="6h", extra={"max_pages": 3, "page_size": 1}
        )
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 3

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY

        assert "insider_trades" in _REGISTRY


class TestInsiderTradesPartialPersist:
    @pytest.mark.asyncio
    async def test_mid_walk_failure_persists_earlier_pages(self, manager) -> None:
        """When page N raises, pages 0..N-1 should still be persisted."""
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-01")],
            [_trade("MSFT", "2026-04-29")],
            RuntimeError("network blip"),
        ]
        cfg = CategoryConfig(
            enabled=True, interval="6h", extra={"max_pages": 10, "page_size": 1}
        )
        h = build_insider_trades(cfg, manager)
        outcome = await h.run_cycle()
        # Pages 0 and 1 succeeded, page 2 raised
        aapl = await manager.cached_client.storage.read(
            ("insider-trading/latest", "AAPL")
        )
        msft = await manager.cached_client.storage.read(
            ("insider-trading/latest", "MSFT")
        )
        assert len(aapl) == 1
        assert len(msft) == 1
        assert outcome.status == RunStatus.PARTIAL
