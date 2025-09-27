"""
MCP Tools for Senate Category

This module provides MCP tool definitions for the Senate category of the FMP API,
including senate and house financial disclosures and trading activity.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_limit,
    validate_page,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_latest_senate_disclosures(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest senate financial disclosures.

    This tool retrieves the latest senate financial disclosures,
    including trading activity and financial information.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest senate disclosures data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest senate financial disclosures with 100 records per page?"
        "Show me the most recent senate trading activity and financial information"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.latest_senate_disclosures(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved latest senate disclosures"
        )

    except Exception as e:
        logger.error(f"Error in get_latest_senate_disclosures: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest senate disclosures: {str(e)}",
        )


@mcp.tool
async def get_house_trading_activity(symbol: str) -> dict[str, Any]:
    """
    Get house trading activity for a specific stock symbol.

    This tool retrieves house trading activity for a specific stock symbol,
    including trading details and representative information.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: House trading activity data
        - message: Optional message about the operation

    Example prompts:
        "What is the house trading activity for Apple (AAPL)?"
        "Show me the house trading activity for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.house_trading_activity(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved house trading activity for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_house_trading_activity: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving house trading activity: {str(e)}",
        )


@mcp.tool
async def get_latest_house_disclosures(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest house financial disclosures.

    This tool retrieves the latest house financial disclosures,
    including trading activity and financial information.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest house disclosures data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest house financial disclosures with 100 records per page?"
        "Show me the most recent house trading activity and financial information"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.latest_house_disclosures(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved latest house disclosures"
        )

    except Exception as e:
        logger.error(f"Error in get_latest_house_disclosures: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest house disclosures: {str(e)}",
        )


@mcp.tool
async def get_senate_trading_activity(symbol: str) -> dict[str, Any]:
    """
    Get senate trading activity for a specific stock symbol.

    This tool retrieves senate trading activity for a specific stock symbol,
    including trading details and senator information.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Senate trading activity data
        - message: Optional message about the operation

    Example prompts:
        "What is the senate trading activity for Apple (AAPL)?"
        "Show me the senate trading activity for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.senate_trading_activity(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved senate trading activity for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_senate_trading_activity: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving senate trading activity: {str(e)}",
        )


@mcp.tool
async def get_senate_trades_by_name(name: str) -> dict[str, Any]:
    """
    Search Senate trading activity by Senator name.

    This tool searches for Senate trading activity by Senator name,
    including trade details and disclosure information.

    Args:
        name: Senator name to search for - e.g., "Jerry", "Nancy", "Mitch"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of Senate trading activity for the specified name with trade details and disclosure info
        - message: Optional message about the operation

    Example prompts:
        "What are the senate trades for senators named Jerry?"
        "Show me the senate trading activity for senators named Nancy"
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.senate_trades_by_name(name=name)

        return create_tool_response(
            data=results, success=True, message=f"Retrieved senate trades for {name}"
        )

    except Exception as e:
        logger.error(f"Error in get_senate_trades_by_name: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving senate trades by name: {str(e)}",
        )


@mcp.tool
async def get_house_trades_by_name(name: str) -> dict[str, Any]:
    """
    Search House trading activity by Representative name.

    This tool searches for House trading activity by Representative name,
    including trade details and disclosure information.

    Args:
        name: Representative name to search for - e.g., "James", "Nancy", "Kevin"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of House trading activity for the specified name with trade details and disclosure info
        - message: Optional message about the operation

    Example prompts:
        "What are the house trades for representatives named James?"
        "Show me the house trading activity for representatives named Nancy"
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.senate.house_trades_by_name(name=name)

        return create_tool_response(
            data=results, success=True, message=f"Retrieved house trades for {name}"
        )

    except Exception as e:
        logger.error(f"Error in get_house_trades_by_name: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving house trades by name: {str(e)}",
        )
