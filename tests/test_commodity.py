"""
Unit tests for FMP Commodity category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.commodity import CommodityCategory


class TestCommodityCategory:
    """Test cases for CommodityCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def commodity_category(self, mock_client):
        """Commodity category instance with mocked client"""
        return CommodityCategory(mock_client)

    @pytest.mark.asyncio
    async def test_commodities_list_basic(self, commodity_category, mock_client):
        """Test commodities list with no parameters"""
        mock_response = [
            {
                "symbol": "HEUSX",
                "name": "Lean Hogs Futures",
                "exchange": None,
                "tradeMonth": "Dec",
                "currency": "USX",
            },
            {
                "symbol": "GCUSD",
                "name": "Gold Futures",
                "exchange": "COMEX",
                "tradeMonth": "Dec",
                "currency": "USD",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.commodities_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("commodities-list", {})

    @pytest.mark.asyncio
    async def test_commodities_list_response_structure(
        self, commodity_category, mock_client
    ):
        """Test commodities list response structure"""
        mock_response = [
            {
                "symbol": "CLUSD",
                "name": "Crude Oil Futures",
                "exchange": "NYMEX",
                "tradeMonth": "Jan",
                "currency": "USD",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.commodities_list()

        assert len(result) == 1
        assert result[0]["symbol"] == "CLUSD"
        assert result[0]["name"] == "Crude Oil Futures"
        assert result[0]["exchange"] == "NYMEX"
        assert result[0]["tradeMonth"] == "Jan"
        assert result[0]["currency"] == "USD"
        mock_client._make_request.assert_called_once_with("commodities-list", {})

    @pytest.mark.asyncio
    async def test_quote_basic(self, commodity_category, mock_client):
        """Test quote with required parameters only"""
        mock_response = [
            {
                "symbol": "GCUSD",
                "name": "Gold Futures",
                "price": 3375.3,
                "changePercentage": -0.65635,
                "change": -22.3,
                "volume": 170936,
                "dayLow": 3355.2,
                "dayHigh": 3401.1,
                "yearHigh": 3509.9,
                "yearLow": 2354.6,
                "marketCap": None,
                "priceAvg50": 3358.706,
                "priceAvg200": 3054.501,
                "exchange": "COMMODITY",
                "open": 3398.6,
                "previousClose": 3397.6,
                "timestamp": 1753372205,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "GCUSD"})

    @pytest.mark.asyncio
    async def test_quote_response_structure(self, commodity_category, mock_client):
        """Test quote response structure"""
        mock_response = [
            {
                "symbol": "SIUSD",
                "name": "Silver Futures",
                "price": 25.50,
                "changePercentage": 1.25,
                "change": 0.32,
                "volume": 50000,
                "dayLow": 25.10,
                "dayHigh": 25.75,
                "yearHigh": 26.00,
                "yearLow": 20.00,
                "marketCap": None,
                "priceAvg50": 24.80,
                "priceAvg200": 23.50,
                "exchange": "COMMODITY",
                "open": 25.20,
                "previousClose": 25.18,
                "timestamp": 1753372205,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote("SIUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "SIUSD"
        assert result[0]["name"] == "Silver Futures"
        assert result[0]["price"] == 25.50
        assert result[0]["change"] == 0.32
        assert result[0]["volume"] == 50000
        assert result[0]["exchange"] == "COMMODITY"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "SIUSD"})

    @pytest.mark.asyncio
    async def test_quote_short_basic(self, commodity_category, mock_client):
        """Test quote short with required parameters only"""
        mock_response = [
            {"symbol": "GCUSD", "price": 3375.3, "change": -22.3, "volume": 170936}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote_short("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_quote_short_response_structure(
        self, commodity_category, mock_client
    ):
        """Test quote short response structure"""
        mock_response = [
            {"symbol": "CLUSD", "price": 75.25, "change": 1.50, "volume": 250000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote_short("CLUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "CLUSD"
        assert result[0]["price"] == 75.25
        assert result[0]["change"] == 1.50
        assert result[0]["volume"] == 250000
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "CLUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_basic(self, commodity_category, mock_client):
        """Test historical price light with required parameters only"""
        mock_response = [
            {"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8, "volume": 174758}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_light("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_dates(
        self, commodity_category, mock_client
    ):
        """Test historical price light with date parameters"""
        mock_response = [
            {"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8, "volume": 174758}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_light(
            "GCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_from_date_only(
        self, commodity_category, mock_client
    ):
        """Test historical price light with only from_date parameter"""
        mock_response = [{"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8}]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_light(
            "GCUSD", from_date="2025-04-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "GCUSD", "from": "2025-04-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_to_date_only(
        self, commodity_category, mock_client
    ):
        """Test historical price light with only to_date parameter"""
        mock_response = [{"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8}]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_light(
            "GCUSD", to_date="2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "GCUSD", "to": "2025-07-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_basic(self, commodity_category, mock_client):
        """Test historical price full with required parameters only"""
        mock_response = [
            {
                "symbol": "GCUSD",
                "date": "2025-07-24",
                "open": 3398.6,
                "high": 3401.1,
                "low": 3355.2,
                "close": 3373.8,
                "volume": 174758,
                "change": -24.8,
                "changePercent": -0.72971223,
                "vwap": 3376.7,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_full("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_with_dates(
        self, commodity_category, mock_client
    ):
        """Test historical price full with date parameters"""
        mock_response = [
            {"symbol": "GCUSD", "date": "2025-07-24", "open": 3398.6, "close": 3373.8}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_full(
            "GCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_basic(self, commodity_category, mock_client):
        """Test intraday 1min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:18:00",
                "open": 3374.5,
                "low": 3373.7,
                "high": 3374.5,
                "close": 3374,
                "volume": 123,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_1min("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_with_dates(self, commodity_category, mock_client):
        """Test intraday 1min with date parameters"""
        mock_response = [{"date": "2025-07-24 12:18:00", "open": 3374.5, "close": 3374}]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_1min(
            "GCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_basic(self, commodity_category, mock_client):
        """Test intraday 5min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:15:00",
                "open": 3374,
                "low": 3374,
                "high": 3374.8,
                "close": 3374.4,
                "volume": 193,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_5min("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_with_dates(self, commodity_category, mock_client):
        """Test intraday 5min with date parameters"""
        mock_response = [{"date": "2025-07-24 12:15:00", "open": 3374, "close": 3374.4}]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_5min(
            "GCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_basic(self, commodity_category, mock_client):
        """Test intraday 1hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 11:30:00",
                "open": 3378.4,
                "low": 3373.1,
                "high": 3378.8,
                "close": 3374.4,
                "volume": 7108,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_1hour("GCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_with_dates(self, commodity_category, mock_client):
        """Test intraday 1hour with date parameters"""
        mock_response = [
            {"date": "2025-07-24 11:30:00", "open": 3378.4, "close": 3374.4}
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_1hour(
            "GCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, commodity_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await commodity_category.commodities_list()

        assert result == []
        mock_client._make_request.assert_called_once_with("commodities-list", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, commodity_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple commodities
        large_response = [
            {
                "symbol": f"COMM{i}",
                "name": f"Commodity {i}",
                "exchange": f"EXCH{i % 3}",
                "tradeMonth": "Dec",
                "currency": "USD",
            }
            for i in range(1, 101)  # 100 commodities
        ]
        mock_client._make_request.return_value = large_response

        result = await commodity_category.commodities_list()

        assert len(result) == 100
        assert result[0]["symbol"] == "COMM1"
        assert result[99]["symbol"] == "COMM100"
        mock_client._make_request.assert_called_once_with("commodities-list", {})

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, commodity_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "GCUSD",
                "name": "Gold Futures",
                "price": 3375.3,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote("GCUSD")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "GCUSD"})

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, commodity_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await commodity_category.historical_price_light("GCUSD", "2025-04-25")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "GCUSD", "from": "2025-04-25"}
        )

        # Test with only to_date
        result = await commodity_category.historical_price_light(
            "GCUSD", to_date="2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "GCUSD", "to": "2025-07-25"}
        )

        # Test with both dates
        result = await commodity_category.historical_price_light(
            "GCUSD", "2025-04-25", "2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light",
            {"symbol": "GCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, commodity_category, mock_client):
        """Test commodity functionality with different symbols"""
        mock_response = [{"symbol": "SIUSD", "name": "Silver Futures", "price": 25.50}]
        mock_client._make_request.return_value = mock_response

        # Test with Silver
        result = await commodity_category.quote("SIUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "SIUSD"})

        # Test with Crude Oil
        result = await commodity_category.quote("CLUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "CLUSD"})

        # Test with Natural Gas
        result = await commodity_category.quote("NGUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "NGUSD"})

    @pytest.mark.asyncio
    async def test_commodities_list_response_validation(
        self, commodity_category, mock_client
    ):
        """Test commodities list response validation"""
        mock_response = [
            {
                "symbol": "HEUSX",
                "name": "Lean Hogs Futures",
                "exchange": None,
                "tradeMonth": "Dec",
                "currency": "USX",
            },
            {
                "symbol": "GCUSD",
                "name": "Gold Futures",
                "exchange": "COMEX",
                "tradeMonth": "Dec",
                "currency": "USD",
            },
            {
                "symbol": "CLUSD",
                "name": "Crude Oil Futures",
                "exchange": "NYMEX",
                "tradeMonth": "Jan",
                "currency": "USD",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.commodities_list()

        assert len(result) == 3
        assert result[0]["symbol"] == "HEUSX"
        assert result[0]["name"] == "Lean Hogs Futures"
        assert result[0]["exchange"] is None
        assert result[1]["symbol"] == "GCUSD"
        assert result[1]["exchange"] == "COMEX"
        assert result[2]["symbol"] == "CLUSD"
        assert result[2]["exchange"] == "NYMEX"
        mock_client._make_request.assert_called_once_with("commodities-list", {})

    @pytest.mark.asyncio
    async def test_quote_response_validation(self, commodity_category, mock_client):
        """Test quote response validation"""
        mock_response = [
            {
                "symbol": "GCUSD",
                "name": "Gold Futures",
                "price": 3375.3,
                "changePercentage": -0.65635,
                "change": -22.3,
                "volume": 170936,
                "dayLow": 3355.2,
                "dayHigh": 3401.1,
                "yearHigh": 3509.9,
                "yearLow": 2354.6,
                "marketCap": None,
                "priceAvg50": 3358.706,
                "priceAvg200": 3054.501,
                "exchange": "COMMODITY",
                "open": 3398.6,
                "previousClose": 3397.6,
                "timestamp": 1753372205,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.quote("GCUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "GCUSD"
        assert result[0]["name"] == "Gold Futures"
        assert result[0]["price"] == 3375.3
        assert result[0]["change"] == -22.3
        assert result[0]["volume"] == 170936
        assert result[0]["exchange"] == "COMMODITY"
        assert result[0]["timestamp"] == 1753372205
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "GCUSD"})

    @pytest.mark.asyncio
    async def test_historical_price_full_response_validation(
        self, commodity_category, mock_client
    ):
        """Test historical price full response validation"""
        mock_response = [
            {
                "symbol": "GCUSD",
                "date": "2025-07-24",
                "open": 3398.6,
                "high": 3401.1,
                "low": 3355.2,
                "close": 3373.8,
                "volume": 174758,
                "change": -24.8,
                "changePercent": -0.72971223,
                "vwap": 3376.7,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.historical_price_full("GCUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "GCUSD"
        assert result[0]["date"] == "2025-07-24"
        assert result[0]["open"] == 3398.6
        assert result[0]["high"] == 3401.1
        assert result[0]["low"] == 3355.2
        assert result[0]["close"] == 3373.8
        assert result[0]["volume"] == 174758
        assert result[0]["change"] == -24.8
        assert result[0]["changePercent"] == -0.72971223
        assert result[0]["vwap"] == 3376.7
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "GCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_response_validation(self, commodity_category, mock_client):
        """Test intraday response validation"""
        mock_response = [
            {
                "date": "2025-07-24 12:18:00",
                "open": 3374.5,
                "low": 3373.7,
                "high": 3374.5,
                "close": 3374,
                "volume": 123,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await commodity_category.intraday_1min("GCUSD")

        assert len(result) == 1
        assert result[0]["date"] == "2025-07-24 12:18:00"
        assert result[0]["open"] == 3374.5
        assert result[0]["low"] == 3373.7
        assert result[0]["high"] == 3374.5
        assert result[0]["close"] == 3374
        assert result[0]["volume"] == 123
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "GCUSD"}
        )
