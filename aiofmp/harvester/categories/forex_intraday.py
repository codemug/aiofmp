"""forex_intraday category."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_forex_intraday(
    cfg: CategoryConfig, manager: HarvesterManager
) -> GapFillHarvester:
    return _build_intraday(
        "forex_intraday", "forex", False, "forex_pairs", cfg, manager
    )


register_category("forex_intraday", build_forex_intraday)
