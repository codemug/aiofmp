"""Harvester — public API for cache warming."""

import logging
from typing import Any

from .config import HarvestConfig
from .result import HarvestResult
from .runner import run_harvest
from .scheduler import HarvestScheduler

logger = logging.getLogger(__name__)


class Harvester:
    """Cache warmer that proactively calls CachedClient methods.

    Usage::

        from aiofmp import FmpClient
        from aiofmp.cachedclient import CachedClient
        from aiofmp.harvester import Harvester, HarvestConfig, SymbolsConfig

        fmp = FmpClient(api_key="YOUR_KEY")
        cached = CachedClient(fmp)
        config = HarvestConfig(
            categories=["chart", "statements"],
            symbols=SymbolsConfig(mode="explicit", symbols=["AAPL", "MSFT"]),
        )

        harvester = Harvester(cached, config)
        async with cached:
            # Single harvest
            results = await harvester.run_once()

            # Or run on a schedule
            await harvester.run_scheduled()
    """

    def __init__(
        self,
        cached_client: Any,  # CachedClient (avoid circular import)
        config: HarvestConfig | None = None,
    ) -> None:
        self._cached = cached_client
        self._config = config or HarvestConfig()
        self._scheduler: HarvestScheduler | None = None

    async def run_once(self) -> list[HarvestResult]:
        """Execute a single harvest cycle. Returns results."""
        return await run_harvest(self._cached, self._config)

    async def run_scheduled(self) -> None:
        """Run harvest cycles on the configured interval. Blocks until stopped."""
        self._scheduler = HarvestScheduler(self._cached, self._config)
        await self._scheduler.run()

    def stop(self) -> None:
        """Signal the scheduler to stop after the current cycle."""
        if self._scheduler:
            self._scheduler.stop()

    @property
    def config(self) -> HarvestConfig:
        return self._config
