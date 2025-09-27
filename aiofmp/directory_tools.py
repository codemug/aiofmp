"""
MCP Tools for Directory Category

This module provides MCP tool definitions for the Directory category of the FMP API,
including company symbols, ETFs, exchanges, sectors, and industries.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp

logger = logging.getLogger(__name__)


@mcp.tool
async def get_company_symbols() -> dict[str, Any]:
    """
    Get a complete list of all available company symbols.

    This tool retrieves a comprehensive list of all available
    company symbols in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all available company symbols
        - message: Optional message about the operation

    Example prompts:
        "What company symbols are available for trading?"
        "Show me the complete list of all company symbols in the database"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.company_symbols()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} company symbols",
        )

    except Exception as e:
        logger.error(f"Error in get_company_symbols: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving company symbols: {str(e)}",
        )


@mcp.tool
async def get_etf_list() -> dict[str, Any]:
    """
    Get a complete list of available ETFs.

    This tool retrieves a comprehensive list of all available
    ETFs in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all available ETFs
        - message: Optional message about the operation

    Example prompts:
        "What ETFs are available for trading?"
        "Show me the complete list of all ETFs in the database"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.etf_list()

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {len(results)} ETFs"
        )

    except Exception as e:
        logger.error(f"Error in get_etf_list: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving ETF list: {str(e)}"
        )


@mcp.tool
async def get_available_exchanges() -> dict[str, Any]:
    """
    Get a list of all supported stock exchanges.

    This tool retrieves a list of all supported stock exchanges
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all supported stock exchanges
        - message: Optional message about the operation

    Example prompts:
        "What stock exchanges are supported?"
        "Show me the list of all available stock exchanges"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.available_exchanges()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} stock exchanges",
        )

    except Exception as e:
        logger.error(f"Error in get_available_exchanges: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving available exchanges: {str(e)}",
        )


@mcp.tool
async def get_available_sectors() -> dict[str, Any]:
    """
    Get a list of all available industry sectors.

    This tool retrieves a list of all available industry sectors
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all available industry sectors
        - message: Optional message about the operation

    Example prompts:
        "What industry sectors are available?"
        "Show me the list of all available industry sectors"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.available_sectors()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} industry sectors",
        )

    except Exception as e:
        logger.error(f"Error in get_available_sectors: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving available sectors: {str(e)}",
        )


@mcp.tool
async def get_available_industries() -> dict[str, Any]:
    """
    Get a list of all available industries.

    This tool retrieves a list of all available industries
    in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all available industries
        - message: Optional message about the operation

    Example prompts:
        "What industries are available?"
        "Show me the list of all available industries"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.available_industries()

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {len(results)} industries"
        )

    except Exception as e:
        logger.error(f"Error in get_available_industries: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving available industries: {str(e)}",
        )


@mcp.tool
async def get_financial_symbols() -> dict[str, Any]:
    """
    Get a list of companies with available financial statements.

    This tool retrieves a list of all companies that have
    available financial statements in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of companies with financial statements
        - message: Optional message about the operation

    Example prompts:
        "What companies have available financial statements?"
        "Show me the list of companies with financial data"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.financial_symbols()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} financial symbols",
        )

    except Exception as e:
        logger.error(f"Error in get_financial_symbols: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving financial symbols: {str(e)}",
        )


@mcp.tool
async def get_actively_trading() -> dict[str, Any]:
    """
    Get a list of actively trading companies and financial instruments.

    This tool retrieves a list of all actively trading
    companies and financial instruments in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of actively trading securities
        - message: Optional message about the operation

    Example prompts:
        "What companies are actively trading?"
        "Show me the list of actively trading securities"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.actively_trading()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} actively trading securities",
        )

    except Exception as e:
        logger.error(f"Error in get_actively_trading: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving actively trading securities: {str(e)}",
        )


@mcp.tool
async def get_earnings_transcripts() -> dict[str, Any]:
    """
    Get a list of companies with available earnings transcripts.

    This tool retrieves a list of all companies that have
    available earnings transcripts in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of companies with earnings transcripts
        - message: Optional message about the operation

    Example prompts:
        "What companies have earnings transcripts available?"
        "Show me the list of companies with earnings call transcripts"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.earnings_transcripts()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} companies with earnings transcripts",
        )

    except Exception as e:
        logger.error(f"Error in get_earnings_transcripts: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving earnings transcripts: {str(e)}",
        )


@mcp.tool
async def get_available_countries() -> dict[str, Any]:
    """
    Get a comprehensive list of countries where stock symbols are available.

    This tool retrieves a list of all countries where
    stock symbols are available in the FMP database.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available countries with country codes
        - message: Optional message about the operation

    Example prompts:
        "What countries have stock symbols available?"
        "Show me the list of available countries with their codes"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.directory.available_countries()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} available countries",
        )

    except Exception as e:
        logger.error(f"Error in get_available_countries: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving available countries: {str(e)}",
        )
