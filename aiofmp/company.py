"""
Company category for FMP API

This module provides company functionality including company profiles, notes, employee counts,
market capitalization data, shares float information, mergers & acquisitions data,
executives, and compensation information.
"""

from typing import Any

from .base import FMPBaseClient


class CompanyCategory:
    """Company category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the company category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def profile(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get detailed company profile data

        Endpoint: /profile

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of company profile data with comprehensive company information

        Example:
            >>> data = await client.company.profile("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "companyName": "Apple Inc.", "marketCap": 3500823120000, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("profile", params)

    async def notes(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get company-issued notes information

        Endpoint: /company-notes

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of company notes data with CIK, symbol, title, and exchange

        Example:
            >>> data = await client.company.notes("AAPL")
            >>> # Returns: [{"cik": "0000320193", "symbol": "AAPL", "title": "1.000% Notes due 2022", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("company-notes", params)

    async def employee_count(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get company employee count information

        Endpoint: /employee-count

        Args:
            symbol: Stock symbol (required)
            limit: Maximum number of results to return (optional)

        Returns:
            List of employee count data with workforce information and SEC filing details

        Example:
            >>> data = await client.company.employee_count("AAPL", limit=10)
            >>> # Returns: [{"symbol": "AAPL", "employeeCount": 164000, "filingDate": "2024-11-01", ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("employee-count", params)

    async def historical_employee_count(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical employee count data for a company

        Endpoint: /historical-employee-count

        Args:
            symbol: Stock symbol (required)
            limit: Maximum number of results to return (optional)

        Returns:
            List of historical employee count data showing workforce evolution over time

        Example:
            >>> data = await client.company.historical_employee_count("AAPL", limit=20)
            >>> # Returns: [{"symbol": "AAPL", "employeeCount": 164000, "periodOfReport": "2024-09-28", ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("historical-employee-count", params)

    async def market_cap(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get company market capitalization data

        Endpoint: /market-capitalization

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of market cap data with symbol, date, and market capitalization value

        Example:
            >>> data = await client.company.market_cap("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "marketCap": 3500823120000}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("market-capitalization", params)

    async def batch_market_cap(self, symbols: list[str]) -> list[dict[str, Any]]:
        """
        Get market capitalization data for multiple companies

        Endpoint: /market-capitalization-batch

        Args:
            symbols: List of stock symbols (required)

        Returns:
            List of market cap data for multiple companies

        Example:
            >>> data = await client.company.batch_market_cap(["AAPL", "MSFT", "GOOGL"])
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "marketCap": 3500823120000}, ...]
        """
        symbols_str = ",".join(symbols)
        params = {"symbols": symbols_str}
        return await self._client._make_request("market-capitalization-batch", params)

    async def historical_market_cap(
        self,
        symbol: str,
        limit: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical market capitalization data for a company

        Endpoint: /historical-market-capitalization

        Args:
            symbol: Stock symbol (required)
            limit: Maximum number of results to return (optional)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of historical market cap data showing market value changes over time

        Example:
            >>> data = await client.company.historical_market_cap("AAPL", "2025-01-01", "2025-03-31")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-02-29", "marketCap": 2784608472000}, ...]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request(
            "historical-market-capitalization", params
        )

    async def shares_float(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get company share float and liquidity information

        Endpoint: /shares-float

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of shares float data with free float, float shares, and outstanding shares

        Example:
            >>> data = await client.company.shares_float("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04 17:01:35", "freeFloat": 99.9095, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("shares-float", params)

    async def all_shares_float(
        self, limit: int | None = None, page: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get shares float data for all available companies

        Endpoint: /shares-float-all

        Args:
            limit: Maximum number of results to return (optional)
            page: Page number for pagination (optional)

        Returns:
            List of shares float data for all companies

        Example:
            >>> data = await client.company.all_shares_float(limit=1000, page=0)
            >>> # Returns: [{"symbol": "6898.HK", "date": "2025-02-04 17:27:01", "freeFloat": 33.2536, ...}]
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page

        return await self._client._make_request("shares-float-all", params)

    async def latest_mergers_acquisitions(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get latest mergers and acquisitions data

        Endpoint: /mergers-acquisitions-latest

        Args:
            page: Page number for pagination (optional)
            limit: Maximum number of results to return (optional)

        Returns:
            List of latest M&A data with transaction details and SEC filing links

        Example:
            >>> data = await client.company.latest_mergers_acquisitions(page=0, limit=100)
            >>> # Returns: [{"symbol": "NLOK", "companyName": "NortonLifeLock Inc.", "transactionDate": "2025-02-03", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("mergers-acquisitions-latest", params)

    async def search_mergers_acquisitions(self, name: str) -> list[dict[str, Any]]:
        """
        Search for specific mergers and acquisitions data

        Endpoint: /mergers-acquisitions-search

        Args:
            name: Company name to search for (required)

        Returns:
            List of M&A data matching the search criteria

        Example:
            >>> data = await client.company.search_mergers_acquisitions("Apple")
            >>> # Returns: [{"symbol": "PEGY", "companyName": "Pineapple Energy Inc.", "transactionDate": "2021-11-12", ...}]
        """
        params = {"name": name}
        return await self._client._make_request("mergers-acquisitions-search", params)

    async def executives(
        self, symbol: str, active: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get company executives information

        Endpoint: /key-executives

        Args:
            symbol: Stock symbol (required)
            active: Filter for active executives (optional)

        Returns:
            List of executive data with names, titles, compensation, and demographic details

        Example:
            >>> data = await client.company.executives("AAPL", active="true")
            >>> # Returns: [{"title": "Vice President of Worldwide Sales", "name": "Mr. Michael Fenger", ...}]
        """
        params = {"symbol": symbol}
        if active is not None:
            params["active"] = active

        return await self._client._make_request("key-executives", params)

    async def executive_compensation(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get executive compensation data

        Endpoint: /governance-executive-compensation

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of executive compensation data with salaries, stock awards, and total compensation

        Example:
            >>> data = await client.company.executive_compensation("AAPL")
            >>> # Returns: [{"cik": "0000320193", "symbol": "AAPL", "nameAndPosition": "Kate Adams Senior Vice President...", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request(
            "governance-executive-compensation", params
        )

    async def executive_compensation_benchmark(
        self, year: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get executive compensation benchmark data by industry

        Endpoint: /executive-compensation-benchmark

        Args:
            year: Year for benchmark data (optional)

        Returns:
            List of industry benchmark data with average compensation by industry

        Example:
            >>> data = await client.company.executive_compensation_benchmark("2024")
            >>> # Returns: [{"industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS", "year": 2023, ...}]
        """
        params = {}
        if year is not None:
            params["year"] = year

        return await self._client._make_request(
            "executive-compensation-benchmark", params
        )
