"""statements category — Pattern P1 (discover-then-fill) + monthly safety-net sweep."""

from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig, parse_interval
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


# The 13 statement endpoints split by SDK signature shape.
PERIOD_AND_LIMIT_ENDPOINTS: list[str] = [
    "income_statement",
    "balance_sheet_statement",
    "cash_flow_statement",
    "key_metrics",
    "financial_ratios",
    "enterprise_values",
    "income_statement_growth",
    "balance_sheet_statement_growth",
    "cash_flow_statement_growth",
    "financial_statement_growth",
]

LIMIT_ONLY_ENDPOINTS: list[str] = [
    "owner_earnings",
]

PERIOD_ONLY_ENDPOINTS: list[str] = [
    "revenue_product_segmentation",
    "revenue_geographic_segmentation",
]


class StatementsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("statements", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._cached = manager.cached_client
        self._periods: list[str] = list(cfg.extra.get("periods", ["annual", "quarter"]))
        self._initial_limit = int(cfg.extra.get("initial_limit", 40))
        self._incremental_limit = int(cfg.extra.get("incremental_limit", 2))
        self._safety_net_seconds = parse_interval(str(cfg.extra.get("safety_net_interval", "30d")))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        if self._should_run_safety_net(today):
            outcome = await self._run_safety_net(today)
            # Mark the safety-net last-run in a separate scope
            self.state.set_checkpoint("statements_safetynet", "global", today.isoformat())
            # Also bump primary checkpoint so incremental window doesn't span both
            self.state.set_checkpoint("statements", "global", today.isoformat())
            return outcome

        return await self._run_incremental(today)

    def _should_run_safety_net(self, today: date) -> bool:
        last = self.state.get_checkpoint("statements_safetynet", "global")
        if last is None:
            # The safety-net has never explicitly run.  Don't fire it here;
            # let the normal incremental path handle the first run.
            return False
        try:
            last_d = date.fromisoformat(last)
        except ValueError:
            return True
        age_sec = (today - last_d).days * 86400
        return age_sec >= self._safety_net_seconds

    async def _run_safety_net(self, today: date) -> RunOutcome:
        symbols = await self._catalog.symbols("financial_symbols")
        return await self._iterate_symbols(symbols, self._incremental_limit)

    async def _run_incremental(self, today: date) -> RunOutcome:
        last = self.state.get_checkpoint("statements", "global")
        if last is None:
            # First run ever (and not yet a safety-net run): treat as full backfill
            symbols = await self._catalog.symbols("financial_symbols")
            outcome = await self._iterate_symbols(symbols, self._initial_limit)
            self.state.set_checkpoint("statements", "global", today.isoformat())
            return outcome

        try:
            from_date = date.fromisoformat(last)
        except ValueError:
            from_date = today - timedelta(days=30)

        from_s, to_s = from_date.isoformat(), today.isoformat()
        records = await self._cached.calendar.earnings_calendar(from_s, to_s)

        symbols = sorted({r["symbol"] for r in records if r.get("symbol")})
        outcome = await self._iterate_symbols(symbols, self._incremental_limit)
        self.state.set_checkpoint("statements", "global", today.isoformat())
        return outcome

    async def _iterate_symbols(self, symbols: list[str], limit: int) -> RunOutcome:
        if not symbols:
            return RunOutcome(status=RunStatus.OK)
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            # 10 (period, limit) endpoints × periods
            for endpoint in PERIOD_AND_LIMIT_ENDPOINTS:
                for period in self._periods:
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, limit=limit, period=period)
                        succeeded += 1
                    except Exception as exc:
                        logger.warning("statements.%s(%s, %s) failed: %s", endpoint, symbol, period, exc)
            # limit-only endpoints (owner_earnings)
            for endpoint in LIMIT_ONLY_ENDPOINTS:
                attempted += 1
                method = getattr(self._cached.statements, endpoint)
                try:
                    await method(symbol, limit=limit)
                    succeeded += 1
                except Exception as exc:
                    logger.warning("statements.%s(%s) failed: %s", endpoint, symbol, exc)
            # period-only endpoints (segmentation)
            for endpoint in PERIOD_ONLY_ENDPOINTS:
                for period in self._periods:
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, period=period)
                        succeeded += 1
                    except Exception as exc:
                        logger.warning("statements.%s(%s, %s) failed: %s", endpoint, symbol, period, exc)
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_statements(cfg: CategoryConfig, manager: "HarvesterManager") -> StatementsHarvester:
    return StatementsHarvester(cfg, manager)


register_category("statements", build_statements)
