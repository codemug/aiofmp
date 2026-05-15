"""analyst_snapshots category — Pattern P4 (snapshot overwrite per symbol)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


# Maps the YAML "include" name -> (SDK method on client.analyst, snapshot endpoint key).
_INCLUDE_MAP: dict[str, tuple[str, str]] = {
    "ratings_snapshot": ("ratings_snapshot", "ratings-snapshot"),
    "price_target_consensus": ("price_target_consensus", "price-target-consensus"),
    "price_target_summary": ("price_target_summary", "price-target-summary"),
    "stock_grades_summary": ("stock_grades_summary", "grades-consensus"),
}

_DEFAULT_INCLUDE = list(_INCLUDE_MAP.keys())


class AnalystSnapshotsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: HarvesterManager) -> None:
        super().__init__(
            "analyst_snapshots",
            cfg,
            manager.state,
            manager.budget,
            manager.config.retry,
        )
        self._catalog = manager.catalog
        self._fmp = manager.fmp_client
        self._snapshots = SnapshotStore(manager.cached_client.storage)
        include = list(cfg.extra.get("include", _DEFAULT_INCLUDE))
        for n in include:
            if n not in _INCLUDE_MAP:
                raise ValueError(f"analyst_snapshots: unknown include {n!r}")
        self._include = include

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols("actively_trading")
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            if self.should_stop():
                break
            for name in self._include:
                attempted += 1
                method_name, endpoint = _INCLUDE_MAP[name]
                method = getattr(self._fmp.analyst, method_name)
                try:
                    rows = await method(symbol)
                    payload = rows[0] if isinstance(rows, list) and rows else None
                    if payload:
                        await self._snapshots.write(endpoint, symbol, payload)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "analyst_snapshots.%s(%s) failed: %s",
                        method_name,
                        symbol,
                        exc,
                    )
        if self.should_stop():
            return RunOutcome(
                status=RunStatus.PARTIAL, items_attempted=attempted, items_succeeded=succeeded
            )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(
            status=status, items_attempted=attempted, items_succeeded=succeeded
        )


def build_analyst_snapshots(
    cfg: CategoryConfig, manager: HarvesterManager
) -> AnalystSnapshotsHarvester:
    return AnalystSnapshotsHarvester(cfg, manager)


register_category("analyst_snapshots", build_analyst_snapshots)
