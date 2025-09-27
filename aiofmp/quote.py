"""
Quote category for FMP API

This module provides quote functionality including real-time stock quotes, aftermarket trades,
aftermarket quotes, and stock price changes across various time periods.
"""

from typing import Any

from .base import FMPBaseClient


class QuoteCategory:
    """Quote category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the quote category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def stock_quote(self, symbol: str) -> dict[str, Any]:
        """
        Get real-time stock quote for a specific symbol

        Endpoint: /quote

        Args:
            symbol: Stock symbol (required)

        Returns:
            Stock quote data with price, change, volume, highs/lows, market cap, and averages

        Example:
            >>> data = await client.quote.stock_quote("AAPL")
            >>> # Returns: {"symbol": "AAPL", "name": "Apple Inc.", "price": 232.8, "changePercentage": 2.1008, ...}
        """
        return await self._client._make_request("quote", {"symbol": symbol})

    async def aftermarket_trade(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get aftermarket trade data for a specific symbol

        Endpoint: /aftermarket-trade

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of aftermarket trades with price, trade size, and timestamp

        Example:
            >>> data = await client.quote.aftermarket_trade("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "price": 232.53, "tradeSize": 132, "timestamp": 1738715334311}]
        """
        return await self._client._make_request("aftermarket-trade", {"symbol": symbol})

    async def aftermarket_quote(self, symbol: str) -> dict[str, Any]:
        """
        Get aftermarket quote data for a specific symbol

        Endpoint: /aftermarket-quote

        Args:
            symbol: Stock symbol (required)

        Returns:
            Aftermarket quote data with bid/ask prices, sizes, volume, and timestamp

        Example:
            >>> data = await client.quote.aftermarket_quote("AAPL")
            >>> # Returns: {"symbol": "AAPL", "bidSize": 1, "bidPrice": 232.45, "askSize": 3, "askPrice": 232.64, ...}
        """
        return await self._client._make_request("aftermarket-quote", {"symbol": symbol})

    async def stock_price_change(self, symbol: str) -> dict[str, Any]:
        """
        Get stock price change data across various time periods

        Endpoint: /stock-price-change

        Args:
            symbol: Stock symbol (required)

        Returns:
            Price change data across multiple time periods (1D, 5D, 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, 10Y, max)

        Example:
            >>> data = await client.quote.stock_price_change("AAPL")
            >>> # Returns: {"symbol": "AAPL", "1D": 2.1008, "5D": -2.45946, "1M": -4.33925, ...}
        """
        return await self._client._make_request(
            "stock-price-change", {"symbol": symbol}
        )
