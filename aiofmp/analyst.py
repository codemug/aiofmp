"""
Analyst category for FMP API

This module provides analyst functionality including financial estimates, ratings,
price targets, stock grades, and related news and historical data.
"""

from typing import Any

from .base import FMPBaseClient


class AnalystCategory:
    """Analyst category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the analyst category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def financial_estimates(
        self,
        symbol: str,
        period: str,
        page: int | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get analyst financial estimates for a stock symbol

        Endpoint: /analyst-estimates

        Args:
            symbol: Stock symbol (required)
            period: Period type - 'annual' or 'quarter' (required)
            page: Page number for pagination (default: 0)
            limit: Number of results per page (default: 10)

        Returns:
            List of financial estimates with analyst projections

        Example:
            >>> estimates = await client.analyst.financial_estimates("AAPL", "annual", limit=20)
            >>> # Returns: [{"symbol": "AAPL", "date": "2029-09-28", "revenueAvg": 483093000000, ...}]
        """
        params = {"symbol": symbol, "period": period}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("analyst-estimates", params)

    async def ratings_snapshot(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get current financial ratings snapshot for a stock symbol

        Endpoint: /ratings-snapshot

        Args:
            symbol: Stock symbol (required)
            limit: Number of results (default: 1)

        Returns:
            List of current ratings with financial scores

        Example:
            >>> ratings = await client.analyst.ratings_snapshot("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "rating": "A-", "overallScore": 4, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("ratings-snapshot", params)

    async def historical_ratings(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical financial ratings for a stock symbol

        Endpoint: /ratings-historical

        Args:
            symbol: Stock symbol (required)
            limit: Number of historical ratings (default: 1)

        Returns:
            List of historical ratings with dates and scores

        Example:
            >>> historical = await client.analyst.historical_ratings("AAPL", limit=10)
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "rating": "A-", ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("ratings-historical", params)

    async def price_target_summary(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get price target summary from analysts for a stock symbol

        Endpoint: /price-target-summary

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of price target summaries across different timeframes

        Example:
            >>> summary = await client.analyst.price_target_summary("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "lastMonthAvgPriceTarget": 200.75, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("price-target-summary", params)

    async def price_target_consensus(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get price target consensus from analysts for a stock symbol

        Endpoint: /price-target-consensus

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of consensus price targets (high, low, median, consensus)

        Example:
            >>> consensus = await client.analyst.price_target_consensus("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "targetHigh": 300, "targetConsensus": 251.7, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("price-target-consensus", params)

    async def price_target_news(
        self, symbol: str, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get news about analyst price targets for a stock symbol

        Endpoint: /price-target-news

        Args:
            symbol: Stock symbol (required)
            page: Page number for pagination (default: 0)
            limit: Number of results per page (default: 10)

        Returns:
            List of price target news articles with analyst insights

        Example:
            >>> news = await client.analyst.price_target_news("AAPL", limit=5)
            >>> # Returns: [{"symbol": "AAPL", "newsTitle": "...", "analystName": "...", ...}]
        """
        params = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("price-target-news", params)

    async def price_target_latest_news(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get latest analyst price target news for all stock symbols

        Endpoint: /price-target-latest-news

        Args:
            page: Page number for pagination (default: 0)
            limit: Number of results per page (default: 10)

        Returns:
            List of latest price target news across all symbols

        Example:
            >>> latest_news = await client.analyst.price_target_latest_news(limit=20)
            >>> # Returns: [{"symbol": "OLN", "newsTitle": "...", "analystName": "...", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("price-target-latest-news", params)

    async def stock_grades(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get latest stock grades from analysts for a stock symbol

        Endpoint: /grades

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of analyst grades with grading company and actions

        Example:
            >>> grades = await client.analyst.stock_grades("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "gradingCompany": "Morgan Stanley", "newGrade": "Overweight", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("grades", params)

    async def historical_stock_grades(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get historical analyst grades for a stock symbol

        Endpoint: /grades-historical

        Args:
            symbol: Stock symbol (required)
            limit: Number of historical grades (default: 100)

        Returns:
            List of historical analyst ratings breakdowns

        Example:
            >>> historical_grades = await client.analyst.historical_stock_grades("AAPL", limit=50)
            >>> # Returns: [{"symbol": "AAPL", "analystRatingsBuy": 8, "analystRatingsHold": 14, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("grades-historical", params)

    async def stock_grades_summary(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get summary of analyst grades consensus for a stock symbol

        Endpoint: /grades-consensus

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of grade summaries with consensus ratings

        Example:
            >>> summary = await client.analyst.stock_grades_summary("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "strongBuy": 1, "buy": 29, "consensus": "Buy", ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("grades-consensus", params)

    async def stock_grade_news(
        self, symbol: str, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get news about analyst grade changes for a stock symbol

        Endpoint: /grades-news

        Args:
            symbol: Stock symbol (required)
            page: Page number for pagination (default: 0)
            limit: Number of results per page (default: 1)

        Returns:
            List of grade change news articles

        Example:
            >>> grade_news = await client.analyst.stock_grade_news("AAPL", limit=5)
            >>> # Returns: [{"symbol": "AAPL", "newsTitle": "...", "newGrade": "Buy", ...}]
        """
        params = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("grades-news", params)

    async def stock_grade_latest_news(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get latest analyst grade change news for all stock symbols

        Endpoint: /grades-latest-news

        Args:
            page: Page number for pagination (default: 0)
            limit: Number of results per page (default: 10)

        Returns:
            List of latest grade change news across all symbols

        Example:
            >>> latest_grades = await client.analyst.stock_grade_latest_news(limit=20)
            >>> # Returns: [{"symbol": "PYPL", "newsTitle": "...", "newGrade": "Overweight", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("grades-latest-news", params)
