"""
Unit tests for FMP Indexes category
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.indexes import IndexesCategory


class TestIndexesCategory:
    """Test cases for IndexesCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def indexes_category(self, mock_client):
        """Indexes category instance with mocked client"""
        return IndexesCategory(mock_client)

    @pytest.mark.asyncio
    async def test_index_list_basic(self, indexes_category, mock_client):
        """Test index list with no parameters"""
        mock_response = [
            {
                "symbol": "^TTIN",
                "name": "S&P/TSX Capped Industrials Index",
                "exchange": "TSX",
                "currency": "CAD",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("index-list")

    @pytest.mark.asyncio
    async def test_index_quote_basic(self, indexes_category, mock_client):
        """Test index quote with required parameters"""
        mock_response = [
            {
                "symbol": "^GSPC",
                "name": "S&P 500",
                "price": 6366.13,
                "changePercentage": 0.11354,
                "change": 7.22,
                "volume": 1498664000,
                "dayLow": 6360.57,
                "dayHigh": 6379.54,
                "yearHigh": 6379.54,
                "yearLow": 4835.04,
                "marketCap": 0,
                "priceAvg50": 6068.663,
                "priceAvg200": 5880.0864,
                "exchange": "INDEX",
                "open": 6368.6,
                "previousClose": 6358.91,
                "timestamp": 1753374601,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_quote("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "^GSPC"})

    @pytest.mark.asyncio
    async def test_index_quote_short_basic(self, indexes_category, mock_client):
        """Test index quote short with required parameters"""
        mock_response = [
            {"symbol": "^GSPC", "price": 6366.13, "change": 7.22, "volume": 1498664000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_quote_short("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_all_index_quotes_basic(self, indexes_category, mock_client):
        """Test all index quotes with no parameters"""
        mock_response = [
            {"symbol": "^DJBGIE", "price": 4155.76, "change": 1.09, "volume": 0}
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.all_index_quotes()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("batch-index-quotes", {})

    @pytest.mark.asyncio
    async def test_all_index_quotes_with_short(self, indexes_category, mock_client):
        """Test all index quotes with short parameter"""
        mock_response = [{"symbol": "^DJBGIE", "price": 4155.76}]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.all_index_quotes(short=True)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "batch-index-quotes", {"short": True}
        )

    @pytest.mark.asyncio
    async def test_historical_price_eod_light_basic(
        self, indexes_category, mock_client
    ):
        """Test historical price EOD light with required parameters only"""
        mock_response = [
            {
                "symbol": "^GSPC",
                "date": "2025-07-24",
                "price": 6365.77,
                "volume": 1499302000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.historical_price_eod_light("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_eod_light_with_dates(
        self, indexes_category, mock_client
    ):
        """Test historical price EOD light with date parameters"""
        mock_response = [{"symbol": "^GSPC", "date": "2025-07-24", "price": 6365.77}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 4, 25)
        to_date = date(2025, 7, 25)

        result = await indexes_category.historical_price_eod_light(
            "^GSPC", from_date, to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "^GSPC", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_eod_full_basic(self, indexes_category, mock_client):
        """Test historical price EOD full with required parameters only"""
        mock_response = [
            {
                "symbol": "^GSPC",
                "date": "2025-07-24",
                "open": 6368.6,
                "high": 6379.54,
                "low": 6360.57,
                "close": 6365.77,
                "volume": 1499302000,
                "change": -2.83,
                "changePercent": -0.04443677,
                "vwap": 6368.63,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.historical_price_eod_full("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_eod_full_with_dates(
        self, indexes_category, mock_client
    ):
        """Test historical price EOD full with date parameters"""
        mock_response = [{"symbol": "^GSPC", "date": "2025-07-24", "open": 6368.6}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 4, 25)
        to_date = date(2025, 7, 25)

        result = await indexes_category.historical_price_eod_full(
            "^GSPC", from_date, to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full",
            {"symbol": "^GSPC", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_basic(self, indexes_category, mock_client):
        """Test intraday 1min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 6365.34,
                "low": 6365.34,
                "high": 6366.09,
                "close": 6366.09,
                "volume": 4428000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.intraday_1min("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_with_dates(self, indexes_category, mock_client):
        """Test intraday 1min with date parameters"""
        mock_response = [{"date": "2025-07-24 12:29:00", "open": 6365.34}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 4, 25)
        to_date = date(2025, 7, 25)

        result = await indexes_category.intraday_1min("^GSPC", from_date, to_date)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min",
            {"symbol": "^GSPC", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_basic(self, indexes_category, mock_client):
        """Test intraday 5min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:30:00",
                "open": 6366.18,
                "low": 6365.57,
                "high": 6366.18,
                "close": 6365.69,
                "volume": 1574690,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.intraday_5min("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_with_dates(self, indexes_category, mock_client):
        """Test intraday 5min with date parameters"""
        mock_response = [{"date": "2025-07-24 12:30:00", "open": 6366.18}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 4, 25)
        to_date = date(2025, 7, 25)

        result = await indexes_category.intraday_5min("^GSPC", from_date, to_date)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min",
            {"symbol": "^GSPC", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_basic(self, indexes_category, mock_client):
        """Test intraday 1hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:30:00",
                "open": 6366.18,
                "low": 6365.57,
                "high": 6366.18,
                "close": 6365.69,
                "volume": 1574690,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.intraday_1hour("^GSPC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_with_dates(self, indexes_category, mock_client):
        """Test intraday 1hour with date parameters"""
        mock_response = [{"date": "2025-07-24 12:30:00", "open": 6366.18}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 4, 25)
        to_date = date(2025, 7, 25)

        result = await indexes_category.intraday_1hour("^GSPC", from_date, to_date)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour",
            {"symbol": "^GSPC", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, indexes_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await indexes_category.index_list()

        assert result == []
        mock_client._make_request.assert_called_once_with("index-list")

    @pytest.mark.asyncio
    async def test_large_response_handling(self, indexes_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple indexes
        large_response = [
            {
                "symbol": f"^INDEX{i:03d}",
                "name": f"Test Index {i}",
                "exchange": "TEST",
                "currency": "USD",
            }
            for i in range(1, 101)  # 100 indexes
        ]
        mock_client._make_request.return_value = large_response

        result = await indexes_category.index_list()

        assert len(result) == 100
        assert result[0]["symbol"] == "^INDEX001"
        assert result[99]["symbol"] == "^INDEX100"
        mock_client._make_request.assert_called_once_with("index-list")

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, indexes_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "^TTIN",
                "name": "S&P/TSX Capped Industrials Index",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_list()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("index-list")

    @pytest.mark.asyncio
    async def test_different_symbols(self, indexes_category, mock_client):
        """Test indexes functionality with different symbols"""
        mock_response = [{"symbol": "^GSPC", "name": "S&P 500"}]
        mock_client._make_request.return_value = mock_response

        # Test with S&P 500
        result = await indexes_category.index_quote("^GSPC")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "^GSPC"})

        # Test with Dow Jones
        result = await indexes_category.index_quote("^DJI")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "^DJI"})

        # Test with NASDAQ
        result = await indexes_category.index_quote("^IXIC")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "^IXIC"})

    @pytest.mark.asyncio
    async def test_different_date_formats(self, indexes_category, mock_client):
        """Test date handling with different date formats"""
        mock_response = [{"symbol": "^GSPC", "date": "2025-07-24"}]
        mock_client._make_request.return_value = mock_response

        # Test with different date combinations
        from_date = date(2025, 1, 1)
        to_date = date(2025, 12, 31)

        result = await indexes_category.historical_price_eod_full(
            "^GSPC", from_date, to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/full",
            {"symbol": "^GSPC", "from": "2025-01-01", "to": "2025-12-31"},
        )

        # Test with only from_date
        result = await indexes_category.historical_price_eod_full("^GSPC", from_date)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/full", {"symbol": "^GSPC", "from": "2025-01-01"}
        )

        # Test with only to_date
        result = await indexes_category.historical_price_eod_full(
            "^GSPC", to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/full", {"symbol": "^GSPC", "to": "2025-12-31"}
        )

    @pytest.mark.asyncio
    async def test_index_list_response_validation(self, indexes_category, mock_client):
        """Test index list response validation"""
        mock_response = [
            {
                "symbol": "^TTIN",
                "name": "S&P/TSX Capped Industrials Index",
                "exchange": "TSX",
                "currency": "CAD",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_list()

        assert len(result) == 1
        assert result[0]["symbol"] == "^TTIN"
        assert result[0]["name"] == "S&P/TSX Capped Industrials Index"
        assert result[0]["exchange"] == "TSX"
        assert result[0]["currency"] == "CAD"
        mock_client._make_request.assert_called_once_with("index-list")

    @pytest.mark.asyncio
    async def test_index_quote_response_validation(self, indexes_category, mock_client):
        """Test index quote response validation"""
        mock_response = [
            {
                "symbol": "^GSPC",
                "name": "S&P 500",
                "price": 6366.13,
                "change": 7.22,
                "volume": 1498664000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.index_quote("^GSPC")

        assert len(result) == 1
        assert result[0]["symbol"] == "^GSPC"
        assert result[0]["name"] == "S&P 500"
        assert result[0]["price"] == 6366.13
        assert result[0]["change"] == 7.22
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "^GSPC"})

    @pytest.mark.asyncio
    async def test_historical_data_response_validation(
        self, indexes_category, mock_client
    ):
        """Test historical data response validation"""
        mock_response = [
            {
                "symbol": "^GSPC",
                "date": "2025-07-24",
                "open": 6368.6,
                "high": 6379.54,
                "low": 6360.57,
                "close": 6365.77,
                "volume": 1499302000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.historical_price_eod_full("^GSPC")

        assert len(result) == 1
        assert result[0]["symbol"] == "^GSPC"
        assert result[0]["date"] == "2025-07-24"
        assert result[0]["open"] == 6368.6
        assert result[0]["high"] == 6379.54
        assert result[0]["low"] == 6360.57
        assert result[0]["close"] == 6365.77
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_intraday_data_response_validation(
        self, indexes_category, mock_client
    ):
        """Test intraday data response validation"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 6365.34,
                "low": 6365.34,
                "high": 6366.09,
                "close": 6366.09,
                "volume": 4428000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.intraday_1min("^GSPC")

        assert len(result) == 1
        assert result[0]["date"] == "2025-07-24 12:29:00"
        assert result[0]["open"] == 6365.34
        assert result[0]["low"] == 6365.34
        assert result[0]["high"] == 6366.09
        assert result[0]["close"] == 6366.09
        assert result[0]["volume"] == 4428000
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "^GSPC"}
        )

    @pytest.mark.asyncio
    async def test_all_index_quotes_response_validation(
        self, indexes_category, mock_client
    ):
        """Test all index quotes response validation"""
        mock_response = [
            {"symbol": "^DJBGIE", "price": 4155.76, "change": 1.09, "volume": 0}
        ]
        mock_client._make_request.return_value = mock_response

        result = await indexes_category.all_index_quotes()

        assert len(result) == 1
        assert result[0]["symbol"] == "^DJBGIE"
        assert result[0]["price"] == 4155.76
        assert result[0]["change"] == 1.09
        assert result[0]["volume"] == 0
        mock_client._make_request.assert_called_once_with("batch-index-quotes", {})

    @pytest.mark.asyncio
    async def test_parameter_edge_cases(self, indexes_category, mock_client):
        """Test parameter edge cases"""
        mock_response = [{"symbol": "^GSPC", "price": 6366.13}]
        mock_client._make_request.return_value = mock_response

        # Test with empty string symbol
        result = await indexes_category.index_quote("")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": ""})

        # Test with special characters in symbol
        result = await indexes_category.index_quote("^GSPC^")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "^GSPC^"})

        # Test with very long symbol
        long_symbol = "A" * 100
        result = await indexes_category.index_quote(long_symbol)
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": long_symbol})

    @pytest.mark.asyncio
    async def test_date_edge_cases(self, indexes_category, mock_client):
        """Test date edge cases"""
        mock_response = [{"symbol": "^GSPC", "date": "2025-07-24"}]
        mock_client._make_request.return_value = mock_response

        # Test with leap year date
        leap_date = date(2024, 2, 29)
        result = await indexes_category.historical_price_eod_light(
            "^GSPC", from_date=leap_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "^GSPC", "from": "2024-02-29"}
        )

        # Test with year boundary
        year_boundary = date(2025, 12, 31)
        result = await indexes_category.historical_price_eod_light(
            "^GSPC", to_date=year_boundary
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "^GSPC", "to": "2025-12-31"}
        )

        # Test with same from and to date
        same_date = date(2025, 7, 24)
        result = await indexes_category.historical_price_eod_light(
            "^GSPC", same_date, same_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light",
            {"symbol": "^GSPC", "from": "2025-07-24", "to": "2025-07-24"},
        )
