"""
MCP Tools for Analyst Category

This module provides MCP tool definitions for the Analyst category of the FMP API,
including financial estimates, ratings, price targets, and stock grades.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_limit,
    validate_page,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_financial_estimates(
    symbol: str, period: str, page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get analyst financial estimates for a stock symbol.

    This tool retrieves analyst financial estimates for a company,
    including revenue, earnings, and other financial projections.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period: Period for estimates - e.g., "annual", "quarter"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 10, 20, 50

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Financial estimates data
        - message: Optional message about the operation

    Example prompts:
        "What are the analyst financial estimates for Apple (AAPL) for the annual period?"
        "Get me the quarterly financial estimates for Microsoft with a limit of 20 results"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        if not period or not isinstance(period, str):
            raise ValueError("Period must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.financial_estimates(
                symbol=validated_symbol,
                period=period,
                page=validated_page,
                limit=validated_limit,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved financial estimates for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_financial_estimates: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving financial estimates: {str(e)}",
        )


@mcp.tool
async def get_ratings_snapshot(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get current financial ratings snapshot for a stock symbol.

    This tool retrieves current analyst ratings for a company,
    including buy, hold, sell recommendations.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Current ratings data
        - message: Optional message about the operation

    Example prompts:
        "What are the current analyst ratings for Apple (AAPL)?"
        "Show me the latest analyst ratings for Tesla with the top 10 results"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.ratings_snapshot(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved ratings snapshot for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_ratings_snapshot: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving ratings snapshot: {str(e)}",
        )


@mcp.tool
async def get_price_target_consensus(symbol: str) -> dict[str, Any]:
    """
    Get price target consensus from analysts for a stock symbol.

    This tool retrieves analyst price target consensus for a company,
    including average, high, and low price targets.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Price target consensus data
        - message: Optional message about the operation

    Example prompts:
        "What is the analyst price target consensus for Apple (AAPL)?"
        "Show me the price target consensus for Microsoft stock"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.price_target_consensus(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved price target consensus for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_price_target_consensus: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving price target consensus: {str(e)}",
        )


@mcp.tool
async def get_stock_grades(symbol: str) -> dict[str, Any]:
    """
    Get latest stock grades from analysts for a stock symbol.

    This tool retrieves latest analyst stock grades for a company,
    including letter grades and recommendations.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock grades data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest analyst stock grades for Apple (AAPL)?"
        "Show me the current stock grades for Tesla from analysts"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.stock_grades(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock grades for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_grades: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving stock grades: {str(e)}"
        )


@mcp.tool
async def get_historical_ratings(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get historical financial ratings for a stock symbol.

    This tool retrieves historical analyst ratings for a company,
    showing how ratings have changed over time.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of historical ratings to return (optional) - e.g., 10, 20, 50

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical ratings data
        - message: Optional message about the operation

    Example prompts:
        "What are the historical analyst ratings for Apple (AAPL) over the last 10 periods?"
        "Show me the historical ratings trend for Microsoft stock"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.historical_ratings(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical ratings for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_ratings: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical ratings: {str(e)}",
        )


@mcp.tool
async def get_price_target_summary(symbol: str) -> dict[str, Any]:
    """
    Get price target summary from analysts for a stock symbol.

    This tool retrieves analyst price target summary for a company,
    including different timeframes and consensus data.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Price target summary data
        - message: Optional message about the operation

    Example prompts:
        "What is the analyst price target summary for Apple (AAPL)?"
        "Show me the price target summary for Tesla stock"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.price_target_summary(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved price target summary for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_price_target_summary: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving price target summary: {str(e)}",
        )


@mcp.tool
async def get_price_target_news(
    symbol: str, page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get news about analyst price targets for a stock symbol.

    This tool retrieves news articles about analyst price targets
    for a company, including analyst insights and updates.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Price target news data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest analyst price target news for Apple (AAPL)?"
        "Show me price target news for Microsoft with 10 results"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.price_target_news(
                symbol=validated_symbol, page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved price target news for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_price_target_news: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving price target news: {str(e)}",
        )


@mcp.tool
async def get_price_target_latest_news(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest analyst price target news for all stock symbols.

    This tool retrieves the latest news articles about analyst
    price targets across all companies in the database.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 10, 20, 50

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest price target news data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest analyst price target news across all stocks?"
        "Show me the most recent price target news with 20 results"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.price_target_latest_news(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved latest price target news"
        )

    except Exception as e:
        logger.error(f"Error in get_price_target_latest_news: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest price target news: {str(e)}",
        )


@mcp.tool
async def get_historical_stock_grades(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get historical analyst grades for a stock symbol.

    This tool retrieves historical analyst stock grades for a company,
    showing how grades have changed over time.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of historical grades to return (optional) - e.g., 10, 20, 50

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical stock grades data
        - message: Optional message about the operation

    Example prompts:
        "What are the historical analyst stock grades for Apple (AAPL) over the last 50 periods?"
        "Show me the historical grade trends for Microsoft stock"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.historical_stock_grades(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical stock grades for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_stock_grades: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical stock grades: {str(e)}",
        )


@mcp.tool
async def get_stock_grades_summary(symbol: str) -> dict[str, Any]:
    """
    Get summary of analyst grades consensus for a stock symbol.

    This tool retrieves a summary of analyst grades consensus for a company,
    including buy, hold, sell breakdowns and consensus rating.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock grades summary data
        - message: Optional message about the operation

    Example prompts:
        "What is the analyst stock grades summary for Apple (AAPL)?"
        "Show me the grades consensus summary for Tesla stock"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.stock_grades_summary(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock grades summary for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_grades_summary: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving stock grades summary: {str(e)}",
        )


@mcp.tool
async def get_stock_grade_news(
    symbol: str, page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get news about analyst grade changes for a stock symbol.

    This tool retrieves news articles about analyst grade changes
    for a company, including upgrades and downgrades.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock grade news data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest analyst stock grade news for Apple (AAPL)?"
        "Show me grade change news for Microsoft with 10 results"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.stock_grade_news(
                symbol=validated_symbol, page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock grade news for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_grade_news: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving stock grade news: {str(e)}",
        )


@mcp.tool
async def get_stock_grade_latest_news(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest analyst grade change news for all stock symbols.

    This tool retrieves the latest news articles about analyst
    grade changes across all companies in the database.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 10, 20, 50

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest stock grade news data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest analyst stock grade news across all stocks?"
        "Show me the most recent grade change news with 20 results"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.analyst.stock_grade_latest_news(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved latest stock grade news"
        )

    except Exception as e:
        logger.error(f"Error in get_stock_grade_latest_news: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest stock grade news: {str(e)}",
        )
