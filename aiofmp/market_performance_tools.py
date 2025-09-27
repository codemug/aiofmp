"""
MCP Tools for Market Performance Category

This module provides MCP tool definitions for the Market Performance category of the FMP API,
including sector performance, market movers, and P/E ratios.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date

logger = logging.getLogger(__name__)


@mcp.tool
async def get_sector_performance_snapshot(
    snapshot_date: str, exchange: str | None = None, sector: str | None = None
) -> dict[str, Any]:
    """
    Get a snapshot of sector performance.

    This tool retrieves sector performance data for a specific date,
    including performance metrics and sector rankings.

    Args:
        snapshot_date: Date for the performance snapshot in YYYY-MM-DD format - e.g., "2025-01-15"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"
        sector: Specific sector to filter (optional) - e.g., "Technology", "Healthcare"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Sector performance data with date, sector, exchange, and average change
        - message: Optional message about the operation

    Example prompts:
        "What is the sector performance snapshot for January 15, 2025 on NASDAQ?"
        "Show me the sector performance data for Technology sector on NYSE"
    """
    try:
        # Validate inputs
        validated_date = validate_date(snapshot_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.sector_performance_snapshot(
                snapshot_date=validated_date, exchange=exchange, sector=sector
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved sector performance snapshot for {validated_date}",
        )

    except Exception as e:
        logger.error(f"Error in get_sector_performance_snapshot: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving sector performance snapshot: {str(e)}",
        )


@mcp.tool
async def get_biggest_gainers() -> dict[str, Any]:
    """
    Get biggest gainers in the market.

    This tool retrieves the biggest gainers in the market,
    including price changes and volume information.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Biggest gainers data
        - message: Optional message about the operation

    Example prompts:
        "What are the biggest gainers in the market today?"
        "Show me the stocks with the highest percentage gains"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.biggest_gainers()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} biggest gainers",
        )

    except Exception as e:
        logger.error(f"Error in get_biggest_gainers: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving biggest gainers: {str(e)}",
        )


@mcp.tool
async def get_biggest_losers() -> dict[str, Any]:
    """
    Get biggest losers in the market.

    This tool retrieves the biggest losers in the market,
    including price changes and volume information.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Biggest losers data
        - message: Optional message about the operation

    Example prompts:
        "What are the biggest losers in the market today?"
        "Show me the stocks with the highest percentage losses"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.biggest_losers()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} biggest losers",
        )

    except Exception as e:
        logger.error(f"Error in get_biggest_losers: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving biggest losers: {str(e)}"
        )


@mcp.tool
async def get_most_active_stocks() -> dict[str, Any]:
    """
    Get the most actively traded stocks.

    This tool retrieves the most actively traded stocks in the market,
    including volume and price information.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Most active stocks with symbol, price, name, change, and percentage change
        - message: Optional message about the operation

    Example prompts:
        "What are the most actively traded stocks today?"
        "Show me the stocks with the highest trading volume"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.most_active_stocks()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} most active stocks",
        )

    except Exception as e:
        logger.error(f"Error in get_most_active_stocks: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving most active stocks: {str(e)}",
        )


@mcp.tool
async def get_industry_performance_snapshot(
    snapshot_date: str, exchange: str | None = None, industry: str | None = None
) -> dict[str, Any]:
    """
    Get a snapshot of industry performance.

    This tool retrieves industry performance data for a specific date,
    including performance metrics and industry rankings.

    Args:
        snapshot_date: Date for the performance snapshot in YYYY-MM-DD format - e.g., "2025-01-15"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"
        industry: Specific industry to filter (optional) - e.g., "Biotechnology", "Advertising Agencies"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Industry performance data with date, industry, exchange, and average change
        - message: Optional message about the operation

    Example prompts:
        "What is the industry performance snapshot for January 15, 2025 on NASDAQ?"
        "Show me the Biotechnology industry performance on NYSE"
    """
    try:
        # Validate inputs
        validated_date = validate_date(snapshot_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.industry_performance_snapshot(
                snapshot_date=validated_date, exchange=exchange, industry=industry
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved industry performance snapshot for {validated_date}",
        )

    except Exception as e:
        logger.error(f"Error in get_industry_performance_snapshot: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving industry performance snapshot: {str(e)}",
        )


@mcp.tool
async def get_historical_sector_performance(
    sector: str,
    from_date: str | None = None,
    to_date: str | None = None,
    exchange: str | None = None,
) -> dict[str, Any]:
    """
    Get historical sector performance data.

    This tool retrieves historical sector performance data over a specified date range,
    including performance metrics and sector rankings.

    Args:
        sector: Sector name - e.g., "Energy", "Technology", "Healthcare"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical sector performance data with date, sector, exchange, and average change
        - message: Optional message about the operation

    Example prompts:
        "What is the historical Energy sector performance from January to December 2024?"
        "Show me the Technology sector performance over the past 6 months"
    """
    try:
        # Validate inputs
        if not sector or not isinstance(sector, str):
            raise ValueError("Sector must be a non-empty string")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.historical_sector_performance(
                sector=sector,
                from_date=validated_from_date,
                to_date=validated_to_date,
                exchange=exchange,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical sector performance for {sector}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_sector_performance: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical sector performance: {str(e)}",
        )


@mcp.tool
async def get_historical_industry_performance(
    industry: str,
    from_date: str | None = None,
    to_date: str | None = None,
    exchange: str | None = None,
) -> dict[str, Any]:
    """
    Get historical industry performance data.

    This tool retrieves historical industry performance data over a specified date range,
    including performance metrics and industry rankings.

    Args:
        industry: Industry name - e.g., "Biotechnology", "Advertising Agencies", "Software"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical industry performance data with date, industry, exchange, and average change
        - message: Optional message about the operation

    Example prompts:
        "What is the historical Biotechnology industry performance from January to December 2024?"
        "Show me the Software industry performance over the past year"
    """
    try:
        # Validate inputs
        if not industry or not isinstance(industry, str):
            raise ValueError("Industry must be a non-empty string")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.historical_industry_performance(
                industry=industry,
                from_date=validated_from_date,
                to_date=validated_to_date,
                exchange=exchange,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical industry performance for {industry}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_industry_performance: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical industry performance: {str(e)}",
        )


@mcp.tool
async def get_sector_pe_snapshot(
    snapshot_date: str, exchange: str | None = None, sector: str | None = None
) -> dict[str, Any]:
    """
    Get price-to-earnings (P/E) ratios for various sectors.

    This tool retrieves P/E ratios for different sectors on a specific date,
    providing valuation insights across sectors.

    Args:
        snapshot_date: Date for the P/E snapshot in YYYY-MM-DD format - e.g., "2025-01-15"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"
        sector: Specific sector to filter (optional) - e.g., "Technology", "Healthcare"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Sector P/E data with date, sector, exchange, and P/E ratio
        - message: Optional message about the operation

    Example prompts:
        "What are the sector P/E ratios for January 15, 2025 on NASDAQ?"
        "Show me the Technology sector P/E ratios on NYSE"
    """
    try:
        # Validate inputs
        validated_date = validate_date(snapshot_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.sector_pe_snapshot(
                snapshot_date=validated_date, exchange=exchange, sector=sector
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved sector P/E snapshot for {validated_date}",
        )

    except Exception as e:
        logger.error(f"Error in get_sector_pe_snapshot: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving sector P/E snapshot: {str(e)}",
        )


@mcp.tool
async def get_industry_pe_snapshot(
    snapshot_date: str, exchange: str | None = None, industry: str | None = None
) -> dict[str, Any]:
    """
    Get price-to-earnings (P/E) ratios for different industries.

    This tool retrieves P/E ratios for different industries on a specific date,
    providing valuation insights across industries.

    Args:
        snapshot_date: Date for the P/E snapshot in YYYY-MM-DD format - e.g., "2025-01-15"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"
        industry: Specific industry to filter (optional) - e.g., "Biotechnology", "Advertising Agencies"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Industry P/E data with date, industry, exchange, and P/E ratio
        - message: Optional message about the operation

    Example prompts:
        "What are the industry P/E ratios for January 15, 2025 on NASDAQ?"
        "Show me the Biotechnology industry P/E ratios on NYSE"
    """
    try:
        # Validate inputs
        validated_date = validate_date(snapshot_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.industry_pe_snapshot(
                snapshot_date=validated_date, exchange=exchange, industry=industry
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved industry P/E snapshot for {validated_date}",
        )

    except Exception as e:
        logger.error(f"Error in get_industry_pe_snapshot: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving industry P/E snapshot: {str(e)}",
        )


@mcp.tool
async def get_historical_sector_pe(
    sector: str,
    from_date: str | None = None,
    to_date: str | None = None,
    exchange: str | None = None,
) -> dict[str, Any]:
    """
    Get historical price-to-earnings (P/E) ratios for various sectors.

    This tool retrieves historical P/E ratios for different sectors over a specified date range,
    providing valuation insights across sectors over time.

    Args:
        sector: Sector name - e.g., "Energy", "Technology", "Healthcare"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical sector P/E data with date, sector, exchange, and P/E ratio
        - message: Optional message about the operation

    Example prompts:
        "What are the historical Energy sector P/E ratios from January to December 2024?"
        "Show me the Technology sector P/E ratios over the past 6 months"
    """
    try:
        # Validate inputs
        if not sector or not isinstance(sector, str):
            raise ValueError("Sector must be a non-empty string")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.historical_sector_pe(
                sector=sector,
                from_date=validated_from_date,
                to_date=validated_to_date,
                exchange=exchange,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical sector P/E for {sector}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_sector_pe: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical sector P/E: {str(e)}",
        )


@mcp.tool
async def get_historical_industry_pe(
    industry: str,
    from_date: str | None = None,
    to_date: str | None = None,
    exchange: str | None = None,
) -> dict[str, Any]:
    """
    Get historical price-to-earnings (P/E) ratios by industry.

    This tool retrieves historical P/E ratios for different industries over a specified date range,
    providing valuation insights across industries over time.

    Args:
        industry: Industry name - e.g., "Biotechnology", "Advertising Agencies", "Software"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"
        exchange: Stock exchange (optional) - e.g., "NASDAQ", "NYSE"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical industry P/E data with date, industry, exchange, and P/E ratio
        - message: Optional message about the operation

    Example prompts:
        "What are the historical Biotechnology industry P/E ratios from January to December 2024?"
        "Show me the Software industry P/E ratios over the past year"
    """
    try:
        # Validate inputs
        if not industry or not isinstance(industry, str):
            raise ValueError("Industry must be a non-empty string")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.market_performance.historical_industry_pe(
                industry=industry,
                from_date=validated_from_date,
                to_date=validated_to_date,
                exchange=exchange,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical industry P/E for {industry}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_industry_pe: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical industry P/E: {str(e)}",
        )
