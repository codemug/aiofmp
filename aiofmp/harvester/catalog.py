"""Symbol-universe catalog backed by SQLite.

Lazily discovers each universe on first access; refreshes when older
than ``refresh_interval_seconds``. All discovery calls run through the
shared FmpClient (not CachedClient — directory endpoints are not in the
cache registry today).
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)

#: Type alias for an optional per-row filter applied during universe refresh.
SymbolFilter = Callable[[str], bool]

# Maps universe name -> (fmp_client.<category>.<method>, ...)
_UNIVERSE_SPECS: dict[str, tuple[str, str]] = {
    "financial_symbols": ("directory", "financial_symbols"),
    "actively_trading": ("directory", "actively_trading"),
    "etf_list": ("directory", "etf_list"),
    "commodities": ("commodity", "commodities_list"),
    "forex_pairs": ("forex", "forex_list"),
    "indexes": ("indexes", "index_list"),
}


class SymbolCatalog:
    def __init__(
        self,
        store: StateStore,
        fmp_client: Any,
        refresh_interval_seconds: int,
        *,
        symbol_filter: SymbolFilter | None = None,
    ) -> None:
        """Build a symbol-universe catalog.

        Args:
            store: SQLite store for cached symbols + refresh timestamps.
            fmp_client: Underlying FmpClient used for discovery calls.
            refresh_interval_seconds: Cache TTL for each universe.
            symbol_filter: Optional predicate ``(symbol: str) -> bool`` applied
                during refresh. Symbols for which it returns ``False`` are
                dropped before persistence. Used by the harvester on Starter
                plan to keep US-only listings (see
                ``aiofmp.harvester.plan.is_us_symbol``). When ``None``, every
                symbol returned by FMP is kept.
        """
        self._store = store
        self._fmp = fmp_client
        self._refresh_seconds = refresh_interval_seconds
        self._symbol_filter = symbol_filter
        self._locks: dict[str, asyncio.Lock] = {}

    def _lock(self, universe: str) -> asyncio.Lock:
        if universe not in self._locks:
            self._locks[universe] = asyncio.Lock()
        return self._locks[universe]

    async def symbols(self, universe: str) -> list[str]:
        if universe not in _UNIVERSE_SPECS:
            raise ValueError(f"unknown universe: {universe!r}")
        async with self._lock(universe):
            if self._is_stale(universe):
                await self._refresh(universe)
            return self._store.list_symbols(universe)

    def _is_stale(self, universe: str) -> bool:
        last = self._store.get_last_refresh(universe)
        if last is None:
            return True
        age = (datetime.now(UTC) - last).total_seconds()
        return age >= self._refresh_seconds

    async def _refresh(self, universe: str) -> None:
        cat_attr, method_name = _UNIVERSE_SPECS[universe]
        category = getattr(self._fmp, cat_attr)
        method = getattr(category, method_name)
        logger.info(
            "Refreshing symbol universe %s via %s.%s", universe, cat_attr, method_name
        )
        records = await method()
        if not isinstance(records, list):
            logger.warning(
                "Universe %s returned non-list (%s); keeping prior cache",
                universe,
                type(records).__name__,
            )
            return
        rows: list[tuple[str, dict[str, Any]]] = []
        dropped = 0
        for r in records:
            if not isinstance(r, dict):
                continue
            symbol = r.get("symbol")
            if not symbol:
                continue
            symbol_s = str(symbol)
            if self._symbol_filter is not None and not self._symbol_filter(symbol_s):
                dropped += 1
                continue
            rows.append((symbol_s, r))
        self._store.replace_universe(universe, rows)
        self._store.set_last_refresh(universe, datetime.now(UTC))
        if dropped:
            logger.info(
                "Universe %s refreshed: %d symbols (%d dropped by filter)",
                universe,
                len(rows),
                dropped,
            )
        else:
            logger.info("Universe %s refreshed: %d symbols", universe, len(rows))
