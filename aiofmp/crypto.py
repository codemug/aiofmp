"""
Crypto category for FMP API

This module provides cryptocurrency functionality including cryptocurrency list, real-time quotes,
historical price data, and intraday charts for various digital assets.
"""

from typing import Any

from .base import FMPBaseClient


class CryptoCategory:
    """Crypto category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the crypto category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def cryptocurrency_list(self) -> list[dict[str, Any]]:
        """
        Get comprehensive list of all cryptocurrencies traded on exchanges worldwide

        Endpoint: /cryptocurrency-list

        Returns:
            List of cryptocurrencies with symbol, name, exchange, ICO date, and supply info

        Example:
            >>> data = await client.crypto.cryptocurrency_list()
            >>> # Returns: [{"symbol": "ALIENUSD", "name": "Alien Inu USD", ...}]
        """
        return await self._client._make_request("cryptocurrency-list", {})

    async def quote(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get real-time quotes for cryptocurrencies with comprehensive data

        Endpoint: /quote

        Args:
            symbol: Cryptocurrency symbol (required)

        Returns:
            List of cryptocurrency quote data with price, changes, volume, and technical indicators

        Example:
            >>> data = await client.crypto.quote("BTCUSD")
            >>> # Returns: [{"symbol": "BTCUSD", "name": "Bitcoin USD", "price": 118741.16, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote", params)

    async def quote_short(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get fast and accurate quotes for cryptocurrencies

        Endpoint: /quote-short

        Args:
            symbol: Cryptocurrency symbol (required)

        Returns:
            List of short cryptocurrency quote data with price, change, and volume

        Example:
            >>> data = await client.crypto.quote_short("BTCUSD")
            >>> # Returns: [{"symbol": "BTCUSD", "price": 118741.16, "change": -37.93, "volume": 75302985728}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote-short", params)

    async def batch_quotes(self, short: bool = True) -> list[dict[str, Any]]:
        """
        Get live price data for a wide range of cryptocurrencies

        Endpoint: /batch-crypto-quotes

        Args:
            short: Whether to return short format quotes (default: True)

        Returns:
            List of cryptocurrency batch quotes with price, change, and volume

        Example:
            >>> data = await client.crypto.batch_quotes(short=True)
            >>> # Returns: [{"symbol": "00USD", "price": 0.01755108, "change": 0.00035108, ...}]
        """
        params = {"short": short}
        return await self._client._make_request("batch-crypto-quotes", params)

    async def historical_price_light(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical end-of-day prices for cryptocurrencies (light version)

        Endpoint: /historical-price-eod/light

        Args:
            symbol: Cryptocurrency symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of historical price data with date, price, and volume

        Example:
            >>> data = await client.crypto.historical_price_light("BTCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "BTCUSD", "date": "2025-07-24", "price": 118741.16, ...}]
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
        Get comprehensive historical end-of-day price data for cryptocurrencies

        Endpoint: /historical-price-eod/full

        Args:
            symbol: Cryptocurrency symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of comprehensive historical price data with OHLCV and technical indicators

        Example:
            >>> data = await client.crypto.historical_price_full("BTCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "BTCUSD", "date": "2025-07-24", "open": 118779.09, ...}]
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
        Get 1-minute interval intraday data for cryptocurrencies

        Endpoint: /historical-chart/1min

        Args:
            symbol: Cryptocurrency symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.crypto.intraday_1min("BTCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:29:00", "open": 118797.96, ...}]
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
        Get 5-minute interval intraday data for cryptocurrencies

        Endpoint: /historical-chart/5min

        Args:
            symbol: Cryptocurrency symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 5-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.crypto.intraday_5min("BTCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:25:00", "open": 118988.32, ...}]
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
        Get 1-hour interval intraday data for cryptocurrencies

        Endpoint: /historical-chart/1hour

        Args:
            symbol: Cryptocurrency symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-hour interval data with OHLCV and timestamp

        Example:
            >>> data = await client.crypto.intraday_1hour("BTCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:00:00", "open": 119189.36, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-chart/1hour", params)
