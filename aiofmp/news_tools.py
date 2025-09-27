"""
MCP Tools for News Category

This module provides MCP tool definitions for the News category of the FMP API,
including FMP articles, general news, and press releases.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_date,
    validate_limit,
    validate_page,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_fmp_articles(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get FMP articles.

    This tool retrieves FMP articles covering market analysis,
    company insights, and financial news.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 20, 50, 100

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: FMP articles data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest FMP articles with 20 records per page?"
        "Show me the most recent FMP market analysis articles"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.fmp_articles(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {len(results)} FMP articles"
        )

    except Exception as e:
        logger.error(f"Error in get_fmp_articles: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving FMP articles: {str(e)}"
        )


@mcp.tool
async def get_stock_news(
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get the latest stock market news.

    This tool retrieves general stock market news and updates
    from various sources with optional date filtering.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock news articles with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the latest stock market news from January 1, 2024?"
        "Show me the most recent stock news with 20 articles per page"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.stock_news(
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} stock news articles",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving stock news: {str(e)}"
        )


@mcp.tool
async def get_general_news(
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get the latest general news articles from various sources.

    This tool retrieves general financial news and market updates
    from various sources with optional date filtering.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for news filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for news filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: General news articles with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the latest general financial news from January 1, 2024?"
        "Show me the most recent general market news with 20 articles per page"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.general_news(
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} general news articles",
        )

    except Exception as e:
        logger.error(f"Error in get_general_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving general news: {str(e)}"
        )


@mcp.tool
async def get_press_releases(
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get the latest company press releases.

    This tool retrieves press releases from companies and organizations
    covering financial announcements and corporate updates with optional date filtering.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of press releases per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Press releases with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What are the latest company press releases from January 1, 2024?"
        "Show me the most recent corporate announcements with 20 releases per page"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.press_releases(
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} press releases",
        )

    except Exception as e:
        logger.error(f"Error in get_press_releases: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving press releases: {str(e)}"
        )


@mcp.tool
async def get_crypto_news(
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get the latest cryptocurrency news.

    This tool retrieves cryptocurrency news and market updates
    from various sources with optional date filtering.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Crypto news articles with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the latest cryptocurrency news from January 1, 2024?"
        "Show me the most recent crypto market updates with 20 articles per page"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.crypto_news(
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} crypto news articles",
        )

    except Exception as e:
        logger.error(f"Error in get_crypto_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving crypto news: {str(e)}"
        )


@mcp.tool
async def get_forex_news(
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get the latest forex news articles.

    This tool retrieves foreign exchange news and market updates
    from various sources with optional date filtering.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Forex news articles with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the latest forex news from January 1, 2024?"
        "Show me the most recent foreign exchange market updates with 20 articles per page"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.forex_news(
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} forex news articles",
        )

    except Exception as e:
        logger.error(f"Error in get_forex_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving forex news: {str(e)}"
        )


@mcp.tool
async def search_press_releases(
    symbols: str,
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Search for company press releases by symbol.

    This tool searches for company press releases by stock symbol(s),
    allowing you to find relevant corporate announcements for specific companies.

    Args:
        symbols: Stock symbol(s) to search for - e.g., "AAPL", "MSFT,GOOGL"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of press releases per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Press releases for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What are the Apple (AAPL) press releases from January 1, 2024?"
        "Show me the latest corporate announcements for Microsoft (MSFT) with 20 releases per page"
    """
    try:
        # Validate inputs
        if not symbols or not isinstance(symbols, str):
            raise ValueError("Symbols must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.search_press_releases(
                symbols=symbols,
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} press releases for {symbols}",
        )

    except Exception as e:
        logger.error(f"Error in search_press_releases: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching press releases: {str(e)}"
        )


@mcp.tool
async def search_stock_news(
    symbols: str,
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Search for stock-related news by symbol.

    This tool searches for stock-related news by stock symbol(s),
    allowing you to find relevant market news and updates for specific companies.

    Args:
        symbols: Stock symbol(s) to search for - e.g., "AAPL", "MSFT,GOOGL"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the Apple (AAPL) stock news from January 1, 2024?"
        "Show me the latest stock market news for Microsoft (MSFT) with 20 articles per page"
    """
    try:
        # Validate inputs
        if not symbols or not isinstance(symbols, str):
            raise ValueError("Symbols must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.search_stock_news(
                symbols=symbols,
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} stock news articles for {symbols}",
        )

    except Exception as e:
        logger.error(f"Error in search_stock_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching stock news: {str(e)}"
        )


@mcp.tool
async def search_crypto_news(
    symbols: str,
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Search for cryptocurrency news by symbol.

    This tool searches for cryptocurrency news by crypto symbol(s),
    allowing you to find relevant crypto market news and updates for specific cryptocurrencies.

    Args:
        symbols: Crypto symbol(s) to search for - e.g., "BTCUSD", "ETHUSD,BTCUSD"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Crypto news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the Bitcoin (BTCUSD) crypto news from January 1, 2024?"
        "Show me the latest cryptocurrency news for Ethereum (ETHUSD) with 20 articles per page"
    """
    try:
        # Validate inputs
        if not symbols or not isinstance(symbols, str):
            raise ValueError("Symbols must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.search_crypto_news(
                symbols=symbols,
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} crypto news articles for {symbols}",
        )

    except Exception as e:
        logger.error(f"Error in search_crypto_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching crypto news: {str(e)}"
        )


@mcp.tool
async def search_forex_news(
    symbols: str,
    page: int | None = None,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Search for forex news by currency pair symbol.

    This tool searches for foreign exchange news by forex symbol(s),
    allowing you to find relevant forex market news and updates for specific currency pairs.

    Args:
        symbols: Forex symbol(s) to search for - e.g., "EURUSD", "GBPUSD,EURUSD"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of articles per page (optional) - e.g., 10, 20, 50
        from_date: Start date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for filtering in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Forex news articles for the specified symbol(s) with symbol, publishedDate, publisher, title, image, site, text, and url
        - message: Optional message about the operation

    Example prompts:
        "What is the EUR/USD forex news from January 1, 2024?"
        "Show me the latest foreign exchange news for GBP/USD with 20 articles per page"
    """
    try:
        # Validate inputs
        if not symbols or not isinstance(symbols, str):
            raise ValueError("Symbols must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.news.search_forex_news(
                symbols=symbols,
                page=validated_page,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} forex news articles for {symbols}",
        )

    except Exception as e:
        logger.error(f"Error in search_forex_news: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching forex news: {str(e)}"
        )
