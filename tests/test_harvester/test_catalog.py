"""Tests for the symbol catalog."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.catalog import SymbolCatalog
from aiofmp.harvester.state import StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def make_fake_fmp() -> MagicMock:
    fmp = MagicMock()
    fmp.directory = MagicMock()
    fmp.directory.financial_symbols = AsyncMock(
        return_value=[
            {"symbol": "AAPL", "companyName": "Apple"},
            {"symbol": "MSFT", "companyName": "MS"},
        ]
    )
    fmp.directory.actively_trading = AsyncMock(
        return_value=[{"symbol": "AAPL"}, {"symbol": "MSFT"}, {"symbol": "TSLA"}]
    )
    fmp.directory.etf_list = AsyncMock(return_value=[{"symbol": "SPY"}])

    fmp.commodity = MagicMock()
    fmp.commodity.commodities_list = AsyncMock(
        return_value=[{"symbol": "GCUSD"}, {"symbol": "CLUSD"}]
    )

    fmp.forex = MagicMock()
    fmp.forex.forex_list = AsyncMock(
        return_value=[{"symbol": "EURUSD"}, {"symbol": "GBPUSD"}]
    )

    fmp.indexes = MagicMock()
    fmp.indexes.index_list = AsyncMock(
        return_value=[{"symbol": "^GSPC"}, {"symbol": "^DJI"}]
    )
    return fmp


class TestSymbolCatalog:
    @pytest.mark.asyncio
    async def test_first_call_discovers(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        result = await catalog.symbols("financial_symbols")
        assert set(result) == {"AAPL", "MSFT"}
        fmp.directory.financial_symbols.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_second_call_uses_cache(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        await catalog.symbols("financial_symbols")
        await catalog.symbols("financial_symbols")
        fmp.directory.financial_symbols.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_stale_cache_triggers_refresh(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        # 1 second refresh
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=1)
        await catalog.symbols("financial_symbols")
        # Forge an old refresh timestamp
        store.set_last_refresh(
            "financial_symbols", datetime.now(UTC) - timedelta(hours=2)
        )
        await catalog.symbols("financial_symbols")
        assert fmp.directory.financial_symbols.await_count == 2

    @pytest.mark.asyncio
    async def test_all_six_universes(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        assert set(await catalog.symbols("financial_symbols")) == {"AAPL", "MSFT"}
        assert set(await catalog.symbols("actively_trading")) == {
            "AAPL",
            "MSFT",
            "TSLA",
        }
        assert set(await catalog.symbols("commodities")) == {"GCUSD", "CLUSD"}
        assert set(await catalog.symbols("forex_pairs")) == {"EURUSD", "GBPUSD"}
        assert set(await catalog.symbols("indexes")) == {"^GSPC", "^DJI"}
        assert set(await catalog.symbols("etf_list")) == {"SPY"}

    @pytest.mark.asyncio
    async def test_unknown_universe_raises(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        with pytest.raises(ValueError, match="unknown universe"):
            await catalog.symbols("crypto")

    @pytest.mark.asyncio
    async def test_concurrent_refresh_is_single_shot(self, store: StateStore) -> None:
        """Two parallel calls during discovery must result in one API call."""
        import asyncio

        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        await asyncio.gather(
            catalog.symbols("commodities"),
            catalog.symbols("commodities"),
            catalog.symbols("commodities"),
        )
        fmp.commodity.commodities_list.assert_awaited_once()
