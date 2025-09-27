"""
MCP Tools for Insider Trades Category

This module provides MCP tool definitions for the Insider Trades category of the FMP API,
including insider trading activity, statistics, and search capabilities.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    mcp,
    validate_date,
    validate_limit,
    validate_page,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_latest_insider_trades(
    page: int | None = None, limit: int | None = None, trade_date: str | None = None
) -> dict[str, Any]:
    """
    Get the latest insider trading activity.

    This tool retrieves the latest insider trading activity across all companies,
    including transaction details and insider information.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of records per page (optional) - e.g., 100, 500, 1000
        trade_date: Specific date for insider trades in YYYY-MM-DD format (optional) - e.g., "2024-01-01"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest insider trading activities with transaction details
        - message: Optional message about the operation

    Example prompts:
        "What are the latest insider trades for January 1, 2024 with 100 records per page?"
        "Show me the most recent insider trading activity across all companies"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)
        validated_trade_date = validate_date(trade_date) if trade_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.latest_insider_trades(
                page=validated_page,
                limit=validated_limit,
                trade_date=validated_trade_date,
            )

        return create_tool_response(
            data=results,
            success=True,
            message="Retrieved latest insider trading activity",
        )

    except Exception as e:
        logger.error(f"Error in get_latest_insider_trades: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest insider trades: {str(e)}",
        )


@mcp.tool
async def get_insider_trade_statistics(symbol: str) -> dict[str, Any]:
    """
    Get insider trading statistics for a specific company.

    This tool retrieves insider trading statistics for a company,
    including trading activity and insider information.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Insider trading statistics with transaction counts and ratios
        - message: Optional message about the operation

    Example prompts:
        "What are the insider trading statistics for Apple (AAPL)?"
        "Show me the insider trading activity statistics for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.insider_trade_statistics(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved insider trade statistics for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_insider_trade_statistics: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving insider trade statistics: {str(e)}",
        )


@mcp.tool
async def search_insider_trades(
    symbol: str | None = None,
    page: int | None = None,
    limit: int | None = None,
    reporting_cik: str | None = None,
    company_cik: str | None = None,
    transaction_type: str | None = None,
) -> dict[str, Any]:
    """
    Search insider trading activity by various criteria.

    This tool searches for insider trading activity by various criteria
    including symbol, CIK, and transaction type.

    Args:
        symbol: Stock symbol to search for (optional) - e.g., "AAPL", "MSFT", "GOOGL"
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Number of records per page (optional) - e.g., 100, 500, 1000
        reporting_cik: CIK of the reporting person (optional) - e.g., "0001548760"
        company_cik: CIK of the company (optional) - e.g., "0000320193"
        transaction_type: Type of transaction (optional) - e.g., "S-Sale", "P-Purchase"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Insider trading activities matching the search criteria
        - message: Optional message about the operation

    Example prompts:
        "What are the insider trades for Apple (AAPL) with sale transactions?"
        "Show me insider trading activity for Microsoft (MSFT) with purchase transactions"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol) if symbol else None
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        if reporting_cik and not isinstance(reporting_cik, str):
            raise ValueError("Reporting CIK must be a string")

        if company_cik and not isinstance(company_cik, str):
            raise ValueError("Company CIK must be a string")

        if transaction_type and not isinstance(transaction_type, str):
            raise ValueError("Transaction type must be a string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.search_insider_trades(
                symbol=validated_symbol,
                page=validated_page,
                limit=validated_limit,
                reporting_cik=reporting_cik,
                company_cik=company_cik,
                transaction_type=transaction_type,
            )

        return create_tool_response(
            data=results,
            success=True,
            message="Retrieved insider trades matching search criteria",
        )

    except Exception as e:
        logger.error(f"Error in search_insider_trades: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving insider trades: {str(e)}"
        )


@mcp.tool
async def search_by_reporting_name(name: str) -> dict[str, Any]:
    """
    Search for insider trading activity by reporting name.

    This tool searches for insider trading activity by the reporting person's name,
    returning matching persons with their CIKs.

    Args:
        name: Name of the reporting person - e.g., "Zuckerberg", "Tim Cook"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of reporting persons matching the name with their CIKs
        - message: Optional message about the operation

    Example prompts:
        "What reporting persons match the name Zuckerberg?"
        "Show me all reporting persons with the name Tim Cook"
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.search_by_reporting_name(name=name)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved reporting persons matching {name}",
        )

    except Exception as e:
        logger.error(f"Error in search_by_reporting_name: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving reporting persons: {str(e)}",
        )


@mcp.tool
async def get_all_transaction_types() -> dict[str, Any]:
    """
    Get all insider transaction types.

    This tool retrieves a comprehensive list of all available insider transaction types,
    useful for understanding the different types of insider trading activities.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of all available insider transaction types
        - message: Optional message about the operation

    Example prompts:
        "What are all the available insider transaction types?"
        "Show me the list of all insider trading transaction types"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.all_transaction_types()

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved {len(results)} transaction types",
        )

    except Exception as e:
        logger.error(f"Error in get_all_transaction_types: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving transaction types: {str(e)}",
        )


@mcp.tool
async def get_acquisition_ownership(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get acquisition ownership changes for a specific company.

    This tool retrieves changes in stock ownership during acquisitions
    for a specific company, including beneficial ownership details.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Acquisition ownership changes data
        - message: Optional message about the operation

    Example prompts:
        "What are the acquisition ownership changes for Apple (AAPL) with 1000 records?"
        "Show me the ownership changes during acquisitions for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.insider_trades.acquisition_ownership(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved acquisition ownership changes for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_acquisition_ownership: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving acquisition ownership changes: {str(e)}",
        )
