"""
ETF And Mutual Funds category for FMP API

This module provides ETF and mutual fund functionality including holdings breakdown,
fund information, country allocation, asset exposure, sector weighting, and disclosures.
"""

from typing import Any

from .base import FMPBaseClient


class EtfAndMutualFundsCategory:
    """ETF And Mutual Funds category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the ETF and mutual funds category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def holdings(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get detailed breakdown of assets held within ETFs and mutual funds

        Endpoint: /etf/holdings

        Args:
            symbol: ETF or mutual fund symbol (required)

        Returns:
            List of holdings data with asset details, shares, weights, and market values

        Example:
            >>> data = await client.etf.holdings("SPY")
            >>> # Returns: [{"symbol": "SPY", "asset": "AAPL", "name": "APPLE INC", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("etf/holdings", params)

    async def info(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get comprehensive information on ETFs and mutual funds

        Endpoint: /etf/info

        Args:
            symbol: ETF or mutual fund symbol (required)

        Returns:
            List of fund information including description, expense ratio, AUM, and more

        Example:
            >>> data = await client.etf.info("SPY")
            >>> # Returns: [{"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("etf/info", params)

    async def country_weightings(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get country allocation breakdown for ETFs and mutual funds

        Endpoint: /etf/country-weightings

        Args:
            symbol: ETF or mutual fund symbol (required)

        Returns:
            List of country allocation data with weight percentages

        Example:
            >>> data = await client.etf.country_weightings("SPY")
            >>> # Returns: [{"country": "United States", "weightPercentage": "97.29%"}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("etf/country-weightings", params)

    async def asset_exposure(self, symbol: str) -> list[dict[str, Any]]:
        """
        Discover which ETFs hold specific stocks

        Endpoint: /etf/asset-exposure

        Args:
            symbol: Stock symbol to find ETF exposure (required)

        Returns:
            List of ETF exposure data showing which ETFs hold the specified stock

        Example:
            >>> data = await client.etf.asset_exposure("AAPL")
            >>> # Returns: [{"symbol": "ZECP", "asset": "AAPL", "sharesNumber": 5482, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("etf/asset-exposure", params)

    async def sector_weightings(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get sector weighting breakdown for ETFs and mutual funds

        Endpoint: /etf/sector-weightings

        Args:
            symbol: ETF or mutual fund symbol (required)

        Returns:
            List of sector weighting data with weight percentages

        Example:
            >>> data = await client.etf.sector_weightings("SPY")
            >>> # Returns: [{"symbol": "SPY", "sector": "Basic Materials", "weightPercentage": 1.97}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("etf/sector-weightings", params)

    async def disclosure_holders_latest(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get latest disclosures from mutual funds and ETFs

        Endpoint: /funds/disclosure-holders-latest

        Args:
            symbol: Stock symbol to find disclosure holders (required)

        Returns:
            List of latest disclosure data for mutual funds and ETFs holding the specified stock

        Example:
            >>> data = await client.etf.disclosure_holders_latest("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "holder": "Fund Name", "shares": 1000000, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request(
            "funds/disclosure-holders-latest", params
        )
