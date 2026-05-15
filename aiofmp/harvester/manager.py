"""HarvesterManager — orchestrates category tasks and lifecycle."""

from __future__ import annotations

import asyncio
import logging
import os
import signal
from pathlib import Path
from typing import Any

from aiofmp.harvester.base import CategoryHarvester
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.catalog import SymbolCatalog
from aiofmp.harvester.config import CategoryConfig, HarvestConfig
from aiofmp.harvester.plan import get_plan_limits, is_us_symbol
from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)


class HarvesterManager:
    """Loads enabled categories, runs them as concurrent asyncio tasks until stopped."""

    def __init__(
        self, config: HarvestConfig, fmp_client: Any, cached_client: Any
    ) -> None:
        self.config = config
        self.fmp_client = fmp_client
        self.cached_client = cached_client

        state_dir = Path(os.path.expanduser(config.state_dir))
        state_dir.mkdir(parents=True, exist_ok=True)
        self.state = StateStore(state_dir / "harvester.sqlite")
        self.state.initialize()

        self.budget = BudgetTracker(self.state, config.budget)
        # Plan-aware symbol filter: drop non-US symbols from every universe when
        # the plan only covers US listings (Basic, Starter). On Premium/Ultimate
        # this is None — all symbols pass through.
        plan_limits = get_plan_limits(config.plan)
        symbol_filter = is_us_symbol if plan_limits.us_only_coverage else None
        self.catalog = SymbolCatalog(
            self.state,
            fmp_client,
            config.discovery.refresh_interval_seconds,
            symbol_filter=symbol_filter,
        )

        self._stop_event = asyncio.Event()
        self._categories: dict[str, CategoryHarvester] = {}
        self._tasks: list[asyncio.Task[None]] = []

    async def start(self) -> None:
        """Construct enabled category harvesters. Does not start tasks."""
        # Wire bandwidth + hard-cap callback into the shared FmpClient
        self.fmp_client.on_response_size = self._on_response_size

        plan_limits = get_plan_limits(self.config.plan)
        for name, cat_cfg in self.config.categories.items():
            if not cat_cfg.enabled:
                logger.info("Category %s is disabled; skipping", name)
                continue
            if name in plan_limits.paywalled_categories:
                logger.info(
                    "Category %s is entirely paywalled on plan %r; skipping. "
                    "Enable a higher plan to harvest it.",
                    name,
                    plan_limits.name,
                )
                continue
            try:
                self._categories[name] = self._build_category(name, cat_cfg)
            except KeyError:
                logger.warning("Unknown category in config: %s (skipping)", name)

    def _on_response_size(self, category: str | None, byte_count: int) -> None:
        """Bandwidth callback installed on FmpClient.

        Records bytes against the current category (or 'user' if outside a cycle),
        then raises FMPBudgetError if the hard cap is breached for harvester traffic.
        """
        self.budget.record_bytes(category, byte_count)
        self.budget.check_hard_cap(category)

    def _build_category(self, name: str, cat_cfg: CategoryConfig) -> CategoryHarvester:
        from aiofmp.harvester.categories import build_category

        return build_category(name, cat_cfg, self)

    def request_stop(self) -> None:
        self._stop_event.set()

    def install_signal_handlers(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self.request_stop)
            loop.add_signal_handler(signal.SIGTERM, self.request_stop)
        except NotImplementedError:
            signal.signal(signal.SIGINT, lambda *_: self.request_stop())

    async def run_until_stopped(self) -> None:
        if not self._categories:
            logger.warning("No enabled categories; manager will idle until stop_event.")
            await self._stop_event.wait()
            return

        for name, cat in self._categories.items():
            self._tasks.append(
                asyncio.create_task(
                    cat.run_forever(self._stop_event), name=f"harvester:{name}"
                )
            )
        await self._stop_event.wait()

        logger.info(
            "Stop requested; waiting for %d categor(y/ies) (grace %ds)",
            len(self._tasks),
            self.config.shutdown_grace_seconds,
        )
        done, pending = await asyncio.wait(
            self._tasks, timeout=self.config.shutdown_grace_seconds
        )
        if pending:
            logger.warning(
                "%d task(s) did not stop within grace; cancelling", len(pending)
            )
            for t in pending:
                t.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

    async def close(self) -> None:
        return None
