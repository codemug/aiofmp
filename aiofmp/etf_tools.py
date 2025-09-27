"""
MCP Tools for ETF and Mutual Funds Category

This module provides MCP tool definitions for the ETF category of the FMP API,
including holdings, fund information, and allocations.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_etf_holdings(symbol: str) -> dict[str, Any]:
    """
    Get ETF holdings breakdown.

    This tool retrieves holdings breakdown for an ETF,
    including individual holdings and their weights.

    Args:
        symbol: ETF symbol - e.g., "SPY", "QQQ", "VTI"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: ETF holdings data
        - message: Optional message about the operation

    Example prompts:
        "What are the holdings of the SPY ETF?"
        "Show me the holdings breakdown for the QQQ ETF"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.holdings(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved ETF holdings for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_holdings: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving ETF holdings: {str(e)}"
        )


@mcp.tool
async def get_etf_info(symbol: str) -> dict[str, Any]:
    """
    Get ETF fund information.

    This tool retrieves fund information for an ETF,
    including fund details, performance, and characteristics.

    Args:
        symbol: ETF symbol - e.g., "SPY", "QQQ", "VTI"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: ETF fund information
        - message: Optional message about the operation

    Example prompts:
        "What is the fund information for SPY?"
        "Show me the details and performance of the VTI ETF"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.info(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved ETF info for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_info: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving ETF info: {str(e)}"
        )


@mcp.tool
async def get_etf_country_weightings(symbol: str) -> dict[str, Any]:
    """
    Get ETF country weightings breakdown.

    This tool retrieves country weightings for an ETF,
    showing the geographic allocation of the fund.

    Args:
        symbol: ETF symbol - e.g., "SPY", "QQQ", "VTI"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: ETF country weightings data
        - message: Optional message about the operation

    Example prompts:
        "What are the country weightings for SPY?"
        "Show me the geographic allocation of the VTI ETF"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.country_weightings(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved country weightings for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_country_weightings: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving country weightings: {str(e)}",
        )


@mcp.tool
async def get_etf_asset_exposure(symbol: str) -> dict[str, Any]:
    """
    Discover which ETFs hold a specific stock.

    This tool finds which ETFs and mutual funds hold
    the specified stock symbol, showing exposure details.

    Args:
        symbol: Stock symbol to find ETF exposure - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: ETF exposure data showing which ETFs hold the stock
        - message: Optional message about the operation

    Example prompts:
        "Which ETFs hold Apple (AAPL) stock?"
        "Show me the ETF exposure for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.asset_exposure(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved asset exposure for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_asset_exposure: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving asset exposure: {str(e)}"
        )


@mcp.tool
async def get_etf_sector_weightings(symbol: str) -> dict[str, Any]:
    """
    Get ETF sector weightings breakdown.

    This tool retrieves sector weightings for an ETF,
    showing the sector allocation of the fund.

    Args:
        symbol: ETF symbol - e.g., "SPY", "QQQ", "VTI"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: ETF sector weightings data
        - message: Optional message about the operation

    Example prompts:
        "What are the sector weightings for SPY?"
        "Show me the sector allocation of the QQQ ETF"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.sector_weightings(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved sector weightings for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_sector_weightings: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving sector weightings: {str(e)}",
        )


@mcp.tool
async def get_etf_disclosure_holders_latest(symbol: str) -> dict[str, Any]:
    """
    Get latest mutual fund and ETF disclosure holders for a stock.

    This tool retrieves the latest disclosure data showing
    which mutual funds and ETFs hold the specified stock.

    Args:
        symbol: Stock symbol to find disclosure holders - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest disclosure data for mutual funds and ETFs holding the stock
        - message: Optional message about the operation

    Example prompts:
        "Which mutual funds and ETFs hold Apple (AAPL) stock?"
        "Show me the latest disclosure holders for Google (GOOGL)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.etf.disclosure_holders_latest(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved disclosure holders for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_etf_disclosure_holders_latest: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving disclosure holders: {str(e)}",
        )
