"""
MCP Tools for Search Category

This module provides MCP tool definitions for the Search category of the FMP API,
including symbol search, company search, and stock screening functionality.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_limit

logger = logging.getLogger(__name__)


@mcp.tool
async def search_symbols(
    query: str, limit: int | None = None, exchange: str | None = None
) -> dict[str, Any]:
    """
    Search for stock symbols by query (symbol or company name).

    This tool searches the Financial Modeling Prep database for stock symbols
    matching the provided query. It can search by both symbol and company name,
    and supports filtering by exchange.

    Args:
        query: Search query (symbol or company name) - e.g., "AAPL", "Apple", "Microsoft"
        limit: Maximum number of results to return (optional) - e.g., 10, 50, 100
        exchange: Exchange to filter by (optional) - e.g., "NASDAQ", "NYSE", "AMEX"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of symbol search results with symbol, name, exchange, etc.
        - message: Optional message about the operation

    Example prompts:
        "Search for Apple (AAPL) symbols on NASDAQ with 10 results"
        "Find all Microsoft-related symbols on NYSE exchange"
    """
    try:
        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        validated_limit = validate_limit(limit)

        # Get FMP client and perform search
        client = get_fmp_client()
        async with client:
            results = await client.search.symbols(
                query=query, limit=validated_limit, exchange=exchange
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Found {len(results)} symbols matching '{query}'",
        )

    except Exception as e:
        logger.error(f"Error in search_symbols: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching symbols: {str(e)}"
        )


@mcp.tool
async def search_companies(
    query: str, limit: int | None = None, exchange: str | None = None
) -> dict[str, Any]:
    """
    Search for companies by name.

    This tool searches the Financial Modeling Prep database for companies
    matching the provided query. It searches by company name and supports
    filtering by exchange.

    Args:
        query: Company name to search for - e.g., "Apple", "Microsoft", "Tesla"
        limit: Maximum number of results to return (optional) - e.g., 10, 50, 100
        exchange: Exchange to filter by (optional) - e.g., "NASDAQ", "NYSE", "AMEX"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of company search results with company details
        - message: Optional message about the operation

    Example prompts:
        "Search for Apple companies on NASDAQ with 5 results"
        "Find all Tesla-related companies on NYSE exchange"
    """
    try:
        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        validated_limit = validate_limit(limit)

        # Get FMP client and perform search
        client = get_fmp_client()
        async with client:
            results = await client.search.companies(
                query=query, limit=validated_limit, exchange=exchange
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Found {len(results)} companies matching '{query}'",
        )

    except Exception as e:
        logger.error(f"Error in search_companies: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error searching companies: {str(e)}"
        )


@mcp.tool
async def screen_stocks(
    sector: str | None = None,
    industry: str | None = None,
    market_cap_more_than: float | None = None,
    market_cap_lower_than: float | None = None,
    price_more_than: float | None = None,
    price_lower_than: float | None = None,
    volume_more_than: int | None = None,
    volume_lower_than: int | None = None,
    beta_more_than: float | None = None,
    beta_lower_than: float | None = None,
    dividend_more_than: float | None = None,
    dividend_lower_than: float | None = None,
    exchange: str | None = None,
    country: str | None = None,
    is_etf: bool | None = None,
    is_fund: bool | None = None,
    is_actively_trading: bool | None = None,
    limit: int | None = None,
    include_all_share_classes: bool | None = None,
) -> dict[str, Any]:
    """
    Screen stocks based on various criteria.

    This tool provides comprehensive stock screening capabilities using multiple
    financial and market criteria. It allows filtering by sector, industry,
    market cap, price, volume, beta, dividends, exchange, country, and more.

    Args:
        sector: Industry sector to filter by - e.g., "Technology", "Healthcare", "Financial"
        industry: Specific industry to filter by - e.g., "Software", "Biotechnology"
        market_cap_more_than: Minimum market capitalization - e.g., 1000000000 (1B)
        market_cap_lower_than: Maximum market capitalization - e.g., 10000000000 (10B)
        price_more_than: Minimum stock price - e.g., 10.0, 50.0
        price_lower_than: Maximum stock price - e.g., 100.0, 500.0
        volume_more_than: Minimum trading volume - e.g., 1000000
        volume_lower_than: Maximum trading volume - e.g., 10000000
        beta_more_than: Minimum beta value - e.g., 0.5, 1.0
        beta_lower_than: Maximum beta value - e.g., 1.5, 2.0
        dividend_more_than: Minimum dividend yield - e.g., 0.02 (2%)
        dividend_lower_than: Maximum dividend yield - e.g., 0.05 (5%)
        exchange: Exchange to filter by - e.g., "NASDAQ", "NYSE", "AMEX"
        country: Country to filter by - e.g., "US", "CA", "GB"
        is_etf: Filter for ETFs only - e.g., True, False
        is_fund: Filter for mutual funds only - e.g., True, False
        is_actively_trading: Filter for actively trading securities - e.g., True, False
        limit: Maximum number of results to return - e.g., 100, 500, 1000
        include_all_share_classes: Include all share classes - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of stocks matching the screening criteria
        - message: Optional message about the operation

    Example prompts:
        "Screen for technology stocks with market cap over $1 billion"
        "Find healthcare stocks with dividend yield between 2% and 5% on NASDAQ"
    """
    try:
        # Validate inputs
        validated_limit = validate_limit(limit)

        # Get FMP client and perform screening
        client = get_fmp_client()
        async with client:
            results = await client.search.screener(
                market_cap_more_than=market_cap_more_than,
                market_cap_lower_than=market_cap_lower_than,
                sector=sector,
                industry=industry,
                beta_more_than=beta_more_than,
                beta_lower_than=beta_lower_than,
                price_more_than=price_more_than,
                price_lower_than=price_lower_than,
                dividend_more_than=dividend_more_than,
                dividend_lower_than=dividend_lower_than,
                volume_more_than=volume_more_than,
                volume_lower_than=volume_lower_than,
                exchange=exchange,
                country=country,
                is_etf=is_etf,
                is_fund=is_fund,
                is_actively_trading=is_actively_trading,
                limit=validated_limit,
                include_all_share_classes=include_all_share_classes,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Found {len(results)} stocks matching screening criteria",
        )

    except Exception as e:
        logger.error(f"Error in screen_stocks: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error screening stocks: {str(e)}"
        )
