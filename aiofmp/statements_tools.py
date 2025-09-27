"""
MCP Tools for Statements Category

This module provides MCP tool definitions for the Statements category of the FMP API,
including financial statements, ratios, and metrics.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_limit, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_income_statement(
    symbol: str, limit: int | None = None, period: str | None = None
) -> dict[str, Any]:
    """
    Get income statement data for a company.

    This tool retrieves income statement data for a company,
    including revenue, expenses, and profitability metrics.

    Args:
        symbol: Company symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Number of periods to retrieve (optional) - e.g., 5, 10, 20
        period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of income statement data with revenue, expenses, and profitability metrics
        - message: Optional message about the operation

    Example prompts:
        "What is the income statement for Apple (AAPL) with 5 annual periods?"
        "Show me the quarterly income statement data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.income_statement(
                symbol=validated_symbol, limit=validated_limit, period=period
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved income statement for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_income_statement: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving income statement: {str(e)}",
        )


@mcp.tool
async def get_balance_sheet(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get balance sheet for a company.

    This tool retrieves balance sheet data for a company,
    including assets, liabilities, and equity.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Balance sheet data
        - message: Optional message about the operation

    Example prompts:
        "What is the balance sheet for Apple (AAPL) with 5 periods?"
        "Show me the balance sheet data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.balance_sheet_statement(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved balance sheet for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_balance_sheet: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving balance sheet: {str(e)}"
        )


@mcp.tool
async def get_cash_flow_statement(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get cash flow statement for a company.

    This tool retrieves cash flow statement data for a company,
    including operating, investing, and financing cash flows.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Cash flow statement data
        - message: Optional message about the operation

    Example prompts:
        "What is the cash flow statement for Apple (AAPL) with 5 periods?"
        "Show me the cash flow statement data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.cash_flow_statement(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved cash flow statement for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_cash_flow_statement: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving cash flow statement: {str(e)}",
        )


@mcp.tool
async def get_key_metrics(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get key financial metrics for a company.

    This tool retrieves key financial metrics for a company,
    including ratios, margins, and performance indicators.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Key metrics data
        - message: Optional message about the operation

    Example prompts:
        "What are the key financial metrics for Apple (AAPL) with 5 periods?"
        "Show me the key metrics data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.key_metrics(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved key metrics for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_key_metrics: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving key metrics: {str(e)}"
        )


@mcp.tool
async def get_financial_ratios(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get financial ratios for a company.

    This tool retrieves financial ratios for a company,
    including liquidity, profitability, and efficiency ratios.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Financial ratios data
        - message: Optional message about the operation

    Example prompts:
        "What are the financial ratios for Apple (AAPL) with 5 periods?"
        "Show me the financial ratios data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.financial_ratios(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved financial ratios for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_financial_ratios: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving financial ratios: {str(e)}",
        )


@mcp.tool
async def get_financial_scores(symbol: str) -> dict[str, Any]:
    """
    Get financial health scores for a company.

    This tool retrieves financial health scores for a company,
    including Altman Z-Score and Piotroski Score.

    Args:
        symbol: Company symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of financial scores data including Altman Z-Score and Piotroski Score
        - message: Optional message about the operation

    Example prompts:
        "What are the financial health scores for Apple (AAPL)?"
        "Show me the Altman Z-Score and Piotroski Score for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.financial_scores(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved financial scores for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_financial_scores: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving financial scores: {str(e)}",
        )


@mcp.tool
async def get_owner_earnings(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get owner earnings for a company.

    This tool retrieves owner earnings data for a company,
    including free cash flow and owner earnings calculations.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Owner earnings data
        - message: Optional message about the operation

    Example prompts:
        "What are the owner earnings for Apple (AAPL) with 5 periods?"
        "Show me the owner earnings data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.owner_earnings(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved owner earnings for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_owner_earnings: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving owner earnings: {str(e)}"
        )


@mcp.tool
async def get_enterprise_values(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get enterprise values for a company.

    This tool retrieves enterprise value data for a company,
    including EV, EV/EBITDA, and other valuation metrics.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Enterprise values data
        - message: Optional message about the operation

    Example prompts:
        "What are the enterprise values for Apple (AAPL) with 5 periods?"
        "Show me the EV and EV/EBITDA data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.enterprise_values(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved enterprise values for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_enterprise_values: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving enterprise values: {str(e)}",
        )


@mcp.tool
async def get_income_statement_growth(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get income statement growth rates for a company.

    This tool retrieves income statement growth rates for a company,
    showing year-over-year growth in revenue, expenses, and net income.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Income statement growth data
        - message: Optional message about the operation

    Example prompts:
        "What are the income statement growth rates for Apple (AAPL) with 5 periods?"
        "Show me the revenue growth data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.income_statement_growth(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved income statement growth for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_income_statement_growth: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving income statement growth: {str(e)}",
        )


@mcp.tool
async def get_balance_sheet_growth(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get balance sheet growth rates for a company.

    This tool retrieves balance sheet growth rates for a company,
    showing year-over-year growth in assets, liabilities, and equity.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Balance sheet growth data
        - message: Optional message about the operation

    Example prompts:
        "What are the balance sheet growth rates for Apple (AAPL) with 5 periods?"
        "Show me the asset growth data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.balance_sheet_statement_growth(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved balance sheet growth for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_balance_sheet_growth: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving balance sheet growth: {str(e)}",
        )


@mcp.tool
async def get_cash_flow_growth(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get cash flow statement growth rates for a company.

    This tool retrieves cash flow statement growth rates for a company,
    showing year-over-year growth in operating, investing, and financing cash flows.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Cash flow growth data
        - message: Optional message about the operation

    Example prompts:
        "What are the cash flow growth rates for Apple (AAPL) with 5 periods?"
        "Show me the operating cash flow growth data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.cash_flow_statement_growth(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved cash flow growth for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_cash_flow_growth: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving cash flow growth: {str(e)}",
        )


@mcp.tool
async def get_financial_statement_growth(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get comprehensive financial statement growth rates for a company.

    This tool retrieves comprehensive financial statement growth rates for a company,
    combining income statement, balance sheet, and cash flow growth data.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 5, 10, 20

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Financial statement growth data
        - message: Optional message about the operation

    Example prompts:
        "What are the comprehensive financial statement growth rates for Apple (AAPL) with 5 periods?"
        "Show me the combined growth data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.financial_statement_growth(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved financial statement growth for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_financial_statement_growth: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving financial statement growth: {str(e)}",
        )


@mcp.tool
async def get_revenue_product_segmentation(
    symbol: str, period: str | None = None, structure: str | None = None
) -> dict[str, Any]:
    """
    Get revenue breakdown by product line for a company.

    This tool retrieves revenue breakdown by product line for a company,
    showing how revenue is distributed across different product categories.

    Args:
        symbol: Company symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period: Period type - annual,quarter (optional)
        structure: Data structure - flat (optional)

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of revenue segmentation data by product categories
        - message: Optional message about the operation

    Example prompts:
        "What is the revenue breakdown by product line for Apple (AAPL) for annual periods?"
        "Show me the product segmentation data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.revenue_product_segmentation(
                symbol=validated_symbol, period=period, structure=structure
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved revenue product segmentation for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_revenue_product_segmentation: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving revenue product segmentation: {str(e)}",
        )


@mcp.tool
async def get_revenue_geographic_segmentation(
    symbol: str, period: str | None = None, structure: str | None = None
) -> dict[str, Any]:
    """
    Get revenue breakdown by geographic region for a company.

    This tool retrieves revenue breakdown by geographic region for a company,
    showing how revenue is distributed across different markets.

    Args:
        symbol: Company symbol - e.g., "AAPL", "MSFT", "GOOGL"
        period: Period type - annual,quarter (optional)
        structure: Data structure - flat (optional)

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: List of revenue segmentation data by geographic regions
        - message: Optional message about the operation

    Example prompts:
        "What is the revenue breakdown by geographic region for Apple (AAPL) for annual periods?"
        "Show me the geographic segmentation data for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.statements.revenue_geographic_segmentation(
                symbol=validated_symbol, period=period, structure=structure
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved revenue geographic segmentation for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_revenue_geographic_segmentation: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving revenue geographic segmentation: {str(e)}",
        )
