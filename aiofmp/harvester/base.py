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

    @abc.abstractmethod
    async def run_cycle(self) -> RunOutcome:
        """Execute one harvest cycle. Must be overridden by subclasses."""
        raise NotImplementedError

    def should_stop(self) -> bool:
        """True if the manager has requested shutdown. Subclasses should check this between iterations."""
        return self._stop_event is not None and self._stop_event.is_set()

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
        self.state.record_run_start(self.name, started)

        if self.budget.is_paused(self.name):
            logger.warning("Category %s paused for budget; skipping cycle", self.name)
            self.state.record_run_finish(
                self.name, started, status=RunStatus.PAUSED_FOR_BUDGET
            )
            return

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
