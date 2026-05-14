"""commodities_intraday category — P3 gap-fill per (symbol, timeframe)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday  # reuse helper
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_commodities_intraday(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    return _build_intraday("commodities_intraday", "commodity", False, "commodities", cfg, manager)


register_category("commodities_intraday", build_commodities_intraday)
