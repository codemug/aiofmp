"""
Directory category for FMP API

This module provides directory functionality including company symbols, financial symbols,
ETFs, actively trading lists, earnings transcripts, and available exchanges, sectors,
industries, and countries.
"""

from typing import Any

from .base import FMPBaseClient


class DirectoryCategory:
    """Directory category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the directory category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def company_symbols(self) -> list[dict[str, Any]]:
        """
        Get a comprehensive list of financial symbols

        Endpoint: /company-symbols-list

        Returns:
            List of company symbols with company names

        Example:
            >>> symbols = await client.directory.company_symbols()
            >>> # Returns: [{"symbol": "6898.HK", "companyName": "China Aluminum Cans Holdings Limited"}, ...]
        """
        return await self._client._make_request("company-symbols-list")

    async def financial_symbols(self) -> list[dict[str, Any]]:
        """
        Get a list of companies with available financial statements

        Endpoint: /financial-symbols-list

        Returns:
            List of financial symbols with company names and currency information

        Example:
            >>> symbols = await client.directory.financial_symbols()
            >>> # Returns: [{"symbol": "6898.HK", "companyName": "China Aluminum Cans Holdings Limited", "tradingCurrency": "HKD", "reportingCurrency": "HKD"}, ...]
        """
        return await self._client._make_request("financial-symbols-list")

    async def etf_list(self) -> list[dict[str, Any]]:
        """
        Get a list of Exchange Traded Funds (ETFs)

        Endpoint: /etf-list

        Returns:
            List of ETFs with symbols and names

        Example:
            >>> etfs = await client.directory.etf_list()
            >>> # Returns: [{"symbol": "GULF", "name": "WisdomTree Middle East Dividend Fund"}, ...]
        """
        return await self._client._make_request("etf-list")

    async def actively_trading(self) -> list[dict[str, Any]]:
        """
        Get a list of actively trading companies and financial instruments

        Endpoint: /actively-trading-list

        Returns:
            List of actively trading securities with symbols and names

        Example:
            >>> active = await client.directory.actively_trading()
            >>> # Returns: [{"symbol": "6898.HK", "name": "China Aluminum Cans Holdings Limited"}, ...]
        """
        return await self._client._make_request("actively-trading-list")

    async def earnings_transcripts(self) -> list[dict[str, Any]]:
        """
        Get a list of companies with available earnings transcripts

        Endpoint: /earnings-transcript-list

        Returns:
            List of companies with earnings transcripts and transcript counts

        Example:
            >>> transcripts = await client.directory.earnings_transcripts()
            >>> # Returns: [{"symbol": "MCUJF", "companyName": "Medicure Inc.", "noOfTranscripts": "16"}, ...]
        """
        return await self._client._make_request("earnings-transcript-list")

    async def available_exchanges(self) -> list[dict[str, Any]]:
        """
        Get a complete list of supported stock exchanges

        Endpoint: /available-exchanges

        Returns:
            List of available exchanges with details

        Example:
            >>> exchanges = await client.directory.available_exchanges()
            >>> # Returns: [{"exchange": "AMEX", "name": "New York Stock Exchange Arca", "countryName": "United States of America", "countryCode": "US", "symbolSuffix": "N/A", "delay": "Real-time"}, ...]
        """
        return await self._client._make_request("available-exchanges")

    async def available_sectors(self) -> list[dict[str, Any]]:
        """
        Get a complete list of industry sectors

        Endpoint: /available-sectors

        Returns:
            List of available sectors

        Example:
            >>> sectors = await client.directory.available_sectors()
            >>> # Returns: [{"sector": "Basic Materials"}, {"sector": "Technology"}, ...]
        """
        return await self._client._make_request("available-sectors")

    async def available_industries(self) -> list[dict[str, Any]]:
        """
        Get a comprehensive list of industries

        Endpoint: /available-industries

        Returns:
            List of available industries

        Example:
            >>> industries = await client.directory.available_industries()
            >>> # Returns: [{"industry": "Steel"}, {"industry": "Consumer Electronics"}, ...]
        """
        return await self._client._make_request("available-industries")

    async def available_countries(self) -> list[dict[str, Any]]:
        """
        Get a comprehensive list of countries where stock symbols are available

        Endpoint: /available-countries

        Returns:
            List of available countries with country codes

        Example:
            >>> countries = await client.directory.available_countries()
            >>> # Returns: [{"country": "US"}, {"country": "CA"}, ...]
        """
        return await self._client._make_request("available-countries")
