"""FMP plan capability matrix.

Each plan tier has a different per-minute API rate, monthly bandwidth cap,
historical-data depth, and set of available endpoints. The harvester reads
``plan`` from ``harvester.yaml`` and uses the values here to:

  - Pace requests so we stay under the per-minute rate cap (see
    ``aiofmp.base._SlidingWindowRateLimiter``).
  - Pick sensible defaults for ``backfill_years`` and ``periods``.
  - Filter symbol universes (Starter is US-only).
  - Auto-disable categories that are entirely paywalled.
  - Skip per-endpoint paywalls (e.g. ``statements.key_metrics`` doesn't
    accept ``period=quarter`` on Starter).

The Starter row was verified by probing the live FMP API in 2026-05
(see ``scripts/probe_plan.sh``). Premium/Ultimate rows are
conservatively populated as "everything Starter blocks plus quarter
fundamentals" — re-probe with a Premium key to verify.

Keep in sync with https://site.financialmodelingprep.com/developer/docs/pricing
when FMP changes their tiers.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlanLimits:
    """Capability snapshot for one FMP plan tier."""

    name: str
    calls_per_minute: int
    monthly_bandwidth_gb: int
    historical_years: int
    us_only_coverage: bool
    #: Categories that are 100% paywalled on this plan. The manager will skip
    #: them at start-up with an info-level log line instead of letting them
    #: discover-and-short-circuit every cycle.
    paywalled_categories: frozenset[str] = field(default_factory=frozenset)
    #: Statement endpoints whose ``period=quarter`` variant is paywalled.
    #: The remaining quarterly endpoints still run.
    quarterly_paywalled_statement_endpoints: frozenset[str] = field(
        default_factory=frozenset
    )
    #: Intraday chart timeframes that the plan doesn't include. The harvester
    #: drops these from each intraday category's ``timeframes`` list with a
    #: one-line log notice.
    intraday_paywalled_timeframes: frozenset[str] = field(default_factory=frozenset)
    #: News variants paywalled on this plan. Filtered out of news.variants.
    paywalled_news_variants: frozenset[str] = field(default_factory=frozenset)
    #: Whether ``analyst.financial_estimates`` with ``period=quarter`` is paywalled.
    quarterly_analyst_estimates_paywalled: bool = False


# Per-plan capability snapshot. Keep in sync with FMP's pricing page.
PLAN_LIMITS: dict[str, PlanLimits] = {
    # Basic is 250 calls/DAY, not per-minute. We normalise to a very low RPM
    # so the limiter never blows the daily cap during sustained use. Not
    # probed live; assume Basic is at least as restricted as Starter.
    "basic": PlanLimits(
        name="basic",
        calls_per_minute=10,
        monthly_bandwidth_gb=0,  # 500 MB; rounded down for the soft cap
        historical_years=5,
        us_only_coverage=True,
        paywalled_categories=frozenset({"form13f"}),
        quarterly_paywalled_statement_endpoints=frozenset(
            {
                "key_metrics",
                "financial_ratios",
                "revenue_product_segmentation",
                "revenue_geographic_segmentation",
            }
        ),
        intraday_paywalled_timeframes=frozenset({"1min"}),
        paywalled_news_variants=frozenset({"press_releases"}),
        quarterly_analyst_estimates_paywalled=True,
    ),
    "starter": PlanLimits(
        # Live testing showed FMP server-side 429s firing under sustained
        # 300 RPM (the documented cap). We pace at 250 RPM to leave a
        # ~17% safety margin and absorb residual transient 429s via the
        # retry inside _make_request.
        name="starter",
        calls_per_minute=250,
        monthly_bandwidth_gb=20,
        historical_years=5,
        us_only_coverage=True,
        paywalled_categories=frozenset({"form13f"}),
        quarterly_paywalled_statement_endpoints=frozenset(
            {
                "key_metrics",
                "financial_ratios",
                "revenue_product_segmentation",
                "revenue_geographic_segmentation",
            }
        ),
        intraday_paywalled_timeframes=frozenset({"1min"}),
        paywalled_news_variants=frozenset({"press_releases"}),
        quarterly_analyst_estimates_paywalled=True,
    ),
    "premium": PlanLimits(
        # Same ~17% safety margin as Starter. FMP's documented cap is 750 RPM.
        name="premium",
        calls_per_minute=625,
        monthly_bandwidth_gb=50,
        historical_years=30,
        us_only_coverage=False,
        # Premium gets everything Starter has plus full fundamentals,
        # intraday and technical indicators. The full 13F path may still
        # require Ultimate; left enabled here and the paywall short-circuit
        # will catch it if so.
    ),
    "ultimate": PlanLimits(
        # Same ~17% safety margin. FMP's documented cap is 3000 RPM.
        name="ultimate",
        calls_per_minute=2500,
        monthly_bandwidth_gb=150,
        historical_years=30,
        us_only_coverage=False,
    ),
}


#: FMP's actual economic-indicator names. The defaults the harvester used
#: to ship (UNRATE, FEDFUNDS, DFF, DCOILWTICO) are FRED codes; FMP uses
#: these instead and returns ``"Invalid name"`` for the FRED codes.
VALID_ECONOMIC_INDICATORS: tuple[str, ...] = (
    "GDP",
    "realGDP",
    "CPI",
    "inflationRate",
    "consumerSentiment",
    "unemploymentRate",
    "federalFunds",
    "retailSales",
)


def get_plan_limits(name: str) -> PlanLimits:
    """Return the capability snapshot for ``name`` or raise ``ValueError``."""
    key = name.lower()
    if key not in PLAN_LIMITS:
        raise ValueError(
            f"unknown plan {name!r}; valid plans: {sorted(PLAN_LIMITS)}"
        )
    return PLAN_LIMITS[key]


def is_us_symbol(symbol: str, payload: dict[str, Any] | None = None) -> bool:
    """Heuristic: True if ``symbol`` is plausibly a US-listed equity/ETF/index.

    Used to filter ``actively_trading`` / ``financial_symbols`` / ``indexes``
    universes when ``us_only_coverage=True``.

    When ``payload`` is provided (write/refresh time), uses the FMP-returned
    metadata as the authoritative signal:
      - ``currency`` (when present and not USD) → drop. This is the most
        reliable signal for indexes, where the symbol heuristic alone is
        insufficient — ``^AVFOCGRW``, ``^AFLI``, ``^AEX`` etc. have no
        suffix dot but are non-US.

    When ``payload`` is absent (read-time pass through stored symbols), or
    when payload doesn't include a currency, falls back to a symbol-shape
    heuristic:
      - Symbols containing ``.`` are foreign exchange suffixes (``.HK``,
        ``.SS``, ``.IS``, ``.JK``, ``.WA``, ``.SG``, etc.) → drop.
      - Symbols starting with ``0P`` are Morningstar mutual-fund identifiers
        for international funds → drop.
      - Everything else (``AAPL``, ``MSFT``, ``BRK-B``, ``^GSPC``, ``^DJI``)
        is kept.

    Some non-US symbols still slip through (e.g. ADRs without an exchange
    suffix). Those hit 402 on Starter and the per-category paywall
    short-circuit catches them.
    """
    if not symbol:
        return False
    if payload is not None:
        currency = payload.get("currency")
        if isinstance(currency, str) and currency.strip() and currency.upper() != "USD":
            return False
    if "." in symbol:
        return False
    if symbol.startswith("0P"):
        return False
    return True
