"""
MCP Tools for Discounted Cash Flow Category

This module provides MCP tool definitions for the DCF category of the FMP API,
including DCF valuations, levered DCF, and custom DCF calculations.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_symbol

logger = logging.getLogger(__name__)


@mcp.tool
async def get_dcf_valuation(symbol: str) -> dict[str, Any]:
    """
    Get basic DCF valuation for a company.

    This tool retrieves basic DCF valuation for a company,
    including DCF value and stock price.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: DCF valuation data
        - message: Optional message about the operation

    Example prompts:
        "What is the DCF valuation for Apple (AAPL)?"
        "Show me the discounted cash flow analysis for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.dcf.dcf_valuation(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved DCF valuation for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_dcf_valuation: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving DCF valuation: {str(e)}"
        )


@mcp.tool
async def get_levered_dcf(symbol: str) -> dict[str, Any]:
    """
    Get levered DCF valuation incorporating debt impact.

    This tool retrieves levered DCF valuation for a company,
    incorporating debt impact for post-debt company valuation.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Levered DCF valuation data
        - message: Optional message about the operation

    Example prompts:
        "What is the levered DCF valuation for Apple (AAPL)?"
        "Show me the debt-adjusted DCF analysis for Google (GOOGL)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.dcf.levered_dcf(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved levered DCF valuation for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_levered_dcf: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving levered DCF valuation: {str(e)}",
        )


@mcp.tool
async def get_custom_dcf_advanced(
    symbol: str,
    revenue_growth_pct: float | None = None,
    ebitda_pct: float | None = None,
    depreciation_and_amortization_pct: float | None = None,
    cash_and_short_term_investments_pct: float | None = None,
    receivables_pct: float | None = None,
    inventories_pct: float | None = None,
    payable_pct: float | None = None,
    ebit_pct: float | None = None,
    capital_expenditure_pct: float | None = None,
    operating_cash_flow_pct: float | None = None,
    selling_general_and_administrative_expenses_pct: float | None = None,
    tax_rate: float | None = None,
    long_term_growth_rate: float | None = None,
    cost_of_debt: float | None = None,
    cost_of_equity: float | None = None,
    market_risk_premium: float | None = None,
    beta: float | None = None,
    risk_free_rate: float | None = None,
) -> dict[str, Any]:
    """
    Get custom DCF analysis with detailed financial parameters.

    This tool calculates custom DCF valuation using detailed financial parameters
    for more precise and comprehensive valuation analysis.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        revenue_growth_pct: Revenue growth percentage (optional) - e.g., 0.109 for 10.9%
        ebitda_pct: EBITDA percentage (optional) - e.g., 0.25 for 25%
        depreciation_and_amortization_pct: Depreciation and amortization percentage (optional)
        cash_and_short_term_investments_pct: Cash and short-term investments percentage (optional)
        receivables_pct: Receivables percentage (optional)
        inventories_pct: Inventories percentage (optional)
        payable_pct: Payable percentage (optional)
        ebit_pct: EBIT percentage (optional)
        capital_expenditure_pct: Capital expenditure percentage (optional)
        operating_cash_flow_pct: Operating cash flow percentage (optional)
        selling_general_and_administrative_expenses_pct: SG&A expenses percentage (optional)
        tax_rate: Tax rate (optional) - e.g., 0.21 for 21%
        long_term_growth_rate: Long-term growth rate (optional) - e.g., 0.02 for 2%
        cost_of_debt: Cost of debt (optional) - e.g., 0.05 for 5%
        cost_of_equity: Cost of equity (optional) - e.g., 0.10 for 10%
        market_risk_premium: Market risk premium (optional) - e.g., 0.06 for 6%
        beta: Beta (optional) - e.g., 1.244
        risk_free_rate: Risk-free rate (optional) - e.g., 0.04 for 4%

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Custom DCF analysis data with detailed financial projections
        - message: Optional message about the operation

    Example prompts:
        "What is the custom DCF analysis for Apple (AAPL) with 10.9% revenue growth and beta of 1.244?"
        "Show me the advanced DCF valuation for Microsoft (MSFT) with custom financial parameters"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.dcf.custom_dcf_advanced(
                symbol=validated_symbol,
                revenue_growth_pct=revenue_growth_pct,
                ebitda_pct=ebitda_pct,
                depreciation_and_amortization_pct=depreciation_and_amortization_pct,
                cash_and_short_term_investments_pct=cash_and_short_term_investments_pct,
                receivables_pct=receivables_pct,
                inventories_pct=inventories_pct,
                payable_pct=payable_pct,
                ebit_pct=ebit_pct,
                capital_expenditure_pct=capital_expenditure_pct,
                operating_cash_flow_pct=operating_cash_flow_pct,
                selling_general_and_administrative_expenses_pct=selling_general_and_administrative_expenses_pct,
                tax_rate=tax_rate,
                long_term_growth_rate=long_term_growth_rate,
                cost_of_debt=cost_of_debt,
                cost_of_equity=cost_of_equity,
                market_risk_premium=market_risk_premium,
                beta=beta,
                risk_free_rate=risk_free_rate,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved custom DCF analysis for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_custom_dcf_advanced: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving custom DCF analysis: {str(e)}",
        )


@mcp.tool
async def get_custom_dcf_levered(
    symbol: str,
    revenue_growth_pct: float | None = None,
    ebitda_pct: float | None = None,
    depreciation_and_amortization_pct: float | None = None,
    cash_and_short_term_investments_pct: float | None = None,
    receivables_pct: float | None = None,
    inventories_pct: float | None = None,
    payable_pct: float | None = None,
    ebit_pct: float | None = None,
    capital_expenditure_pct: float | None = None,
    operating_cash_flow_pct: float | None = None,
    selling_general_and_administrative_expenses_pct: float | None = None,
    tax_rate: float | None = None,
    long_term_growth_rate: float | None = None,
    cost_of_debt: float | None = None,
    cost_of_equity: float | None = None,
    market_risk_premium: float | None = None,
    beta: float | None = None,
    risk_free_rate: float | None = None,
) -> dict[str, Any]:
    """
    Get custom levered DCF analysis with detailed financial parameters.

    This tool calculates custom levered DCF valuation using detailed financial parameters,
    incorporating debt impact for post-debt company valuation.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        revenue_growth_pct: Revenue growth percentage (optional) - e.g., 0.109 for 10.9%
        ebitda_pct: EBITDA percentage (optional) - e.g., 0.25 for 25%
        depreciation_and_amortization_pct: Depreciation and amortization percentage (optional)
        cash_and_short_term_investments_pct: Cash and short-term investments percentage (optional)
        receivables_pct: Receivables percentage (optional)
        inventories_pct: Inventories percentage (optional)
        payable_pct: Payable percentage (optional)
        ebit_pct: EBIT percentage (optional)
        capital_expenditure_pct: Capital expenditure percentage (optional)
        operating_cash_flow_pct: Operating cash flow percentage (optional)
        selling_general_and_administrative_expenses_pct: SG&A expenses percentage (optional)
        tax_rate: Tax rate (optional) - e.g., 0.21 for 21%
        long_term_growth_rate: Long-term growth rate (optional) - e.g., 0.02 for 2%
        cost_of_debt: Cost of debt (optional) - e.g., 0.05 for 5%
        cost_of_equity: Cost of equity (optional) - e.g., 0.10 for 10%
        market_risk_premium: Market risk premium (optional) - e.g., 0.06 for 6%
        beta: Beta (optional) - e.g., 1.244
        risk_free_rate: Risk-free rate (optional) - e.g., 0.04 for 4%

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Custom levered DCF analysis data with detailed financial projections
        - message: Optional message about the operation

    Example prompts:
        "What is the custom levered DCF analysis for Apple (AAPL) with 10.9% revenue growth and beta of 1.244?"
        "Show me the advanced levered DCF valuation for Google (GOOGL) with custom financial parameters"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.dcf.custom_dcf_levered(
                symbol=validated_symbol,
                revenue_growth_pct=revenue_growth_pct,
                ebitda_pct=ebitda_pct,
                depreciation_and_amortization_pct=depreciation_and_amortization_pct,
                cash_and_short_term_investments_pct=cash_and_short_term_investments_pct,
                receivables_pct=receivables_pct,
                inventories_pct=inventories_pct,
                payable_pct=payable_pct,
                ebit_pct=ebit_pct,
                capital_expenditure_pct=capital_expenditure_pct,
                operating_cash_flow_pct=operating_cash_flow_pct,
                selling_general_and_administrative_expenses_pct=selling_general_and_administrative_expenses_pct,
                tax_rate=tax_rate,
                long_term_growth_rate=long_term_growth_rate,
                cost_of_debt=cost_of_debt,
                cost_of_equity=cost_of_equity,
                market_risk_premium=market_risk_premium,
                beta=beta,
                risk_free_rate=risk_free_rate,
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved custom levered DCF analysis for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_custom_dcf_levered: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving custom levered DCF analysis: {str(e)}",
        )
