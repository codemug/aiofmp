"""Tests that historical-price endpoints are registered under commodity/forex/indexes too."""

from __future__ import annotations

from aiofmp.cachedclient.gap import DateParamType
from aiofmp.cachedclient.registry import TemporalPattern, build_default_registry


class TestMultiCategoryRegistration:
    def test_commodity_historical_price_full(self) -> None:
        reg = build_default_registry()
        ep = reg.get("commodity", "historical_price_full")
        assert ep is not None
        assert ep.pattern == TemporalPattern.DATE_RANGE
        assert ep.api_endpoint == "historical-price-eod/full"
        assert ep.entity_key_args == ["symbol"]
        assert ep.date_param_type == DateParamType.STRING

    def test_commodity_intraday(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("commodity", m)
            assert ep is not None, f"missing commodity.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.STRING

    def test_forex_historical_and_intraday(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("historical_price_full", "historical-price-eod/full"),
            ("historical_price_light", "historical-price-eod/light"),
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("forex", m)
            assert ep is not None, f"missing forex.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.STRING

    def test_indexes_uses_date_obj(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("historical_price_eod_full", "historical-price-eod/full"),
            ("historical_price_eod_light", "historical-price-eod/light"),
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("indexes", m)
            assert ep is not None, f"missing indexes.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.DATE_OBJ

    def test_same_storage_key_across_categories(self) -> None:
        """commodity.historical_price_full and chart.historical_price_full must produce
        the same storage key for the same symbol — that's the whole point of multi-registration."""
        from aiofmp.cachedclient.proxy import _derive_storage_key  # private helper

        reg = build_default_registry()
        chart_ep = reg.get("chart", "historical_price_full")
        commodity_ep = reg.get("commodity", "historical_price_full")
        assert chart_ep is not None and commodity_ep is not None
        bound = {"symbol": "GCUSD", "from_date": "2024-01-01", "to_date": "2024-12-31"}
        assert _derive_storage_key(chart_ep, bound) == _derive_storage_key(
            commodity_ep, bound
        )
