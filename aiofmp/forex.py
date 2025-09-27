"""
Forex category for FMP API

This module provides forex functionality including currency pairs list, real-time quotes,
historical price data, and intraday charts for various currency pairs.
"""

from typing import Any

from .base import FMPBaseClient


class ForexCategory:
    """Forex category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the forex category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def forex_list(self) -> list[dict[str, Any]]:
        """
        Get comprehensive list of all currency pairs traded on the forex market

        Endpoint: /forex-list

        Returns:
            List of forex currency pairs with symbol, from/to currencies, and currency names

        Example:
            >>> data = await client.forex.forex_list()
            >>> # Returns: [{"symbol": "ARSMXN", "fromCurrency": "ARS", "toCurrency": "MXN", ...}]
        """
        return await self._client._make_request("forex-list", {})

    async def quote(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get real-time forex quotes for currency pairs

        Endpoint: /quote

        Args:
            symbol: Forex currency pair symbol (required)

        Returns:
            List of forex quote data with price, changes, volume, and technical indicators

        Example:
            >>> data = await client.forex.quote("EURUSD")
            >>> # Returns: [{"symbol": "EURUSD", "name": "EUR/USD", "price": 1.17598, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote", params)

    async def quote_short(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get quick and concise forex pair quotes

        Endpoint: /quote-short

        Args:
            symbol: Forex currency pair symbol (required)

        Returns:
            List of short forex quote data with price, change, and volume

        Example:
            >>> data = await client.forex.quote_short("EURUSD")
            >>> # Returns: [{"symbol": "EURUSD", "price": 1.17598, "change": -0.0017376, "volume": 184065}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote-short", params)

    async def batch_quotes(self, short: bool = True) -> list[dict[str, Any]]:
        """
        Get real-time quotes for multiple forex pairs simultaneously

        Endpoint: /batch-forex-quotes

        Args:
            short: Whether to return short format quotes (default: True)

        Returns:
            List of forex batch quotes with price, change, and volume

        Example:
            >>> data = await client.forex.batch_quotes(short=True)
            >>> # Returns: [{"symbol": "AEDAUD", "price": 0.41372, "change": 0.00153892, ...}]
        """
        params = {"short": short}
        return await self._client._make_request("batch-forex-quotes", params)

    async def historical_price_light(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical end-of-day forex prices (light version)

        Endpoint: /historical-price-eod/light

        Args:
            symbol: Forex currency pair symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of historical price data with date, price, and volume

        Example:
            >>> data = await client.forex.historical_price_light("EURUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "EURUSD", "date": "2025-07-24", "price": 1.17639, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-price-eod/light", params)

    async def historical_price_full(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get comprehensive historical end-of-day forex price data

        Endpoint: /historical-price-eod/full

        Args:
            symbol: Forex currency pair symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of comprehensive historical price data with OHLCV and technical indicators

        Example:
            >>> data = await client.forex.historical_price_full("EURUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "EURUSD", "date": "2025-07-24", "open": 1.17744, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-price-eod/full", params)

    async def intraday_1min(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 1-minute interval intraday data for forex currency pairs

        Endpoint: /historical-chart/1min

        Args:
            symbol: Forex currency pair symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.forex.intraday_1min("EURUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:29:00", "open": 1.17582, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-chart/1min", params)

    async def intraday_5min(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 5-minute interval intraday data for forex currency pairs

        Endpoint: /historical-chart/5min

        Args:
            symbol: Forex currency pair symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 5-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.forex.intraday_5min("EURUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:25:00", "open": 1.17612, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-chart/5min", params)

    async def intraday_1hour(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get 1-hour interval intraday data for forex currency pairs

        Endpoint: /historical-chart/1hour

        Args:
            symbol: Forex currency pair symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-hour interval data with OHLCV and timestamp

        Example:
            >>> data = await client.forex.intraday_1hour("EURUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:00:00", "open": 1.17639, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-chart/1hour", params)
