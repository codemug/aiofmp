"""
Senate category for FMP API

This module provides Senate and House financial disclosure functionality including
latest disclosures, trading activity, name-based searches, and government transparency data.
"""

from typing import Any

from .base import FMPBaseClient


class SenateCategory:
    """Senate category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the senate category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def latest_senate_disclosures(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get the latest financial disclosures from U.S. Senate members

        Endpoint: /senate-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)

        Returns:
            List of latest Senate financial disclosures with trade details, asset info, and links

        Example:
            >>> data = await client.senate.latest_senate_disclosures(page=0, limit=100)
            >>> # Returns: [{"symbol": "LRN", "disclosureDate": "2025-01-31", "transactionDate": "2025-01-02", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("senate-latest", params)

    async def latest_house_disclosures(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get the latest financial disclosures from U.S. House members

        Endpoint: /house-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of records per page (optional)

        Returns:
            List of latest House financial disclosures with trade details, asset info, and links

        Example:
            >>> data = await client.senate.latest_house_disclosures(page=0, limit=100)
            >>> # Returns: [{"symbol": "$VIRTUALUSD", "disclosureDate": "2025-02-03", "transactionDate": "2025-01-03", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("house-latest", params)

    async def senate_trading_activity(self, symbol: str) -> list[dict[str, Any]]:
        """
        Monitor the trading activity of US Senators for a specific symbol

        Endpoint: /senate-trades

        Args:
            symbol: Stock symbol to search for (required)

        Returns:
            List of Senate trading activity for the specified symbol with trade details and disclosure info

        Example:
            >>> data = await client.senate.senate_trading_activity("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "disclosureDate": "2025-01-08", "transactionDate": "2024-12-19", ...}]
        """
        return await self._client._make_request("senate-trades", {"symbol": symbol})

    async def senate_trades_by_name(self, name: str) -> list[dict[str, Any]]:
        """
        Search Senate trading activity by Senator name

        Endpoint: /senate-trades-by-name

        Args:
            name: Senator name to search for (required)

        Returns:
            List of Senate trading activity for the specified name with trade details and disclosure info

        Example:
            >>> data = await client.senate.senate_trades_by_name("Jerry")
            >>> # Returns: [{"symbol": "BRK/B", "disclosureDate": "2025-01-18", "transactionDate": "2024-12-16", ...}]
        """
        return await self._client._make_request("senate-trades-by-name", {"name": name})

    async def house_trading_activity(self, symbol: str) -> list[dict[str, Any]]:
        """
        Track the financial trades made by U.S. House members for a specific symbol

        Endpoint: /house-trades

        Args:
            symbol: Stock symbol to search for (required)

        Returns:
            List of House trading activity for the specified symbol with trade details and disclosure info

        Example:
            >>> data = await client.senate.house_trading_activity("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "disclosureDate": "2025-01-20", "transactionDate": "2024-12-31", ...}]
        """
        return await self._client._make_request("house-trades", {"symbol": symbol})

    async def house_trades_by_name(self, name: str) -> list[dict[str, Any]]:
        """
        Search House trading activity by Representative name

        Endpoint: /house-trades-by-name

        Args:
            name: Representative name to search for (required)

        Returns:
            List of House trading activity for the specified name with trade details and disclosure info

        Example:
            >>> data = await client.senate.house_trades_by_name("James")
            >>> # Returns: [{"symbol": "LUV", "disclosureDate": "2025-01-13", "transactionDate": "2024-12-31", ...}]
        """
        return await self._client._make_request("house-trades-by-name", {"name": name})
