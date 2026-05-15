"""analyst_estimates category — Pattern P2 (per-symbol page walk)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "analyst-estimates"
_MAX_PAGES_SAFETY = 1000


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class AnalystEstimatesHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "analyst_estimates",
            cfg,
            manager.state,
            manager.budget,
            manager.config.retry,
        )
        self._catalog = manager.catalog
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._periods: list[str] = list(cfg.extra.get("estimate_periods", ["annual"]))
        self._max_backfill_days = int(cfg.extra.get("max_backfill_years", 3)) * 365
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols("actively_trading")
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for period in self._periods:
                attempted += 1
                try:
                    await self._walk_symbol(symbol, period)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "analyst_estimates walk failed for %s/%s: %s",
                        symbol,
                        period,
                        exc,
                    )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )

    async def _walk_symbol(self, symbol: str, period: str) -> None:
        scope = f"{symbol}/{period}"
        last_ckpt = _parse_iso(self.state.get_checkpoint("analyst_estimates", scope))
        max_backfill = date.today() - timedelta(days=self._max_backfill_days)
        stop_at: date = (
            last_ckpt if last_ckpt and last_ckpt > max_backfill else max_backfill
        )

        storage_key = (_STORAGE_PREFIX, symbol, period)
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None

        for page in range(_MAX_PAGES_SAFETY):
            records = await self._fmp.analyst.financial_estimates(
                symbol, period, page=page, limit=self._page_size
            )
            if not records:
                break
            all_records.extend(records)
            page_dates = [_parse_iso(r.get("date")) for r in records]
            page_dates = [d for d in page_dates if d is not None]
            if not page_dates:
                # Defensive: if no parseable dates on this page, stop to avoid infinite loop
                break
            oldest_on_page = min(page_dates)
            page_newest = max(page_dates)
            if newest_seen is None or page_newest > newest_seen:
                newest_seen = page_newest
            if oldest_on_page <= stop_at:
                break

        if all_records:
            # Merge with existing storage (dedup by date)
            existing = await self._storage.read(storage_key)
            seen = {r.get("date") for r in existing}
            for r in all_records:
                if r.get("date") not in seen:
                    existing.append(r)
                    seen.add(r.get("date"))
            existing.sort(key=lambda r: str(r.get("date", "")), reverse=True)
            await self._storage.write(storage_key, existing, date_field="date")

        if newest_seen is not None:
            self.state.set_checkpoint(
                "analyst_estimates", scope, newest_seen.isoformat()
            )


def build_analyst_estimates(
    cfg: CategoryConfig, manager: HarvesterManager
) -> AnalystEstimatesHarvester:
    return AnalystEstimatesHarvester(cfg, manager)


register_category("analyst_estimates", build_analyst_estimates)
