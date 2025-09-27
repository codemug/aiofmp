"""
MCP Tools for Indexes Category

This module provides MCP tool definitions for the Indexes category of the FMP API,
including stock market indexes, quotes, and historical data.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_index_quote(symbol: str) -> dict[str, Any]:
    """
    Get real-time index quote.

    This tool retrieves real-time quote for a stock market index,
    including price, change, and volume information.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Index quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the current price of the S&P 500 (^GSPC)?"
        "Show me the real-time quote for the Dow Jones (^DJI)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.index_quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved index quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_quote: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving index quote: {str(e)}"
        )


@mcp.tool
async def get_index_list() -> dict[str, Any]:
    """
    Get list of available stock market indexes.

    This tool retrieves a list of all available stock market indexes
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available indexes
        - message: Optional message about the operation

    Example prompts:
        "What stock market indexes are available?"
        "Show me the list of all available market indexes"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.index_list()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} stock market indexes",
        )

    except Exception as e:
        logger.error(f"Error in get_index_list: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving index list: {str(e)}"
        )


@mcp.tool
async def get_index_quote_short(symbol: str) -> dict[str, Any]:
    """
    Get short index quote.

    This tool retrieves a short version of the index quote,
    containing essential price information in a compact format.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Short index quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the short quote for the S&P 500 (^GSPC)?"
        "Show me the essential price information for the NASDAQ (^IXIC)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.index_quote_short(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved short index quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_quote_short: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving short index quote: {str(e)}",
        )


@mcp.tool
async def get_all_index_quotes(short: bool | None = None) -> dict[str, Any]:
    """
    Get real-time quotes for a wide range of stock indexes.

    This tool retrieves quotes for all available stock market indexes
    in a single request for efficiency.

    Args:
        short: Whether to return short quotes (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Index quotes across multiple indexes
        - message: Optional message about the operation

    Example prompts:
        "What are the short quotes for all available stock market indexes?"
        "Show me the current prices for all major market indexes"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.all_index_quotes(short=short)

        return create_tool_response(
            data=results, success=True, message="Retrieved all index quotes"
        )

    except Exception as e:
        logger.error(f"Error in get_all_index_quotes: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving all index quotes: {str(e)}",
        )


@mcp.tool
async def get_index_historical_price_light(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get end-of-day historical prices for stock indexes (light version).

    This tool retrieves light historical price data for a stock market index
    over a specified date range with basic price information.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical price data with date, price, and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the historical prices for the S&P 500 (^GSPC) from January to December 2024?"
        "Show me the light historical price data for the Dow Jones (^DJI) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.historical_price_eod_light(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical prices for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_historical_price_light: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical prices: {str(e)}",
        )


@mcp.tool
async def get_index_historical_price_full(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get full end-of-day historical prices for stock indexes with comprehensive data.

    This tool retrieves full historical price data for a stock market index
    over a specified date range with complete OHLC, volume, and additional metrics.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Detailed historical price data with OHLC, volume, and additional metrics
        - message: Optional message about the operation

    Example prompts:
        "What are the full historical prices for the S&P 500 (^GSPC) from January to December 2024?"
        "Show me the comprehensive historical data for the NASDAQ (^IXIC) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.historical_price_eod_full(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved full historical prices for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_historical_price_full: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving full historical prices: {str(e)}",
        )


@mcp.tool
async def get_index_intraday_1min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-minute interval intraday data for stock indexes.

    This tool retrieves 1-minute intraday price data for a stock market index
    over a specified date range.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-minute intraday data with OHLC and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-minute intraday prices for the S&P 500 (^GSPC) on January 1, 2024?"
        "Show me the high-frequency trading data for the Dow Jones (^DJI) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.intraday_1min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved 1-minute intraday prices for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_intraday_1min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_index_intraday_5min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 5-minute interval intraday data for stock indexes.

    This tool retrieves 5-minute intraday price data for a stock market index
    over a specified date range.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 5-minute intraday data with OHLC and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the 5-minute intraday prices for the S&P 500 (^GSPC) on January 1, 2024?"
        "Show me the 5-minute trading data for the NASDAQ (^IXIC) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.intraday_5min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved 5-minute intraday prices for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_intraday_5min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 5-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_index_intraday_1hour(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-hour interval intraday data for stock indexes.

    This tool retrieves 1-hour intraday price data for a stock market index
    over a specified date range.

    Args:
        symbol: Index symbol - e.g., "^GSPC", "^DJI", "^IXIC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-hour intraday data with OHLC and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-hour intraday prices for the S&P 500 (^GSPC) on January 1, 2024?"
        "Show me the hourly trading data for the Dow Jones (^DJI) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.indexes.intraday_1hour(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved 1-hour intraday prices for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_index_intraday_1hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-hour intraday prices: {str(e)}",
        )
