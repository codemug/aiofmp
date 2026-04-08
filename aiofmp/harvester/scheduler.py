"""Harvest scheduler — runs harvest cycles on a configurable interval."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any

from .config import HarvestConfig
from .runner import run_harvest

logger = logging.getLogger(__name__)


class HarvestScheduler:
    """Async scheduler that runs harvest cycles at a fixed interval."""

    def __init__(
        self,
        cached_client: Any,  # CachedClient
        config: HarvestConfig,
    ) -> None:
        self._cached = cached_client
        self._config = config
        self._running = False

    async def run(self) -> None:
        """Run the scheduler loop. Blocks until stopped."""
        self._running = True
        interval = self._config.scheduler.interval_seconds

        logger.info(
            "Harvest scheduler started (interval=%ds, run_on_start=%s)",
            interval,
            self._config.scheduler.run_on_start,
        )

        if self._config.scheduler.run_on_start:
            await self._execute_cycle()

        while self._running:
            await asyncio.sleep(interval)
            if not self._running:
                break
            await self._execute_cycle()

    def stop(self) -> None:
        """Signal the scheduler to stop after the current cycle."""
        logger.info("Harvest scheduler stopping")
        self._running = False

    async def _execute_cycle(self) -> None:
        """Execute a single harvest cycle with error handling and timing."""
        started = datetime.now(timezone.utc)
        logger.info("Harvest cycle starting at %s", started.isoformat())
        try:
            results = await run_harvest(self._cached, self._config)
            succeeded = sum(1 for r in results if r.success)
            failed = sum(1 for r in results if not r.success)
            total_records = sum(r.records_fetched for r in results)
            logger.info(
                "Harvest cycle: %d endpoints, %d succeeded, %d failed, %d records",
                len(results), succeeded, failed, total_records,
            )
        except Exception:
            logger.exception("Harvest cycle failed")
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        logger.info("Harvest cycle completed in %.1f seconds", elapsed)
