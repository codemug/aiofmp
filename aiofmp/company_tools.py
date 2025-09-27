"""
MCP Tools for Company Category

This module provides MCP tool definitions for the Company category of the FMP API,
including company profiles, employee data, market cap, executives, and more.
"""

import logging
from typing import Any

from .fmp_client import get_fmp_client
from .mcp_tools import (
    create_tool_response,
    format_currency,
    format_large_number,
    mcp,
    validate_date,
    validate_limit,
    validate_page,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@mcp.tool
async def get_company_profile(symbol: str) -> dict[str, Any]:
    """
    Get detailed company profile data with comprehensive company information.

    This tool retrieves comprehensive company profile information including
    company name, description, sector, industry, market cap, and other key details.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Company profile data with comprehensive information
        - message: Optional message about the operation

    Example prompts:
        "What is the company profile for Apple (AAPL)?"
        "Show me detailed information about Microsoft (MSFT) including market cap and industry"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.profile(symbol=validated_symbol)

        # Format the response with additional formatting
        if results and len(results) > 0:
            profile = results[0]
            # Add formatted values for better readability
            if "marketCap" in profile:
                profile["market_cap_formatted"] = format_large_number(
                    profile["marketCap"]
                )
            if "price" in profile:
                profile["price_formatted"] = format_currency(profile["price"])

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved company profile for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_company_profile: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving company profile: {str(e)}",
        )


@mcp.tool
async def get_company_notes(symbol: str) -> dict[str, Any]:
    """
    Get company-issued notes information with CIK, symbol, title, and exchange.

    This tool retrieves company-issued notes and announcements including
    CIK (Central Index Key), symbol, title, and exchange information.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Company notes data with CIK, symbol, title, and exchange
        - message: Optional message about the operation

    Example prompts:
        "What are the company-issued notes for Apple (AAPL)?"
        "Show me the announcements and notes for Google (GOOGL)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.notes(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved company notes for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_company_notes: {e}")
        return create_tool_response(
            data=[], success=False, message=f"Error retrieving company notes: {str(e)}"
        )


@mcp.tool
async def get_employee_count(symbol: str, limit: int | None = None) -> dict[str, Any]:
    """
    Get company employee count information with workforce data and SEC filing details.

    This tool retrieves current and historical employee count data for a company,
    including workforce information and SEC filing details.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 10, 50, 100

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Employee count data with workforce information
        - message: Optional message about the operation

    Example prompts:
        "What is the employee count for Apple (AAPL)?"
        "Show me the workforce data for Microsoft (MSFT) with the last 10 records"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.employee_count(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved employee count data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_employee_count: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving employee count data: {str(e)}",
        )


@mcp.tool
async def get_historical_employee_count(
    symbol: str, limit: int | None = None
) -> dict[str, Any]:
    """
    Get historical employee count data showing workforce evolution over time.

    This tool retrieves historical employee count data for a company,
    showing how the workforce has evolved over time.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 10, 50, 100

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical employee count data
        - message: Optional message about the operation

    Example prompts:
        "What is the historical employee count for Apple (AAPL) over time?"
        "Show me how Microsoft's (MSFT) workforce has grown with the last 20 records"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.historical_employee_count(
                symbol=validated_symbol, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical employee count data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_employee_count: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical employee count data: {str(e)}",
        )


@mcp.tool
async def get_market_cap(symbol: str) -> dict[str, Any]:
    """
    Get company market capitalization data with symbol, date, and market cap value.

    This tool retrieves current market capitalization data for a company,
    including the symbol, date, and market cap value.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Market capitalization data
        - message: Optional message about the operation

    Example prompts:
        "What is the market capitalization of Apple (AAPL)?"
        "Show me the current market cap for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.market_cap(symbol=validated_symbol)

        # Format the response with additional formatting
        if results and len(results) > 0:
            market_cap = results[0]
            if "marketCap" in market_cap:
                market_cap["market_cap_formatted"] = format_large_number(
                    market_cap["marketCap"]
                )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved market cap data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_market_cap: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving market cap data: {str(e)}",
        )


@mcp.tool
async def get_batch_market_cap(symbols: list[str]) -> dict[str, Any]:
    """
    Get market capitalization data for multiple companies in a single request.

    This tool retrieves market capitalization data for multiple companies
    in a single API call, improving efficiency for batch operations.

    Args:
        symbols: List of stock symbols - e.g., ["AAPL", "MSFT", "GOOGL"]

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Market capitalization data for all requested symbols
        - message: Optional message about the operation

    Example prompts:
        "What are the market caps for Apple, Microsoft, and Google?"
        "Show me the market capitalization for multiple tech companies"
    """
    try:
        # Validate inputs
        if not symbols or not isinstance(symbols, list):
            raise ValueError("Symbols must be a non-empty list")

        validated_symbols = [validate_symbol(symbol) for symbol in symbols]

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.batch_market_cap(symbols=validated_symbols)

        # Format the response with additional formatting
        for result in results:
            if "marketCap" in result:
                result["market_cap_formatted"] = format_large_number(
                    result["marketCap"]
                )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved market cap data for {len(validated_symbols)} companies",
        )

    except Exception as e:
        logger.error(f"Error in get_batch_market_cap: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving batch market cap data: {str(e)}",
        )


@mcp.tool
async def get_historical_market_cap(
    symbol: str,
    limit: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """
    Get historical market capitalization data showing market value changes over time.

    This tool retrieves historical market capitalization data for a company,
    showing how the market value has changed over time.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        limit: Maximum number of results to return (optional) - e.g., 10, 50, 100
        from_date: Start date in YYYY-MM-DD format (optional) - e.g., "2025-01-01"
        to_date: End date in YYYY-MM-DD format (optional) - e.g., "2025-03-31"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Historical market capitalization data
        - message: Optional message about the operation

    Example prompts:
        "What is the historical market cap for Apple (AAPL) from January 2025?"
        "Show me how Microsoft's (MSFT) market value has changed over time"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_limit = validate_limit(limit)
        validated_from_date = validate_date(from_date) if from_date else None
        validated_to_date = validate_date(to_date) if to_date else None

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.historical_market_cap(
                symbol=validated_symbol,
                limit=validated_limit,
                from_date=validated_from_date,
                to_date=validated_to_date,
            )

        # Format the response with additional formatting
        for result in results:
            if "marketCap" in result:
                result["market_cap_formatted"] = format_large_number(
                    result["marketCap"]
                )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved historical market cap data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_historical_market_cap: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving historical market cap data: {str(e)}",
        )


@mcp.tool
async def get_shares_float(symbol: str) -> dict[str, Any]:
    """
    Get company share float and liquidity information including free float and outstanding shares.

    This tool retrieves share float information for a company, including
    free float and outstanding shares data.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Share float and liquidity data
        - message: Optional message about the operation

    Example prompts:
        "What is the share float for Apple (AAPL)?"
        "Show me the free float and outstanding shares for Microsoft (MSFT)"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.shares_float(symbol=validated_symbol)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved shares float data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_shares_float: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving shares float data: {str(e)}",
        )


@mcp.tool
async def get_all_shares_float(
    limit: int | None = None, page: int | None = None
) -> dict[str, Any]:
    """
    Get shares float data for all available companies with pagination support.

    This tool retrieves share float data for all available companies,
    with pagination support for large datasets.

    Args:
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000
        page: Page number for pagination (optional) - e.g., 0, 1, 2

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Share float data for all companies
        - message: Optional message about the operation

    Example prompts:
        "What are the share float data for all companies with 1000 results per page?"
        "Show me the first page of share float data for all available companies"
    """
    try:
        # Validate inputs
        validated_limit = validate_limit(limit)
        validated_page = validate_page(page)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.all_shares_float(
                limit=validated_limit, page=validated_page
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved shares float data for {len(results)} companies",
        )

    except Exception as e:
        logger.error(f"Error in get_all_shares_float: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving all shares float data: {str(e)}",
        )


@mcp.tool
async def get_latest_mergers_acquisitions(
    page: int | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Get latest mergers and acquisitions data with transaction details and SEC filing links.

    This tool retrieves the latest mergers and acquisitions data,
    including transaction details and SEC filing links.

    Args:
        page: Page number for pagination (optional) - e.g., 0, 1, 2
        limit: Maximum number of results to return (optional) - e.g., 100, 500, 1000

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Latest mergers and acquisitions data
        - message: Optional message about the operation

    Example prompts:
        "What are the latest mergers and acquisitions with 100 records per page?"
        "Show me the most recent M&A transactions in the market"
    """
    try:
        # Validate inputs
        validated_page = validate_page(page)
        validated_limit = validate_limit(limit)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.latest_mergers_acquisitions(
                page=validated_page, limit=validated_limit
            )

        return create_tool_response(
            data=results,
            success=True,
            message="Retrieved latest mergers and acquisitions data",
        )

    except Exception as e:
        logger.error(f"Error in get_latest_mergers_acquisitions: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving latest mergers and acquisitions data: {str(e)}",
        )


@mcp.tool
async def search_mergers_acquisitions(name: str) -> dict[str, Any]:
    """
    Search for specific mergers and acquisitions data by company name.

    This tool searches for mergers and acquisitions data involving
    a specific company by name.

    Args:
        name: Company name to search for - e.g., "Apple", "Microsoft", "Tesla"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Mergers and acquisitions data for the specified company
        - message: Optional message about the operation

    Example prompts:
        "What mergers and acquisitions involve Apple?"
        "Show me M&A transactions related to Microsoft"
    """
    try:
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.search_mergers_acquisitions(name=name)

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved mergers and acquisitions data for {name}",
        )

    except Exception as e:
        logger.error(f"Error in search_mergers_acquisitions: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error searching mergers and acquisitions data: {str(e)}",
        )


@mcp.tool
async def get_executives(symbol: str, active: bool | None = None) -> dict[str, Any]:
    """
    Get company executives information with names, titles, compensation, and demographic details.

    This tool retrieves executive information for a company, including
    names, titles, compensation, and demographic details.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"
        active: Filter for active executives only (optional) - e.g., True, False

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Executive information with names, titles, compensation
        - message: Optional message about the operation

    Example prompts:
        "Who are the executives at Apple (AAPL)?"
        "Show me the active executives for Microsoft (MSFT) with their compensation"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.executives(
                symbol=validated_symbol, active=active
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved executive information for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_executives: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving executive information: {str(e)}",
        )


@mcp.tool
async def get_executive_compensation(symbol: str) -> dict[str, Any]:
    """
    Get executive compensation data with salaries, stock awards, and total compensation.

    This tool retrieves executive compensation data for a company,
    including salaries, stock awards, and total compensation.

    Args:
        symbol: Stock symbol - e.g., "AAPL", "MSFT", "GOOGL"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Executive compensation data
        - message: Optional message about the operation

    Example prompts:
        "What is the executive compensation at Apple (AAPL)?"
        "Show me the salaries and stock awards for Microsoft (MSFT) executives"
    """
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.executive_compensation(
                symbol=validated_symbol
            )

        return create_tool_response(
            data=results,
            success=True,
            message=f"Retrieved executive compensation data for {validated_symbol}",
        )

    except Exception as e:
        logger.error(f"Error in get_executive_compensation: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving executive compensation data: {str(e)}",
        )


@mcp.tool
async def get_executive_compensation_benchmark(
    year: str | None = None,
) -> dict[str, Any]:
    """
    Get executive compensation benchmark data by industry for comparison.

    This tool retrieves executive compensation benchmark data by industry,
    useful for comparing compensation across companies.

    Args:
        year: Year for benchmark data (optional) - e.g., "2024", "2023"

    Returns:
        Dictionary containing:
        - success: Boolean indicating if the operation was successful
        - data: Executive compensation benchmark data by industry
        - message: Optional message about the operation

    Example prompts:
        "What is the executive compensation benchmark for 2024 by industry?"
        "Show me the industry comparison of executive compensation for tech companies"
    """
    try:
        # Validate inputs
        if year and not isinstance(year, str):
            raise ValueError("Year must be a string")

        # Get FMP client and fetch data
        client = get_fmp_client()
        async with client:
            results = await client.company.executive_compensation_benchmark(year=year)

        return create_tool_response(
            data=results,
            success=True,
            message="Retrieved executive compensation benchmark data",
        )

    except Exception as e:
        logger.error(f"Error in get_executive_compensation_benchmark: {e}")
        return create_tool_response(
            data=[],
            success=False,
            message=f"Error retrieving executive compensation benchmark data: {str(e)}",
        )
