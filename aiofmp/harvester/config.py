"""Harvester configuration dataclasses + YAML schema.

Defines the structured representation of `harvester.yaml` and the
`parse_interval` helper that turns strings like ``"6h"`` into seconds.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_INTERVAL_RE = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)
_INTERVAL_UNIT_SECONDS: dict[str, int] = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
}


def parse_interval(spec: str) -> int:
    """Parse an interval spec like ``"30s"``, ``"5m"``, ``"6h"``, ``"7d"`` into seconds.

    Raises ``ValueError`` for any other input (empty, missing unit, unknown unit, negative).
    """
    if not isinstance(spec, str):
        raise ValueError(f"interval must be a string, got {type(spec).__name__}")
    match = _INTERVAL_RE.match(spec)
    if not match:
        raise ValueError(f"invalid interval spec: {spec!r}")
    n = int(match.group(1))
    unit = match.group(2).lower()
    if n <= 0:
        raise ValueError(f"interval must be positive: {spec!r}")
    return n * _INTERVAL_UNIT_SECONDS[unit]


@dataclass
class RetryPolicy:
    backoff_seconds: list[int]
    max_attempts: int


@dataclass
class RetryConfig:
    on_429: RetryPolicy = field(
        default_factory=lambda: RetryPolicy(backoff_seconds=[60, 120, 240, 480], max_attempts=4)
    )
    on_5xx: RetryPolicy = field(
        default_factory=lambda: RetryPolicy(backoff_seconds=[10, 30, 60], max_attempts=3)
    )


@dataclass
class BudgetConfig:
    monthly_soft_cap_gb: int = 18
    monthly_hard_cap_gb: int = 20
    soft_cap_behavior: str = "pause_until_next_month"  # | "warn_only"


@dataclass
class DiscoveryConfig:
    refresh_interval: str = "7d"

    @property
    def refresh_interval_seconds(self) -> int:
        return parse_interval(self.refresh_interval)


@dataclass
class CategoryConfig:
    """Generic per-category config; specific keys live in ``extra``.

    Common fields (``enabled``, ``interval``) are split out so the manager
    can inspect them without knowing the category. All other YAML keys go
    into ``extra`` and are interpreted by the concrete category harvester.
    """

    enabled: bool
    interval: str
    extra: dict[str, Any]

    @property
    def interval_seconds(self) -> int:
        return parse_interval(self.interval)


@dataclass
class HarvestConfig:
    state_dir: str = "~/.aiofmp/cache"
    log_level: str = "INFO"
    shutdown_grace_seconds: int = 30
    budget: BudgetConfig = field(default_factory=BudgetConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    categories: dict[str, CategoryConfig] = field(default_factory=dict)
