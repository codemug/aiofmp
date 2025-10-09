"""
Unit tests for MCP tools

This module provides comprehensive unit tests for all MCP tools
in the aiofmp package.
"""

from unittest.mock import AsyncMock, patch

import pytest

from aiofmp.chart_tools import get_historical_price_full, get_intraday_1min
from aiofmp.company_tools import get_company_profile, get_market_cap
from aiofmp.mcp_tools import (
    create_tool_response,
    validate_date,
    validate_limit,
    validate_symbol,
)
from aiofmp.search_tools import screen_stocks, search_companies, search_symbols


class TestMCPToolsUtilities:
    """Test MCP tools utility functions."""

    def test_create_tool_response_success(self):
        """Test creating a successful tool response."""
        data = [{"symbol": "AAPL", "price": 150.0}]
        response = create_tool_response(data, success=True, message="Test message")

        # Check that it's a ToolResult object
        from fastmcp.tools.tool import ToolResult

        assert isinstance(response, ToolResult)

        # Check structured content
        assert response.structured_content["success"] is True
        assert response.structured_content["data"] == data
        assert response.structured_content["message"] == "Test message"

    def test_create_tool_response_failure(self):
        """Test creating a failed tool response."""
        response = create_tool_response(None, success=False, message="Error message")

        # Check that it's a ToolResult object
        from fastmcp.tools.tool import ToolResult

        assert isinstance(response, ToolResult)

        # Check structured content
        assert response.structured_content["success"] is False
        assert response.structured_content["data"] is None
        assert response.structured_content["message"] == "Error message"

    def test_validate_symbol_valid(self):
        """Test validating a valid symbol."""
        result = validate_symbol("AAPL")
        assert result == "AAPL"

    def test_validate_symbol_normalize(self):
        """Test normalizing a symbol."""
        result = validate_symbol("  aapl  ")
        assert result == "AAPL"

    def test_validate_symbol_invalid(self):
        """Test validating an invalid symbol."""
        with pytest.raises(ValueError, match="Symbol must be a non-empty string"):
            validate_symbol("")

        with pytest.raises(ValueError, match="Symbol must be a non-empty string"):
            validate_symbol(None)

    def test_validate_date_valid(self):
        """Test validating a valid date."""
        result = validate_date("2025-01-01")
        assert result == "2025-01-01"

    def test_validate_date_none(self):
        """Test validating None date."""
        result = validate_date(None)
        assert result is None

    def test_validate_date_invalid(self):
        """Test validating an invalid date."""
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("2025/01/01")

        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            validate_date("2025-1-1")

    def test_validate_limit_valid(self):
        """Test validating a valid limit."""
        result = validate_limit(10)
        assert result == 10

    def test_validate_limit_none(self):
        """Test validating None limit."""
        result = validate_limit(None)
        assert result is None

    def test_validate_limit_invalid(self):
        """Test validating an invalid limit."""
        with pytest.raises(ValueError, match="Limit must be positive"):
            validate_limit(0)

        with pytest.raises(ValueError, match="Limit must be positive"):
            validate_limit(-1)

        with pytest.raises(ValueError, match="Limit cannot exceed 10000"):
            validate_limit(10001)


class TestSearchTools:
    """Test search category MCP tools."""

    @pytest.mark.asyncio
    async def test_search_symbols_success(self):
        """Test successful symbol search."""
        mock_data = [{"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"}]

        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.search.symbols.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await search_symbols.fn("AAPL", limit=10, exchange="NASDAQ")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Found 1 symbols matching 'AAPL'"
                in result.structured_content["message"]
            )

    @pytest.mark.asyncio
    async def test_search_symbols_error(self):
        """Test symbol search with error."""
        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.search.symbols.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            result = await search_symbols.fn("AAPL")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is False
            assert result.structured_content["data"] == []
            assert "Error searching symbols" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_search_companies_success(self):
        """Test successful company search."""
        mock_data = [{"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"}]

        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.search.companies.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await search_companies.fn("Apple", limit=5, exchange="NASDAQ")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Found 1 companies matching 'Apple'"
                in result.structured_content["message"]
            )

    @pytest.mark.asyncio
    async def test_screen_stocks_success(self):
        """Test successful stock screening."""
        mock_data = [
            {"symbol": "AAPL", "sector": "Technology", "marketCap": 3000000000000}
        ]

        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.search.screener.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await screen_stocks.fn(
                sector="Technology", market_cap_more_than=1000000000, limit=100
            )

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Found 1 stocks matching screening criteria"
                in result.structured_content["message"]
            )


class TestChartTools:
    """Test chart category MCP tools."""

    @pytest.mark.asyncio
    async def test_get_historical_price_full_success(self):
        """Test successful historical price data retrieval."""
        mock_data = [
            {
                "date": "2025-01-01",
                "open": 150.0,
                "high": 155.0,
                "low": 149.0,
                "close": 154.0,
            }
        ]

        with patch("aiofmp.chart_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chart.historical_price_full.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await get_historical_price_full.fn(
                "AAPL", "2025-01-01", "2025-01-31"
            )

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Retrieved 1 comprehensive historical price records for AAPL"
                in result.structured_content["message"]
            )

    @pytest.mark.asyncio
    async def test_get_intraday_1min_success(self):
        """Test successful intraday data retrieval."""
        mock_data = [
            {
                "date": "2025-01-01 09:30:00",
                "open": 150.0,
                "high": 151.0,
                "low": 149.0,
                "close": 150.5,
            }
        ]

        with patch("aiofmp.chart_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chart.intraday_1min.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await get_intraday_1min.fn("AAPL", "2025-01-01", "2025-01-02")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Retrieved 1 1-minute intraday records for AAPL"
                in result.structured_content["message"]
            )


class TestCompanyTools:
    """Test company category MCP tools."""

    @pytest.mark.asyncio
    async def test_get_company_profile_success(self):
        """Test successful company profile retrieval."""
        mock_data = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "sector": "Technology",
                "marketCap": 3000000000000,
            }
        ]

        with patch("aiofmp.company_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.company.profile.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await get_company_profile.fn("AAPL")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Retrieved company profile for AAPL"
                in result.structured_content["message"]
            )

    @pytest.mark.asyncio
    async def test_get_market_cap_success(self):
        """Test successful market cap retrieval."""
        mock_data = [
            {"symbol": "AAPL", "marketCap": 3000000000000, "date": "2025-01-01"}
        ]

        with patch("aiofmp.company_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.company.market_cap.return_value = mock_data
            mock_get_client.return_value = mock_client

            result = await get_market_cap.fn("AAPL")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is True
            assert result.structured_content["data"] == mock_data
            assert (
                "Retrieved market cap data for AAPL"
                in result.structured_content["message"]
            )


class TestMCPToolsIntegration:
    """Test MCP tools integration."""

    @pytest.mark.asyncio
    async def test_tool_error_handling(self):
        """Test that tools handle errors gracefully."""
        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.search.symbols.side_effect = Exception("Network error")
            mock_get_client.return_value = mock_client

            result = await search_symbols.fn("INVALID")

            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)

            # Check structured content
            assert result.structured_content["success"] is False
            assert result.structured_content["data"] == []
            assert "Error searching symbols" in result.structured_content["message"]

    @pytest.mark.asyncio
    async def test_tool_validation(self):
        """Test that tools validate inputs properly."""
        with patch("aiofmp.search_tools.get_fmp_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_get_client.return_value = mock_client

            # Test with invalid symbol
            result = await search_symbols.fn("")
            # Check that it's a ToolResult object
            from fastmcp.tools.tool import ToolResult

            assert isinstance(result, ToolResult)
            assert result.structured_content["success"] is False
            assert (
                "Query must be a non-empty string"
                in result.structured_content["message"]
            )

            # Test with invalid limit
            result = await search_symbols.fn("AAPL", limit=-1)
            assert isinstance(result, ToolResult)
            assert result.structured_content["success"] is False
            assert "Limit must be positive" in result.structured_content["message"]


if __name__ == "__main__":
    pytest.main([__file__])
