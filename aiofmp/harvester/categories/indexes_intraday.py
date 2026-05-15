"""indexes_intraday category (DATE_OBJ params)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_indexes_intraday(
    cfg: CategoryConfig, manager: HarvesterManager
) -> GapFillHarvester:
    return _build_intraday("indexes_intraday", "indexes", True, "indexes", cfg, manager)


register_category("indexes_intraday", build_indexes_intraday)
