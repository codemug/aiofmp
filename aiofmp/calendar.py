"""
Calendar category for FMP API

This module provides calendar functionality including dividends, earnings, IPOs,
stock splits, and related calendar events across different time periods.
"""

from typing import Any

from .base import FMPBaseClient


class CalendarCategory:
    """Calendar category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the calendar category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def dividends_company(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get dividend information for a specific company

        Endpoint: /dividends

        Args:
            symbol: Stock symbol (required)
            limit: Number of dividend records (default: 100)

        Returns:
            List of dividend records with dates, amounts, and yields

        Example:
            >>> dividends = await client.calendar.dividends_company("AAPL", limit=50)
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-10", "dividend": 0.25, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("dividends", params)

    async def dividends_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get dividend calendar for all stocks within a date range

        Endpoint: /dividends-calendar

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of dividend events across all stocks

        Example:
            >>> dividends = await client.calendar.dividends_calendar("2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "1D0.SI", "date": "2025-02-04", "dividend": 0.01, ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("dividends-calendar", params)

    async def earnings_company(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get earnings information for a specific company

        Endpoint: /earnings

        Args:
            symbol: Stock symbol (required)
            limit: Number of earnings records (default: 100)

        Returns:
            List of earnings records with dates, estimates, and actual results

        Example:
            >>> earnings = await client.calendar.earnings_company("AAPL", limit=20)
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-10-29", "epsEstimated": null, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("earnings", params)

    async def earnings_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get earnings calendar for all companies within a date range

        Endpoint: /earnings-calendar

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of earnings announcements across all companies

        Example:
            >>> earnings = await client.calendar.earnings_calendar("2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "KEC.NS", "date": "2024-11-04", "epsActual": 3.32, ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("earnings-calendar", params)

    async def ipos_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get IPO calendar for upcoming initial public offerings

        Endpoint: /ipos-calendar

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of upcoming IPOs with company details and pricing

        Example:
            >>> ipos = await client.calendar.ipos_calendar("2025-01-01", "2025-06-30")
            >>> # Returns: [{"symbol": "PEVC", "date": "2025-02-03", "company": "Pacer Funds Trust", ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("ipos-calendar", params)

    async def ipos_disclosure(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get IPO disclosure filings for upcoming initial public offerings

        Endpoint: /ipos-disclosure

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of IPO disclosure filings with regulatory information

        Example:
            >>> disclosures = await client.calendar.ipos_disclosure("2025-01-01", "2025-06-30")
            >>> # Returns: [{"symbol": "SCHM", "filingDate": "2025-02-03", "cik": "0001454889", ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("ipos-disclosure", params)

    async def ipos_prospectus(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get IPO prospectus information for upcoming initial public offerings

        Endpoint: /ipos-prospectus

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of IPO prospectuses with financial details and SEC links

        Example:
            >>> prospectuses = await client.calendar.ipos_prospectus("2025-01-01", "2025-06-30")
            >>> # Returns: [{"symbol": "ATAK", "ipoDate": "2022-03-20", "pricePublicPerShare": 0.78, ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("ipos-prospectus", params)

    async def stock_splits_company(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get stock split information for a specific company

        Endpoint: /splits

        Args:
            symbol: Stock symbol (required)
            limit: Number of split records (default: 100)

        Returns:
            List of stock splits with dates and ratios

        Example:
            >>> splits = await client.calendar.stock_splits_company("AAPL", limit=20)
            >>> # Returns: [{"symbol": "AAPL", "date": "2020-08-31", "numerator": 4, "denominator": 1}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("splits", params)

    async def stock_splits_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get stock splits calendar for all companies within a date range

        Endpoint: /splits-calendar

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of upcoming stock splits across all companies

        Example:
            >>> splits = await client.calendar.stock_splits_calendar("2025-01-01", "2025-06-30")
            >>> # Returns: [{"symbol": "EYEN", "date": "2025-02-03", "numerator": 1, "denominator": 80}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("splits-calendar", params)
