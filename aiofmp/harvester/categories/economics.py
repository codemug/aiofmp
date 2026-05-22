"""economics category — P3 (treasury_rates + per-indicator)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING

from aiofmp.base import FMPPaywallError
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.plan import VALID_ECONOMIC_INDICATORS
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

# Defaults use FMP's actual indicator names. The intuitive FRED codes
# (UNRATE, FEDFUNDS, DFF) return ``Invalid name`` against FMP. See
# aiofmp.harvester.plan.VALID_ECONOMIC_INDICATORS for the canonical list.
_DEFAULT_INDICATORS = list(VALID_ECONOMIC_INDICATORS)


class EconomicsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "economics", cfg, manager.state, manager.budget, manager.config.retry
        )
        self._cached = manager.cached_client
        self._indicators = list(cfg.extra.get("indicators", _DEFAULT_INDICATORS))
        self._backfill_years = int(cfg.extra.get("backfill_years", 10))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        from_date = today - timedelta(days=self._backfill_years * 365)
        from_s, to_s = from_date.isoformat(), today.isoformat()
        attempted = 0
        succeeded = 0
        paywall_short_circuit = False

        attempted += 1
        try:
            await self._cached.economics.treasury_rates(from_s, to_s)
        except FMPPaywallError as exc:
            if self.note_paywall():
                logger.warning(
                    "%s: %d consecutive paywalls; short-circuiting cycle. "
                    "Last failure: treasury_rates: %s",
                    self.name,
                    self.PAYWALL_THRESHOLD,
                    exc,
                )
                paywall_short_circuit = True
        except Exception as exc:
            logger.warning("economics.treasury_rates failed: %s", exc)
        else:
            self.note_success()
            succeeded += 1

        if not paywall_short_circuit:
            for ind in self._indicators:
                if self.should_stop():
                    break
                attempted += 1
                try:
                    await self._cached.economics.economic_indicators(ind, from_s, to_s)
                except FMPPaywallError as exc:
                    if self.note_paywall():
                        logger.warning(
                            "%s: %d consecutive paywalls; short-circuiting cycle. "
                            "Last failure: economic_indicators/%s: %s",
                            self.name,
                            self.PAYWALL_THRESHOLD,
                            ind,
                            exc,
                        )
                        paywall_short_circuit = True
                        break
                except Exception as exc:
                    logger.warning(
                        "economics.economic_indicators(%s) failed: %s", ind, exc
                    )
                else:
                    self.note_success()
                    succeeded += 1

        if paywall_short_circuit or self.should_stop():
            return RunOutcome(
                status=RunStatus.PARTIAL,
                items_attempted=attempted,
                items_succeeded=succeeded,
            )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )


def build_economics(
    cfg: CategoryConfig, manager: HarvesterManager
) -> EconomicsHarvester:
    return EconomicsHarvester(cfg, manager)


register_category("economics", build_economics)
