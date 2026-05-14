"""Category-specific harvester implementations.

Concrete category modules call ``register_category(name, factory)`` at import
time. ``build_category(name, cfg, manager)`` then dispatches via the registry.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiofmp.harvester.base import CategoryHarvester
    from aiofmp.harvester.config import CategoryConfig
    from aiofmp.harvester.manager import HarvesterManager

CategoryFactory = Callable[..., "CategoryHarvester"]

_REGISTRY: dict[str, CategoryFactory] = {}


def register_category(name: str, factory: CategoryFactory) -> None:
    _REGISTRY[name] = factory


def build_category(name: str, cfg: "CategoryConfig", manager: "HarvesterManager") -> "CategoryHarvester":
    if name not in _REGISTRY:
        raise KeyError(name)
    return _REGISTRY[name](cfg, manager)


def registered_names() -> list[str]:
    return sorted(_REGISTRY.keys())


# Import concrete category modules so their register_category() calls fire.
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    analyst_snapshots,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    dcf,
    economics,
    forex_eod,
    forex_intraday,
    form13f,
    indexes_eod,
    indexes_intraday,
    insider_trades,
    news,
    statements,
    technical_indicators,
)
