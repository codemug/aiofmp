"""
MCP Tools for Crypto Category

This module provides MCP tool definitions for the Crypto category of the FMP API,
including cryptocurrency list, real-time quotes, and historical prices.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_cryptocurrency_list() -> dict[str, Any]:
    """
    Get list of available cryptocurrencies.

    This tool retrieves a list of all available cryptocurrencies
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available cryptocurrencies
        - message: Optional message about the operation

    Example prompts:
        "What cryptocurrencies are available for trading?"
        "Show me the list of all cryptocurrencies in the database"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.cryptocurrency_list()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} cryptocurrencies",
        )

    except Exception as e:
        logger.error(f"Error in get_cryptocurrency_list: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving cryptocurrency list: {str(e)}",
        )


@mcp.tool
async def get_crypto_quote(symbol: str) -> dict[str, Any]:
    """
    Get real-time cryptocurrency quote.

    This tool retrieves real-time quote for a cryptocurrency,
    including price, change, and volume information.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Cryptocurrency quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the current price of Bitcoin (BTCUSD)?"
        "Show me the real-time quote for Ethereum (ETHUSD)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.quote(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved crypto quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_crypto_quote: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving crypto quote: {str(e)}"
        )


@mcp.tool
async def get_crypto_quote_short(symbol: str) -> dict[str, Any]:
    """
    Get short cryptocurrency quote with essential price information.

    This tool retrieves a short version of the cryptocurrency quote,
    containing essential price information in a compact format.

    Args:
        symbol: Cryptocurrency symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Short cryptocurrency quote data
        - message: Optional message about the operation

    Example prompts:
        "What is the short quote for Bitcoin (BTCUSD)?"
        "Show me the essential price information for Cardano (ADAUSD)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.quote_short(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved short crypto quote for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_crypto_quote_short: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving short crypto quote: {str(e)}",
        )


@mcp.tool
async def get_crypto_batch_quotes(short: bool = True) -> dict[str, Any]:
    """
    Get batch cryptocurrency quotes for multiple cryptocurrencies.

    This tool retrieves batch quotes for multiple cryptocurrencies
    in a single request for efficiency.

    Args:
        short: Whether to return short format quotes (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Batch cryptocurrency quotes data
        - message: Optional message about the operation

    Example prompts:
        "What are the batch quotes for multiple cryptocurrencies in short format?"
        "Show me the current prices for all major cryptocurrencies"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.batch_quotes(short=short)

        return create_tool_response(
            data=results, success=True, message="Retrieved batch crypto quotes"
        )

    except Exception as e:
        logger.error(f"Error in get_crypto_batch_quotes: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving batch crypto quotes: {str(e)}",
        )


@mcp.tool
async def get_crypto_historical_price_light(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get light historical cryptocurrency prices.

    This tool retrieves light historical price data for a cryptocurrency
    over a specified date range with basic price information.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical cryptocurrency price data
        - message: Optional message about the operation

    Example prompts:
        "What are the historical prices for Bitcoin (BTCUSD) from January to December 2024?"
        "Show me the light historical price data for Ethereum (ETHUSD) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.historical_price_light(
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
        logger.error(f"Error in get_crypto_historical_price_light: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical prices: {str(e)}",
        )


@mcp.tool
async def get_crypto_historical_price_full(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get full historical cryptocurrency prices.

    This tool retrieves full historical price data for a cryptocurrency
    over a specified date range with complete price information.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Full historical cryptocurrency price data
        - message: Optional message about the operation

    Example prompts:
        "What are the full historical prices for Bitcoin (BTCUSD) from January to December 2024?"
        "Show me the complete historical price data for Cardano (ADAUSD) in 2024"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.historical_price_full(
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
        logger.error(f"Error in get_crypto_historical_price_full: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving full historical prices: {str(e)}",
        )


@mcp.tool
async def get_crypto_intraday_1min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-minute intraday cryptocurrency prices.

    This tool retrieves 1-minute intraday price data for a cryptocurrency
    over a specified date range.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-minute intraday cryptocurrency price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-minute intraday prices for Bitcoin (BTCUSD) on January 1, 2024?"
        "Show me the high-frequency trading data for Ethereum (ETHUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.intraday_1min(
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
        logger.error(f"Error in get_crypto_intraday_1min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_crypto_intraday_5min(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 5-minute intraday cryptocurrency prices.

    This tool retrieves 5-minute intraday price data for a cryptocurrency
    over a specified date range.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 5-minute intraday cryptocurrency price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 5-minute intraday prices for Bitcoin (BTCUSD) on January 1, 2024?"
        "Show me the 5-minute trading data for Cardano (ADAUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.intraday_5min(
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
        logger.error(f"Error in get_crypto_intraday_5min: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 5-minute intraday prices: {str(e)}",
        )


@mcp.tool
async def get_crypto_intraday_1hour(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get 1-hour intraday cryptocurrency prices.

    This tool retrieves 1-hour intraday price data for a cryptocurrency
    over a specified date range.

    Args:
        symbol: Crypto symbol - e.g., "BTCUSD", "ETHUSD", "ADAUSD"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-01-02"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: 1-hour intraday cryptocurrency price data
        - message: Optional message about the operation

    Example prompts:
        "What are the 1-hour intraday prices for Bitcoin (BTCUSD) on January 1, 2024?"
        "Show me the hourly trading data for Ethereum (ETHUSD) for the past 2 days"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.crypto.intraday_1hour(
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
        logger.error(f"Error in get_crypto_intraday_1hour: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving 1-hour intraday prices: {str(e)}",
        )
