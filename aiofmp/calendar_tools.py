"""
MCP Tools for Calendar Category

This module provides MCP tool definitions for the Calendar category of the FMP API,
including dividends, earnings, IPOs, and stock splits.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_date,
    validate_limit,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_dividends_company(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get dividend information for a specific company.

    This tool retrieves dividend information for a company, including
    dividend amounts, ex-dates, record dates, and payment dates.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 50, 100, 200

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Dividend information for the company
        - message: Optional message about the operation

    Example prompts:
        "What are the dividend payments for Apple (AAPL) stock?"
        "Show me the dividend history for Microsoft with the last 50 records"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.dividends_company(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved dividend information for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_dividends_company: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving dividend information: {str(e)}",
        )


@mcp.tool
async def get_dividends_calendar(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get dividend calendar for all stocks within a date range.

    This tool retrieves dividend calendar information for all stocks
    within a specified date range.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Dividend calendar for all stocks
        - message: Optional message about the operation

    Example prompts:
        "What are the upcoming dividend payments for all stocks in Q1 2025?"
        "Show me the dividend calendar from January 1 to March 31, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.dividends_calendar(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved dividend calendar for {len(results)} stocks",
        )

    except Exception as e:
        logger.error(f"Error in get_dividends_calendar: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving dividend calendar: {str(e)}",
        )


@mcp.tool
async def get_earnings_company(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get earnings information for a specific company.

    This tool retrieves earnings information for a company, including
    earnings dates, estimates, and actual results.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 20, 50, 100

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Earnings information for the company
        - message: Optional message about the operation

    Example prompts:
        "What are the earnings dates and results for Apple (AAPL) stock?"
        "Show me the earnings history for Microsoft with the last 20 quarters"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.earnings_company(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved earnings information for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_earnings_company: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving earnings information: {str(e)}",
        )


@mcp.tool
async def get_earnings_calendar(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get earnings calendar for all companies within a date range.

    This tool retrieves earnings calendar information for all companies
    within a specified date range.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Earnings calendar for all companies
        - message: Optional message about the operation

    Example prompts:
        "What are the upcoming earnings announcements for all companies in Q1 2025?"
        "Show me the earnings calendar from January 1 to March 31, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.earnings_calendar(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved earnings calendar for {len(results)} companies",
        )

    except Exception as e:
        logger.error(f"Error in get_earnings_calendar: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving earnings calendar: {str(e)}",
        )


@mcp.tool
async def get_ipos_calendar(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get IPO calendar for upcoming initial public offerings.

    This tool retrieves IPO calendar information for upcoming
    initial public offerings within a specified date range.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-06-30"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: IPO calendar for upcoming offerings
        - message: Optional message about the operation

    Example prompts:
        "What are the upcoming IPOs in the first half of 2025?"
        "Show me the IPO calendar from January 1 to June 30, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.ipos_calendar(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved IPO calendar for {len(results)} upcoming offerings",
        )

    except Exception as e:
        logger.error(f"Error in get_ipos_calendar: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving IPO calendar: {str(e)}"
        )


@mcp.tool
async def get_stock_splits_company(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get stock split information for a specific company.

    This tool retrieves stock split information for a company, including
    split dates, split ratios, and split factors.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 20, 50, 100

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock split information for the company
        - message: Optional message about the operation

    Example prompts:
        "What are the stock splits for Apple (AAPL) stock?"
        "Show me the stock split history for Microsoft with the last 20 records"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.stock_splits_company(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock split information for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_splits_company: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving stock split information: {str(e)}",
        )


@mcp.tool
async def get_stock_splits_calendar(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get stock splits calendar for all companies within a date range.

    This tool retrieves stock splits calendar information for all companies
    within a specified date range.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-06-30"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock splits calendar for all companies
        - message: Optional message about the operation

    Example prompts:
        "What are the upcoming stock splits in the first half of 2025?"
        "Show me the stock splits calendar from January 1 to June 30, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.stock_splits_calendar(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock splits calendar for {len(results)} companies",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_splits_calendar: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving stock splits calendar: {str(e)}",
        )


@mcp.tool
async def get_ipos_disclosure(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get IPO disclosure filings for upcoming initial public offerings.

    This tool retrieves IPO disclosure filings for upcoming IPOs,
    including regulatory information and filing details.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-06-30"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: IPO disclosure filings data
        - message: Optional message about the operation

    Example prompts:
        "What are the IPO disclosure filings for the first half of 2025?"
        "Show me IPO disclosure filings from January 1 to June 30, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.ipos_disclosure(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved IPO disclosure filings"
        )

    except Exception as e:
        logger.error(f"Error in get_ipos_disclosure: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving IPO disclosure filings: {str(e)}",
        )


@mcp.tool
async def get_ipos_prospectus(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get IPO prospectus information for upcoming initial public offerings.

    This tool retrieves IPO prospectus information for upcoming IPOs,
    including financial details and SEC links.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-06-30"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: IPO prospectus information
        - message: Optional message about the operation

    Example prompts:
        "What are the IPO prospectus details for the first half of 2025?"
        "Show me IPO prospectus information from January 1 to June 30, 2025"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.calendar.ipos_prospectus(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved IPO prospectus information"
        )

    except Exception as e:
        logger.error(f"Error in get_ipos_prospectus: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving IPO prospectus information: {str(e)}",
        )
