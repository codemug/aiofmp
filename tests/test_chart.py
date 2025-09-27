"""
Unit tests for FMP Chart category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.chart import ChartCategory


class TestChartCategory:
    """Test cases for ChartCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def chart_category(self, mock_client):
        """Chart category instance with mocked client"""
        return ChartCategory(mock_client)

    @pytest.mark.asyncio
    async def test_historical_price_light_basic(self, chart_category, mock_client):
        """Test historical price light with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2025-02-04", "price": 232.8, "volume": 44489128}
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_light("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_dates(self, chart_category, mock_client):
        """Test historical price light with date parameters"""
        mock_response = [{"symbol": "AAPL", "date": "2025-02-04", "price": 232.8}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_light(
            "AAPL", "2025-01-01", "2025-03-31"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_basic(self, chart_category, mock_client):
        """Test historical price full with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "change": 5.6,
                "changePercent": 2.46479,
                "vwap": 230.86,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_full("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_with_dates(self, chart_category, mock_client):
        """Test historical price full with date parameters"""
        mock_response = [{"symbol": "AAPL", "date": "2025-02-04", "close": 232.8}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_full(
            "AAPL", "2025-01-01", "2025-03-31"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_unadjusted_basic(self, chart_category, mock_client):
        """Test historical price unadjusted with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "adjOpen": 227.2,
                "adjHigh": 233.13,
                "adjLow": 226.65,
                "adjClose": 232.8,
                "volume": 44489128,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_unadjusted("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/non-split-adjusted", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_unadjusted_with_dates(
        self, chart_category, mock_client
    ):
        """Test historical price unadjusted with date parameters"""
        mock_response = [{"symbol": "AAPL", "date": "2025-02-04", "adjClose": 232.8}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_unadjusted(
            "AAPL", "2025-01-01", "2025-03-31"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/non-split-adjusted",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_dividend_adjusted_basic(
        self, chart_category, mock_client
    ):
        """Test historical price dividend adjusted with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "adjOpen": 227.2,
                "adjHigh": 233.13,
                "adjLow": 226.65,
                "adjClose": 232.8,
                "volume": 44489128,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_dividend_adjusted("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/dividend-adjusted", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_dividend_adjusted_with_dates(
        self, chart_category, mock_client
    ):
        """Test historical price dividend adjusted with date parameters"""
        mock_response = [{"symbol": "AAPL", "date": "2025-02-04", "adjClose": 232.8}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_dividend_adjusted(
            "AAPL", "2025-01-01", "2025-03-31"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/dividend-adjusted",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_basic(self, chart_category, mock_client):
        """Test intraday 1min with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 15:59:00",
                "open": 233.01,
                "low": 232.72,
                "high": 233.13,
                "close": 232.79,
                "volume": 720121,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_1min("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_with_all_params(self, chart_category, mock_client):
        """Test intraday 1min with all parameters"""
        mock_response = [{"date": "2025-02-04 15:59:00", "close": 232.79}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_1min(
            "AAPL", "2025-01-01", "2025-01-02", False
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min",
            {
                "symbol": "AAPL",
                "from": "2025-01-01",
                "to": "2025-01-02",
                "nonadjusted": False,
            },
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_basic(self, chart_category, mock_client):
        """Test intraday 5min with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 15:55:00",
                "open": 232.87,
                "low": 232.72,
                "high": 233.13,
                "close": 232.79,
                "volume": 1555040,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_5min("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_with_dates(self, chart_category, mock_client):
        """Test intraday 5min with date parameters"""
        mock_response = [{"date": "2025-02-04 15:55:00", "close": 232.79}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_5min("AAPL", "2025-01-01", "2025-01-02")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-01-02"},
        )

    @pytest.mark.asyncio
    async def test_intraday_15min_basic(self, chart_category, mock_client):
        """Test intraday 15min with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 15:45:00",
                "open": 232.25,
                "low": 232.18,
                "high": 233.13,
                "close": 232.79,
                "volume": 2535629,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_15min("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/15min", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_intraday_15min_with_nonadjusted(self, chart_category, mock_client):
        """Test intraday 15min with nonadjusted parameter"""
        mock_response = [{"date": "2025-02-04 15:45:00", "close": 232.79}]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_15min("AAPL", nonadjusted=True)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/15min", {"symbol": "AAPL", "nonadjusted": True}
        )

    @pytest.mark.asyncio
    async def test_intraday_30min_basic(self, chart_category, mock_client):
        """Test intraday 30min with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 15:30:00",
                "open": 232.29,
                "low": 232.01,
                "high": 233.13,
                "close": 232.79,
                "volume": 3476320,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_30min("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/30min", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_basic(self, chart_category, mock_client):
        """Test intraday 1hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 15:30:00",
                "open": 232.29,
                "low": 232.01,
                "high": 233.13,
                "close": 232.37,
                "volume": 15079381,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_1hour("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_intraday_4hour_basic(self, chart_category, mock_client):
        """Test intraday 4hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 12:30:00",
                "open": 231.79,
                "low": 231.37,
                "high": 233.13,
                "close": 232.37,
                "volume": 23781913,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.intraday_4hour("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/4hour", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, chart_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await chart_category.historical_price_light("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, chart_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {
                "symbol": "AAPL",
                "date": f"2025-01-{i:02d}",
                "price": 200.0 + (i - 1) * 0.1,
                "volume": 1000000 + (i - 1) * 10000,
            }
            for i in range(1, 101)
        ]
        mock_client._make_request.return_value = large_response

        result = await chart_category.historical_price_light(
            "AAPL", "2025-01-01", "2025-04-10"
        )

        assert len(result) == 100
        assert result[0]["price"] == 200.0
        assert result[99]["price"] == 209.9
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-04-10"},
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, chart_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "price": 232.8,
                "volume": 44489128,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await chart_category.historical_price_light("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, chart_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "AAPL", "date": "2025-01-01", "price": 232.8}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await chart_category.historical_price_light("AAPL", "2025-01-01")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "AAPL", "from": "2025-01-01"}
        )

        # Test with only to_date
        result = await chart_category.historical_price_light(
            "AAPL", to_date="2025-03-31"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "AAPL", "to": "2025-03-31"}
        )

        # Test with both dates
        result = await chart_category.historical_price_light(
            "AAPL", "2025-01-01", "2025-03-31"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_nonadjusted_parameter_combinations(
        self, chart_category, mock_client
    ):
        """Test various nonadjusted parameter combinations for intraday methods"""
        mock_response = [{"date": "2025-01-01 15:30:00", "close": 232.8}]
        mock_client._make_request.return_value = mock_response

        # Test with nonadjusted=True
        result = await chart_category.intraday_1min("AAPL", nonadjusted=True)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-chart/1min", {"symbol": "AAPL", "nonadjusted": True}
        )

        # Test with nonadjusted=False
        result = await chart_category.intraday_5min("AAPL", nonadjusted=False)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-chart/5min", {"symbol": "AAPL", "nonadjusted": False}
        )

        # Test with nonadjusted=None (should not be included in params)
        result = await chart_category.intraday_15min("AAPL", nonadjusted=None)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-chart/15min", {"symbol": "AAPL"}
        )
