"""Harvester configuration dataclasses + YAML schema.

Defines the structured representation of `harvester.yaml` and the
`parse_interval` helper that turns strings like ``"6h"`` into seconds.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

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
        default_factory=lambda: RetryPolicy(
            backoff_seconds=[60, 120, 240, 480], max_attempts=4
        )
    )
    on_5xx: RetryPolicy = field(
        default_factory=lambda: RetryPolicy(
            backoff_seconds=[10, 30, 60], max_attempts=3
        )
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


def _parse_retry_policy(
    raw: dict[str, Any] | None, default: RetryPolicy
) -> RetryPolicy:
    if raw is None:
        return default
    return RetryPolicy(
        backoff_seconds=list(raw.get("backoff_seconds", default.backoff_seconds)),
        max_attempts=int(raw.get("max_attempts", default.max_attempts)),
    )


def _parse_categories(raw: dict[str, Any] | None) -> dict[str, CategoryConfig]:
    if not raw:
        return {}
    out: dict[str, CategoryConfig] = {}
    for name, body in raw.items():
        if not isinstance(body, dict):
            raise ValueError(
                f"category {name!r} must be a mapping, got {type(body).__name__}"
            )
        if "interval" not in body:
            raise ValueError(f"category {name!r} is missing required field: interval")
        if "enabled" not in body:
            raise ValueError(f"category {name!r} is missing required field: enabled")
        extra = {k: v for k, v in body.items() if k not in ("enabled", "interval")}
        out[name] = CategoryConfig(
            enabled=bool(body["enabled"]),
            interval=str(body["interval"]),
            extra=extra,
        )
        # Validate interval format early
        parse_interval(out[name].interval)
    return out


def load_config_from_yaml(path: str | Path) -> HarvestConfig:
    """Parse a YAML file into a HarvestConfig. Raises FileNotFoundError / ValueError on issues."""
    p = Path(os.path.expanduser(str(path)))
    if not p.exists():
        raise FileNotFoundError(f"config file not found: {p}")
    try:
        with open(p, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"yaml parse error: {e}") from e

    defaults = HarvestConfig()

    budget_raw = raw.get("budget") or {}
    budget = BudgetConfig(
        monthly_soft_cap_gb=int(
            budget_raw.get("monthly_soft_cap_gb", defaults.budget.monthly_soft_cap_gb)
        ),
        monthly_hard_cap_gb=int(
            budget_raw.get("monthly_hard_cap_gb", defaults.budget.monthly_hard_cap_gb)
        ),
        soft_cap_behavior=str(
            budget_raw.get("soft_cap_behavior", defaults.budget.soft_cap_behavior)
        ),
    )

    retry_raw = raw.get("retry") or {}
    retry = RetryConfig(
        on_429=_parse_retry_policy(retry_raw.get("on_429"), defaults.retry.on_429),
        on_5xx=_parse_retry_policy(retry_raw.get("on_5xx"), defaults.retry.on_5xx),
    )

    discovery_raw = raw.get("discovery") or {}
    discovery = DiscoveryConfig(
        refresh_interval=str(
            discovery_raw.get("refresh_interval", defaults.discovery.refresh_interval)
        ),
    )
    # Validate discovery interval early
    parse_interval(discovery.refresh_interval)

    return HarvestConfig(
        state_dir=str(raw.get("state_dir", defaults.state_dir)),
        log_level=str(raw.get("log_level", defaults.log_level)),
        shutdown_grace_seconds=int(
            raw.get("shutdown_grace_seconds", defaults.shutdown_grace_seconds)
        ),
        budget=budget,
        retry=retry,
        discovery=discovery,
        categories=_parse_categories(raw.get("categories")),
    )
