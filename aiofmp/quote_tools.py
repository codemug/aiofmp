"""
MCP Tools for Quote Category

This module provides MCP tool definitions for the Quote category of the FMP API,
including real-time stock quotes and price changes.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_stock_quote(symbol: str) -> dict[str, Any]:
    """
    Get real-time stock quote for a specific symbol.

    This tool retrieves real-time stock quote data including current price,
    change percentage, volume, market cap, highs/lows, and trading averages.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Stock quote data with symbol, name, price, changePercentage, volume, marketCap, etc.
        - message: Optional message about the operation

    Example prompts:
        "What is the current stock quote for Apple (AAPL)?"
        "Show me the real-time price and market data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.quote.stock_quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved stock quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_quote: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving stock quote: {str(e)}"
        )


@mcp.tool
async def get_stock_price_change(symbol: str) -> dict[str, Any]:
    """
    Get stock price change data across various time periods.

    This tool retrieves price change data for a stock symbol across multiple
    time periods including 1D, 5D, 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, 10Y, and max.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Price change data with percentage changes across multiple time periods
        - message: Optional message about the operation

    Example prompts:
        "What are the price changes for Apple (AAPL) across different time periods?"
        "Show me the percentage changes for Microsoft (MSFT) over 1D, 1M, 1Y, and 5Y"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.quote.stock_price_change(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved price change for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_stock_price_change: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving price change: {str(e)}"
        )


@mcp.tool
async def get_aftermarket_trade(symbol: str) -> dict[str, Any]:
    """
    Get aftermarket trade data for a specific symbol.

    This tool retrieves aftermarket trade data for a stock symbol,
    including trades executed after regular market hours with price,
    trade size, and timestamp information.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of aftermarket trades with price, tradeSize, and timestamp
        - message: Optional message about the operation

    Example prompts:
        "What are the aftermarket trades for Apple (AAPL)?"
        "Show me the recent aftermarket trading activity for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.quote.aftermarket_trade(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved aftermarket trade data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_aftermarket_trade: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving aftermarket trade data: {str(e)}",
        )


@mcp.tool
async def get_aftermarket_quote(symbol: str) -> dict[str, Any]:
    """
    Get aftermarket quote data for a specific symbol.

    This tool retrieves aftermarket quote data for a stock symbol,
    including bid/ask prices, sizes, volume, and timestamp information
    after regular market hours.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Aftermarket quote data with bidSize, bidPrice, askSize, askPrice, etc.
        - message: Optional message about the operation

    Example prompts:
        "What is the aftermarket quote for Apple (AAPL)?"
        "Show me the aftermarket bid/ask prices for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.quote.aftermarket_quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved aftermarket quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_aftermarket_quote: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving aftermarket quote: {str(e)}",
        )
