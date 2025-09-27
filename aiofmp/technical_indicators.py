"""
Technical Indicators category for FMP API

This module provides technical analysis functionality including various moving averages,
RSI, standard deviation, Williams %R, ADX, and other technical indicators for market analysis.
"""

from datetime import date
from typing import Any, Literal

from .base import FMPBaseClient


class TechnicalIndicatorsCategory:
    """Technical Indicators category for FMP API endpoints"""

    # Define valid timeframe options
    Timeframe = Literal["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the technical indicators category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def simple_moving_average(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Simple Moving Average (SMA) technical indicator

        Endpoint: /technical-indicators/sma

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of SMA data with date, OHLCV data, and SMA values

        Example:
            >>> data = await client.technical_indicators.simple_moving_average("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "sma": 231.215}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/sma", params)

    async def exponential_moving_average(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Exponential Moving Average (EMA) technical indicator

        Endpoint: /technical-indicators/ema

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of EMA data with date, OHLCV data, and EMA values

        Example:
            >>> data = await client.technical_indicators.exponential_moving_average("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "ema": 232.8406611792779}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/ema", params)

    async def weighted_moving_average(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Weighted Moving Average (WMA) technical indicator

        Endpoint: /technical-indicators/wma

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of WMA data with date, OHLCV data, and WMA values

        Example:
            >>> data = await client.technical_indicators.weighted_moving_average("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "wma": 233.04745454545454}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/wma", params)

    async def double_exponential_moving_average(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Double Exponential Moving Average (DEMA) technical indicator

        Endpoint: /technical-indicators/dema

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of DEMA data with date, OHLCV data, and DEMA values

        Example:
            >>> data = await client.technical_indicators.double_exponential_moving_average("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "dema": 232.10592058582725}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/dema", params)

    async def triple_exponential_moving_average(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Triple Exponential Moving Average (TEMA) technical indicator

        Endpoint: /technical-indicators/tema

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of TEMA data with date, OHLCV data, and TEMA values

        Example:
            >>> data = await client.technical_indicators.triple_exponential_moving_average("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "tema": 233.66383715917516}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/tema", params)

    async def relative_strength_index(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Relative Strength Index (RSI) technical indicator

        Endpoint: /technical-indicators/rsi

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of RSI data with date, OHLCV data, and RSI values

        Example:
            >>> data = await client.technical_indicators.relative_strength_index("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "rsi": 47.64507340768903}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/rsi", params)

    async def standard_deviation(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Standard Deviation technical indicator

        Endpoint: /technical-indicators/standarddeviation

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of Standard Deviation data with date, OHLCV data, and standardDeviation values

        Example:
            >>> data = await client.technical_indicators.standard_deviation("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "standardDeviation": 6.139182763202282}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request(
            "technical-indicators/standarddeviation", params
        )

    async def williams_percent_r(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Williams %R technical indicator

        Endpoint: /technical-indicators/williams

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of Williams %R data with date, OHLCV data, and williams values

        Example:
            >>> data = await client.technical_indicators.williams_percent_r("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "williams": -52.51824817518242}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/williams", params)

    async def average_directional_index(
        self,
        symbol: str,
        period_length: int,
        timeframe: Timeframe,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get Average Directional Index (ADX) technical indicator

        Endpoint: /technical-indicators/adx

        Args:
            symbol: Stock symbol (required)
            period_length: Number of periods for calculation (required)
            timeframe: Time interval for data (required)
            from_date: Start date for data (optional)
            to_date: End date for data (optional)

        Returns:
            List of ADX data with date, OHLCV data, and adx values

        Example:
            >>> data = await client.technical_indicators.average_directional_index("AAPL", 10, "1day")
            >>> # Returns: [{"date": "2025-02-04 00:00:00", "open": 227.2, "high": 233.13, "low": 226.65, "close": 232.8, "volume": 44489128, "adx": 26.414065772772613}]
        """
        params = {
            "symbol": symbol,
            "periodLength": period_length,
            "timeframe": timeframe,
        }
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("technical-indicators/adx", params)
