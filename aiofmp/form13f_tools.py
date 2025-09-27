"""
MCP Tools for Form 13F Category

This module provides MCP tool definitions for the Form 13F category of the FMP API,
including institutional ownership filings and analytics.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_limit, validate_page

logger = logging.getLogger(__name__)


@mcp.tool
async def get_latest_filings(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest Form 13F filings.

    This tool retrieves the latest Form 13F filings from institutional investors,
    including filing details and holdings information.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest Form 13F filings data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest Form 13F filings with 100 records per page?"
        "Show me the most recent institutional investor filings"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.latest_filings(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved latest Form 13F filings"
        )

    except Exception as e:
        logger.error(f"Error in get_latest_filings: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving latest filings: {str(e)}"
        )


@mcp.tool
async def get_filings_extract(cik: str, year: str, quarter: str) -> dict[str, Any]:
    """
    Extract detailed data from SEC filings for a specific institutional investor.

    This tool extracts detailed data from SEC filings for a specific institutional investor
    identified by their CIK (Central Index Key) for a specific year and quarter.

    Args:
        cik: Central Index Key (CIK) of the institutional investor - e.g., "0001388838"
        year: Year of the filing - e.g., "2023", "2024"
        quarter: Quarter of the filing - e.g., "1", "2", "3", "4"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Detailed filing data with security information, shares, and values
        - message: Optional message about the operation

    Example prompts:
        "What are the detailed filings for CIK 0001388838 in Q3 2023?"
        "Show me the SEC filing extract for institutional investor 0001067983 in Q2 2024"
    """
    try:
        # Validate inputs
        if not cik or not isinstance(cik, str):
            raise ValueError("CIK must be a non-empty string")

        if not year or not isinstance(year, str):
            raise ValueError("Year must be a non-empty string")

        if not quarter or not isinstance(quarter, str):
            raise ValueError("Quarter must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.filings_extract(
                cik=cik, year=year, quarter=quarter
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved Form 13F filings extract for CIK {cik} Q{quarter} {year}",
        )

    except Exception as e:
        logger.error(f"Error in get_filings_extract: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving filings extract: {str(e)}",
        )


@mcp.tool
async def get_filings_dates(
    cik: str, page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get Form 13F filing dates for a specific CIK.

    This tool retrieves filing dates for Form 13F filings for a specific
    institutional investor identified by their CIK.

    Args:
        cik: Central Index Key (CIK) of the institutional investor - e.g., "0001067983"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Form 13F filing dates data
        - message: Optional message about the operation

    Example prompts:
        "What are the filing dates for CIK 0001067983?"
        "Show me the Form 13F filing history for institutional investor 0001388838"
    """
    try:
        # Validate inputs
        if not cik or not isinstance(cik, str):
            raise ValueError("CIK must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.filings_dates(
                cik=cik, page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved Form 13F filing dates for CIK {cik}",
        )

    except Exception as e:
        logger.error(f"Error in get_filings_dates: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving filing dates: {str(e)}"
        )


@mcp.tool
async def get_filings_extract_analytics_by_holder(
    symbol: str,
    year: str,
    quarter: str,
    page: int | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """
    Get analytical breakdown of institutional filings by holder for a specific stock.

    This tool retrieves analytical breakdown of institutional filings by holder
    for a specific stock, including performance metrics and changes.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        year: Year of the filing - e.g., "2023", "2024"
        quarter: Quarter of the filing - e.g., "1", "2", "3", "4"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Institutional holder analytics data
        - message: Optional message about the operation

    Example prompts:
        "What are the institutional holder analytics for Apple (AAPL) in Q3 2023?"
        "Show me the institutional investor breakdown for Microsoft (MSFT) in Q2 2024"
    """
    try:
        # Validate inputs
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")

        if not year or not isinstance(year, str):
            raise ValueError("Year must be a non-empty string")

        if not quarter or not isinstance(quarter, str):
            raise ValueError("Quarter must be a non-empty string")

        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.filings_extract_analytics_by_holder(
                symbol=symbol,
                year=year,
                quarter=quarter,
                page=validated_page,
                limit=validated_limit,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved institutional holder analytics for {symbol} Q{quarter} {year}",
        )

    except Exception as e:
        logger.error(f"Error in get_filings_extract_analytics_by_holder: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving institutional holder analytics: {str(e)}",
        )


@mcp.tool
async def get_holder_performance_summary(
    cik: str, page: int | None = None
) -> dict[str, Any]:
    """
    Get performance summary for institutional investors based on their stock holdings.

    This tool retrieves performance summary for institutional investors
    based on their stock holdings and investment performance.

    Args:
        cik: Central Index Key (CIK) of the institutional investor - e.g., "0001067983"
        page: Page number for pagination (optional) - e.g., 0, 1, 2

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Holder performance summary data
        - message: Optional message about the operation

    Example prompts:
        "What is the performance summary for CIK 0001067983?"
        "Show me the investment performance for institutional investor 0001388838"
    """
    try:
        # Validate inputs
        if not cik or not isinstance(cik, str):
            raise ValueError("CIK must be a non-empty string")

        validated_page = validate_page(page)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.holder_performance_summary(
                cik=cik, page=validated_page
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved holder performance summary for CIK {cik}",
        )

    except Exception as e:
        logger.error(f"Error in get_holder_performance_summary: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving holder performance summary: {str(e)}",
        )


@mcp.tool
async def get_holder_industry_breakdown(
    cik: str, year: str, quarter: str
) -> dict[str, Any]:
    """
    Get industry breakdown of institutional holdings for a specific investor.

    This tool retrieves industry breakdown of institutional holdings for a specific
    investor, showing industry allocations with weights, performance, and changes.

    Args:
        cik: Central Index Key (CIK) of the institutional investor - e.g., "0001067983"
        year: Year of the filing - e.g., "2023", "2024"
        quarter: Quarter of the filing - e.g., "1", "2", "3", "4"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Industry allocations with weights, performance, and changes
        - message: Optional message about the operation

    Example prompts:
        "What is the industry breakdown for CIK 0001067983 in Q3 2023?"
        "Show me the industry allocation for institutional investor 0001388838 in Q2 2024"
    """
    try:
        # Validate inputs
        if not cik or not isinstance(cik, str):
            raise ValueError("CIK must be a non-empty string")

        if not year or not isinstance(year, str):
            raise ValueError("Year must be a non-empty string")

        if not quarter or not isinstance(quarter, str):
            raise ValueError("Quarter must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.holder_industry_breakdown(
                cik=cik, year=year, quarter=quarter
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved holder industry breakdown for CIK {cik} Q{quarter} {year}",
        )

    except Exception as e:
        logger.error(f"Error in get_holder_industry_breakdown: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving holder industry breakdown: {str(e)}",
        )


@mcp.tool
async def get_symbol_positions_summary(
    symbol: str, year: str, quarter: str
) -> dict[str, Any]:
    """
    Get comprehensive snapshot of institutional holdings for a specific stock symbol.

    This tool retrieves comprehensive snapshot of institutional holdings for a specific
    stock symbol, showing position summaries with investor counts, shares, values, and changes.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        year: Year of the filing - e.g., "2023", "2024"
        quarter: Quarter of the filing - e.g., "1", "2", "3", "4"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Position summaries with investor counts, shares, values, and changes
        - message: Optional message about the operation

    Example prompts:
        "What is the positions summary for Apple (AAPL) in Q3 2023?"
        "Show me the institutional holdings summary for Google (GOOGL) in Q2 2024"
    """
    try:
        # Validate inputs
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string")

        if not year or not isinstance(year, str):
            raise ValueError("Year must be a non-empty string")

        if not quarter or not isinstance(quarter, str):
            raise ValueError("Quarter must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.symbol_positions_summary(
                symbol=symbol, year=year, quarter=quarter
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved symbol positions summary for {symbol} Q{quarter} {year}",
        )

    except Exception as e:
        logger.error(f"Error in get_symbol_positions_summary: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving symbol positions summary: {str(e)}",
        )


@mcp.tool
async def get_industry_performance_summary(year: str, quarter: str) -> dict[str, Any]:
    """
    Get overview of how various industries are performing financially.

    This tool retrieves overview of how various industries are performing financially,
    showing industry performance data with values and dates.

    Args:
        year: Year of the filing - e.g., "2023", "2024"
        quarter: Quarter of the filing - e.g., "1", "2", "3", "4"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Industry performance data with values and dates
        - message: Optional message about the operation

    Example prompts:
        "What is the industry performance summary for Q3 2023?"
        "Show me how different industries are performing in Q2 2024"
    """
    try:
        # Validate inputs
        if not year or not isinstance(year, str):
            raise ValueError("Year must be a non-empty string")

        if not quarter or not isinstance(quarter, str):
            raise ValueError("Quarter must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.form13f.industry_performance_summary(
                year=year, quarter=quarter
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved industry performance summary for Q{quarter} {year}",
        )

    except Exception as e:
        logger.error(f"Error in get_industry_performance_summary: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving industry performance summary: {str(e)}",
        )
