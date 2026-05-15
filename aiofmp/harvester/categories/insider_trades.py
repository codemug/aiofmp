"""insider_trades category — Pattern P2 (global walk; per-symbol shard on write)."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "insider-trading/latest"


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class InsiderTradesHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "insider_trades", cfg, manager.state, manager.budget, manager.config.retry
        )
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._max_pages = int(cfg.extra.get("max_pages", 200))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        last_ckpt = _parse_iso(self.state.get_checkpoint("insider_trades", "global"))
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None

        for page in range(self._max_pages):
            if self.should_stop():
                break
            records = await self._fmp.insider_trades.latest_insider_trades(
                page=page, limit=self._page_size
            )
            if not records:
                break
            all_records.extend(records)
            page_dates = [_parse_iso(r.get("filingDate")) for r in records]
            page_dates = [d for d in page_dates if d is not None]
            if page_dates:
                page_newest = max(page_dates)
                page_oldest = min(page_dates)
                if newest_seen is None or page_newest > newest_seen:
                    newest_seen = page_newest
                if last_ckpt is not None and page_oldest <= last_ckpt:
                    break

        if all_records:
            await self._persist(all_records)

        if newest_seen is not None:
            self.state.set_checkpoint(
                "insider_trades", "global", newest_seen.isoformat()
            )

        status = RunStatus.PARTIAL if self.should_stop() else RunStatus.OK
        return RunOutcome(
            status=status,
            items_attempted=len(all_records),
            items_succeeded=len(all_records),
        )

    async def _persist(self, records: list[dict[str, Any]]) -> None:
        # Global stream
        global_key = (_STORAGE_PREFIX, "_global")
        existing_global = await self._storage.read(global_key)
        seen_global = {
            (r.get("symbol"), r.get("filingDate"), r.get("transactionType"))
            for r in existing_global
        }
        for r in records:
            tup = (r.get("symbol"), r.get("filingDate"), r.get("transactionType"))
            if tup not in seen_global:
                existing_global.append(r)
                seen_global.add(tup)
        existing_global.sort(key=lambda r: str(r.get("filingDate", "")), reverse=True)
        await self._storage.write(global_key, existing_global, date_field="filingDate")

        # Per-symbol shard
        by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in records:
            sym = r.get("symbol")
            if sym:
                by_symbol[str(sym)].append(r)
        for sym, rows in by_symbol.items():
            key = (_STORAGE_PREFIX, sym)
            existing = await self._storage.read(key)
            seen = {(r.get("filingDate"), r.get("transactionType")) for r in existing}
            for r in rows:
                tup = (r.get("filingDate"), r.get("transactionType"))
                if tup not in seen:
                    existing.append(r)
                    seen.add(tup)
            existing.sort(key=lambda r: str(r.get("filingDate", "")), reverse=True)
            await self._storage.write(key, existing, date_field="filingDate")


def build_insider_trades(
    cfg: CategoryConfig, manager: HarvesterManager
) -> InsiderTradesHarvester:
    return InsiderTradesHarvester(cfg, manager)


register_category("insider_trades", build_insider_trades)
