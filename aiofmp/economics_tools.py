"""
MCP Tools for Economics Category

This module provides MCP tool definitions for the Economics category of the FMP API,
including treasury rates, economic indicators, and economic calendar.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import create_tool_response, mcp, validate_date

logger = logging.getLogger(__name__)


@mcp.tool
async def get_treasury_rates(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get real-time and historical Treasury rates for all maturities.

    This tool retrieves treasury rates for a specified date range,
    including various maturity periods. If no dates are provided,
    returns the most recent data.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-04-24"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-07-24"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Treasury rates data with various maturity periods
        - message: Optional message about the operation

    Example prompts:
        "What are the Treasury rates from April to July 2025?"
        "Show me the current Treasury rates for all maturities"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.economics.treasury_rates(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved treasury rates"
        )

    except Exception as e:
        logger.error(f"Error in get_treasury_rates: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving treasury rates: {str(e)}"
        )


@mcp.tool
async def get_economic_indicators(
    name: str, from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get real-time and historical economic data for key indicators.

    This tool retrieves economic indicators for a specified date range,
    including GDP, inflation, unemployment, and other key indicators.

    Args:
        name: Economic indicator name (required) - e.g., "GDP", "CPI", "unemploymentRate"
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2024-07-24"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-07-24"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Economic indicators data with name, date, and value
        - message: Optional message about the operation

    Example prompts:
        "What is the GDP data from July 2024 to July 2025?"
        "Show me the inflation rate (CPI) for the past year"

    Available indicators:
        - GDP, realGDP, nominalPotentialGDP, realGDPPerCapita
        - federalFunds, CPI, inflationRate, inflation
        - retailSales, consumerSentiment, durableGoods
        - unemploymentRate, totalNonfarmPayroll, initialClaims
        - industrialProductionTotalIndex, newPrivatelyOwnedHousingUnitsStartedTotalUnits
        - totalVehicleSales, retailMoneyFunds, smoothedUSRecessionProbabilities
        - 3MonthOr90DayRatesAndYieldsCertificatesOfDeposit
        - commercialBankInterestRateOnCreditCardPlansAllAccounts
        - 30YearFixedRateMortgageAverage, 15YearFixedRateMortgageAverage
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.economics.economic_indicators(
                name=name, from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results, success=True, message=f"Retrieved {name} data"
        )

    except Exception as e:
        logger.error(f"Error in get_economic_indicators: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving economic indicators: {str(e)}",
        )


@mcp.tool
async def get_economic_calendar(
    from_date: str | None = None, to_date: str | None = None
) -> dict[str, Any]:
    """
    Get economic calendar events for a specified date range.

    This tool retrieves economic calendar events for a specified date range,
    including important economic announcements and indicators.

    Args:
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-12-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Economic calendar data
        - message: Optional message about the operation

    Example prompts:
        "What economic events are scheduled for 2025?"
        "Show me the economic calendar for the next quarter"
    """
    try:
        # Validate inputs
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.economics.economic_calendar(
                from_date=validated_from_date, to_date=validated_to_date
            )

        return create_tool_response(
            data=results, success=True, message="Retrieved economic calendar events"
        )

    except Exception as e:
        logger.error(f"Error in get_economic_calendar: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving economic calendar: {str(e)}",
        )


@mcp.tool
async def get_market_risk_premium() -> dict[str, Any]:
    """
    Get market risk premium data.

    This tool retrieves market risk premium data,
    which is used in financial modeling and valuation.

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Market risk premium data
        - message: Optional message about the operation

    Example prompts:
        "What is the current market risk premium?"
        "Show me the market risk premium data for financial modeling"
    """
    try:
        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.economics.market_risk_premium()

        return create_tool_response(
            data=results, success=True, message="Retrieved market risk premium data"
        )

    except Exception as e:
        logger.error(f"Error in get_market_risk_premium: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving market risk premium: {str(e)}",
        )
