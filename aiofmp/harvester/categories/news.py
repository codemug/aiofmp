"""news category — P3 over no entity (the call has from/to but no symbol)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
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
        self._variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
        self._backfill_days = int(cfg.extra.get("backfill_days_initial", 30))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        from_date = today - timedelta(days=self._backfill_days)
        attempted = 0
        succeeded = 0
        for v in self._variants:
            attempted += 1
            method = getattr(self._cached.news, v)
            try:
                await method(
                    page=0, limit=self._page_size, from_date=from_date, to_date=today
                )
                succeeded += 1
            except Exception as exc:
                logger.warning("news.%s failed: %s", v, exc)
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )


def build_news(cfg: CategoryConfig, manager: HarvesterManager) -> NewsHarvester:
    return NewsHarvester(cfg, manager)


register_category("news", build_news)
