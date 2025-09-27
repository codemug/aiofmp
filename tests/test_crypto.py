"""
Unit tests for FMP Crypto category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.crypto import CryptoCategory


class TestCryptoCategory:
    """Test cases for CryptoCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def crypto_category(self, mock_client):
        """Crypto category instance with mocked client"""
        return CryptoCategory(mock_client)

    @pytest.mark.asyncio
    async def test_cryptocurrency_list_basic(self, crypto_category, mock_client):
        """Test cryptocurrency list with no parameters"""
        mock_response = [
            {
                "symbol": "ALIENUSD",
                "name": "Alien Inu USD",
                "exchange": "CCC",
                "icoDate": "2021-11-22",
                "circulatingSupply": 0,
                "totalSupply": None,
            },
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin USD",
                "exchange": "CCC",
                "icoDate": "2009-01-03",
                "circulatingSupply": 19500000,
                "totalSupply": 21000000,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.cryptocurrency_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("cryptocurrency-list", {})

    @pytest.mark.asyncio
    async def test_cryptocurrency_list_response_structure(
        self, crypto_category, mock_client
    ):
        """Test cryptocurrency list response structure"""
        mock_response = [
            {
                "symbol": "ETHUSD",
                "name": "Ethereum USD",
                "exchange": "CCC",
                "icoDate": "2015-07-30",
                "circulatingSupply": 120000000,
                "totalSupply": None,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.cryptocurrency_list()

        assert len(result) == 1
        assert result[0]["symbol"] == "ETHUSD"
        assert result[0]["name"] == "Ethereum USD"
        assert result[0]["exchange"] == "CCC"
        assert result[0]["icoDate"] == "2015-07-30"
        assert result[0]["circulatingSupply"] == 120000000
        assert result[0]["totalSupply"] is None
        mock_client._make_request.assert_called_once_with("cryptocurrency-list", {})

    @pytest.mark.asyncio
    async def test_quote_basic(self, crypto_category, mock_client):
        """Test quote with required parameters only"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin USD",
                "price": 118741.16,
                "changePercentage": -0.03193323,
                "change": -37.93,
                "volume": 75302985728,
                "dayLow": 117435.22,
                "dayHigh": 119535.45,
                "yearHigh": 123091.61,
                "yearLow": 49121.24,
                "marketCap": 2344693699320,
                "priceAvg50": 109824.32,
                "priceAvg200": 98161.086,
                "exchange": "CRYPTO",
                "open": 118779.09,
                "previousClose": 118779.09,
                "timestamp": 1753374602,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "BTCUSD"})

    @pytest.mark.asyncio
    async def test_quote_response_structure(self, crypto_category, mock_client):
        """Test quote response structure"""
        mock_response = [
            {
                "symbol": "ETHUSD",
                "name": "Ethereum USD",
                "price": 3500.50,
                "changePercentage": 2.5,
                "change": 85.25,
                "volume": 25000000000,
                "dayLow": 3400.00,
                "dayHigh": 3550.00,
                "yearHigh": 4000.00,
                "yearLow": 2000.00,
                "marketCap": 420000000000,
                "priceAvg50": 3300.00,
                "priceAvg200": 3000.00,
                "exchange": "CRYPTO",
                "open": 3415.25,
                "previousClose": 3415.25,
                "timestamp": 1753374602,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote("ETHUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "ETHUSD"
        assert result[0]["name"] == "Ethereum USD"
        assert result[0]["price"] == 3500.50
        assert result[0]["change"] == 85.25
        assert result[0]["volume"] == 25000000000
        assert result[0]["exchange"] == "CRYPTO"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "ETHUSD"})

    @pytest.mark.asyncio
    async def test_quote_short_basic(self, crypto_category, mock_client):
        """Test quote short with required parameters only"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "price": 118741.16,
                "change": -37.93,
                "volume": 75302985728,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote_short("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_quote_short_response_structure(self, crypto_category, mock_client):
        """Test quote short response structure"""
        mock_response = [
            {"symbol": "ADAUSD", "price": 0.45, "change": 0.02, "volume": 1000000000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote_short("ADAUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "ADAUSD"
        assert result[0]["price"] == 0.45
        assert result[0]["change"] == 0.02
        assert result[0]["volume"] == 1000000000
        mock_client._make_request.assert_called_once_with(
            "quote-short", {"symbol": "ADAUSD"}
        )

    @pytest.mark.asyncio
    async def test_batch_quotes_default(self, crypto_category, mock_client):
        """Test batch quotes with default short parameter"""
        mock_response = [
            {
                "symbol": "00USD",
                "price": 0.01755108,
                "change": 0.00035108,
                "volume": 3719492.41,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.batch_quotes()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "batch-crypto-quotes", {"short": True}
        )

    @pytest.mark.asyncio
    async def test_batch_quotes_with_short_false(self, crypto_category, mock_client):
        """Test batch quotes with short=False"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "price": 118741.16,
                "change": -37.93,
                "volume": 75302985728,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.batch_quotes(short=False)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "batch-crypto-quotes", {"short": False}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_basic(self, crypto_category, mock_client):
        """Test historical price light with required parameters only"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "date": "2025-07-24",
                "price": 118741.16,
                "volume": 75302985728,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_light("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_dates(
        self, crypto_category, mock_client
    ):
        """Test historical price light with date parameters"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "date": "2025-07-24",
                "price": 118741.16,
                "volume": 75302985728,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_light(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_from_date_only(
        self, crypto_category, mock_client
    ):
        """Test historical price light with only from_date parameter"""
        mock_response = [{"symbol": "BTCUSD", "date": "2025-07-24", "price": 118741.16}]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_light(
            "BTCUSD", from_date="2025-04-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "BTCUSD", "from": "2025-04-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_light_with_to_date_only(
        self, crypto_category, mock_client
    ):
        """Test historical price light with only to_date parameter"""
        mock_response = [{"symbol": "BTCUSD", "date": "2025-07-24", "price": 118741.16}]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_light(
            "BTCUSD", to_date="2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/light", {"symbol": "BTCUSD", "to": "2025-07-25"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_basic(self, crypto_category, mock_client):
        """Test historical price full with required parameters only"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "date": "2025-07-24",
                "open": 118779.09,
                "high": 119535.45,
                "low": 117435.22,
                "close": 118741.16,
                "volume": 75302985728,
                "change": -37.93,
                "changePercent": -0.03193323,
                "vwap": 118570.61,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_full("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_historical_price_full_with_dates(self, crypto_category, mock_client):
        """Test historical price full with date parameters"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "date": "2025-07-24",
                "open": 118779.09,
                "close": 118741.16,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_full(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_basic(self, crypto_category, mock_client):
        """Test intraday 1min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 118797.96,
                "low": 118760.42,
                "high": 118818.11,
                "close": 118784.04,
                "volume": 52293740.08888889,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_1min("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1min_with_dates(self, crypto_category, mock_client):
        """Test intraday 1min with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:29:00", "open": 118797.96, "close": 118784.04}
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_1min(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_basic(self, crypto_category, mock_client):
        """Test intraday 5min with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:25:00",
                "open": 118988.32,
                "low": 118797.03,
                "high": 118997.22,
                "close": 118797.03,
                "volume": 208601161.95555556,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_5min("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_5min_with_dates(self, crypto_category, mock_client):
        """Test intraday 5min with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:25:00", "open": 118988.32, "close": 118797.03}
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_5min(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/5min",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_basic(self, crypto_category, mock_client):
        """Test intraday 1hour with required parameters only"""
        mock_response = [
            {
                "date": "2025-07-24 12:00:00",
                "open": 119189.36,
                "low": 118768.68,
                "high": 119272.88,
                "close": 118797.03,
                "volume": 1493617925.6888888,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_1hour("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_1hour_with_dates(self, crypto_category, mock_client):
        """Test intraday 1hour with date parameters"""
        mock_response = [
            {"date": "2025-07-24 12:00:00", "open": 119189.36, "close": 118797.03}
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_1hour(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1hour",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, crypto_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await crypto_category.cryptocurrency_list()

        assert result == []
        mock_client._make_request.assert_called_once_with("cryptocurrency-list", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, crypto_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple cryptocurrencies
        large_response = [
            {
                "symbol": f"CRYPTO{i}",
                "name": f"Cryptocurrency {i}",
                "exchange": "CCC",
                "icoDate": "2020-01-01",
                "circulatingSupply": 1000000 + i * 100000,
                "totalSupply": 2000000 + i * 200000,
            }
            for i in range(1, 101)  # 100 cryptocurrencies
        ]
        mock_client._make_request.return_value = large_response

        result = await crypto_category.cryptocurrency_list()

        assert len(result) == 100
        assert result[0]["symbol"] == "CRYPTO1"
        assert result[99]["symbol"] == "CRYPTO100"
        mock_client._make_request.assert_called_once_with("cryptocurrency-list", {})

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, crypto_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin USD",
                "price": 118741.16,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote("BTCUSD")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "BTCUSD"})

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, crypto_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "BTCUSD", "date": "2025-07-24", "price": 118741.16}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await crypto_category.historical_price_light("BTCUSD", "2025-04-25")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "BTCUSD", "from": "2025-04-25"}
        )

        # Test with only to_date
        result = await crypto_category.historical_price_light(
            "BTCUSD", to_date="2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light", {"symbol": "BTCUSD", "to": "2025-07-25"}
        )

        # Test with both dates
        result = await crypto_category.historical_price_light(
            "BTCUSD", "2025-04-25", "2025-07-25"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-price-eod/light",
            {"symbol": "BTCUSD", "from": "2025-04-25", "to": "2025-07-25"},
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, crypto_category, mock_client):
        """Test crypto functionality with different symbols"""
        mock_response = [{"symbol": "ETHUSD", "name": "Ethereum USD", "price": 3500.50}]
        mock_client._make_request.return_value = mock_response

        # Test with Ethereum
        result = await crypto_category.quote("ETHUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "ETHUSD"})

        # Test with Cardano
        result = await crypto_category.quote("ADAUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "ADAUSD"})

        # Test with Solana
        result = await crypto_category.quote("SOLUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with("quote", {"symbol": "SOLUSD"})

    @pytest.mark.asyncio
    async def test_cryptocurrency_list_response_validation(
        self, crypto_category, mock_client
    ):
        """Test cryptocurrency list response validation"""
        mock_response = [
            {
                "symbol": "ALIENUSD",
                "name": "Alien Inu USD",
                "exchange": "CCC",
                "icoDate": "2021-11-22",
                "circulatingSupply": 0,
                "totalSupply": None,
            },
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin USD",
                "exchange": "CCC",
                "icoDate": "2009-01-03",
                "circulatingSupply": 19500000,
                "totalSupply": 21000000,
            },
            {
                "symbol": "ETHUSD",
                "name": "Ethereum USD",
                "exchange": "CCC",
                "icoDate": "2015-07-30",
                "circulatingSupply": 120000000,
                "totalSupply": None,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.cryptocurrency_list()

        assert len(result) == 3
        assert result[0]["symbol"] == "ALIENUSD"
        assert result[0]["name"] == "Alien Inu USD"
        assert result[0]["circulatingSupply"] == 0
        assert result[1]["symbol"] == "BTCUSD"
        assert result[1]["totalSupply"] == 21000000
        assert result[2]["symbol"] == "ETHUSD"
        assert result[2]["icoDate"] == "2015-07-30"
        mock_client._make_request.assert_called_once_with("cryptocurrency-list", {})

    @pytest.mark.asyncio
    async def test_quote_response_validation(self, crypto_category, mock_client):
        """Test quote response validation"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin USD",
                "price": 118741.16,
                "changePercentage": -0.03193323,
                "change": -37.93,
                "volume": 75302985728,
                "dayLow": 117435.22,
                "dayHigh": 119535.45,
                "yearHigh": 123091.61,
                "yearLow": 49121.24,
                "marketCap": 2344693699320,
                "priceAvg50": 109824.32,
                "priceAvg200": 98161.086,
                "exchange": "CRYPTO",
                "open": 118779.09,
                "previousClose": 118779.09,
                "timestamp": 1753374602,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.quote("BTCUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "BTCUSD"
        assert result[0]["name"] == "Bitcoin USD"
        assert result[0]["price"] == 118741.16
        assert result[0]["change"] == -37.93
        assert result[0]["volume"] == 75302985728
        assert result[0]["exchange"] == "CRYPTO"
        assert result[0]["timestamp"] == 1753374602
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "BTCUSD"})

    @pytest.mark.asyncio
    async def test_historical_price_full_response_validation(
        self, crypto_category, mock_client
    ):
        """Test historical price full response validation"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "date": "2025-07-24",
                "open": 118779.09,
                "high": 119535.45,
                "low": 117435.22,
                "close": 118741.16,
                "volume": 75302985728,
                "change": -37.93,
                "changePercent": -0.03193323,
                "vwap": 118570.61,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.historical_price_full("BTCUSD")

        assert len(result) == 1
        assert result[0]["symbol"] == "BTCUSD"
        assert result[0]["date"] == "2025-07-24"
        assert result[0]["open"] == 118779.09
        assert result[0]["high"] == 119535.45
        assert result[0]["low"] == 117435.22
        assert result[0]["close"] == 118741.16
        assert result[0]["volume"] == 75302985728
        assert result[0]["change"] == -37.93
        assert result[0]["changePercent"] == -0.03193323
        assert result[0]["vwap"] == 118570.61
        mock_client._make_request.assert_called_once_with(
            "historical-price-eod/full", {"symbol": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_intraday_response_validation(self, crypto_category, mock_client):
        """Test intraday response validation"""
        mock_response = [
            {
                "date": "2025-07-24 12:29:00",
                "open": 118797.96,
                "low": 118760.42,
                "high": 118818.11,
                "close": 118784.04,
                "volume": 52293740.08888889,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await crypto_category.intraday_1min("BTCUSD")

        assert len(result) == 1
        assert result[0]["date"] == "2025-07-24 12:29:00"
        assert result[0]["open"] == 118797.96
        assert result[0]["low"] == 118760.42
        assert result[0]["high"] == 118818.11
        assert result[0]["close"] == 118784.04
        assert result[0]["volume"] == 52293740.08888889
        mock_client._make_request.assert_called_once_with(
            "historical-chart/1min", {"symbol": "BTCUSD"}
        )
