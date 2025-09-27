"""
News category for FMP API

This module provides news functionality including FMP articles, general news, press releases,
stock news, crypto news, forex news, and search capabilities across all news types.
"""

from datetime import date
from typing import Any

from .base import FMPBaseClient


class NewsCategory:
    """News category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the news category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def fmp_articles(
        self, page: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get the latest articles from Financial Modeling Prep

        Endpoint: /fmp-articles

        Args:
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)

        Returns:
            List of FMP articles with title, date, content, tickers, image, link, author, and site

        Example:
            >>> data = await client.news.fmp_articles(page=0, limit=20)
            >>> # Returns: [{"title": "Merck Shares Plunge 8%...", "date": "2025-02-04 09:33:00", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("fmp-articles", params)

    async def general_news(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest general news articles from various sources

        Endpoint: /news/general-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for news filtering (optional)
            to_date: End date for news filtering (optional)

        Returns:
            List of general news articles with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.general_news(page=0, limit=20)
            >>> # Returns: [{"symbol": null, "publishedDate": "2025-02-03 23:51:37", "publisher": "CNBC", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/general-latest", params)

    async def press_releases(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest company press releases

        Endpoint: /news/press-releases-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of press releases per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of press releases with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.press_releases(page=0, limit=20)
            >>> # Returns: [{"symbol": "LNW", "publishedDate": "2025-02-03 23:32:00", "publisher": "PRNewsWire", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/press-releases-latest", params)

    async def stock_news(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest stock market news

        Endpoint: /news/stock-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of stock news articles with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.stock_news(page=0, limit=20)
            >>> # Returns: [{"symbol": "INSG", "publishedDate": "2025-02-03 23:53:40", "publisher": "Seeking Alpha", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/stock-latest", params)

    async def crypto_news(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest cryptocurrency news

        Endpoint: /news/crypto-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of crypto news articles with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.crypto_news(page=0, limit=20)
            >>> # Returns: [{"symbol": "BTCUSD", "publishedDate": "2025-02-03 23:32:19", "publisher": "Coingape", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/crypto-latest", params)

    async def forex_news(
        self,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get the latest forex news articles

        Endpoint: /news/forex-latest

        Args:
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of forex news articles with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.forex_news(page=0, limit=20)
            >>> # Returns: [{"symbol": "XAUUSD", "publishedDate": "2025-02-03 23:55:44", "publisher": "FX Street", ...}]
        """
        params = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/forex-latest", params)

    async def search_press_releases(
        self,
        symbols: str,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for company press releases by symbol

        Endpoint: /news/press-releases

        Args:
            symbols: Stock symbol(s) to search for (required)
            page: Page number for pagination (optional)
            limit: Number of press releases per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of press releases for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.search_press_releases("AAPL", page=0, limit=20)
            >>> # Returns: [{"symbol": "AAPL", "publishedDate": "2025-01-30 16:30:00", "publisher": "Business Wire", ...}]
        """
        params = {"symbols": symbols}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/press-releases", params)

    async def search_stock_news(
        self,
        symbols: str,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for stock-related news by symbol

        Endpoint: /news/stock

        Args:
            symbols: Stock symbol(s) to search for (required)
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of stock news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.search_stock_news("AAPL", page=0, limit=20)
            >>> # Returns: [{"symbol": "AAPL", "publishedDate": "2025-02-03 21:05:14", "publisher": "Zacks Investment Research", ...}]
        """
        params = {"symbols": symbols}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/stock", params)

    async def search_crypto_news(
        self,
        symbols: str,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for cryptocurrency news by symbol

        Endpoint: /news/crypto

        Args:
            symbols: Crypto symbol(s) to search for (required)
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of crypto news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.search_crypto_news("BTCUSD", page=0, limit=20)
            >>> # Returns: [{"symbol": "BTCUSD", "publishedDate": "2025-02-03 23:32:19", "publisher": "Coingape", ...}]
        """
        params = {"symbols": symbols}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/crypto", params)

    async def search_forex_news(
        self,
        symbols: str,
        page: int | None = None,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for forex news by currency pair symbol

        Endpoint: /news/forex

        Args:
            symbols: Forex symbol(s) to search for (required)
            page: Page number for pagination (optional)
            limit: Number of articles per page (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of forex news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url

        Example:
            >>> data = await client.news.search_forex_news("EURUSD", page=0, limit=20)
            >>> # Returns: [{"symbol": "EURUSD", "publishedDate": "2025-02-03 18:43:01", "publisher": "FX Street", ...}]
        """
        params = {"symbols": symbols}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if from_date is not None:
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date is not None:
            params["to"] = to_date.strftime("%Y-%m-%d")

        return await self._client._make_request("news/forex", params)
