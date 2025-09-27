"""
MCP Tools for Technical Indicators Category

This module provides MCP tool definitions for the Technical Indicators category of the FMP API,
including moving averages, RSI, and other technical analysis tools.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_simple_moving_average(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Simple Moving Average (SMA) technical indicator.

    This tool retrieves Simple Moving Average data for a stock symbol
    over a specified period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of SMA data with date, OHLCV data, and SMA values
        - message: Optional message about the operation

    Example prompts:
        "What is the 10-day Simple Moving Average for Apple (AAPL) from January to December 2024?"
        "Show me the 20-day SMA for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.simple_moving_average(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period SMA for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_simple_moving_average: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving simple moving average: {str(e)}",
        )


@mcp.tool
async def get_relative_strength_index(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Relative Strength Index (RSI) technical indicator.

    This tool retrieves RSI data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 14, 21, 30
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of RSI data with date, OHLCV data, and RSI values
        - message: Optional message about the operation

    Example prompts:
        "What is the 14-period RSI for Apple (AAPL) from January to December 2024?"
        "Show me the 21-period RSI for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.relative_strength_index(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period RSI for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_relative_strength_index: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving relative strength index: {str(e)}",
        )


@mcp.tool
async def get_exponential_moving_average(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Exponential Moving Average (EMA) technical indicator.

    This tool retrieves EMA data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of EMA data with date, OHLCV data, and EMA values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Exponential Moving Average for Apple (AAPL) from January to December 2024?"
        "Show me the 50-period EMA for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.exponential_moving_average(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period EMA for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_exponential_moving_average: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving exponential moving average: {str(e)}",
        )


@mcp.tool
async def get_weighted_moving_average(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Weighted Moving Average (WMA) technical indicator.

    This tool retrieves WMA data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of WMA data with date, OHLCV data, and WMA values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Weighted Moving Average for Apple (AAPL) from January to December 2024?"
        "Show me the 10-period WMA for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.weighted_moving_average(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period WMA for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_weighted_moving_average: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving weighted moving average: {str(e)}",
        )


@mcp.tool
async def get_double_exponential_moving_average(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Double Exponential Moving Average (DEMA) technical indicator.

    This tool retrieves DEMA data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of DEMA data with date, OHLCV data, and DEMA values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Double Exponential Moving Average for Apple (AAPL) from January to December 2024?"
        "Show me the 10-period DEMA for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = (
                await client.technical_indicators.double_exponential_moving_average(
                    symbol=validated_symbol,
                    period_length=period_length,
                    timeframe=timeframe,
                    from_date=validated_from_date,
                    to_date=validated_to_date,
                )
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period DEMA for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_double_exponential_moving_average: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving double exponential moving average: {str(e)}",
        )


@mcp.tool
async def get_triple_exponential_moving_average(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Triple Exponential Moving Average (TEMA) technical indicator.

    This tool retrieves TEMA data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of TEMA data with date, OHLCV data, and TEMA values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Triple Exponential Moving Average for Apple (AAPL) from January to December 2024?"
        "Show me the 10-period TEMA for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = (
                await client.technical_indicators.triple_exponential_moving_average(
                    symbol=validated_symbol,
                    period_length=period_length,
                    timeframe=timeframe,
                    from_date=validated_from_date,
                    to_date=validated_to_date,
                )
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period TEMA for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_triple_exponential_moving_average: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving triple exponential moving average: {str(e)}",
        )


@mcp.tool
async def get_standard_deviation(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Standard Deviation technical indicator.

    This tool retrieves standard deviation data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of Standard Deviation data with date, OHLCV data, and standardDeviation values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Standard Deviation for Apple (AAPL) from January to December 2024?"
        "Show me the 10-period standard deviation for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.standard_deviation(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period standard deviation for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_standard_deviation: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving standard deviation: {str(e)}",
        )


@mcp.tool
async def get_williams_percent_r(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Williams %R technical indicator.

    This tool retrieves Williams %R data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of Williams %R data with date, OHLCV data, and williams values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Williams %R for Apple (AAPL) from January to December 2024?"
        "Show me the 14-period Williams %R for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.williams_percent_r(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period Williams %R for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_williams_percent_r: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving Williams %R: {str(e)}"
        )


@mcp.tool
async def get_average_directional_index(
    symbol: str,
    period_length: int,
    timeframe: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get Average Directional Index (ADX) technical indicator.

    This tool retrieves ADX data for a stock symbol over a specified
    period and timeframe with optional date filtering.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period_length: Number of periods for calculation - e.g., 10, 20, 50
        timeframe: Time interval for data - e.g., "1min", "5min", "15min", "30min", "1hour", "4hour", "1day"
        from_date: Start date for data in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date for data in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of ADX data with date, OHLCV data, and adx values
        - message: Optional message about the operation

    Example prompts:
        "What is the 20-period Average Directional Index for Apple (AAPL) from January to December 2024?"
        "Show me the 14-period ADX for Microsoft (MSFT) on daily timeframe"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        if not isinstance(period_length, int) or period_length <= 0:
            raise ValueError("Period length must be a positive integer")

        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
        if (
            not timeframe
            or not isinstance(timeframe, str)
            or timeframe not in valid_timeframes
        ):
            raise ValueError(f"Timeframe must be one of: {', '.join(valid_timeframes)}")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.technical_indicators.average_directional_index(
                symbol=validated_symbol,
                period_length=period_length,
                timeframe=timeframe,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {period_length}-period ADX for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_average_directional_index: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving Average Directional Index: {str(e)}",
        )
