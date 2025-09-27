"""
MCP Tools for Forex Category

This module provides MCP tool definitions for the Forex category of the FMP API,
including currency pairs list, real-time quotes, and historical prices.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_forex_list() -> dict[str, Any]:
    """
    Get list of available currency pairs.

    This tool retrieves a list of all available currency pairs
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available currency pairs
        - message: Optional message about the operation

    Example prompts:
        "What currency pairs are available for trading?"
        "Show me the list of all available forex pairs"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.forex_list()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} currency pairs",
        )

    except Exception as e:
        logger.error(f"Error in get_forex_list: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving forex list: {str(e)}"
        )


@mcp.tool
async def get_forex_quote(symbol: str) -> dict[str, Any]:
    """
    Get real-time forex quote.

    This tool retrieves real-time quote for a currency pair,
    including price, change, and volume information.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Forex quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the current price of EUR/USD?"
        "Show me the real-time quote for GBP/USD"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved forex quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_forex_quote: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving forex quote: {str(e)}"
        )


@mcp.tool
async def get_forex_quote_short(symbol: str) -> dict[str, Any]:
    """
    Get short forex quote.

    This tool retrieves a short version of the forex quote for a currency pair,
    containing essential price information in a compact format.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Short forex quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the short quote for EUR/USD?"
        "Show me the essential price information for USD/JPY"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.quote_short(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved short forex quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_forex_quote_short: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving short forex quote: {str(e)}",
        )


@mcp.tool
async def get_forex_batch_quotes(short: bool = True) -> dict[str, Any]:
    """
    Get real-time quotes for multiple forex pairs simultaneously.

    This tool retrieves batch quotes for multiple currency pairs
    in a single request for efficiency.

    Args:
        short: Whether to return short format quotes (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Batch forex quotes data with price, change, and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the batch quotes for multiple currency pairs in short format?"
        "Show me the current prices for all major forex pairs"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.batch_quotes(short=short)

        return create_tool_response(
            data=results, success=True, message="Retrieved batch forex quotes"
        )

    except Exception as e:
        logger.error(f"Error in get_forex_batch_quotes: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving batch forex quotes: {str(e)}",
        )


@mcp.tool
async def get_forex_historical_price_light(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get historical end-of-day forex prices (light version).

    This tool retrieves light historical price data for a currency pair
    over a specified date range with basic price information.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical forex price data with date, price, and volume
        - message: Optional message about the operation

    Example prompts:
        "What are the historical prices for EUR/USD from January to December 2024?"
        "Show me the light historical price data for GBP/USD in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.historical_price_light(
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
        logger.error(f"Error in get_forex_historical_price_light: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical prices: {str(e)}",
        )


@mcp.tool
async def get_forex_historical_price_full(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get comprehensive historical end-of-day forex price data.

    This tool retrieves full historical price data for a currency pair
    over a specified date range with complete OHLCV and technical indicators.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Comprehensive historical forex price data with OHLCV and technical indicators
        - message: Optional message about the operation

    Example prompts:
        "What are the full historical prices for EUR/USD from January to December 2024?"
        "Show me the comprehensive historical data for USD/JPY in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.historical_price_full(
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
        logger.error(f"Error in get_forex_historical_price_full: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving full historical prices: {str(e)}",
        )


@mcp.tool
async def get_forex_intraday_1min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-minute interval intraday data for forex currency pairs.

    This tool retrieves 1-minute intraday price data for a currency pair
    over a specified date range.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-minute interval data with OHLCV and timestamp
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-minute intraday prices for EUR/USD on January 1, 2024?"
        "Show me the high-frequency trading data for GBP/USD for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.intraday_1min(
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
        logger.error(f"Error in get_forex_intraday_1min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_forex_intraday_5min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 5-minute interval intraday data for forex currency pairs.

    This tool retrieves 5-minute intraday price data for a currency pair
    over a specified date range.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 5-minute interval data with OHLCV and timestamp
        - message: Optional message about the operation

    Example prompts:
        "What are the 5-minute intraday prices for EUR/USD on January 1, 2024?"
        "Show me the 5-minute trading data for USD/JPY for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.intraday_5min(
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
        logger.error(f"Error in get_forex_intraday_5min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 5-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_forex_intraday_1hour(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-hour interval intraday data for forex currency pairs.

    This tool retrieves 1-hour intraday price data for a currency pair
    over a specified date range.

    Args:
        symbol: Forex symbol - e.g., "EURUSD", "GBPUSD", "USDJPY"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-hour interval data with OHLCV and timestamp
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-hour intraday prices for EUR/USD on January 1, 2024?"
        "Show me the hourly trading data for EUR/USD for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.forex.intraday_1hour(
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
        logger.error(f"Error in get_forex_intraday_1hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-hour intraday prices: {str(e)}",
        )
