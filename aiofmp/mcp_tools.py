"""
MCP Tools Utilities

This module provides utilities for creating and managing MCP tools
for the Financial Modeling Prep API.
"""

import logging
from typing import Any

from fastmcp.tools.tool import ToolResult

from .mcp_server import mcp

logger = logging.getLogger(__name__)


def create_tool_response(
    data: Any, success: bool = True, message: str = ""
) -> ToolResult:
    """
    Create a standardized response for MCP tools.

    Args:
        data: The actual data to return
        success: Whether the operation was successful
        message: Optional message to include

    Returns:
        ToolResult object for MCP tools
    """
    response = {"success": success, "data": data}

    if message:
        response["message"] = message

    # Check if text content should be included alongside structured content
    import os

    include_text_content = (
        os.getenv("MCP_INCLUDE_TEXT_CONTENT", "false").lower() == "true"
    )

    if include_text_content:
        # Return both text and structured content
        import json

        text_content = json.dumps(response, indent=2)
        return ToolResult(content=text_content, structured_content=response)
    else:
        # Return with structured content only (text content empty when structured content is present)
        return ToolResult(content="", structured_content=response)


def handle_async_operation(operation_name: str):
    """
    Decorator to handle async operations with proper error handling.

    Args:
        operation_name: Name of the operation for logging
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"Starting {operation_name}")
                result = await func(*args, **kwargs)
                logger.info(f"Completed {operation_name} successfully")
                return create_tool_response(result, success=True)
            except Exception as e:
                logger.error(f"Error in {operation_name}: {e}")
                return create_tool_response(
                    None, success=False, message=f"Error in {operation_name}: {str(e)}"
                )

        return wrapper

    return decorator


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize a stock symbol.

    Args:
        symbol: Stock symbol to validate

    Returns:
        Normalized symbol

    Raises:
        ValueError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")

    # Normalize symbol (uppercase, strip whitespace)
    normalized = symbol.strip().upper()

    if not normalized:
        raise ValueError("Symbol cannot be empty")

    return normalized


def validate_date(date_str: str | None) -> str | None:
    """
    Validate a date string in YYYY-MM-DD format.

    Args:
        date_str: Date string to validate

    Returns:
        Validated date string or None

    Raises:
        ValueError: If date format is invalid
    """
    if not date_str:
        return None

    if not isinstance(date_str, str):
        raise ValueError("Date must be a string")

    # Basic format validation
    if len(date_str) != 10 or date_str.count("-") != 2:
        raise ValueError("Date must be in YYYY-MM-DD format")

    try:
        year, month, day = date_str.split("-")
        int(year)
        int(month)
        int(day)
    except ValueError as e:
        raise ValueError("Date must be in YYYY-MM-DD format") from e

    return date_str


def validate_limit(limit: int | None) -> int | None:
    """
    Validate a limit parameter.

    Args:
        limit: Limit value to validate

    Returns:
        Validated limit or None

    Raises:
        ValueError: If limit is invalid
    """
    if limit is None:
        return None

    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    if limit > 10000:  # Reasonable upper limit
        raise ValueError("Limit cannot exceed 10000")

    return limit


def validate_page(page: int | None) -> int | None:
    """
    Validate a page parameter.

    Args:
        page: Page value to validate

    Returns:
        Validated page or None

    Raises:
        ValueError: If page is invalid
    """
    if page is None:
        return None

    if not isinstance(page, int):
        raise ValueError("Page must be an integer")

    if page < 0:
        raise ValueError("Page must be non-negative")

    return page


def format_currency(value: float | None, currency: str = "USD") -> str:
    """
    Format a currency value for display.

    Args:
        value: Currency value to format
        currency: Currency code

    Returns:
        Formatted currency string
    """
    if value is None:
        return "N/A"

    if currency == "USD":
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"


def format_percentage(value: float | None, decimals: int = 2) -> str:
    """
    Format a percentage value for display.

    Args:
        value: Percentage value to format
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}%"


def format_large_number(value: float | None) -> str:
    """
    Format a large number with appropriate suffixes (K, M, B, T).

    Args:
        value: Number to format

    Returns:
        Formatted number string
    """
    if value is None:
        return "N/A"

    if value >= 1e12:
        return f"{value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.2f}"


def create_summary_stats(data: list[dict[str, Any]], key: str) -> dict[str, Any]:
    """
    Create summary statistics for a list of data.

    Args:
        data: List of data dictionaries
        key: Key to extract values from

    Returns:
        Summary statistics dictionary
    """
    if not data:
        return {"count": 0, "min": None, "max": None, "avg": None}

    values = [item.get(key) for item in data if item.get(key) is not None]

    if not values:
        return {"count": len(data), "min": None, "max": None, "avg": None}

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }


# Export the mcp instance for use in other modules
__all__ = [
    "mcp",
    "create_tool_response",
    "handle_async_operation",
    "validate_symbol",
    "validate_date",
    "validate_limit",
    "validate_page",
    "format_currency",
    "format_percentage",
    "format_large_number",
    "create_summary_stats",
]
