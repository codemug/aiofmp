"""
Unit tests for FMP Directory category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.directory import DirectoryCategory


class TestDirectoryCategory:
    """Test cases for DirectoryCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def directory_category(self, mock_client):
        """Directory category instance with mocked client"""
        return DirectoryCategory(mock_client)

    @pytest.mark.asyncio
    async def test_company_symbols(self, directory_category, mock_client):
        """Test company symbols list"""
        mock_response = [
            {
                "symbol": "6898.HK",
                "companyName": "China Aluminum Cans Holdings Limited",
            },
            {"symbol": "AAPL", "companyName": "Apple Inc."},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.company_symbols()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("company-symbols-list")

    @pytest.mark.asyncio
    async def test_financial_symbols(self, directory_category, mock_client):
        """Test financial symbols list"""
        mock_response = [
            {
                "symbol": "6898.HK",
                "companyName": "China Aluminum Cans Holdings Limited",
                "tradingCurrency": "HKD",
                "reportingCurrency": "HKD",
            },
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "tradingCurrency": "USD",
                "reportingCurrency": "USD",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.financial_symbols()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("financial-symbols-list")

    @pytest.mark.asyncio
    async def test_etf_list(self, directory_category, mock_client):
        """Test ETF list"""
        mock_response = [
            {"symbol": "GULF", "name": "WisdomTree Middle East Dividend Fund"},
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.etf_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("etf-list")

    @pytest.mark.asyncio
    async def test_actively_trading(self, directory_category, mock_client):
        """Test actively trading list"""
        mock_response = [
            {"symbol": "6898.HK", "name": "China Aluminum Cans Holdings Limited"},
            {"symbol": "AAPL", "name": "Apple Inc."},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.actively_trading()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("actively-trading-list")

    @pytest.mark.asyncio
    async def test_earnings_transcripts(self, directory_category, mock_client):
        """Test earnings transcripts list"""
        mock_response = [
            {
                "symbol": "MCUJF",
                "companyName": "Medicure Inc.",
                "noOfTranscripts": "16",
            },
            {"symbol": "AAPL", "companyName": "Apple Inc.", "noOfTranscripts": "45"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.earnings_transcripts()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("earnings-transcript-list")

    @pytest.mark.asyncio
    async def test_available_exchanges(self, directory_category, mock_client):
        """Test available exchanges list"""
        mock_response = [
            {
                "exchange": "AMEX",
                "name": "New York Stock Exchange Arca",
                "countryName": "United States of America",
                "countryCode": "US",
                "symbolSuffix": "N/A",
                "delay": "Real-time",
            },
            {
                "exchange": "NASDAQ",
                "name": "NASDAQ Stock Market",
                "countryName": "United States of America",
                "countryCode": "US",
                "symbolSuffix": "N/A",
                "delay": "Real-time",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.available_exchanges()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("available-exchanges")

    @pytest.mark.asyncio
    async def test_available_sectors(self, directory_category, mock_client):
        """Test available sectors list"""
        mock_response = [
            {"sector": "Basic Materials"},
            {"sector": "Technology"},
            {"sector": "Healthcare"},
            {"sector": "Financial Services"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.available_sectors()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("available-sectors")

    @pytest.mark.asyncio
    async def test_available_industries(self, directory_category, mock_client):
        """Test available industries list"""
        mock_response = [
            {"industry": "Steel"},
            {"industry": "Consumer Electronics"},
            {"industry": "Software"},
            {"industry": "Banking"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.available_industries()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("available-industries")

    @pytest.mark.asyncio
    async def test_available_countries(self, directory_category, mock_client):
        """Test available countries list"""
        mock_response = [
            {"country": "US"},
            {"country": "CA"},
            {"country": "GB"},
            {"country": "DE"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.available_countries()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("available-countries")

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, directory_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await directory_category.company_symbols()

        assert result == []
        mock_client._make_request.assert_called_once_with("company-symbols-list")

    @pytest.mark.asyncio
    async def test_large_response_handling(self, directory_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {"symbol": f"SYMBOL{i}", "companyName": f"Company {i}"} for i in range(1000)
        ]
        mock_client._make_request.return_value = large_response

        result = await directory_category.company_symbols()

        assert len(result) == 1000
        assert result[0]["symbol"] == "SYMBOL0"
        assert result[999]["symbol"] == "SYMBOL999"
        mock_client._make_request.assert_called_once_with("company-symbols-list")

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, directory_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "tradingCurrency": "USD",
                "reportingCurrency": "USD",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await directory_category.financial_symbols()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("financial-symbols-list")
