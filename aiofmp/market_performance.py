"""
Market Performance category for FMP API

This module provides market performance functionality including sector and industry performance,
P/E ratios, historical data, and market movers (gainers, losers, most active).
"""

from datetime import date
from typing import Any

from .base import FMPBaseClient


class MarketPerformanceCategory:
    """Market Performance category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the market performance category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def sector_performance_snapshot(
        self,
        snapshot_date: date,
        exchange: str | None = None,
        sector: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get a snapshot of sector performance

        Endpoint: /sector-performance-snapshot

        Args:
            snapshot_date: Date for the performance snapshot (required)
            exchange: Stock exchange (optional)
            sector: Specific sector to filter (optional)

        Returns:
            List of sector performance data with date, sector, exchange, and average change

        Example:
            >>> data = await client.market_performance.sector_performance_snapshot(date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "sector": "Basic Materials", "exchange": "NASDAQ", "averageChange": -0.3148}]
        """
        params = {"date": snapshot_date.strftime("%Y-%m-%d")}
        if exchange is not None:
            params["exchange"] = exchange
        if sector is not None:
            params["sector"] = sector

        return await self._client._make_request("sector-performance-snapshot", params)

    async def industry_performance_snapshot(
        self,
        snapshot_date: date,
        exchange: str | None = None,
        industry: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get a snapshot of industry performance

        Endpoint: /industry-performance-snapshot

        Args:
            snapshot_date: Date for the performance snapshot (required)
            exchange: Stock exchange (optional)
            industry: Specific industry to filter (optional)

        Returns:
            List of industry performance data with date, industry, exchange, and average change

        Example:
            >>> data = await client.market_performance.industry_performance_snapshot(date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "industry": "Advertising Agencies", "exchange": "NASDAQ", "averageChange": 3.8660}]
        """
        params = {"date": snapshot_date.strftime("%Y-%m-%d")}
        if exchange is not None:
            params["exchange"] = exchange
        if industry is not None:
            params["industry"] = industry

        return await self._client._make_request("industry-performance-snapshot", params)

    async def historical_sector_performance(
        self,
        sector: str,
        from_date: date | None = None,
        to_date: date | None = None,
        exchange: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical sector performance data

        Endpoint: /historical-sector-performance

        Args:
            sector: Sector name (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)
            exchange: Stock exchange (optional)

        Returns:
            List of historical sector performance data with date, sector, exchange, and average change

        Example:
            >>> data = await client.market_performance.historical_sector_performance("Energy", from_date=date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "sector": "Energy", "exchange": "NASDAQ", "averageChange": 0.6398}]
        """
        params = {"sector": sector}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request("historical-sector-performance", params)

    async def historical_industry_performance(
        self,
        industry: str,
        from_date: date | None = None,
        to_date: date | None = None,
        exchange: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical industry performance data

        Endpoint: /historical-industry-performance

        Args:
            industry: Industry name (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)
            exchange: Stock exchange (optional)

        Returns:
            List of historical industry performance data with date, industry, exchange, and average change

        Example:
            >>> data = await client.market_performance.historical_industry_performance("Biotechnology", from_date=date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "industry": "Biotechnology", "exchange": "NASDAQ", "averageChange": 1.1479}]
        """
        params = {"industry": industry}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request(
            "historical-industry-performance", params
        )

    async def sector_pe_snapshot(
        self,
        snapshot_date: date,
        exchange: str | None = None,
        sector: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get price-to-earnings (P/E) ratios for various sectors

        Endpoint: /sector-pe-snapshot

        Args:
            snapshot_date: Date for the P/E snapshot (required)
            exchange: Stock exchange (optional)
            sector: Specific sector to filter (optional)

        Returns:
            List of sector P/E data with date, sector, exchange, and P/E ratio

        Example:
            >>> data = await client.market_performance.sector_pe_snapshot(date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "sector": "Basic Materials", "exchange": "NASDAQ", "pe": 15.6877}]
        """
        params = {"date": snapshot_date.strftime("%Y-%m-%d")}
        if exchange is not None:
            params["exchange"] = exchange
        if sector is not None:
            params["sector"] = sector

        return await self._client._make_request("sector-pe-snapshot", params)

    async def industry_pe_snapshot(
        self,
        snapshot_date: date,
        exchange: str | None = None,
        industry: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get price-to-earnings (P/E) ratios for different industries

        Endpoint: /industry-pe-snapshot

        Args:
            snapshot_date: Date for the P/E snapshot (required)
            exchange: Stock exchange (optional)
            industry: Specific industry to filter (optional)

        Returns:
            List of industry P/E data with date, industry, exchange, and P/E ratio

        Example:
            >>> data = await client.market_performance.industry_pe_snapshot(date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "industry": "Advertising Agencies", "exchange": "NASDAQ", "pe": 71.0960}]
        """
        params = {"date": snapshot_date.strftime("%Y-%m-%d")}
        if exchange is not None:
            params["exchange"] = exchange
        if industry is not None:
            params["industry"] = industry

        return await self._client._make_request("industry-pe-snapshot", params)

    async def historical_sector_pe(
        self,
        sector: str,
        from_date: date | None = None,
        to_date: date | None = None,
        exchange: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical price-to-earnings (P/E) ratios for various sectors

        Endpoint: /historical-sector-pe

        Args:
            sector: Sector name (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)
            exchange: Stock exchange (optional)

        Returns:
            List of historical sector P/E data with date, sector, exchange, and P/E ratio

        Example:
            >>> data = await client.market_performance.historical_sector_pe("Energy", from_date=date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "sector": "Energy", "exchange": "NASDAQ", "pe": 14.4114}]
        """
        params = {"sector": sector}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request("historical-sector-pe", params)

    async def historical_industry_pe(
        self,
        industry: str,
        from_date: date | None = None,
        to_date: date | None = None,
        exchange: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical price-to-earnings (P/E) ratios by industry

        Endpoint: /historical-industry-pe

        Args:
            industry: Industry name (required)
            from_date: Start date for historical data (optional)
            to_date: End date for historical data (optional)
            exchange: Stock exchange (optional)

        Returns:
            List of historical industry P/E data with date, industry, exchange, and P/E ratio

        Example:
            >>> data = await client.market_performance.historical_industry_pe("Biotechnology", from_date=date(2024, 2, 1))
            >>> # Returns: [{"date": "2024-02-01", "industry": "Biotechnology", "exchange": "NASDAQ", "pe": 10.1816}]
        """
        params = {"industry": industry}
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request("historical-industry-pe", params)

    async def biggest_gainers(self) -> list[dict[str, Any]]:
        """
        Get the stocks with the largest price increases

        Endpoint: /biggest-gainers

        Returns:
            List of biggest gainer stocks with symbol, price, name, change, and percentage change

        Example:
            >>> data = await client.market_performance.biggest_gainers()
            >>> # Returns: [{"symbol": "LTRY", "price": 0.5876, "name": "Lottery.com Inc.", "change": 0.2756, "changesPercentage": 88.3333}]
        """
        return await self._client._make_request("biggest-gainers")

    async def biggest_losers(self) -> list[dict[str, Any]]:
        """
        Get the stocks with the largest price drops

        Endpoint: /biggest-losers

        Returns:
            List of biggest loser stocks with symbol, price, name, change, and percentage change

        Example:
            >>> data = await client.market_performance.biggest_losers()
            >>> # Returns: [{"symbol": "IDEX", "price": 0.0021, "name": "Ideanomics, Inc.", "change": -0.0029, "changesPercentage": -58}]
        """
        return await self._client._make_request("biggest-losers")

    async def most_active_stocks(self) -> list[dict[str, Any]]:
        """
        Get the most actively traded stocks

        Endpoint: /most-actives

        Returns:
            List of most active stocks with symbol, price, name, change, and percentage change

        Example:
            >>> data = await client.market_performance.most_active_stocks()
            >>> # Returns: [{"symbol": "LUCY", "price": 5.03, "name": "Innovative Eyewear, Inc.", "change": -0.01, "changesPercentage": -0.1984}]
        """
        return await self._client._make_request("most-actives")
