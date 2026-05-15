"""chart_intraday category — P3 gap-fill per (symbol, timeframe)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_TIMEFRAMES = ["1hour"]
_TF_TO_METHOD = {
    "1min": "intraday_1min",
    "5min": "intraday_5min",
    "15min": "intraday_15min",
    "30min": "intraday_30min",
    "1hour": "intraday_1hour",
    "4hour": "intraday_4hour",
}


def _build_intraday(
    name: str,
    category_attr: str,
    use_date_obj: bool,
    universe: str,
    cfg: CategoryConfig,
    manager: HarvesterManager,
) -> GapFillHarvester:
    timeframes = list(cfg.extra.get("timeframes", _DEFAULT_TIMEFRAMES))
    for tf in timeframes:
        if tf not in _TF_TO_METHOD:
            raise ValueError(
                f"{name}: unknown timeframe {tf!r}; valid: {list(_TF_TO_METHOD)}"
            )
    backfill_days = int(cfg.extra.get("backfill_days", 30))
    user_universe = str(cfg.extra.get("symbol_universe", universe))

    targets = [
        GapFillTarget(
            category_attr=category_attr,
            method_name=_TF_TO_METHOD[tf],
            use_date_obj=use_date_obj,
        )
        for tf in timeframes
    ]
    return GapFillHarvester(
        name=name,
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe=user_universe,
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_days * 86400,
    )


def build_chart_intraday(
    cfg: CategoryConfig, manager: HarvesterManager
) -> GapFillHarvester:
    return _build_intraday(
        "chart_intraday", "chart", False, "actively_trading", cfg, manager
    )


register_category("chart_intraday", build_chart_intraday)
