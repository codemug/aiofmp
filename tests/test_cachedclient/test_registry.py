"""Tests for the endpoint registry."""

from aiofmp.cachedclient.gap import DateParamType
from aiofmp.cachedclient.registry import (
    CacheableEndpoint,
    EndpointRegistry,
    TemporalPattern,
    build_default_registry,
)


class TestEndpointRegistry:
    def test_register_and_get(self):
        registry = EndpointRegistry()
        ep = CacheableEndpoint(
            category="chart",
            method="historical_price_full",
            api_endpoint="historical-price-eod/full",
            pattern=TemporalPattern.DATE_RANGE,
            entity_key_args=["symbol"],
        )
        registry.register(ep)
        assert registry.get("chart", "historical_price_full") is ep

    def test_get_nonexistent(self):
        registry = EndpointRegistry()
        assert registry.get("chart", "nonexistent") is None

    def test_is_cacheable(self):
        registry = EndpointRegistry()
        ep = CacheableEndpoint(
            category="chart",
            method="historical_price_full",
            api_endpoint="historical-price-eod/full",
            pattern=TemporalPattern.DATE_RANGE,
        )
        registry.register(ep)
        assert registry.is_cacheable("chart", "historical_price_full")
        assert not registry.is_cacheable("chart", "nonexistent")
        assert not registry.is_cacheable("nonexistent", "historical_price_full")

    def test_all_endpoints(self):
        registry = EndpointRegistry()
        ep1 = CacheableEndpoint(
            category="chart",
            method="m1",
            api_endpoint="e1",
            pattern=TemporalPattern.DATE_RANGE,
        )
        ep2 = CacheableEndpoint(
            category="statements",
            method="m2",
            api_endpoint="e2",
            pattern=TemporalPattern.PERIOD_BASED,
        )
        registry.register(ep1)
        registry.register(ep2)
        assert len(registry.all_endpoints()) == 2


class TestDefaultRegistry:
    def setup_method(self):
        self.registry = build_default_registry()

    # --- Pattern A: Chart daily ---
    def test_chart_daily_endpoints_registered(self):
        for method in [
            "historical_price_light",
            "historical_price_full",
            "historical_price_unadjusted",
            "historical_price_dividend_adjusted",
        ]:
            ep = self.registry.get("chart", method)
            assert ep is not None, f"chart.{method} not registered"
            assert ep.pattern == TemporalPattern.DATE_RANGE
            assert ep.entity_key_args == ["symbol"]
            assert ep.date_param_type == DateParamType.STRING

    # --- Pattern A: Chart intraday ---
    def test_chart_intraday_endpoints_registered(self):
        for method in [
            "intraday_1min",
            "intraday_5min",
            "intraday_15min",
            "intraday_30min",
            "intraday_1hour",
            "intraday_4hour",
        ]:
            ep = self.registry.get("chart", method)
            assert ep is not None, f"chart.{method} not registered"
            assert ep.pattern == TemporalPattern.DATE_RANGE
            assert ep.response_date_format == "%Y-%m-%d %H:%M:%S"

    # --- Pattern A: Economics ---
    def test_economics_endpoints_registered(self):
        ep = self.registry.get("economics", "treasury_rates")
        assert ep is not None
        assert ep.entity_key_args == []  # global dataset

        ep = self.registry.get("economics", "economic_indicators")
        assert ep is not None
        assert ep.entity_key_args == ["name"]

    # --- Pattern A: COT ---
    def test_cot_endpoints_registered(self):
        for method in ["cot_report", "cot_analysis"]:
            ep = self.registry.get("cot", method)
            assert ep is not None
            assert ep.entity_key_args == ["symbol"]

    # --- Pattern A: Technical Indicators ---
    def test_technical_indicators_registered(self):
        for method in [
            "simple_moving_average",
            "exponential_moving_average",
            "relative_strength_index",
        ]:
            ep = self.registry.get("technical_indicators", method)
            assert ep is not None
            assert ep.extra_key_args == ["period_length", "timeframe"]
            assert ep.date_param_type == DateParamType.DATE_OBJ

    # --- Pattern A: Market Performance ---
    def test_market_performance_registered(self):
        ep = self.registry.get("market_performance", "historical_sector_performance")
        assert ep is not None
        assert ep.entity_key_args == ["sector"]
        assert ep.date_param_type == DateParamType.DATE_OBJ

        ep = self.registry.get("market_performance", "historical_industry_pe")
        assert ep is not None
        assert ep.entity_key_args == ["industry"]

    # --- Pattern A: Calendar ---
    def test_calendar_date_range_registered(self):
        for method in [
            "dividends_calendar",
            "earnings_calendar",
            "ipos_calendar",
        ]:
            ep = self.registry.get("calendar", method)
            assert ep is not None
            assert ep.pattern == TemporalPattern.DATE_RANGE

    # --- Pattern A: News ---
    def test_news_registered(self):
        ep = self.registry.get("news", "stock_news")
        assert ep is not None
        assert ep.response_date_field == "publishedDate"
        assert ep.date_param_type == DateParamType.DATE_OBJ

        ep = self.registry.get("news", "search_stock_news")
        assert ep is not None
        assert ep.entity_key_args == ["symbols"]

    # --- Pattern B: Statements ---
    def test_statements_registered(self):
        for method in [
            "income_statement",
            "balance_sheet_statement",
            "cash_flow_statement",
            "key_metrics",
            "financial_ratios",
        ]:
            ep = self.registry.get("statements", method)
            assert ep is not None, f"statements.{method} not registered"
            assert ep.pattern == TemporalPattern.PERIOD_BASED
            assert ep.entity_key_args == ["symbol"]
            assert ep.extra_key_args == ["period"]
            assert ep.limit_param == "limit"

    def test_owner_earnings_registered(self):
        ep = self.registry.get("statements", "owner_earnings")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PERIOD_BASED
        assert ep.extra_key_args == []  # no period param

    # --- Non-cacheable endpoints are NOT in registry ---
    def test_non_cacheable_not_registered(self):
        assert not self.registry.is_cacheable("company", "profile")
        assert not self.registry.is_cacheable("search", "symbols")
        assert not self.registry.is_cacheable("dcf", "dcf_valuation")
        assert not self.registry.is_cacheable("quote", "stock_quote")

    def test_total_endpoint_count(self):
        """Ensure we have a reasonable number of registered endpoints."""
        all_eps = self.registry.all_endpoints()
        # Phase 1: ~56 endpoints
        assert len(all_eps) >= 50
