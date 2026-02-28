"""Endpoint metadata registry for the cached client.

Describes which SDK methods are cacheable and how to extract
date ranges, storage keys, and temporal patterns from their arguments.
"""

from dataclasses import dataclass, field
from enum import Enum

from .gap import DateParamType


class TemporalPattern(str, Enum):
    """How an endpoint's time-series data is parameterized."""

    DATE_RANGE = "date_range"  # Pattern A: from/to date params
    PERIOD_BASED = "period_based"  # Pattern B: limit/period params


@dataclass(frozen=True)
class CacheableEndpoint:
    """Metadata describing how to cache a specific endpoint."""

    # Identity: (category, method) is the lookup key
    category: str  # e.g., "chart"
    method: str  # e.g., "historical_price_full"
    api_endpoint: str  # e.g., "historical-price-eod/full"

    # Temporal pattern
    pattern: TemporalPattern

    # Positional/keyword arg names that form the entity part of the storage key.
    # e.g., ["symbol"] for chart, ["name"] for economic_indicators
    entity_key_args: list[str] = field(default_factory=list)

    # Response date field name and format
    response_date_field: str = "date"
    response_date_format: str = "%Y-%m-%d"

    # Pattern A: which kwargs hold the date range
    from_param: str = "from_date"
    to_param: str = "to_date"
    date_param_type: DateParamType = DateParamType.STRING

    # Pattern B: which kwargs hold the period selector and limit
    period_param: str | None = None
    limit_param: str | None = None

    # Extra params that form part of the storage key but aren't entity identifiers.
    # e.g., ["period_length", "timeframe"] for technical indicators,
    #        ["period"] for statements (annual vs quarter)
    extra_key_args: list[str] = field(default_factory=list)

    # Ordered list of parameter names (excluding `self`) matching the real
    # SDK method signature.  Used by the proxy to bind positional args to
    # names without relying on runtime introspection.
    call_params: list[str] = field(default_factory=list)


class EndpointRegistry:
    """Registry mapping (category, method) to CacheableEndpoint metadata."""

    def __init__(self) -> None:
        self._endpoints: dict[tuple[str, str], CacheableEndpoint] = {}

    def register(self, endpoint: CacheableEndpoint) -> None:
        key = (endpoint.category, endpoint.method)
        self._endpoints[key] = endpoint

    def get(self, category: str, method: str) -> CacheableEndpoint | None:
        return self._endpoints.get((category, method))

    def is_cacheable(self, category: str, method: str) -> bool:
        return (category, method) in self._endpoints

    def all_endpoints(self) -> list[CacheableEndpoint]:
        return list(self._endpoints.values())


def build_default_registry() -> EndpointRegistry:
    """Build the default registry with all Phase 1 cacheable endpoints."""
    registry = EndpointRegistry()

    # =========================================================================
    # Pattern A: Date-range endpoints (from/to params)
    # =========================================================================

    # --- Chart (daily) --- str dates ---
    for method, endpoint in [
        ("historical_price_light", "historical-price-eod/light"),
        ("historical_price_full", "historical-price-eod/full"),
        ("historical_price_unadjusted", "historical-price-eod/non-split-adjusted"),
        (
            "historical_price_dividend_adjusted",
            "historical-price-eod/dividend-adjusted",
        ),
    ]:
        registry.register(
            CacheableEndpoint(
                category="chart",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )

    # --- Chart (intraday) --- str dates ---
    for method, endpoint in [
        ("intraday_1min", "historical-chart/1min"),
        ("intraday_5min", "historical-chart/5min"),
        ("intraday_15min", "historical-chart/15min"),
        ("intraday_30min", "historical-chart/30min"),
        ("intraday_1hour", "historical-chart/1hour"),
        ("intraday_4hour", "historical-chart/4hour"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="chart",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )

    # --- Economics --- str dates ---
    registry.register(
        CacheableEndpoint(
            category="economics",
            method="treasury_rates",
            api_endpoint="treasury-rates",
            pattern=TemporalPattern.DATE_RANGE,
            entity_key_args=[],
            date_param_type=DateParamType.STRING,
            call_params=["from_date", "to_date"],
        )
    )
    registry.register(
        CacheableEndpoint(
            category="economics",
            method="economic_indicators",
            api_endpoint="economic-indicators",
            pattern=TemporalPattern.DATE_RANGE,
            entity_key_args=["name"],
            date_param_type=DateParamType.STRING,
            call_params=["name", "from_date", "to_date"],
        )
    )
    registry.register(
        CacheableEndpoint(
            category="economics",
            method="economic_calendar",
            api_endpoint="economic-calendar",
            pattern=TemporalPattern.DATE_RANGE,
            entity_key_args=[],
            response_date_format="%Y-%m-%d %H:%M:%S",
            date_param_type=DateParamType.STRING,
            call_params=["from_date", "to_date"],
        )
    )

    # --- COT --- str dates ---
    for method, endpoint in [
        ("cot_report", "commitment-of-traders-report"),
        ("cot_analysis", "commitment-of-traders-analysis"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="cot",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )

    # --- Company historical market cap --- str dates ---
    registry.register(
        CacheableEndpoint(
            category="company",
            method="historical_market_cap",
            api_endpoint="historical-market-capitalization",
            pattern=TemporalPattern.DATE_RANGE,
            entity_key_args=["symbol"],
            date_param_type=DateParamType.STRING,
            call_params=["symbol", "limit", "from_date", "to_date"],
        )
    )

    # --- Market Performance (historical) --- date objects ---
    for method, endpoint in [
        ("historical_sector_performance", "historical-sector-performance"),
        ("historical_industry_performance", "historical-industry-performance"),
    ]:
        entity_arg = "sector" if "sector" in method else "industry"
        registry.register(
            CacheableEndpoint(
                category="market_performance",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=[entity_arg],
                date_param_type=DateParamType.DATE_OBJ,
                call_params=[entity_arg, "from_date", "to_date", "exchange"],
            )
        )
    for method, endpoint in [
        ("historical_sector_pe", "historical-sector-pe"),
        ("historical_industry_pe", "historical-industry-pe"),
    ]:
        entity_arg = "sector" if "sector" in method else "industry"
        registry.register(
            CacheableEndpoint(
                category="market_performance",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=[entity_arg],
                date_param_type=DateParamType.DATE_OBJ,
                call_params=[entity_arg, "from_date", "to_date", "exchange"],
            )
        )

    # --- Technical Indicators --- date objects, extra key args ---
    for method, endpoint_suffix in [
        ("simple_moving_average", "sma"),
        ("exponential_moving_average", "ema"),
        ("weighted_moving_average", "wma"),
        ("double_exponential_moving_average", "dema"),
        ("triple_exponential_moving_average", "tema"),
        ("relative_strength_index", "rsi"),
        ("standard_deviation", "standarddeviation"),
        ("williams_percent_r", "williams"),
        ("average_directional_index", "adx"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="technical_indicators",
                method=method,
                api_endpoint=f"technical-indicators/{endpoint_suffix}",
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                extra_key_args=["period_length", "timeframe"],
                date_param_type=DateParamType.DATE_OBJ,
                response_date_format="%Y-%m-%d %H:%M:%S",
                call_params=[
                    "symbol",
                    "period_length",
                    "timeframe",
                    "from_date",
                    "to_date",
                ],
            )
        )

    # --- Calendar (date-range) --- str dates ---
    for method, endpoint in [
        ("dividends_calendar", "dividends-calendar"),
        ("earnings_calendar", "earnings-calendar"),
        ("ipos_calendar", "ipos-calendar"),
        ("ipos_disclosure", "ipos-disclosure"),
        ("ipos_prospectus", "ipos-prospectus"),
        ("stock_splits_calendar", "splits-calendar"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="calendar",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=[],
                date_param_type=DateParamType.STRING,
                call_params=["from_date", "to_date"],
            )
        )

    # --- News (date-range, latest variants) --- date objects ---
    for method, endpoint in [
        ("general_news", "news/general-latest"),
        ("press_releases", "news/press-releases-latest"),
        ("stock_news", "news/stock-latest"),
        ("crypto_news", "news/crypto-latest"),
        ("forex_news", "news/forex-latest"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="news",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=[],
                response_date_field="publishedDate",
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.DATE_OBJ,
                call_params=["page", "limit", "from_date", "to_date"],
            )
        )

    # --- News (search variants with symbols) --- date objects ---
    for method, endpoint in [
        ("search_press_releases", "news/press-releases"),
        ("search_stock_news", "news/stock"),
        ("search_crypto_news", "news/crypto"),
        ("search_forex_news", "news/forex"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="news",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbols"],
                response_date_field="publishedDate",
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.DATE_OBJ,
                call_params=["symbols", "page", "limit", "from_date", "to_date"],
            )
        )

    # =========================================================================
    # Pattern B: Period-based endpoints (limit/period params)
    # =========================================================================

    # --- Statements (with period param) ---
    for method, endpoint in [
        ("income_statement", "income-statement"),
        ("balance_sheet_statement", "balance-sheet-statement"),
        ("cash_flow_statement", "cash-flow-statement"),
        ("key_metrics", "key-metrics"),
        ("financial_ratios", "ratios"),
        ("enterprise_values", "enterprise-values"),
        ("income_statement_growth", "income-statement-growth"),
        ("balance_sheet_statement_growth", "balance-sheet-statement-growth"),
        ("cash_flow_statement_growth", "cash-flow-statement-growth"),
        ("financial_statement_growth", "financial-growth"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="statements",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.PERIOD_BASED,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                period_param="period",
                limit_param="limit",
                call_params=["symbol", "limit", "period"],
            )
        )

    # --- Statements (owner earnings — no period param) ---
    registry.register(
        CacheableEndpoint(
            category="statements",
            method="owner_earnings",
            api_endpoint="owner-earnings",
            pattern=TemporalPattern.PERIOD_BASED,
            entity_key_args=["symbol"],
            limit_param="limit",
            call_params=["symbol", "limit"],
        )
    )

    # --- Statements segmentation ---
    for method, endpoint in [
        ("revenue_product_segmentation", "revenue-product-segmentation"),
        ("revenue_geographic_segmentation", "revenue-geographic-segmentation"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="statements",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.PERIOD_BASED,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                period_param="period",
                call_params=["symbol", "period", "structure"],
            )
        )

    return registry
