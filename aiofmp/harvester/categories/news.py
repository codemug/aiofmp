"""news category — P3 over no entity (the call has from/to but no symbol)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING

from aiofmp.base import FMPPaywallError
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.plan import get_plan_limits
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_DEFAULT_VARIANTS = [
    "general_news",
    "press_releases",
    "stock_news",
    "crypto_news",
    "forex_news",
]


class NewsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "news", cfg, manager.state, manager.budget, manager.config.retry
        )
        self._cached = manager.cached_client
        variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
        # Plan-aware variant filter: e.g. press_releases is paywalled on Starter.
        plan_limits = get_plan_limits(manager.config.plan)
        paywalled = plan_limits.paywalled_news_variants
        blocked = [v for v in variants if v in paywalled]
        if blocked:
            logger.info(
                "news (plan=%s): dropping paywalled variants %s",
                plan_limits.name, blocked,
            )
            variants = [v for v in variants if v not in paywalled]
        self._variants = variants
        self._backfill_days = int(cfg.extra.get("backfill_days_initial", 30))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        from_date = today - timedelta(days=self._backfill_days)
        attempted = 0
        succeeded = 0
        paywall_short_circuit = False
        _MAX_PAGES = 10  # safety cap
        for v in self._variants:
            if self.should_stop():
                break
            attempted += 1
            method = getattr(self._cached.news, v)
            variant_ok = True
            for page in range(_MAX_PAGES):
                try:
                    batch = await method(
                        page=page, limit=self._page_size, from_date=from_date, to_date=today
                    )
                except FMPPaywallError as exc:
                    if self.note_paywall():
                        logger.warning(
                            "%s: %d consecutive paywalls; short-circuiting cycle. "
                            "Last failure: %s page %d: %s",
                            self.name, self.PAYWALL_THRESHOLD, v, page, exc,
                        )
                        paywall_short_circuit = True
                    variant_ok = False
                    break
                except Exception as exc:
                    logger.warning("news.%s failed: %s", v, exc)
                    variant_ok = False
                    break
                else:
                    self.note_success()
                if not batch:
                    break
            if variant_ok:
                succeeded += 1
            if paywall_short_circuit:
                break
        if paywall_short_circuit or self.should_stop():
            return RunOutcome(
                status=RunStatus.PARTIAL, items_attempted=attempted, items_succeeded=succeeded
            )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )


def build_news(cfg: CategoryConfig, manager: HarvesterManager) -> NewsHarvester:
    return NewsHarvester(cfg, manager)


register_category("news", build_news)
