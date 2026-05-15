"""GapFillHarvester — DRY base for P3 categories that delegate to CachedClient gap-fill."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from aiofmp.base import FMPPaywallError
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GapFillTarget:
    """One (category_attr, method_name) pair to call per symbol."""

    category_attr: str  # e.g. "chart", "commodity", "forex", "indexes"
    method_name: str  # e.g. "historical_price_full"
    use_date_obj: bool  # True for indexes.*, False elsewhere


class GapFillHarvester(CategoryHarvester):
    """Generic P3 harvester: for each symbol in a universe, call each target
    method with ``(symbol, from_date, to_date)`` and let CachedClient gap-fill.
    """

    def __init__(
        self,
        name: str,
        config: CategoryConfig,
        state: StateStore,
        budget: BudgetTracker,
        retry: RetryConfig,
        *,
        symbol_catalog: Any,
        symbol_universe: str,
        cached_client: Any,
        targets: list[GapFillTarget],
        backfill_seconds: int,
    ) -> None:
        super().__init__(name, config, state, budget, retry)
        self._catalog = symbol_catalog
        self._universe = symbol_universe
        self._cached = cached_client
        self._targets = list(targets)
        self._backfill_seconds = backfill_seconds

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols(self._universe)
        if not symbols:
            return RunOutcome(status=RunStatus.OK)

        today = date.today()
        from_date = today - timedelta(seconds=self._backfill_seconds)

        attempted = 0
        succeeded = 0
        paywall_short_circuit = False
        for symbol in symbols:
            if self.should_stop():
                break
            for target in self._targets:
                attempted += 1
                try:
                    await self._call_target(target, symbol, from_date, today)
                    succeeded += 1
                    self.note_success()
                except FMPPaywallError as exc:
                    if self.note_paywall():
                        logger.warning(
                            "%s: %d consecutive paywalls; short-circuiting cycle. "
                            "Last failure: %s.%s(%s): %s",
                            self.name,
                            self.PAYWALL_THRESHOLD,
                            target.category_attr,
                            target.method_name,
                            symbol,
                            exc,
                        )
                        paywall_short_circuit = True
                        break
                except Exception as exc:
                    logger.warning(
                        "%s: %s.%s(%s) failed: %s",
                        self.name,
                        target.category_attr,
                        target.method_name,
                        symbol,
                        exc,
                    )
            if paywall_short_circuit:
                break

        if self.should_stop() or paywall_short_circuit:
            return RunOutcome(
                status=RunStatus.PARTIAL,
                items_attempted=attempted,
                items_succeeded=succeeded,
            )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )

    async def _call_target(
        self,
        target: GapFillTarget,
        symbol: str,
        from_d: date,
        to_d: date,
    ) -> None:
        category = getattr(self._cached, target.category_attr)
        method = getattr(category, target.method_name)
        if target.use_date_obj:
            await method(symbol, from_d, to_d)
        else:
            await method(symbol, from_d.isoformat(), to_d.isoformat())
