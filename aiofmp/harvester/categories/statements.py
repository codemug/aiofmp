"""statements category — Pattern P1 (discover-then-fill) + monthly safety-net sweep."""

from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

from aiofmp.base import FMPPaywallError, current_harvest_category
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig, parse_interval
from aiofmp.harvester.plan import get_plan_limits
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
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "statements", cfg, manager.state, manager.budget, manager.config.retry
        )
        self._catalog = manager.catalog
        self._cached = manager.cached_client
        self._periods: list[str] = list(cfg.extra.get("periods", ["annual", "quarter"]))
        # Plan-aware per-endpoint paywall: e.g. on Starter, key_metrics +
        # ratios + segmentation don't accept period=quarter, but the other
        # 10 statement endpoints do. The whole-category quarter-drop the
        # earlier code did was too aggressive.
        plan_limits = get_plan_limits(manager.config.plan)
        self._quarterly_paywalled: frozenset[str] = (
            plan_limits.quarterly_paywalled_statement_endpoints
        )
        if "quarter" in self._periods and self._quarterly_paywalled:
            logger.info(
                "statements (plan=%s): period=quarter will be skipped for %s",
                plan_limits.name,
                sorted(self._quarterly_paywalled),
            )
        self._initial_limit = int(cfg.extra.get("initial_limit", 40))
        self._incremental_limit = int(cfg.extra.get("incremental_limit", 2))
        self._safety_net_seconds = parse_interval(
            str(cfg.extra.get("safety_net_interval", "30d"))
        )

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        if self._should_run_safety_net(today):
            return await self._run_safety_net_with_row(today)
        return await self._run_incremental(today)

    async def _run_safety_net_with_row(self, today: date) -> RunOutcome:
        """Run the safety-net sweep, bookkept under the 'statements_safetynet' category row."""
        started = datetime.now(UTC)
        self.state.record_run_start("statements_safetynet", started)
        token = current_harvest_category.set("statements_safetynet")
        try:
            outcome = await self._run_safety_net(today)
        except Exception as e:
            self.state.record_run_finish(
                "statements_safetynet",
                started,
                status=RunStatus.ERROR,
                error=f"{type(e).__name__}: {e}",
            )
            raise
        finally:
            current_harvest_category.reset(token)

        self.state.record_run_finish(
            "statements_safetynet",
            started,
            status=outcome.status,
            items_attempted=outcome.items_attempted,
            items_succeeded=outcome.items_succeeded,
            bytes_estimate=outcome.bytes_estimate,
            error=outcome.error,
        )
        # Always update the safety-net checkpoint so the next sweep fires safety_net_interval from now
        self.state.set_checkpoint("statements_safetynet", "global", today.isoformat())
        # Also bump the primary statements checkpoint so the incremental window doesn't span both
        self.state.set_checkpoint("statements", "global", today.isoformat())
        return outcome

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
            # Seed the safety-net checkpoint so the 30-day timer starts from today
            self.state.set_checkpoint("statements_safetynet", "global", today.isoformat())
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
        paywall_short_circuit = False
        for symbol in symbols:
            if self.should_stop():
                break
            # 10 (period, limit) endpoints × periods
            for endpoint in PERIOD_AND_LIMIT_ENDPOINTS:
                for period in self._periods:
                    # Skip endpoints we know are paywalled for this period
                    # on the current plan (e.g. Starter blocks
                    # period=quarter for key_metrics/ratios).
                    if (
                        period == "quarter"
                        and endpoint in self._quarterly_paywalled
                    ):
                        continue
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, limit=limit, period=period)
                    except FMPPaywallError as exc:
                        if self.note_paywall():
                            logger.warning(
                                "%s: %d consecutive paywalls; short-circuiting cycle. "
                                "Last failure: %s/%s/%s: %s",
                                self.name, self.PAYWALL_THRESHOLD,
                                endpoint, symbol, period, exc,
                            )
                            paywall_short_circuit = True
                            break
                    except Exception as exc:
                        logger.warning(
                            "statements.%s(%s, %s) failed: %s",
                            endpoint,
                            symbol,
                            period,
                            exc,
                        )
                    else:
                        self.note_success()
                        succeeded += 1
                if paywall_short_circuit:
                    break
            if paywall_short_circuit:
                break
            # limit-only endpoints (owner_earnings)
            for endpoint in LIMIT_ONLY_ENDPOINTS:
                attempted += 1
                method = getattr(self._cached.statements, endpoint)
                try:
                    await method(symbol, limit=limit)
                except FMPPaywallError as exc:
                    if self.note_paywall():
                        logger.warning(
                            "%s: %d consecutive paywalls; short-circuiting cycle. "
                            "Last failure: %s/%s: %s",
                            self.name, self.PAYWALL_THRESHOLD, endpoint, symbol, exc,
                        )
                        paywall_short_circuit = True
                        break
                except Exception as exc:
                    logger.warning(
                        "statements.%s(%s) failed: %s", endpoint, symbol, exc
                    )
                else:
                    self.note_success()
                    succeeded += 1
            if paywall_short_circuit:
                break
            # period-only endpoints (segmentation)
            for endpoint in PERIOD_ONLY_ENDPOINTS:
                for period in self._periods:
                    if (
                        period == "quarter"
                        and endpoint in self._quarterly_paywalled
                    ):
                        continue
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, period=period)
                    except FMPPaywallError as exc:
                        if self.note_paywall():
                            logger.warning(
                                "%s: %d consecutive paywalls; short-circuiting cycle. "
                                "Last failure: %s/%s/%s: %s",
                                self.name, self.PAYWALL_THRESHOLD,
                                endpoint, symbol, period, exc,
                            )
                            paywall_short_circuit = True
                            break
                    except Exception as exc:
                        logger.warning(
                            "statements.%s(%s, %s) failed: %s",
                            endpoint,
                            symbol,
                            period,
                            exc,
                        )
                    else:
                        self.note_success()
                        succeeded += 1
                if paywall_short_circuit:
                    break
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


def build_statements(
    cfg: CategoryConfig, manager: HarvesterManager
) -> StatementsHarvester:
    return StatementsHarvester(cfg, manager)


register_category("statements", build_statements)
