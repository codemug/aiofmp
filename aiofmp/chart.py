"""
Chart category for FMP API

This module provides chart functionality including historical price data, intraday data,
and various time intervals for stock price and volume analysis.
"""

from typing import Any

from .base import FMPBaseClient


class ChartCategory:
    """Chart category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the chart category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def historical_price_light(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get simplified stock chart data (light version)

        Endpoint: /historical-price-eod/light

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of price data with date, price, and volume

        Example:
            >>> data = await client.chart.historical_price_light("AAPL", "2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "price": 232.8, "volume": 44489128}]
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
        Get comprehensive stock price and volume data

        Endpoint: /historical-price-eod/full

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of detailed price data with OHLC, volume, changes, and VWAP

        Example:
            >>> data = await client.chart.historical_price_full("AAPL", "2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "open": 227.2, "high": 233.13, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("historical-price-eod/full", params)

    async def historical_price_unadjusted(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get stock price data without split adjustments

        Endpoint: /historical-price-eod/non-split-adjusted

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of unadjusted price data with OHLC and volume

        Example:
            >>> data = await client.chart.historical_price_unadjusted("AAPL", "2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "adjOpen": 227.2, "adjHigh": 233.13, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request(
            "historical-price-eod/non-split-adjusted", params
        )

    async def historical_price_dividend_adjusted(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get stock price data with dividend adjustments

        Endpoint: /historical-price-eod/dividend-adjusted

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of dividend-adjusted price data with OHLC and volume

        Example:
            >>> data = await client.chart.historical_price_dividend_adjusted("AAPL", "2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "adjOpen": 227.2, "adjHigh": 233.13, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request(
            "historical-price-eod/dividend-adjusted", params
        )

    async def intraday_1min(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 1-minute interval intraday stock data

        Endpoint: /historical-chart/1min

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 1-minute interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_1min("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 15:59:00", "open": 233.01, "low": 232.72, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/1min", params)

    async def intraday_5min(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 5-minute interval intraday stock data

        Endpoint: /historical-chart/5min

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 5-minute interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_5min("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 15:55:00", "open": 232.87, "low": 232.72, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/5min", params)

    async def intraday_15min(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 15-minute interval intraday stock data

        Endpoint: /historical-chart/15min

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 15-minute interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_15min("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 15:45:00", "open": 232.25, "low": 232.18, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/15min", params)

    async def intraday_30min(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 30-minute interval intraday stock data

        Endpoint: /historical-chart/30min

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 30-minute interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_30min("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 15:30:00", "open": 232.29, "low": 232.01, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/30min", params)

    async def intraday_1hour(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 1-hour interval intraday stock data

        Endpoint: /historical-chart/1hour

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 1-hour interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_1hour("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 15:30:00", "open": 232.29, "low": 232.01, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/1hour", params)

    async def intraday_4hour(
        self,
        symbol: str,
        from_date: str | None = None,
        to_date: str | None = None,
        nonadjusted: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get 4-hour interval intraday stock data

        Endpoint: /historical-chart/4hour

        Args:
            symbol: Stock symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)
            nonadjusted: Whether to use non-adjusted data (optional)

        Returns:
            List of 4-hour interval price data with OHLC and volume

        Example:
            >>> data = await client.chart.intraday_4hour("AAPL", "2025-01-01", "2025-01-02")
            >>> # Returns: [{"date": "2025-02-04 12:30:00", "open": 231.79, "low": 231.37, ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if nonadjusted is not None:
            params["nonadjusted"] = nonadjusted

        return await self._client._make_request("historical-chart/4hour", params)
