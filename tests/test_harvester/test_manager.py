"""Tests for HarvesterManager."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.config import (
    CategoryConfig,
    HarvestConfig,
)
from aiofmp.harvester.manager import HarvesterManager
from aiofmp.harvester.state import RunStatus


class CountingCategory(CategoryHarvester):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cycle_count = 0

    async def run_cycle(self) -> RunOutcome:
        self.cycle_count += 1
        return RunOutcome(status=RunStatus.OK, items_attempted=1, items_succeeded=1)


class StuckCategory(CategoryHarvester):
    async def run_cycle(self) -> RunOutcome:
        await asyncio.sleep(60)
        return RunOutcome(status=RunStatus.OK)


@pytest.fixture
def cfg(tmp_path: Path) -> HarvestConfig:
    return HarvestConfig(
        state_dir=str(tmp_path),
        shutdown_grace_seconds=2,
        categories={
            "alpha": CategoryConfig(enabled=True, interval="1s", extra={}),
            "beta": CategoryConfig(enabled=True, interval="1s", extra={}),
            "gamma": CategoryConfig(enabled=False, interval="1s", extra={}),
        },
    )


def _patch_builder(mgr: HarvesterManager, cls: type[CategoryHarvester]) -> dict:
    instances: dict[str, CategoryHarvester] = {}

    def build(name, c):
        if name not in ("alpha", "beta"):
            raise KeyError(name)
        inst = cls(name, c, mgr.state, mgr.budget, mgr.config.retry)
        instances[name] = inst
        return inst

    mgr._build_category = build
    return instances


class TestHarvesterManager:
    @pytest.mark.asyncio
    async def test_spawns_only_enabled(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.05)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=3.0)
        await mgr.close()
        assert set(mgr._categories.keys()) == {"alpha", "beta"}

    @pytest.mark.asyncio
    async def test_categories_run_concurrently(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        instances = _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.1)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=3.0)
        await mgr.close()
        assert instances["alpha"].cycle_count >= 1
        assert instances["beta"].cycle_count >= 1

    @pytest.mark.asyncio
    async def test_stop_event_finishes_cleanly(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=cfg.shutdown_grace_seconds + 2)
        await mgr.close()

    @pytest.mark.asyncio
    async def test_grace_timeout_cancels(self, cfg: HarvestConfig) -> None:
        cfg.shutdown_grace_seconds = 1
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, StuckCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.05)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=4.0)
        await mgr.close()

    @pytest.mark.asyncio
    async def test_unknown_category_in_config_skipped(self, cfg: HarvestConfig) -> None:
        cfg.categories["nonexistent"] = CategoryConfig(enabled=True, interval="1s", extra={})
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        assert "nonexistent" not in mgr._categories
        await mgr.close()
