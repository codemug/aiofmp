"""
Commodity category for FMP API

This module provides commodity functionality including commodities list, real-time quotes,
historical price data, and intraday charts for various commodity futures.
"""

from typing import Any

from .base import FMPBaseClient


class CommodityCategory:
    """Commodity category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the commodity category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def commodities_list(self) -> list[dict[str, Any]]:
        """
        Get extensive list of tracked commodities across various sectors

        Endpoint: /commodities-list

        Returns:
            List of commodities with symbol, name, exchange, trade month, and currency

        Example:
            >>> data = await client.commodity.commodities_list()
            >>> # Returns: [{"symbol": "HEUSX", "name": "Lean Hogs Futures", ...}]
        """
        return await self._client._make_request("commodities-list", {})

    async def quote(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get real-time price quotes for commodities

        Endpoint: /quote

        Args:
            symbol: Commodity symbol (required)

        Returns:
            List of commodity quote data with price, changes, volume, and technical indicators

        Example:
            >>> data = await client.commodity.quote("GCUSD")
            >>> # Returns: [{"symbol": "GCUSD", "name": "Gold Futures", "price": 3375.3, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote", params)

    async def quote_short(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get fast and accurate quotes for commodities

        Endpoint: /quote-short

        Args:
            symbol: Commodity symbol (required)

        Returns:
            List of short commodity quote data with price, change, and volume

        Example:
            >>> data = await client.commodity.quote_short("GCUSD")
            >>> # Returns: [{"symbol": "GCUSD", "price": 3375.3, "change": -22.3, "volume": 170936}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("quote-short", params)

    async def historical_price_light(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical end-of-day prices for commodities (light version)

        Endpoint: /historical-price-eod/light

        Args:
            symbol: Commodity symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of historical price data with date, price, and volume

        Example:
            >>> data = await client.commodity.historical_price_light("GCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "GCUSD", "date": "2025-07-24", "price": 3373.8, ...}]
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
        Get full historical end-of-day price data for commodities

        Endpoint: /historical-price-eod/full

        Args:
            symbol: Commodity symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of comprehensive historical price data with OHLCV and technical indicators

        Example:
            >>> data = await client.commodity.historical_price_full("GCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"symbol": "GCUSD", "date": "2025-07-24", "open": 3398.6, ...}]
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
        Get 1-minute interval intraday data for commodities

        Endpoint: /historical-chart/1min

        Args:
            symbol: Commodity symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.commodity.intraday_1min("GCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:18:00", "open": 3374.5, ...}]
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
        Get 5-minute interval intraday data for commodities

        Endpoint: /historical-chart/5min

        Args:
            symbol: Commodity symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 5-minute interval data with OHLCV and timestamp

        Example:
            >>> data = await client.commodity.intraday_5min("GCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 12:15:00", "open": 3374, ...}]
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
        Get 1-hour interval intraday data for commodities

        Endpoint: /historical-chart/1hour

        Args:
            symbol: Commodity symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of 1-hour interval data with OHLCV and timestamp

        Example:
            >>> data = await client.commodity.intraday_1hour("GCUSD", "2025-04-25", "2025-07-25")
            >>> # Returns: [{"date": "2025-07-24 11:30:00", "open": 3378.4, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-chart/1hour", params)
