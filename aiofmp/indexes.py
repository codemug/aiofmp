"""
Indexes category for FMP API

This module provides stock market index functionality including index lists, quotes,
historical data, and intraday charts for various time intervals.
"""

from datetime import date
from typing import Any

from .base import FMPBaseClient


class IndexesCategory:
    """Indexes category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the indexes category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def index_list(self) -> list[dict[str, Any]]:
        """
        Get a comprehensive list of stock market indexes across global exchanges

        Endpoint: /index-list

        Returns:
            List of stock market indexes with symbol, name, exchange, and currency

        Example:
            >>> data = await client.indexes.index_list()
            >>> # Returns: [{"symbol": "^TTIN", "name": "S&P/TSX Capped Industrials Index", ...}]
        """
        return await self._client._make_request("index-list")

    async def index_quote(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get real-time stock index quotes with comprehensive market data

        Endpoint: /quote

        Args:
            symbol: Index symbol (required)

        Returns:
            List of index quote data with price, change, volume, and technical indicators

        Example:
            >>> data = await client.indexes.index_quote("^GSPC")
            >>> # Returns: [{"symbol": "^GSPC", "name": "S&P 500", "price": 6366.13, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote", params)

    async def index_quote_short(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get concise stock index quotes with essential price and volume data

        Endpoint: /quote-short

        Args:
            symbol: Index symbol (required)

        Returns:
            List of short index quote data with price, change, and volume

        Example:
            >>> data = await client.indexes.index_quote_short("^GSPC")
            >>> # Returns: [{"symbol": "^GSPC", "price": 6366.13, "change": 7.22, "volume": 1498664000}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote-short", params)

    async def all_index_quotes(self, short: bool | None = None) -> list[dict[str, Any]]:
        """
        Get real-time quotes for a wide range of stock indexes

        Endpoint: /batch-index-quotes

        Args:
            short: Whether to return short quotes (optional)

        Returns:
            List of index quotes across multiple indexes

        Example:
            >>> data = await client.indexes.all_index_quotes(short=True)
            >>> # Returns: [{"symbol": "^DJBGIE", "price": 4155.76, "change": 1.09, "volume": 0}]
        """
        params = {}
        if short is not None:
            params["short"] = short

        return await self._client._make_request("batch-index-quotes", params)

    async def historical_price_eod_light(
        self, symbol: str, from_date: date | None = None, to_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Get end-of-day historical prices for stock indexes (light version)

        Endpoint: /historical-price-eod/light

        Args:
            symbol: Index symbol (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)

        Returns:
            List of historical price data with date, price, and volume

        Example:
            >>> data = await client.indexes.historical_price_eod_light("^GSPC", from_date=date(2025, 4, 25))
            >>> # Returns: [{"symbol": "^GSPC", "date": "2025-07-24", "price": 6365.77, "volume": 1499302000}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("historical-price-eod/light", params)

    async def historical_price_eod_full(
        self, symbol: str, from_date: date | None = None, to_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Get full end-of-day historical prices for stock indexes with comprehensive data

        Endpoint: /historical-price-eod/full

        Args:
            symbol: Index symbol (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)

        Returns:
            List of detailed historical price data with OHLC, volume, and additional metrics

        Example:
            >>> data = await client.indexes.historical_price_eod_full("^GSPC", from_date=date(2025, 4, 25))
            >>> # Returns: [{"symbol": "^GSPC", "date": "2025-07-24", "open": 6368.6, "high": 6379.54, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("historical-price-eod/full", params)

    async def intraday_1min(
        self, symbol: str, from_date: date | None = None, to_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 1-minute interval intraday data for stock indexes

        Endpoint: /historical-chart/1min

        Args:
            symbol: Index symbol (required)
            from_date: Start date for intraday data (optional)
            to_date: End date for intraday data (optional)

        Returns:
            List of 1-minute intraday data with OHLC and volume

        Example:
            >>> data = await client.indexes.intraday_1min("^GSPC", from_date=date(2025, 4, 25))
            >>> # Returns: [{"date": "2025-07-24 12:29:00", "open": 6365.34, "low": 6365.34, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("historical-chart/1min", params)

    async def intraday_5min(
        self, symbol: str, from_date: date | None = None, to_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 5-minute interval intraday data for stock indexes

        Endpoint: /historical-chart/5min

        Args:
            symbol: Index symbol (required)
            from_date: Start date for intraday data (optional)
            to_date: End date for intraday data (optional)

        Returns:
            List of 5-minute intraday data with OHLC and volume

        Example:
            >>> data = await client.indexes.intraday_5min("^GSPC", from_date=date(2025, 4, 25))
            >>> # Returns: [{"date": "2025-07-24 12:30:00", "open": 6366.18, "low": 6365.57, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("historical-chart/5min", params)

    async def intraday_1hour(
        self, symbol: str, from_date: date | None = None, to_date: date | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 1-hour interval intraday data for stock indexes

        Endpoint: /historical-chart/1hour

        Args:
            symbol: Index symbol (required)
            from_date: Start date for intraday data (optional)
            to_date: End date for intraday data (optional)

        Returns:
            List of 1-hour intraday data with OHLC and volume

        Example:
            >>> data = await client.indexes.intraday_1hour("^GSPC", from_date=date(2025, 4, 25))
            >>> # Returns: [{"date": "2025-07-24 12:30:00", "open": 6366.18, "low": 6365.57, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("historical-chart/1hour", params)
