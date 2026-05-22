"""form13f category — Pattern P2 (global walk; per-CIK shard on write)."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING, Any

from aiofmp.base import FMPPaywallError
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "institutional-ownership/latest"


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class Form13FHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "form13f", cfg, manager.state, manager.budget, manager.config.retry
        )
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._max_pages = int(cfg.extra.get("max_pages", 50))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        last_ckpt = _parse_iso(self.state.get_checkpoint("form13f", "global"))
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None
        fetch_errors = 0
        paywall_short_circuit = False

        try:
            for page in range(self._max_pages):
                if self.should_stop():
                    break
                try:
                    records = await self._fmp.form13f.latest_filings(
                        page=page, limit=self._page_size
                    )
                except FMPPaywallError as exc:
                    logger.warning(
                        "%s: %d consecutive paywalls; short-circuiting cycle. "
                        "Last failure: page %d: %s",
                        self.name,
                        self.PAYWALL_THRESHOLD,
                        page,
                        exc,
                    )
                    paywall_short_circuit = True
                    break
                except Exception as exc:
                    fetch_errors += 1
                    logger.warning("form13f page %d failed: %s", page, exc)
                    break
                if not records:
                    break
                all_records.extend(records)
                self.note_success()
                page_dates = [_parse_iso(r.get("acceptedDate")) for r in records]
                page_dates = [d for d in page_dates if d is not None]
                if page_dates:
                    page_newest = max(page_dates)
                    page_oldest = min(page_dates)
                    if newest_seen is None or page_newest > newest_seen:
                        newest_seen = page_newest
                    if last_ckpt is not None and page_oldest <= last_ckpt:
                        break
        finally:
            if all_records:
                await self._persist(all_records)
            if newest_seen is not None:
                self.state.set_checkpoint("form13f", "global", newest_seen.isoformat())

        if paywall_short_circuit:
            return RunOutcome(
                status=RunStatus.PARTIAL,
                items_attempted=len(all_records),
                items_succeeded=len(all_records),
            )
        status = (
            RunStatus.PARTIAL
            if (fetch_errors > 0 or self.should_stop())
            else RunStatus.OK
        )
        return RunOutcome(
            status=status,
            items_attempted=len(all_records) + fetch_errors,
            items_succeeded=len(all_records),
        )

    async def _persist(self, records: list[dict[str, Any]]) -> None:
        global_key = (_STORAGE_PREFIX, "_global")
        existing_global = await self._storage.read(global_key)
        seen_global = {(r.get("cik"), r.get("acceptedDate")) for r in existing_global}
        for r in records:
            tup = (r.get("cik"), r.get("acceptedDate"))
            if tup not in seen_global:
                existing_global.append(r)
                seen_global.add(tup)
        existing_global.sort(key=lambda r: str(r.get("acceptedDate", "")), reverse=True)
        await self._storage.write(
            global_key, existing_global, date_field="acceptedDate"
        )

        by_cik: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in records:
            cik = r.get("cik")
            if cik:
                by_cik[str(cik)].append(r)
        for cik, rows in by_cik.items():
            key = (_STORAGE_PREFIX, cik)
            existing = await self._storage.read(key)
            seen = {r.get("acceptedDate") for r in existing}
            for r in rows:
                if r.get("acceptedDate") not in seen:
                    existing.append(r)
                    seen.add(r.get("acceptedDate"))
            existing.sort(key=lambda r: str(r.get("acceptedDate", "")), reverse=True)
            await self._storage.write(key, existing, date_field="acceptedDate")


def build_form13f(cfg: CategoryConfig, manager: HarvesterManager) -> Form13FHarvester:
    return Form13FHarvester(cfg, manager)


register_category("form13f", build_form13f)
