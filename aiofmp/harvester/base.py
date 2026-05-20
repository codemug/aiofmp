"""CategoryHarvester abstract base class.

Concrete categories override ``run_cycle()`` and return a ``RunOutcome``.
The base class handles the run/sleep loop, retry/backoff for ``FMPRateLimitError``,
state-store bookkeeping, budget pause-before-run, and the ``current_harvest_category``
ContextVar plumbing so byte-counting attributes every request to the right category.
"""

from __future__ import annotations

import abc
import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from aiofmp.base import (
    FMPBudgetError,
    FMPRateLimitError,
    FMPServerError,
    current_harvest_category,
)
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import CategoryConfig, RetryConfig, RetryPolicy
from aiofmp.harvester.state import RunStatus, StateStore

logger = logging.getLogger(__name__)


@dataclass
class RunOutcome:
    """Result of a single run_cycle() invocation."""

    status: RunStatus
    items_attempted: int = 0
    items_succeeded: int = 0
    bytes_estimate: int = 0
    error: str | None = None


class CategoryHarvester(abc.ABC):
    """Abstract base for one harvester category."""

    #: Number of consecutive FMPPaywallError items before the cycle short-circuits.
    #: Tunes how many wasted requests we spend "discovering" that the category is
    #: entirely paywalled on the current plan. 10 is enough to ride through a
    #: paywalled alphabetical prefix in small universes (commodities ~40 syms,
    #: where DXUSD/ESUSD/etc. are blocked but GCUSD/SIUSD work) while still
    #: stopping fast when the whole endpoint is paywalled.
    PAYWALL_THRESHOLD: int = 10

    #: Seconds to remember a paywall short-circuit before re-probing. When
    #: a cycle hits ``PAYWALL_THRESHOLD`` consecutive 402s, subsequent cycles
    #: skip the category silently until this much time has passed. Default
    #: 24h keeps daily-interval categories quiet for a day while still
    #: re-probing once a day in case the user upgraded plans. In-memory only
    #: (resets on process restart, which forces a re-probe at startup).
    PAYWALL_REPROBE_SECONDS: int = 24 * 60 * 60

    def __init__(
        self,
        name: str,
        config: CategoryConfig,
        state: StateStore,
        budget: BudgetTracker,
        retry: RetryConfig,
    ) -> None:
        self.name = name
        self.config = config
        self.state = state
        self.budget = budget
        self.retry = retry
        self._stop_event: asyncio.Event | None = None
        self._consecutive_paywalls: int = 0
        #: Set to ``now()`` each time the cycle short-circuits via PAYWALL.
        #: While this is recent (within ``PAYWALL_REPROBE_SECONDS``) the
        #: pre-cycle check skips the cycle entirely without making any
        #: requests. In-memory only — restart re-probes.
        self._paywalled_at: datetime | None = None

    @abc.abstractmethod
    async def run_cycle(self) -> RunOutcome:
        """Execute one harvest cycle. Must be overridden by subclasses."""
        raise NotImplementedError

    def should_stop(self) -> bool:
        """True if the manager has requested shutdown. Subclasses should check this between iterations."""
        return self._stop_event is not None and self._stop_event.is_set()

    def note_paywall(self) -> bool:
        """Record a paywall (HTTP 402) for the current cycle.

        Returns ``True`` once consecutive paywalls reach ``PAYWALL_THRESHOLD``,
        signalling the per-item loop should short-circuit and the cycle should
        end as ``PARTIAL``. Callers should reset the counter on success via
        ``note_success()``. When the threshold trips we also remember the
        timestamp so subsequent cycles can skip the category entirely until
        ``PAYWALL_REPROBE_SECONDS`` elapses.
        """
        self._consecutive_paywalls += 1
        if self._consecutive_paywalls >= self.PAYWALL_THRESHOLD:
            self._paywalled_at = datetime.now(UTC)
            return True
        return False

    def note_success(self) -> None:
        """Reset the consecutive-paywall counter after a successful request.

        Also clears the paywall-memory marker — a successful call proves the
        category is reachable again (e.g. plan was upgraded mid-process).
        """
        self._consecutive_paywalls = 0
        self._paywalled_at = None

    def _reset_paywall_state(self) -> None:
        """Reset paywall tracking at the start of each cycle.

        Only clears the per-cycle consecutive counter — NOT the cross-cycle
        ``_paywalled_at`` marker, which is what lets subsequent cycles skip
        a known-paywalled category silently.
        """
        self._consecutive_paywalls = 0

    def _paywall_skip_remaining_seconds(self) -> int:
        """How many seconds remain before the next paywall re-probe.

        Returns 0 when no recent paywall is recorded or when the marker
        is older than ``PAYWALL_REPROBE_SECONDS``.
        """
        if self._paywalled_at is None:
            return 0
        elapsed = (datetime.now(UTC) - self._paywalled_at).total_seconds()
        remaining = self.PAYWALL_REPROBE_SECONDS - int(elapsed)
        return max(0, remaining)

    async def run_forever(self, stop_event: asyncio.Event) -> None:
        """Main loop: run a cycle each ``interval_seconds`` until stop_event fires."""
        self._stop_event = stop_event
        interval = self.config.interval_seconds
        while not stop_event.is_set():
            await self._run_once_and_record()
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

    async def _run_once_and_record(self) -> None:
        """Run one cycle with state bookkeeping and budget checks."""
        started = datetime.now(UTC)

        # If we recently learned this category is paywalled on the current
        # plan (last cycle short-circuited via threshold), skip silently
        # until the re-probe window elapses. Avoids 10 wasted requests per
        # cycle for categories the user knows are paywalled.
        skip_seconds = self._paywall_skip_remaining_seconds()
        if skip_seconds > 0:
            hours_left = skip_seconds // 3600
            logger.info(
                "Category %s skipped (paywalled; re-probe in ~%dh)",
                self.name, max(1, hours_left),
            )
            self.state.record_run_start(self.name, started)
            self.state.record_run_finish(
                self.name, started, status=RunStatus.PAUSED_FOR_BUDGET,
                error="paywalled (skipped pending re-probe)",
            )
            return

        self.state.record_run_start(self.name, started)

        if self.budget.is_paused(self.name):
            logger.warning("Category %s paused for budget; skipping cycle", self.name)
            self.state.record_run_finish(
                self.name, started, status=RunStatus.PAUSED_FOR_BUDGET
            )
            return

        # Each cycle gets a fresh paywall counter — a category that was
        # short-circuited last cycle gets a chance to retry (e.g. after a
        # plan upgrade).
        self._reset_paywall_state()

        token = current_harvest_category.set(self.name)
        try:
            outcome = await self._run_cycle_with_retry()
        except Exception as e:
            logger.exception("Unhandled error in %s.run_cycle", self.name)
            self.state.record_run_finish(
                self.name,
                started,
                status=RunStatus.ERROR,
                error=f"{type(e).__name__}: {e}",
            )
            return
        finally:
            current_harvest_category.reset(token)

        self.state.record_run_finish(
            self.name,
            started,
            status=outcome.status,
            items_attempted=outcome.items_attempted,
            items_succeeded=outcome.items_succeeded,
            bytes_estimate=outcome.bytes_estimate,
            error=outcome.error,
        )

    async def _run_cycle_with_retry(self) -> RunOutcome:
        """Wrap a single run_cycle() with retry/backoff policy for 429 and 5xx."""
        policy_429: RetryPolicy = self.retry.on_429
        policy_5xx: RetryPolicy = self.retry.on_5xx
        attempt_429 = 0
        attempt_5xx = 0

        while True:
            try:
                return await self.run_cycle()
            except FMPRateLimitError as e:
                attempt_429 += 1
                if attempt_429 >= policy_429.max_attempts:
                    return RunOutcome(
                        status=RunStatus.PARTIAL,
                        error=f"rate-limit retries exhausted: {e}",
                    )
                delay = policy_429.backoff_seconds[
                    min(attempt_429 - 1, len(policy_429.backoff_seconds) - 1)
                ]
                logger.warning(
                    "%s hit 429 (attempt %d/%d); sleeping %ds",
                    self.name,
                    attempt_429,
                    policy_429.max_attempts,
                    delay,
                )
                if delay > 0:
                    await asyncio.sleep(delay)
            except FMPServerError as e:
                attempt_5xx += 1
                if attempt_5xx >= policy_5xx.max_attempts:
                    return RunOutcome(
                        status=RunStatus.PARTIAL,
                        error=f"server-error retries exhausted: {e}",
                    )
                delay = policy_5xx.backoff_seconds[
                    min(attempt_5xx - 1, len(policy_5xx.backoff_seconds) - 1)
                ]
                logger.warning(
                    "%s hit 5xx (attempt %d/%d); sleeping %ds",
                    self.name,
                    attempt_5xx,
                    policy_5xx.max_attempts,
                    delay,
                )
                if delay > 0:
                    await asyncio.sleep(delay)
            except FMPBudgetError as e:
                logger.warning("%s hit budget hard cap: %s", self.name, e)
                return RunOutcome(status=RunStatus.PARTIAL, error=str(e))
