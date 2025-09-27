"""
Unit tests for FMP Search category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.search import SearchCategory


class TestSearchCategory:
    """Test cases for SearchCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def search_category(self, mock_client):
        """Search category instance with mocked client"""
        return SearchCategory(mock_client)

    @pytest.mark.asyncio
    async def test_symbols_search_basic(self, search_category, mock_client):
        """Test basic symbol search"""
        # Mock response
        mock_response = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "currency": "USD",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        # Test
        result = await search_category.symbols("AAPL")

        # Verify
        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-symbol", {"query": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_symbols_search_with_limit(self, search_category, mock_client):
        """Test symbol search with limit parameter"""
        mock_response = [{"symbol": "AAPL", "name": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.symbols("AAPL", limit=10)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-symbol", {"query": "AAPL", "limit": 10}
        )

    @pytest.mark.asyncio
    async def test_symbols_search_with_exchange(self, search_category, mock_client):
        """Test symbol search with exchange filter"""
        mock_response = [{"symbol": "AAPL", "name": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.symbols("AAPL", exchange="NASDAQ")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-symbol", {"query": "AAPL", "exchange": "NASDAQ"}
        )

    @pytest.mark.asyncio
    async def test_symbols_search_with_all_params(self, search_category, mock_client):
        """Test symbol search with all parameters"""
        mock_response = [{"symbol": "AAPL", "name": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.symbols("AAPL", limit=20, exchange="NASDAQ")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-symbol", {"query": "AAPL", "limit": 20, "exchange": "NASDAQ"}
        )

    @pytest.mark.asyncio
    async def test_companies_search_basic(self, search_category, mock_client):
        """Test basic company search"""
        mock_response = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "currency": "USD",
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await search_category.companies("Apple")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-name", {"query": "Apple"}
        )

    @pytest.mark.asyncio
    async def test_companies_search_with_limit(self, search_category, mock_client):
        """Test company search with limit parameter"""
        mock_response = [{"symbol": "AAPL", "name": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.companies("Apple", limit=5)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-name", {"query": "Apple", "limit": 5}
        )

    @pytest.mark.asyncio
    async def test_companies_search_with_exchange(self, search_category, mock_client):
        """Test company search with exchange filter"""
        mock_response = [{"symbol": "AAPL", "name": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.companies("Apple", exchange="NASDAQ")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "search-name", {"query": "Apple", "exchange": "NASDAQ"}
        )

    @pytest.mark.asyncio
    async def test_screener_basic(self, search_category, mock_client):
        """Test basic stock screener"""
        mock_response = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "marketCap": 3435062313000,
                "sector": "Technology",
                "industry": "Consumer Electronics",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("company-screener", {})

    @pytest.mark.asyncio
    async def test_screener_with_market_cap_filters(self, search_category, mock_client):
        """Test screener with market cap filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            market_cap_more_than=1000000000, market_cap_lower_than=5000000000
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener",
            {"marketCapMoreThan": 1000000000, "marketCapLowerThan": 5000000000},
        )

    @pytest.mark.asyncio
    async def test_screener_with_sector_and_industry(
        self, search_category, mock_client
    ):
        """Test screener with sector and industry filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            sector="Technology", industry="Consumer Electronics"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener",
            {"sector": "Technology", "industry": "Consumer Electronics"},
        )

    @pytest.mark.asyncio
    async def test_screener_with_price_filters(self, search_category, mock_client):
        """Test screener with price filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            price_more_than=100, price_lower_than=500
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"priceMoreThan": 100, "priceLowerThan": 500}
        )

    @pytest.mark.asyncio
    async def test_screener_with_volume_filters(self, search_category, mock_client):
        """Test screener with volume filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            volume_more_than=1000000, volume_lower_than=100000000
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener",
            {"volumeMoreThan": 1000000, "volumeLowerThan": 100000000},
        )

    @pytest.mark.asyncio
    async def test_screener_with_beta_filters(self, search_category, mock_client):
        """Test screener with beta filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(beta_more_than=0.5, beta_lower_than=1.5)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"betaMoreThan": 0.5, "betaLowerThan": 1.5}
        )

    @pytest.mark.asyncio
    async def test_screener_with_dividend_filters(self, search_category, mock_client):
        """Test screener with dividend filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            dividend_more_than=0.5, dividend_lower_than=2.0
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"dividendMoreThan": 0.5, "dividendLowerThan": 2.0}
        )

    @pytest.mark.asyncio
    async def test_screener_with_exchange_and_country(
        self, search_category, mock_client
    ):
        """Test screener with exchange and country filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(exchange="NASDAQ", country="US")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"exchange": "NASDAQ", "country": "US"}
        )

    @pytest.mark.asyncio
    async def test_screener_with_boolean_filters(self, search_category, mock_client):
        """Test screener with boolean filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            is_etf=False, is_fund=False, is_actively_trading=True
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener",
            {"isEtf": False, "isFund": False, "isActivelyTrading": True},
        )

    @pytest.mark.asyncio
    async def test_screener_with_limit_and_share_classes(
        self, search_category, mock_client
    ):
        """Test screener with limit and share classes filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            limit=100, include_all_share_classes=True
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"limit": 100, "includeAllShareClasses": True}
        )

    @pytest.mark.asyncio
    async def test_screener_complex_filters(self, search_category, mock_client):
        """Test screener with multiple complex filters"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            market_cap_more_than=1000000000,
            sector="Technology",
            exchange="NASDAQ",
            country="US",
            is_etf=False,
            limit=50,
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener",
            {
                "marketCapMoreThan": 1000000000,
                "sector": "Technology",
                "exchange": "NASDAQ",
                "country": "US",
                "isEtf": False,
                "limit": 50,
            },
        )

    @pytest.mark.asyncio
    async def test_screener_filters_out_none_values(self, search_category, mock_client):
        """Test that screener filters out None values"""
        mock_response = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await search_category.screener(
            sector="Technology",
            limit=100,
            # These should be filtered out
            market_cap_more_than=None,
            industry=None,
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-screener", {"sector": "Technology", "limit": 100}
        )
