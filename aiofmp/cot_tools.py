"""
MCP Tools for Commitment of Traders Category

This module provides MCP tool definitions for the COT category of the FMP API,
including COT reports, analysis, and available symbols.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_cot_report(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get comprehensive Commitment of Traders (COT) reports.

    This tool retrieves COT reports for commodities and futures,
    including detailed position information.

    Args:
        symbol: COT symbol - e.g., "KC", "NG", "B6", "GC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-03-01"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: COT report data
        - message: Optional message about the operation

    Example prompts:
        "What is the COT report for Coffee (KC) from January to March 2024?"
        "Show me the Commitment of Traders data for Natural Gas (NG) for the past 3 months"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.cot.cot_report(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved COT report for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_cot_report: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving COT report: {str(e)}"
        )


@mcp.tool
async def get_cot_analysis(
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get COT analysis with market sentiment insights.

    This tool retrieves COT analysis for commodities and futures,
    including market sentiment and trend information.

    Args:
        symbol: COT symbol - e.g., "KC", "NG", "B6", "GC"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2024-03-01"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: COT analysis data
        - message: Optional message about the operation

    Example prompts:
        "What is the COT analysis for British Pound (B6) from January to March 2024?"
        "Show me the market sentiment analysis for Gold (GC) futures"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_from_date = validate_date(from_date)
        validated_to_date = validate_date(to_date)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.cot.cot_analysis(
                symbol=validated_symbol,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved COT analysis for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_cot_analysis: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving COT analysis: {str(e)}"
        )


@mcp.tool
async def get_cot_list() -> dict[str, Any]:
    """
    Get list of available COT report symbols.

    This tool retrieves a list of all available COT symbols
    for commodities and futures.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of available COT symbols
        - message: Optional message about the operation

    Example prompts:
        "What COT symbols are available for analysis?"
        "Show me the list of all commodities and futures with COT data"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.cot.cot_list()

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {len(results)} COT symbols"
        )

    except Exception as e:
        logger.error(f"Error in get_cot_list: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving COT list: {str(e)}"
        )
