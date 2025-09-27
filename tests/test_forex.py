"""
Unit tests for FMP Forex category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.forex import ForexCategory


class TestForexCategory:
    """Test cases for ForexCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def forex_category(self, mock_client):
        """Forex category instance with mocked client"""
        return ForexCategory(mock_client)

    @pytest.mark.asyncio
    async def test_forex_list_basic(self, forex_category, mock_client):
        """Test forex list with no parameters"""
        mock_response = [
            {
                "symbol": "ARSMXN",
                "fromCurrency": "ARS",
                "toCurrency": "MXN",
                "fromName": "Argentine Peso",
                "toName": "Mexican Peso",
            },
            {
                "symbol": "EURUSD",
                "fromCurrency": "EUR",
                "toCurrency": "USD",
                "fromName": "Euro",
                "toName": "US Dollar",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.forex_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("forex-list", {})

    @pytest.mark.asyncio
    async def test_forex_list_response_structure(self, forex_category, mock_client):
        """Test forex list response structure"""
        mock_response = [
            {
                "symbol": "GBPUSD",
                "fromCurrency": "GBP",
                "toCurrency": "USD",
                "fromName": "British Pound",
                "toName": "US Dollar",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.forex_list()

        assert len(result) == 1
        assert result[0]["symbol"] == "GBPUSD"
        assert result[0]["fromCurrency"] == "GBP"
        assert result[0]["toCurrency"] == "USD"
        assert result[0]["fromName"] == "British Pound"
        assert result[0]["toName"] == "US Dollar"
        mock_client._make_request.assert_called_once_with("forex-list", {})

    @pytest.mark.asyncio
    async def test_quote_basic(self, forex_category, mock_client):
        """Test quote with required parameters only"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "name": "EUR/USD",
                "price": 1.17598,
                "changePercentage": -0.14754,
                "change": -0.0017376,
                "volume": 184065,
                "dayLow": 1.17371,
                "dayHigh": 1.17911,
                "yearHigh": 1.18303,
                "yearLow": 1.01838,
                "marketCap": None,
                "priceAvg50": 1.15244,
                "priceAvg200": 1.08866,
                "exchange": "FOREX",
                "open": 1.17744,
                "previousClose": 1.17772,
                "timestamp": 1753374603,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "EURUSD"})

    @pytest.mark.asyncio
    async def test_quote_response_structure(self, forex_category, mock_client):
        """Test quote response structure"""
        mock_response = [
            {
                "symbol": "GBPUSD",
                "name": "GBP/USD",
                "price": 1.2850,
                "changePercentage": 0.25,
                "change": 0.0032,
                "volume": 150000,
                "dayLow": 1.2800,
                "dayHigh": 1.2900,
                "yearHigh": 1.3000,
                "yearLow": 1.2000,
                "marketCap": None,
                "priceAvg50": 1.2750,
                "priceAvg200": 1.2500,
                "exchange": "FOREX",
                "open": 1.2818,
                "previousClose": 1.2818,
                "timestamp": 1753374603,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote("GBPUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "GBPUSD"
        assert result[0]["name"] == "GBP/USD"
        assert result[0]["price"] == 1.2850
        assert result[0]["change"] == 0.0032
        assert result[0]["volume"] == 150000
        assert result[0]["exchange"] == "FOREX"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "GBPUSD"})

    @pytest.mark.asyncio
    async def test_quote_short_basic(self, forex_category, mock_client):
        """Test quote short with required parameters only"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "price": 1.17598,
                "change": -0.0017376,
                "volume": 184065,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote_short("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_quote_short_response_structure(self, forex_category, mock_client):
        """Test quote short response structure"""
        mock_response = [
            {"symbol": "USDJPY", "price": 110.50, "change": 0.25, "volume": 200000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote_short("USDJPY")

        assert len(result) == 1
        assert result[0]["symbol"] == "USDJPY"
        assert result[0]["price"] == 110.50
        assert result[0]["change"] == 0.25
        assert result[0]["volume"] == 200000
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "USDJPY"}
        )

    @pytest.mark.asyncio
    async def test_batch_quotes_default(self, forex_category, mock_client):
        """Test batch quotes with default short parameter"""
        mock_response = [
            {"symbol": "AEDAUD", "price": 0.41372, "change": 0.00153892, "volume": 0}
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.batch_quotes()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "batch-forex-quotes", {"short": True}
        )

    @pytest.mark.asyncio
    async def test_batch_quotes_with_short_false(self, forex_category, mock_client):
        """Test batch quotes with short=False"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "price": 1.17598,
                "change": -0.0017376,
                "volume": 184065,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.batch_quotes(short=False)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "batch-forex-quotes", {"short": False}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_basic(self, forex_category, mock_client):
        """Test historical price light with required parameters only"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "date": "2025-07-24",
                "price": 1.17639,
                "volume": 182290,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_light("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_dates(self, forex_category, mock_client):
        """Test historical price light with date parameters"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "date": "2025-07-24",
                "price": 1.17639,
                "volume": 182290,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_light(
            "EURUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_from_date_only(
        self, forex_category, mock_client
    ):
        """Test historical price light with only from_date parameter"""
        mock_response = [{"symbol": "EURUSD", "date": "2025-07-24", "price": 1.17639}]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_light(
            "EURUSD", from_date="2025-04-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "EURUSD", "from": "2025-04-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_to_date_only(
        self, forex_category, mock_client
    ):
        """Test historical price light with only to_date parameter"""
        mock_response = [{"symbol": "EURUSD", "date": "2025-07-24", "price": 1.17639}]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_light(
            "EURUSD", to_date="2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "EURUSD", "to": "2025-07-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_basic(self, forex_category, mock_client):
        """Test historical price full with required parameters only"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "date": "2025-07-24",
                "open": 1.17744,
                "high": 1.17911,
                "low": 1.17371,
                "close": 1.17639,
                "volume": 182290,
                "change": -0.00105,
                "changePercent": -0.08917652,
                "vwap": 1.18,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_full("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_with_dates(self, forex_category, mock_client):
        """Test historical price full with date parameters"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "date": "2025-07-24",
                "open": 1.17744,
                "close": 1.17639,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_full(
            "EURUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_basic(self, forex_category, mock_client):
        """Test intraday 1min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 1.17582,
                "low": 1.17582,
                "high": 1.17599,
                "close": 1.17598,
                "volume": 184,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_1min("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_with_dates(self, forex_category, mock_client):
        """Test intraday 1min with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:29:00", "open": 1.17582, "close": 1.17598}
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_1min(
            "EURUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_basic(self, forex_category, mock_client):
        """Test intraday 5min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:25:00",
                "open": 1.17612,
                "low": 1.17571,
                "high": 1.17613,
                "close": 1.17578,
                "volume": 873,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_5min("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_with_dates(self, forex_category, mock_client):
        """Test intraday 5min with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:25:00", "open": 1.17612, "close": 1.17578}
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_5min(
            "EURUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_basic(self, forex_category, mock_client):
        """Test intraday 1hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:00:00",
                "open": 1.17639,
                "low": 1.17571,
                "high": 1.1773,
                "close": 1.17578,
                "volume": 4909,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_1hour("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_with_dates(self, forex_category, mock_client):
        """Test intraday 1hour with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:00:00", "open": 1.17639, "close": 1.17578}
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_1hour(
            "EURUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, forex_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await forex_category.forex_list()

        assert result == []
        mock_client._make_request.assert_called_once_with("forex-list", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, forex_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple forex pairs
        large_response = [
            {
                "symbol": f"FOREX{i}",
                "fromCurrency": f"CUR{i % 3}",
                "toCurrency": f"CUR{(i + 1) % 3}",
                "fromName": f"Currency {i % 3}",
                "toName": f"Currency {(i + 1) % 3}",
            }
            for i in range(1, 101)  # 100 forex pairs
        ]
        mock_client._make_request.return_value = large_response

        result = await forex_category.forex_list()

        assert len(result) == 100
        assert result[0]["symbol"] == "FOREX1"
        assert result[99]["symbol"] == "FOREX100"
        mock_client._make_request.assert_called_once_with("forex-list", {})

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, forex_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "name": "EUR/USD",
                "price": 1.17598,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote("EURUSD")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "EURUSD"})

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, forex_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "EURUSD", "date": "2025-07-24", "price": 1.17639}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await forex_category.historical_price_light("EURUSD", "2025-04-25")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "EURUSD", "from": "2025-04-25"}
        )

        # Test with only to_date
        result = await forex_category.historical_price_light(
            "EURUSD", to_date="2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "EURUSD", "to": "2025-07-25"}
        )

        # Test with both dates
        result = await forex_category.historical_price_light(
            "EURUSD", "2025-04-25", "2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light",
            {"symbol": "EURUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, forex_category, mock_client):
        """Test forex functionality with different symbols"""
        mock_response = [{"symbol": "GBPUSD", "name": "GBP/USD", "price": 1.2850}]
        mock_client._make_request.return_value = mock_response

        # Test with GBP/USD
        result = await forex_category.quote("GBPUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "GBPUSD"})

        # Test with USD/JPY
        result = await forex_category.quote("USDJPY")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "USDJPY"})

        # Test with AUD/USD
        result = await forex_category.quote("AUDUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "AUDUSD"})

    @pytest.mark.asyncio
    async def test_forex_list_response_validation(self, forex_category, mock_client):
        """Test forex list response validation"""
        mock_response = [
            {
                "symbol": "ARSMXN",
                "fromCurrency": "ARS",
                "toCurrency": "MXN",
                "fromName": "Argentine Peso",
                "toName": "Mexican Peso",
            },
            {
                "symbol": "EURUSD",
                "fromCurrency": "EUR",
                "toCurrency": "USD",
                "fromName": "Euro",
                "toName": "US Dollar",
            },
            {
                "symbol": "GBPUSD",
                "fromCurrency": "GBP",
                "toCurrency": "USD",
                "fromName": "British Pound",
                "toName": "US Dollar",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.forex_list()

        assert len(result) == 3
        assert result[0]["symbol"] == "ARSMXN"
        assert result[0]["fromCurrency"] == "ARS"
        assert result[0]["toCurrency"] == "MXN"
        assert result[1]["symbol"] == "EURUSD"
        assert result[1]["fromName"] == "Euro"
        assert result[2]["symbol"] == "GBPUSD"
        assert result[2]["toName"] == "US Dollar"
        mock_client._make_request.assert_called_once_with("forex-list", {})

    @pytest.mark.asyncio
    async def test_quote_response_validation(self, forex_category, mock_client):
        """Test quote response validation"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "name": "EUR/USD",
                "price": 1.17598,
                "changePercentage": -0.14754,
                "change": -0.0017376,
                "volume": 184065,
                "dayLow": 1.17371,
                "dayHigh": 1.17911,
                "yearHigh": 1.18303,
                "yearLow": 1.01838,
                "marketCap": None,
                "priceAvg50": 1.15244,
                "priceAvg200": 1.08866,
                "exchange": "FOREX",
                "open": 1.17744,
                "previousClose": 1.17772,
                "timestamp": 1753374603,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.quote("EURUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "EURUSD"
        assert result[0]["name"] == "EUR/USD"
        assert result[0]["price"] == 1.17598
        assert result[0]["change"] == -0.0017376
        assert result[0]["volume"] == 184065
        assert result[0]["exchange"] == "FOREX"
        assert result[0]["timestamp"] == 1753374603
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "EURUSD"})

    @pytest.mark.asyncio
    async def test_historical_price_full_response_validation(
        self, forex_category, mock_client
    ):
        """Test historical price full response validation"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "date": "2025-07-24",
                "open": 1.17744,
                "high": 1.17911,
                "low": 1.17371,
                "close": 1.17639,
                "volume": 182290,
                "change": -0.00105,
                "changePercent": -0.08917652,
                "vwap": 1.18,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.historical_price_full("EURUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "EURUSD"
        assert result[0]["date"] == "2025-07-24"
        assert result[0]["open"] == 1.17744
        assert result[0]["high"] == 1.17911
        assert result[0]["low"] == 1.17371
        assert result[0]["close"] == 1.17639
        assert result[0]["volume"] == 182290
        assert result[0]["change"] == -0.00105
        assert result[0]["changePercent"] == -0.08917652
        assert result[0]["vwap"] == 1.18
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_response_validation(self, forex_category, mock_client):
        """Test intraday response validation"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 1.17582,
                "low": 1.17582,
                "high": 1.17599,
                "close": 1.17598,
                "volume": 184,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await forex_category.intraday_1min("EURUSD")

        assert len(result) == 1
        assert result[0]["date"] == "2025-07-24 12:29:00"
        assert result[0]["open"] == 1.17582
        assert result[0]["low"] == 1.17582
        assert result[0]["high"] == 1.17599
        assert result[0]["close"] == 1.17598
        assert result[0]["volume"] == 184
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "EURUSD"}
        )
