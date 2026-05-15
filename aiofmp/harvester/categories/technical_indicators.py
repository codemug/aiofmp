"""technical_indicators category — P3 per (symbol, indicator, period, timeframe)."""

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

_VALID_METHODS = {
    "simple_moving_average",
    "exponential_moving_average",
    "weighted_moving_average",
    "double_exponential_moving_average",
    "triple_exponential_moving_average",
    "relative_strength_index",
    "standard_deviation",
    "williams_percent_r",
    "average_directional_index",
}


class TechnicalIndicatorsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "technical_indicators",
            cfg,
            manager.state,
            manager.budget,
            manager.config.retry,
        )
        self._catalog = manager.catalog
        self._cached = manager.cached_client
        self._universe = str(cfg.extra.get("symbol_universe", "actively_trading"))
        self._backfill_years = int(cfg.extra.get("backfill_years", 5))

        indicators: list[dict[str, Any]] = list(cfg.extra.get("indicators", []))
        for ind in indicators:
            if ind.get("method") not in _VALID_METHODS:
                raise ValueError(
                    f"technical_indicators: unknown method {ind.get('method')!r}"
                )
        self._indicators = indicators

    async def run_cycle(self) -> RunOutcome:
        if not self._indicators:
            return RunOutcome(status=RunStatus.OK)
        symbols = await self._catalog.symbols(self._universe)
        today = date.today()
        from_date = today - timedelta(days=self._backfill_years * 365)
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            if self.should_stop():
                break
            for ind in self._indicators:
                attempted += 1
                method_name = ind["method"]
                period_length = int(ind["period_length"])
                timeframe = str(ind["timeframe"])
                method = getattr(self._cached.technical_indicators, method_name)
                try:
                    await method(symbol, period_length, timeframe, from_date, today)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "technical_indicators.%s(%s, %d, %s) failed: %s",
                        method_name,
                        symbol,
                        period_length,
                        timeframe,
                        exc,
                    )
        if self.should_stop():
            return RunOutcome(
                status=RunStatus.PARTIAL, items_attempted=attempted, items_succeeded=succeeded
            )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )


def build_technical_indicators(
    cfg: CategoryConfig, manager: HarvesterManager
) -> TechnicalIndicatorsHarvester:
    return TechnicalIndicatorsHarvester(cfg, manager)


register_category("technical_indicators", build_technical_indicators)
