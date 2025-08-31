"""
Search category for FMP API

This module provides search functionality including symbol search, company name search,
and stock screening capabilities.
"""

from typing import Any, Dict, List, Optional

from .base import FMPBaseClient


class SearchCategory:
    """Search category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the search category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def symbols(
            self,
            query: str,
            limit: Optional[int] = None,
            exchange: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for stock symbols by query

        Endpoint: /search-symbol

        Args:
            query: Search query (symbol or company name)
            limit: Maximum number of results (default: API default)
            exchange: Filter by exchange (e.g., NASDAQ, NYSE)

        Returns:
            List of matching symbols with company information

        Example:
            >>> symbols = await client.search.symbols("AAPL", limit=10, exchange="NASDAQ")
            >>> # Returns: [{"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", ...}]
        """
        params = {"query": query}
        if limit is not None:
            params["limit"] = limit
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request("search-symbol", params)

    async def companies(
            self,
            query: str,
            limit: Optional[int] = None,
            exchange: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for companies by name

        Endpoint: /search-name

        Args:
            query: Company name or partial name to search for
            limit: Maximum number of results (default: API default)
            exchange: Filter by exchange (e.g., NASDAQ, NYSE)

        Returns:
            List of matching companies with symbol information

        Example:
            >>> companies = await client.search.companies("Apple", limit=5)
            >>> # Returns: [{"symbol": "AAPL", "name": "Apple Inc.", "currency": "USD", ...}]
        """
        params = {"query": query}
        if limit is not None:
            params["limit"] = limit
        if exchange is not None:
            params["exchange"] = exchange

        return await self._client._make_request("search-name", params)

    async def screener(
            self,
            *,
            market_cap_more_than: Optional[float] = None,
            market_cap_lower_than: Optional[float] = None,
            sector: Optional[str] = None,
            industry: Optional[str] = None,
            beta_more_than: Optional[float] = None,
            beta_lower_than: Optional[float] = None,
            price_more_than: Optional[float] = None,
            price_lower_than: Optional[float] = None,
            dividend_more_than: Optional[float] = None,
            dividend_lower_than: Optional[float] = None,
            volume_more_than: Optional[int] = None,
            volume_lower_than: Optional[int] = None,
            exchange: Optional[str] = None,
            country: Optional[str] = None,
            is_etf: Optional[bool] = None,
            is_fund: Optional[bool] = None,
            is_actively_trading: Optional[bool] = None,
            limit: Optional[int] = None,
            include_all_share_classes: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Screen stocks based on various criteria

        Endpoint: /company-screener

        Args:
            market_cap_more_than: Minimum market cap value
            market_cap_lower_than: Maximum market cap value
            sector: Filter by sector (e.g., Technology, Healthcare)
            industry: Filter by industry (e.g., Consumer Electronics)
            beta_more_than: Minimum beta value
            beta_lower_than: Maximum beta value
            price_more_than: Minimum stock price
            price_lower_than: Maximum stock price
            dividend_more_than: Minimum dividend yield
            dividend_lower_than: Maximum dividend yield
            volume_more_than: Minimum trading volume
            volume_lower_than: Maximum trading volume
            exchange: Filter by exchange (e.g., NASDAQ, NYSE)
            country: Filter by country (e.g., US, CA)
            is_etf: Filter for ETFs only
            is_fund: Filter for funds only
            is_actively_trading: Filter for actively trading securities
            limit: Maximum number of results (default: 1000)
            include_all_share_classes: Include all share classes

        Returns:
            List of stocks matching the screening criteria

        Example:
            >>> screener = await client.search.screener(
            ...     market_cap_more_than=1000000000,  # $1B+
            ...     sector="Technology",
            ...     exchange="NASDAQ",
            ...     limit=100
            ... )
            >>> # Returns: [{"symbol": "AAPL", "companyName": "Apple Inc.", ...}]
        """
        # Build parameters dict, filtering out None values
        params = {}

        if market_cap_more_than is not None:
            params["marketCapMoreThan"] = market_cap_more_than
        if market_cap_lower_than is not None:
            params["marketCapLowerThan"] = market_cap_lower_than
        if sector is not None:
            params["sector"] = sector
        if industry is not None:
            params["industry"] = industry
        if beta_more_than is not None:
            params["betaMoreThan"] = beta_more_than
        if beta_lower_than is not None:
            params["betaLowerThan"] = beta_lower_than
        if price_more_than is not None:
            params["priceMoreThan"] = price_more_than
        if price_lower_than is not None:
            params["priceLowerThan"] = price_lower_than
        if dividend_more_than is not None:
            params["dividendMoreThan"] = dividend_more_than
        if dividend_lower_than is not None:
            params["dividendLowerThan"] = dividend_lower_than
        if volume_more_than is not None:
            params["volumeMoreThan"] = volume_more_than
        if volume_lower_than is not None:
            params["volumeLowerThan"] = volume_lower_than
        if exchange is not None:
            params["exchange"] = exchange
        if country is not None:
            params["country"] = country
        if is_etf is not None:
            params["isEtf"] = is_etf
        if is_fund is not None:
            params["isFund"] = is_fund
        if is_actively_trading is not None:
            params["isActivelyTrading"] = is_actively_trading
        if limit is not None:
            params["limit"] = limit
        if include_all_share_classes is not None:
            params["includeAllShareClasses"] = include_all_share_classes

        return await self._client._make_request("company-screener", params)
