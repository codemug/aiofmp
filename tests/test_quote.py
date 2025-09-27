"""
Unit tests for FMP Quote category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.quote import QuoteCategory


class TestQuoteCategory:
    """Test cases for QuoteCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def quote_category(self, mock_client):
        """Quote category instance with mocked client"""
        return QuoteCategory(mock_client)

    @pytest.mark.asyncio
    async def test_stock_quote_basic(self, quote_category, mock_client):
        """Test stock quote with required parameters"""
        mock_response = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 232.8,
            "changePercentage": 2.1008,
            "change": 4.79,
            "volume": 44489128,
            "dayLow": 226.65,
            "dayHigh": 233.13,
            "yearHigh": 260.1,
            "yearLow": 164.08,
            "marketCap": 3500823120000,
            "priceAvg50": 240.2278,
            "priceAvg200": 219.98755,
            "exchange": "NASDAQ",
            "open": 227.2,
            "previousClose": 228.01,
            "timestamp": 1738702801,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_quote("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_stock_quote_different_symbol(self, quote_category, mock_client):
        """Test stock quote with different symbol"""
        mock_response = {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "price": 450.25,
            "changePercentage": 1.5,
            "change": 6.75,
            "volume": 25000000,
            "dayLow": 445.0,
            "dayHigh": 452.0,
            "yearHigh": 500.0,
            "yearLow": 300.0,
            "marketCap": 3000000000000,
            "priceAvg50": 440.0,
            "priceAvg200": 420.0,
            "exchange": "NASDAQ",
            "open": 446.0,
            "previousClose": 443.5,
            "timestamp": 1738702801,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_quote("MSFT")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "MSFT"})

    @pytest.mark.asyncio
    async def test_aftermarket_trade_basic(self, quote_category, mock_client):
        """Test aftermarket trade with required parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "price": 232.53,
                "tradeSize": 132,
                "timestamp": 1738715334311,
            },
            {
                "symbol": "AAPL",
                "price": 232.60,
                "tradeSize": 500,
                "timestamp": 1738715335000,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_trade("AAPL")

        assert result == mock_response
        assert len(result) == 2
        mock_client._make_request.assert_called_once_with(
            "aftermarket-trade", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_aftermarket_trade_empty(self, quote_category, mock_client):
        """Test aftermarket trade with empty response"""
        mock_client._make_request.return_value = []

        result = await quote_category.aftermarket_trade("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "aftermarket-trade", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_aftermarket_trade_different_symbol(
        self, quote_category, mock_client
    ):
        """Test aftermarket trade with different symbol"""
        mock_response = [
            {
                "symbol": "GOOGL",
                "price": 150.25,
                "tradeSize": 100,
                "timestamp": 1738715334311,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_trade("GOOGL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "aftermarket-trade", {"symbol": "GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_aftermarket_quote_basic(self, quote_category, mock_client):
        """Test aftermarket quote with required parameters"""
        mock_response = {
            "symbol": "AAPL",
            "bidSize": 1,
            "bidPrice": 232.45,
            "askSize": 3,
            "askPrice": 232.64,
            "volume": 41647042,
            "timestamp": 1738715334311,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_quote("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "aftermarket-quote", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_aftermarket_quote_different_symbol(
        self, quote_category, mock_client
    ):
        """Test aftermarket quote with different symbol"""
        mock_response = {
            "symbol": "TSLA",
            "bidSize": 5,
            "bidPrice": 180.50,
            "askSize": 2,
            "askPrice": 180.75,
            "volume": 50000000,
            "timestamp": 1738715334311,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_quote("TSLA")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "aftermarket-quote", {"symbol": "TSLA"}
        )

    @pytest.mark.asyncio
    async def test_stock_price_change_basic(self, quote_category, mock_client):
        """Test stock price change with required parameters"""
        mock_response = {
            "symbol": "AAPL",
            "1D": 2.1008,
            "5D": -2.45946,
            "1M": -4.33925,
            "3M": 4.86014,
            "6M": 5.88556,
            "ytd": -4.53147,
            "1Y": 24.04092,
            "3Y": 35.04264,
            "5Y": 192.05871,
            "10Y": 678.8558,
            "max": 181279.04168,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_price_change("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "stock-price-change", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_stock_price_change_different_symbol(
        self, quote_category, mock_client
    ):
        """Test stock price change with different symbol"""
        mock_response = {
            "symbol": "NVDA",
            "1D": 5.25,
            "5D": 8.75,
            "1M": 15.50,
            "3M": 25.75,
            "6M": 45.25,
            "ytd": 35.50,
            "1Y": 120.75,
            "3Y": 250.25,
            "5Y": 800.50,
            "10Y": 1500.75,
            "max": 2000.25,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_price_change("NVDA")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "stock-price-change", {"symbol": "NVDA"}
        )

    @pytest.mark.asyncio
    async def test_stock_price_change_negative_values(
        self, quote_category, mock_client
    ):
        """Test stock price change with negative values"""
        mock_response = {
            "symbol": "META",
            "1D": -1.25,
            "5D": -3.75,
            "1M": -8.50,
            "3M": -12.25,
            "6M": -5.75,
            "ytd": -2.50,
            "1Y": 15.25,
            "3Y": 45.75,
            "5Y": 120.50,
            "10Y": 300.25,
            "max": 500.75,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_price_change("META")

        assert result == mock_response
        assert result["1D"] == -1.25
        assert result["5D"] == -3.75
        assert result["1M"] == -8.50
        mock_client._make_request.assert_called_once_with(
            "stock-price-change", {"symbol": "META"}
        )

    @pytest.mark.asyncio
    async def test_stock_price_change_zero_values(self, quote_category, mock_client):
        """Test stock price change with zero values"""
        mock_response = {
            "symbol": "BRK.A",
            "1D": 0.0,
            "5D": 0.0,
            "1M": 0.0,
            "3M": 0.0,
            "6M": 0.0,
            "ytd": 0.0,
            "1Y": 0.0,
            "3Y": 0.0,
            "5Y": 0.0,
            "10Y": 0.0,
            "max": 0.0,
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_price_change("BRK.A")

        assert result == mock_response
        assert result["1D"] == 0.0
        assert result["5D"] == 0.0
        assert result["1M"] == 0.0
        mock_client._make_request.assert_called_once_with(
            "stock-price-change", {"symbol": "BRK.A"}
        )

    @pytest.mark.asyncio
    async def test_stock_quote_response_structure(self, quote_category, mock_client):
        """Test stock quote response structure validation"""
        mock_response = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 232.8,
            "changePercentage": 2.1008,
            "change": 4.79,
            "volume": 44489128,
            "dayLow": 226.65,
            "dayHigh": 233.13,
            "yearHigh": 260.1,
            "yearLow": 164.08,
            "marketCap": 3500823120000,
            "priceAvg50": 240.2278,
            "priceAvg200": 219.98755,
            "exchange": "NASDAQ",
            "open": 227.2,
            "previousClose": 228.01,
            "timestamp": 1738702801,
            "extraField": "should be preserved",
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_quote("AAPL")

        assert result == mock_response
        assert result["symbol"] == "AAPL"
        assert result["name"] == "Apple Inc."
        assert result["price"] == 232.8
        assert result["changePercentage"] == 2.1008
        assert result["change"] == 4.79
        assert result["volume"] == 44489128
        assert result["dayLow"] == 226.65
        assert result["dayHigh"] == 233.13
        assert result["yearHigh"] == 260.1
        assert result["yearLow"] == 164.08
        assert result["marketCap"] == 3500823120000
        assert result["priceAvg50"] == 240.2278
        assert result["priceAvg200"] == 219.98755
        assert result["exchange"] == "NASDAQ"
        assert result["open"] == 227.2
        assert result["previousClose"] == 228.01
        assert result["timestamp"] == 1738702801
        assert result["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("quote", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_aftermarket_trade_response_structure(
        self, quote_category, mock_client
    ):
        """Test aftermarket trade response structure validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "price": 232.53,
                "tradeSize": 132,
                "timestamp": 1738715334311,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_trade("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["price"] == 232.53
        assert result[0]["tradeSize"] == 132
        assert result[0]["timestamp"] == 1738715334311
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "aftermarket-trade", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_aftermarket_quote_response_structure(
        self, quote_category, mock_client
    ):
        """Test aftermarket quote response structure validation"""
        mock_response = {
            "symbol": "AAPL",
            "bidSize": 1,
            "bidPrice": 232.45,
            "askSize": 3,
            "askPrice": 232.64,
            "volume": 41647042,
            "timestamp": 1738715334311,
            "extraField": "should be preserved",
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.aftermarket_quote("AAPL")

        assert result["symbol"] == "AAPL"
        assert result["bidSize"] == 1
        assert result["bidPrice"] == 232.45
        assert result["askSize"] == 3
        assert result["askPrice"] == 232.64
        assert result["volume"] == 41647042
        assert result["timestamp"] == 1738715334311
        assert result["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "aftermarket-quote", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_stock_price_change_response_structure(
        self, quote_category, mock_client
    ):
        """Test stock price change response structure validation"""
        mock_response = {
            "symbol": "AAPL",
            "1D": 2.1008,
            "5D": -2.45946,
            "1M": -4.33925,
            "3M": 4.86014,
            "6M": 5.88556,
            "ytd": -4.53147,
            "1Y": 24.04092,
            "3Y": 35.04264,
            "5Y": 192.05871,
            "10Y": 678.8558,
            "max": 181279.04168,
            "extraField": "should be preserved",
        }
        mock_client._make_request.return_value = mock_response

        result = await quote_category.stock_price_change("AAPL")

        assert result["symbol"] == "AAPL"
        assert result["1D"] == 2.1008
        assert result["5D"] == -2.45946
        assert result["1M"] == -4.33925
        assert result["3M"] == 4.86014
        assert result["6M"] == 5.88556
        assert result["ytd"] == -4.53147
        assert result["1Y"] == 24.04092
        assert result["3Y"] == 35.04264
        assert result["5Y"] == 192.05871
        assert result["10Y"] == 678.8558
        assert result["max"] == 181279.04168
        assert result["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "stock-price-change", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_multiple_symbols_consistency(self, quote_category, mock_client):
        """Test that all methods work consistently with different symbols"""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

        for symbol in symbols:
            # Test stock quote
            mock_quote = {"symbol": symbol, "price": 100.0}
            mock_client._make_request.return_value = mock_quote
            result = await quote_category.stock_quote(symbol)
            assert result["symbol"] == symbol
            mock_client._make_request.assert_called_with("quote", {"symbol": symbol})

            # Test aftermarket trade
            mock_trades = [{"symbol": symbol, "price": 100.0, "tradeSize": 100}]
            mock_client._make_request.return_value = mock_trades
            result = await quote_category.aftermarket_trade(symbol)
            assert result[0]["symbol"] == symbol
            mock_client._make_request.assert_called_with(
                "aftermarket-trade", {"symbol": symbol}
            )

            # Test aftermarket quote
            mock_quote_after = {"symbol": symbol, "bidPrice": 99.5, "askPrice": 100.5}
            mock_client._make_request.return_value = mock_quote_after
            result = await quote_category.aftermarket_quote(symbol)
            assert result["symbol"] == symbol
            mock_client._make_request.assert_called_with(
                "aftermarket-quote", {"symbol": symbol}
            )

            # Test stock price change
            mock_change = {"symbol": symbol, "1D": 1.0, "5D": 2.0}
            mock_client._make_request.return_value = mock_change
            result = await quote_category.stock_price_change(symbol)
            assert result["symbol"] == symbol
            mock_client._make_request.assert_called_with(
                "stock-price-change", {"symbol": symbol}
            )

    @pytest.mark.asyncio
    async def test_large_aftermarket_trade_response(self, quote_category, mock_client):
        """Test handling of large aftermarket trade responses"""
        # Create a large mock response with multiple trades
        large_response = [
            {
                "symbol": "AAPL",
                "price": 232.53 + (i * 0.01),
                "tradeSize": 100 + (i * 10),
                "timestamp": 1738715334311 + (i * 1000),
            }
            for i in range(100)  # 100 trades
        ]
        mock_client._make_request.return_value = large_response

        result = await quote_category.aftermarket_trade("AAPL")

        assert len(result) == 100
        assert result[0]["price"] == 232.53
        assert result[99]["price"] == 233.52
        assert result[0]["tradeSize"] == 100
        assert result[99]["tradeSize"] == 1090
        mock_client._make_request.assert_called_once_with(
            "aftermarket-trade", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_edge_case_symbols(self, quote_category, mock_client):
        """Test edge case symbols (special characters, numbers, etc.)"""
        edge_symbols = ["BRK.A", "BRK.B", "5", "A", "ZZZZZ", "SPY", "QQQ"]

        for symbol in edge_symbols:
            mock_response = {"symbol": symbol, "price": 100.0}
            mock_client._make_request.return_value = mock_response

            result = await quote_category.stock_quote(symbol)
            assert result["symbol"] == symbol
            mock_client._make_request.assert_called_with("quote", {"symbol": symbol})

    @pytest.mark.asyncio
    async def test_method_consistency(self, quote_category, mock_client):
        """Test that all methods follow the same parameter pattern"""
        methods = [
            ("stock_quote", "quote"),
            ("aftermarket_trade", "aftermarket-trade"),
            ("aftermarket_quote", "aftermarket-quote"),
            ("stock_price_change", "stock-price-change"),
        ]

        for method_name, endpoint in methods:
            method = getattr(quote_category, method_name)
            mock_response = {"symbol": "AAPL", "test": "data"}
            mock_client._make_request.return_value = mock_response

            result = await method("AAPL")
            assert result == mock_response
            mock_client._make_request.assert_called_with(endpoint, {"symbol": "AAPL"})
