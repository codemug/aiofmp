"""FMP plan capability matrix.

Each plan tier has a different per-minute API rate, monthly bandwidth cap,
historical-data depth, and set of available endpoints. The harvester reads
``plan`` from ``harvester.yaml`` and uses the values here to:

  - Pace requests so we stay under the per-minute rate cap (see
    ``aiofmp.base._SlidingWindowRateLimiter``).
  - Pick sensible defaults for ``backfill_years`` and ``periods``.
  - Filter symbol universes (Starter is US-only).
  - Short-circuit categories that are guaranteed paywalled on the plan.

Values come from https://site.financialmodelingprep.com/developer/docs/pricing
(as of 2026-05). Keep in sync with that page when FMP changes their tiers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanLimits:
    """Capability snapshot for one FMP plan tier."""

    name: str
    calls_per_minute: int
    monthly_bandwidth_gb: int
    historical_years: int
    has_quarterly_fundamentals: bool
    us_only_coverage: bool


# Per-plan capability snapshot. Keep in sync with FMP's pricing page.
PLAN_LIMITS: dict[str, PlanLimits] = {
    # Basic is 250 calls/DAY, not per-minute. We normalise to a very low RPM
    # so the limiter never blows the daily cap during sustained use.
    "basic": PlanLimits(
        name="basic",
        calls_per_minute=10,
        monthly_bandwidth_gb=0,  # 500 MB, rounded down to 0 GB for the soft cap
        historical_years=5,
        has_quarterly_fundamentals=False,
        us_only_coverage=True,
    ),
    "starter": PlanLimits(
        name="starter",
        calls_per_minute=300,
        monthly_bandwidth_gb=20,
        historical_years=5,
        has_quarterly_fundamentals=False,
        us_only_coverage=True,
    ),
    "premium": PlanLimits(
        name="premium",
        calls_per_minute=750,
        monthly_bandwidth_gb=50,
        historical_years=30,
        has_quarterly_fundamentals=True,
        us_only_coverage=False,
    ),
    "ultimate": PlanLimits(
        name="ultimate",
        calls_per_minute=3000,
        monthly_bandwidth_gb=150,
        historical_years=30,
        has_quarterly_fundamentals=True,
        us_only_coverage=False,
    ),
}


def get_plan_limits(name: str) -> PlanLimits:
    """Return the capability snapshot for ``name`` or raise ``ValueError``."""
    key = name.lower()
    if key not in PLAN_LIMITS:
        raise ValueError(
            f"unknown plan {name!r}; valid plans: {sorted(PLAN_LIMITS)}"
        )
    return PLAN_LIMITS[key]


def is_us_symbol(symbol: str) -> bool:
    """Heuristic: True if ``symbol`` is plausibly a US-listed equity/ETF/index.

    Used to filter ``actively_trading`` / ``financial_symbols`` universes
    when ``us_only_coverage=True``. Rules:
      - Symbols containing ``.`` are foreign exchange suffixes (``.HK``,
        ``.SS``, ``.IS``, ``.JK``, ``.WA``, ``.SG``, etc.) → drop.
      - Symbols starting with ``0P`` are Morningstar mutual-fund identifiers
        for international funds → drop.
      - Symbols starting with ``^`` are indexes; keep only those without ``.``.
      - Everything else (``AAPL``, ``MSFT``, ``BRK-B``, ``GOOG.L`` — wait, dot drops
        this; that's intentional, ``GOOG.L`` is the London listing) → keep.

    This is a heuristic, not a guarantee. Some non-US symbols slip through
    (e.g. ADRs without an exchange suffix). Those will hit 402 on Starter and
    be filtered out by the per-category paywall short-circuit.
    """
    if not symbol:
        return False
    if "." in symbol:
        return False
    if symbol.startswith("0P"):
        return False
    return True
