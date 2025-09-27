"""
Insider Trades category for FMP API

This module provides insider trading functionality including latest trades, search capabilities,
transaction types, statistics, and acquisition ownership tracking.
"""

from datetime import date
from typing import Any

from .base import FMPBaseClient


class InsiderTradesCategory:
    """Insider Trades category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the insider trades category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def latest_insider_trades(
        self,
        page: int | None = None,
        limit: int | None = None,
        trade_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest insider trading activity

        Endpoint: /insider-trading/latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)
            trade_date: Specific date for insider trades (optional)

        Returns:
            List of latest insider trading activities with transaction details

        Example:
            >>> data = await client.insider_trades.latest_insider_trades(page=0, limit=100)
            >>> # Returns: [{"symbol": "APA", "filingDate": "2025-02-04", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if trade_date is not None:
            params["date"] = trade_date.strftime("%Y-%m-%d")

        return await self._client._make_request("insider-trading/latest", params)

    async def search_insider_trades(
        self,
        symbol: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        reporting_cik: str | None = None,
        company_cik: str | None = None,
        transaction_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search insider trading activity by various criteria

        Endpoint: /insider-trading/search

        Args:
            symbol: Stock symbol to search for (optional)
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)
            reporting_cik: CIK of the reporting person (optional)
            company_cik: CIK of the company (optional)
            transaction_type: Type of transaction (e.g., "S-Sale", "P-Purchase") (optional)

        Returns:
            List of insider trading activities matching the search criteria

        Example:
            >>> data = await client.insider_trades.search_insider_trades(symbol="AAPL", transaction_type="S-Sale")
            >>> # Returns: [{"symbol": "AAPL", "transactionType": "S-Sale", ...}]
        """
        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if reporting_cik is not None:
            params["reportingCik"] = reporting_cik
        if company_cik is not None:
            params["companyCik"] = company_cik
        if transaction_type is not None:
            params["transactionType"] = transaction_type

        return await self._client._make_request("insider-trading/search", params)

    async def search_by_reporting_name(self, name: str) -> list[dict[str, Any]]:
        """
        Search for insider trading activity by reporting name

        Endpoint: /insider-trading/reporting-name

        Args:
            name: Name of the reporting person (required)

        Returns:
            List of reporting persons matching the name with their CIKs

        Example:
            >>> data = await client.insider_trades.search_by_reporting_name("Zuckerberg")
            >>> # Returns: [{"reportingCik": "0001548760", "reportingName": "Zuckerberg Mark"}]
        """
        params = {"name": name}
        return await self._client._make_request(
            "insider-trading/reporting-name", params
        )

    async def all_transaction_types(self) -> list[dict[str, Any]]:
        """
        Get a comprehensive list of all insider transaction types

        Endpoint: /insider-trading-transaction-type

        Returns:
            List of all available insider transaction types

        Example:
            >>> data = await client.insider_trades.all_transaction_types()
            >>> # Returns: [{"transactionType": "A-Award"}, {"transactionType": "P-Purchase"}, ...]
        """
        return await self._client._make_request("insider-trading-transaction-type")

    async def insider_trade_statistics(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get insider trading statistics for a specific company

        Endpoint: /insider-trading/statistics

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of insider trading statistics with transaction counts and ratios

        Example:
            >>> data = await client.insider_trades.insider_trade_statistics("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "year": 2024, "quarter": 4, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("insider-trading/statistics", params)

    async def acquisition_ownership(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Track changes in stock ownership during acquisitions

        Endpoint: /acquisition-of-beneficial-ownership

        Args:
            symbol: Stock symbol (required)
            limit: Maximum number of records to return (optional)

        Returns:
            List of acquisition ownership changes with beneficial ownership details

        Example:
            >>> data = await client.insider_trades.acquisition_ownership("AAPL", limit=1000)
            >>> # Returns: [{"cik": "0000320193", "symbol": "AAPL", "filingDate": "2024-02-14", ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request(
            "acquisition-of-beneficial-ownership", params
        )
