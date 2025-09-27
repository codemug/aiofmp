"""
Commitment of Traders (COT) category for FMP API

This module provides COT functionality including comprehensive COT reports,
market sentiment analysis, and available COT symbols for commodities and futures.
"""

from typing import Any

from .base import FMPBaseClient


class CommitmentOfTradersCategory:
    """Commitment of Traders (COT) category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the COT category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def cot_report(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get comprehensive Commitment of Traders (COT) reports

        Endpoint: /commitment-of-traders-report

        Args:
            symbol: Commodity or futures symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of COT report data with detailed position information

        Example:
            >>> data = await client.cot.cot_report("KC", "2024-01-01", "2024-03-01")
            >>> # Returns: [{"symbol": "KC", "name": "Coffee (KC)", "sector": "SOFTS", ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("commitment-of-traders-report", params)

    async def cot_analysis(
        self, symbol: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get COT analysis with market sentiment insights

        Endpoint: /commitment-of-traders-analysis

        Args:
            symbol: Commodity or futures symbol (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of COT analysis data with market sentiment and trend information

        Example:
            >>> data = await client.cot.cot_analysis("B6", "2024-01-01", "2024-03-01")
            >>> # Returns: [{"symbol": "B6", "name": "British Pound (B6)", "marketSituation": "Bullish", ...}]
        """
        params = {"symbol": symbol}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request(
            "commitment-of-traders-analysis", params
        )

    async def cot_list(self) -> list[dict[str, Any]]:
        """
        Get list of available COT report symbols

        Endpoint: /commitment-of-traders-list

        Returns:
            List of available COT symbols and their names

        Example:
            >>> data = await client.cot.cot_list()
            >>> # Returns: [{"symbol": "NG", "name": "Natural Gas (NG)"}, ...]
        """
        return await self._client._make_request("commitment-of-traders-list", {})
