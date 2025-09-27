"""
Form 13F category for FMP API

This module provides Form 13F and institutional ownership functionality including
latest filings, extracts, analytics, performance summaries, and industry breakdowns.
"""

from typing import Any

from .base import FMPBaseClient


class Form13FCategory:
    """Form 13F category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the Form 13F category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def latest_filings(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get the most recent SEC filings related to institutional ownership

        Endpoint: /institutional-ownership/latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)

        Returns:
            List of latest institutional ownership filings with CIK, name, dates, and links

        Example:
            >>> data = await client.form13f.latest_filings(page=0, limit=100)
            >>> # Returns: [{"cik": "0001963967", "name": "CPA ASSET MANAGEMENT LLC", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request(
            "institutional-ownership/latest", params
        )

    async def filings_extract(
        self, cik: str, year: str, quarter: str
    ) -> list[dict[str, Any]]:
        """
        Extract detailed data from SEC filings for a specific institutional investor

        Endpoint: /institutional-ownership/extract

        Args:
            cik: Central Index Key of the institutional investor (required)
            year: Year of the filing (required)
            quarter: Quarter of the filing (required)

        Returns:
            List of detailed filing data with security information, shares, and values

        Example:
            >>> data = await client.form13f.filings_extract("0001388838", "2023", "3")
            >>> # Returns: [{"date": "2023-09-30", "cik": "0001388838", "symbol": "CHRD", ...}]
        """
        params = {"cik": cik, "year": year, "quarter": quarter}
        return await self._client._make_request(
            "institutional-ownership/extract", params
        )

    async def filings_dates(self, cik: str) -> list[dict[str, Any]]:
        """
        Get dates associated with Form 13F filings by institutional investors

        Endpoint: /institutional-ownership/dates

        Args:
            cik: Central Index Key of the institutional investor (required)

        Returns:
            List of filing dates with year and quarter information

        Example:
            >>> data = await client.form13f.filings_dates("0001067983")
            >>> # Returns: [{"date": "2024-09-30", "year": 2024, "quarter": 3}]
        """
        params = {"cik": cik}
        return await self._client._make_request("institutional-ownership/dates", params)

    async def filings_extract_analytics_by_holder(
        self,
        symbol: str,
        year: str,
        quarter: str,
        page: int | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get analytical breakdown of institutional filings by holder for a specific stock

        Endpoint: /institutional-ownership/extract-analytics/holder

        Args:
            symbol: Stock symbol (required)
            year: Year of the filing (required)
            quarter: Quarter of the filing (required)
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)

        Returns:
            List of institutional holder analytics with performance metrics and changes

        Example:
            >>> data = await client.form13f.filings_extract_analytics_by_holder("AAPL", "2023", "3", page=0, limit=10)
            >>> # Returns: [{"date": "2023-09-30", "cik": "0000102909", "investorName": "VANGUARD GROUP INC", ...}]
        """
        params = {"symbol": symbol, "year": year, "quarter": quarter}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request(
            "institutional-ownership/extract-analytics/holder", params
        )

    async def holder_performance_summary(
        self, cik: str, page: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get performance summary for institutional investors based on their stock holdings

        Endpoint: /institutional-ownership/holder-performance-summary

        Args:
            cik: Central Index Key of the institutional investor (required)
            page: Page number for pagination (optional)

        Returns:
            List of performance metrics including portfolio changes, returns, and benchmarks

        Example:
            >>> data = await client.form13f.holder_performance_summary("0001067983", page=0)
            >>> # Returns: [{"date": "2024-09-30", "cik": "0001067983", "investorName": "BERKSHIRE HATHAWAY INC", ...}]
        """
        params = {"cik": cik}
        if page is not None:
            params["page"] = page

        return await self._client._make_request(
            "institutional-ownership/holder-performance-summary", params
        )

    async def holder_industry_breakdown(
        self, cik: str, year: str, quarter: str
    ) -> list[dict[str, Any]]:
        """
        Get industry breakdown of institutional holdings for a specific investor

        Endpoint: /institutional-ownership/holder-industry-breakdown

        Args:
            cik: Central Index Key of the institutional investor (required)
            year: Year of the filing (required)
            quarter: Quarter of the filing (required)

        Returns:
            List of industry allocations with weights, performance, and changes

        Example:
            >>> data = await client.form13f.holder_industry_breakdown("0001067983", "2023", "3")
            >>> # Returns: [{"date": "2023-09-30", "cik": "0001067983", "industryTitle": "ELECTRONIC COMPUTERS", ...}]
        """
        params = {"cik": cik, "year": year, "quarter": quarter}
        return await self._client._make_request(
            "institutional-ownership/holder-industry-breakdown", params
        )

    async def symbol_positions_summary(
        self, symbol: str, year: str, quarter: str
    ) -> list[dict[str, Any]]:
        """
        Get comprehensive snapshot of institutional holdings for a specific stock symbol

        Endpoint: /institutional-ownership/symbol-positions-summary

        Args:
            symbol: Stock symbol (required)
            year: Year of the filing (required)
            quarter: Quarter of the filing (required)

        Returns:
            List of position summaries with investor counts, shares, values, and changes

        Example:
            >>> data = await client.form13f.symbol_positions_summary("AAPL", "2023", "3")
            >>> # Returns: [{"symbol": "AAPL", "cik": "0000320193", "investorsHolding": 4805, ...}]
        """
        params = {"symbol": symbol, "year": year, "quarter": quarter}
        return await self._client._make_request(
            "institutional-ownership/symbol-positions-summary", params
        )

    async def industry_performance_summary(
        self, year: str, quarter: str
    ) -> list[dict[str, Any]]:
        """
        Get overview of how various industries are performing financially

        Endpoint: /institutional-ownership/industry-summary

        Args:
            year: Year of the filing (required)
            quarter: Quarter of the filing (required)

        Returns:
            List of industry performance data with values and dates

        Example:
            >>> data = await client.form13f.industry_performance_summary("2023", "3")
            >>> # Returns: [{"industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS", ...}]
        """
        params = {"year": year, "quarter": quarter}
        return await self._client._make_request(
            "institutional-ownership/industry-summary", params
        )
