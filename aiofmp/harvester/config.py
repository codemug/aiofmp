"""Configuration for the harvester."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SchedulerConfig:
    """Scheduler settings for recurring harvest cycles."""
    interval_seconds: int = 3600
    run_on_start: bool = True


@dataclass
class ThrottleConfig:
    """Throttling settings between categories."""
    delay_seconds: float = 2.0


@dataclass
class SymbolsConfig:
    """Symbol resolution configuration."""
    mode: str = "explicit"  # "explicit" | "discover" | "file:/path/to/symbols.txt"
    symbols: list[str] = field(default_factory=list)


@dataclass
class HarvestConfig:
    """Main configuration for the harvester."""
    categories: list[str] = field(default_factory=lambda: [
        "directory", "analyst", "calendar", "chart", "company",
        "commodity", "form13f", "dcf", "insider_trades", "statements",
        "forex", "economics", "etf", "indexes", "news", "quote",
    ])
    symbols: SymbolsConfig = field(default_factory=SymbolsConfig)
    lookback_days: int = 1825  # 5 years
    statement_limit: int = 40
    periods: list[str] = field(default_factory=lambda: ["annual", "quarter"])
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    throttle: ThrottleConfig = field(default_factory=ThrottleConfig)
    overrides: dict[str, dict[str, Any]] = field(default_factory=dict)
