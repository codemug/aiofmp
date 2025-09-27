"""
MCP Tools for Chart Category

This module provides MCP tool definitions for the Chart category of the FMP API,
including historical price data, intraday data, and various time intervals.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_date,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_historical_price_light(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get simplified stock chart data (light version).

    This tool retrieves essential historical price data for a stock symbol
    with a simplified data structure containing date, price, and volume.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of simplified price data with date, price, and volume
        - message: Optional message about the operation

    Example prompts:
        "What is the simplified stock price data for Apple (AAPL) from January to March 2025?"
        "Show me the light historical price data for Microsoft stock in Q1 2025"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.historical_price_light(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} historical price records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_price_light: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical price data: {str(e)}",
        )


@mcp.tool
async def get_historical_price_full(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get comprehensive stock price and volume data including OHLC, changes, and VWAP.

    This tool retrieves detailed historical price data for a stock symbol
    with comprehensive information including open, high, low, close, volume,
    changes, and VWAP (Volume Weighted Average Price).

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of comprehensive price data with OHLC, volume, changes, VWAP
        - message: Optional message about the operation

    Example prompts:
        "What is the comprehensive stock price data for Apple (AAPL) from January to March 2025?"
        "Show me the full historical price data with OHLC and VWAP for Microsoft stock in Q1 2025"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.historical_price_full(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} comprehensive historical price records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_price_full: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving comprehensive historical price data: {str(e)}",
        )


@mcp.tool
async def get_historical_price_unadjusted(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get stock price data without adjustments for stock splits.

    This tool retrieves historical price data for a stock symbol without
    any adjustments for stock splits, providing the raw price data.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of unadjusted price data
        - message: Optional message about the operation

    Example prompts:
        "What is the unadjusted stock price data for Apple (AAPL) from January to March 2025?"
        "Show me the raw historical price data without stock split adjustments for Microsoft in Q1 2025"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.historical_price_unadjusted(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} unadjusted historical price records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_price_unadjusted: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving unadjusted historical price data: {str(e)}",
        )


@mcp.tool
async def get_historical_price_dividend_adjusted(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get stock price data with dividend adjustments.

    This tool retrieves historical price data for a stock symbol with
    adjustments for dividends, providing a more accurate representation
    of total returns.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of dividend-adjusted price data
        - message: Optional message about the operation

    Example prompts:
        "What is the dividend-adjusted stock price data for Apple (AAPL) from January to March 2025?"
        "Show me the historical price data with dividend adjustments for Microsoft in Q1 2025"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.historical_price_dividend_adjusted(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} dividend-adjusted historical price records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_price_dividend_adjusted: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving dividend-adjusted historical price data: {str(e)}",
        )


@mcp.tool
async def get_intraday_1min(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 1-minute interval intraday stock data.

    This tool retrieves high-frequency intraday data for a stock symbol
    with 1-minute intervals, useful for detailed technical analysis.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 1-minute intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 1-minute intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the high-frequency trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_1min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 1-minute intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_1min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-minute intraday data: {str(e)}",
        )


@mcp.tool
async def get_intraday_5min(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 5-minute interval intraday stock data.

    This tool retrieves intraday data for a stock symbol with 5-minute intervals,
    providing a good balance between detail and data volume.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 5-minute intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 5-minute intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the 5-minute trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_5min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 5-minute intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_5min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 5-minute intraday data: {str(e)}",
        )


@mcp.tool
async def get_intraday_15min(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 15-minute interval intraday stock data.

    This tool retrieves intraday data for a stock symbol with 15-minute intervals,
    useful for medium-term technical analysis.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 15-minute intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 15-minute intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the 15-minute trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_15min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 15-minute intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_15min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 15-minute intraday data: {str(e)}",
        )


@mcp.tool
async def get_intraday_30min(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 30-minute interval intraday stock data.

    This tool retrieves intraday data for a stock symbol with 30-minute intervals,
    useful for longer-term intraday analysis.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 30-minute intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 30-minute intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the 30-minute trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_30min(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 30-minute intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_30min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 30-minute intraday data: {str(e)}",
        )


@mcp.tool
async def get_intraday_1hour(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 1-hour interval intraday stock data.

    This tool retrieves intraday data for a stock symbol with 1-hour intervals,
    useful for daily analysis and longer-term intraday patterns.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 1-hour intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 1-hour intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the hourly trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_1hour(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 1-hour intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_1hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-hour intraday data: {str(e)}",
        )


@mcp.tool
async def get_intraday_4hour(
    symbol: str,
    from_date: str | None = None,
    to_date: str | None = None,
    nonadjusted: bool | None = None,
) -> dict[str, Any]:
    """
    Get 4-hour interval intraday stock data.

    This tool retrieves intraday data for a stock symbol with 4-hour intervals,
    useful for longer-term intraday analysis and swing trading.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-01-02"
        nonadjusted: Whether to return non-adjusted data (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of 4-hour intraday data
        - message: Optional message about the operation

    Example prompts:
        "What is the 4-hour intraday data for Apple (AAPL) on January 1, 2025?"
        "Show me the 4-hour trading data for Microsoft stock for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.chart.intraday_4hour(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
                nonadjusted=nonadjusted,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} 4-hour intraday records for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_intraday_4hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 4-hour intraday data: {str(e)}",
        )
