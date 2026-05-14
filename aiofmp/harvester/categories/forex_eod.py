"""forex_eod category — P3 gap-fill over the forex_pairs universe."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_VARIANTS = ["historical_price_full"]


def build_forex_eod(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
    backfill_years = int(cfg.extra.get("backfill_years", 10))
    targets = [
        GapFillTarget(category_attr="forex", method_name=v, use_date_obj=False)
        for v in variants
    ]
    return GapFillHarvester(
        name="forex_eod",
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe="forex_pairs",
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_years * 365 * 86400,
    )


register_category("forex_eod", build_forex_eod)
