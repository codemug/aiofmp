"""
MCP Tools for Commodity Category

This module provides MCP tool definitions for the Commodity category of the FMP API,
including commodities list, real-time quotes, and historical prices.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_commodities_list() -> dict[str, Any]:
    """
    Get list of available commodities.

    This tool retrieves a list of all available commodities
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available commodities
        - message: Optional message about the operation

    Example prompts:
        "What commodities are available for trading?"
        "Show me the list of all commodities in the database"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.commodities_list()

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {len(results)} commodities"
        )

    except Exception as e:
        logger.error(f"Error in get_commodities_list: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving commodities list: {str(e)}",
        )


@mcp.tool
async def get_commodity_quote(symbol: str) -> dict[str, Any]:
    """
    Get real-time commodity quote.

    This tool retrieves real-time quote for a commodity,
    including price, change, and volume information.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Commodity quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the current price of Gold (GCUSD)?"
        "Show me the real-time quote for Crude Oil (CLUSD)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved commodity quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_commodity_quote: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving commodity quote: {str(e)}",
        )


@mcp.tool
async def get_commodity_quote_short(symbol: str) -> dict[str, Any]:
    """
    Get short commodity quote with essential price information.

    This tool retrieves a short version of the commodity quote,
    containing essential price information in a compact format.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Short commodity quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the short quote for Gold (GCUSD)?"
        "Show me the essential price information for Natural Gas (NGUSD)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.quote_short(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved short commodity quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_commodity_quote_short: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving short commodity quote: {str(e)}",
        )


@mcp.tool
async def get_commodity_historical_price_light(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get light historical commodity prices.

    This tool retrieves light historical price data for a commodity
    over a specified date range with basic price information.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical commodity price data
        - message: Optional message about the operation

    Example prompts:
        "What are the historical prices for Gold (GCUSD) from January to December 2024?"
        "Show me the light historical price data for Crude Oil (CLUSD) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.historical_price_light(
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
        logger.error(f"Error in get_commodity_historical_price_light: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical prices: {str(e)}",
        )


@mcp.tool
async def get_commodity_historical_price_full(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get full historical commodity prices.

    This tool retrieves full historical price data for a commodity
    over a specified date range with complete price information.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Full historical commodity price data
        - message: Optional message about the operation

    Example prompts:
        "What are the full historical prices for Gold (GCUSD) from January to December 2024?"
        "Show me the complete historical price data for Crude Oil (CLUSD) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.historical_price_full(
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
        logger.error(f"Error in get_commodity_historical_price_full: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving full historical prices: {str(e)}",
        )


@mcp.tool
async def get_commodity_intraday_1min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-minute intraday commodity prices.

    This tool retrieves 1-minute intraday price data for a commodity
    over a specified date range.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-minute intraday commodity price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-minute intraday prices for Gold (GCUSD) on January 1, 2024?"
        "Show me the high-frequency trading data for Natural Gas (NGUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.intraday_1min(
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
        logger.error(f"Error in get_commodity_intraday_1min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_commodity_intraday_5min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 5-minute intraday commodity prices.

    This tool retrieves 5-minute intraday price data for a commodity
    over a specified date range.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 5-minute intraday commodity price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 5-minute intraday prices for Gold (GCUSD) on January 1, 2024?"
        "Show me the 5-minute trading data for Crude Oil (CLUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.intraday_5min(
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
        logger.error(f"Error in get_commodity_intraday_5min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 5-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_commodity_intraday_1hour(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-hour intraday commodity prices.

    This tool retrieves 1-hour intraday price data for a commodity
    over a specified date range.

    Args:
        symbol: Commodity symbol - e.g., "GCUSD", "CLUSD", "NGUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-hour intraday commodity price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-hour intraday prices for Gold (GCUSD) on January 1, 2024?"
        "Show me the hourly trading data for Natural Gas (NGUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.commodity.intraday_1hour(
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
        logger.error(f"Error in get_commodity_intraday_1hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-hour intraday prices: {str(e)}",
        )
