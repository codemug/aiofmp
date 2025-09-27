"""
Unit tests for FMP Analyst category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.analyst import AnalystCategory
from aiofmp.base import FMPBaseClient


class TestAnalystCategory:
    """Test cases for AnalystCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def analyst_category(self, mock_client):
        """Analyst category instance with mocked client"""
        return AnalystCategory(mock_client)

    @pytest.mark.asyncio
    async def test_financial_estimates_basic(self, analyst_category, mock_client):
        """Test financial estimates with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2029-09-28",
                "revenueAvg": 483093000000,
                "epsAvg": 9.68,
                "numAnalystsRevenue": 16,
                "numAnalystsEps": 6,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.financial_estimates("AAPL", "annual")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "analyst-estimates", {"symbol": "AAPL", "period": "annual"}
        )

    @pytest.mark.asyncio
    async def test_financial_estimates_with_optional_params(
        self, analyst_category, mock_client
    ):
        """Test financial estimates with all parameters"""
        mock_response = [{"symbol": "AAPL", "revenueAvg": 483093000000}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.financial_estimates(
            "AAPL", "quarter", page=2, limit=20
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "analyst-estimates",
            {"symbol": "AAPL", "period": "quarter", "page": 2, "limit": 20},
        )

    @pytest.mark.asyncio
    async def test_ratings_snapshot_basic(self, analyst_category, mock_client):
        """Test ratings snapshot with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "rating": "A-",
                "overallScore": 4,
                "discountedCashFlowScore": 3,
                "returnOnEquityScore": 5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.ratings_snapshot("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ratings-snapshot", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_ratings_snapshot_with_limit(self, analyst_category, mock_client):
        """Test ratings snapshot with limit parameter"""
        mock_response = [{"symbol": "AAPL", "rating": "A-"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.ratings_snapshot("AAPL", limit=5)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ratings-snapshot", {"symbol": "AAPL", "limit": 5}
        )

    @pytest.mark.asyncio
    async def test_historical_ratings_basic(self, analyst_category, mock_client):
        """Test historical ratings with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2025-02-04", "rating": "A-", "overallScore": 4}
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.historical_ratings("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ratings-historical", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_ratings_with_limit(self, analyst_category, mock_client):
        """Test historical ratings with limit parameter"""
        mock_response = [{"symbol": "AAPL", "date": "2025-02-04"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.historical_ratings("AAPL", limit=10)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ratings-historical", {"symbol": "AAPL", "limit": 10}
        )

    @pytest.mark.asyncio
    async def test_price_target_summary(self, analyst_category, mock_client):
        """Test price target summary"""
        mock_response = [
            {
                "symbol": "AAPL",
                "lastMonthCount": 1,
                "lastMonthAvgPriceTarget": 200.75,
                "lastQuarterCount": 3,
                "lastQuarterAvgPriceTarget": 204.2,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_summary("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-summary", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_price_target_consensus(self, analyst_category, mock_client):
        """Test price target consensus"""
        mock_response = [
            {
                "symbol": "AAPL",
                "targetHigh": 300,
                "targetLow": 200,
                "targetConsensus": 251.7,
                "targetMedian": 258,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_consensus("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-consensus", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_price_target_news_basic(self, analyst_category, mock_client):
        """Test price target news with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "newsTitle": "Apple Gets Rare Downgrade",
                "analystName": "Edison Lee",
                "priceTarget": 200.75,
                "newsPublisher": "Benzinga",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_news("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-news", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_price_target_news_with_optional_params(
        self, analyst_category, mock_client
    ):
        """Test price target news with all parameters"""
        mock_response = [{"symbol": "AAPL", "newsTitle": "Test"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_news("AAPL", page=1, limit=5)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-news", {"symbol": "AAPL", "page": 1, "limit": 5}
        )

    @pytest.mark.asyncio
    async def test_price_target_latest_news_basic(self, analyst_category, mock_client):
        """Test price target latest news with no parameters"""
        mock_response = [
            {
                "symbol": "OLN",
                "newsTitle": "Analysts Cut Forecasts",
                "analystName": "Peter Osterland",
                "priceTarget": 32,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_latest_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-latest-news", {}
        )

    @pytest.mark.asyncio
    async def test_price_target_latest_news_with_params(
        self, analyst_category, mock_client
    ):
        """Test price target latest news with parameters"""
        mock_response = [{"symbol": "OLN", "newsTitle": "Test"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.price_target_latest_news(page=2, limit=15)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "price-target-latest-news", {"page": 2, "limit": 15}
        )

    @pytest.mark.asyncio
    async def test_stock_grades(self, analyst_category, mock_client):
        """Test stock grades"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-01-31",
                "gradingCompany": "Morgan Stanley",
                "previousGrade": "Overweight",
                "newGrade": "Overweight",
                "action": "maintain",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grades("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("grades", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_historical_stock_grades_basic(self, analyst_category, mock_client):
        """Test historical stock grades with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-01",
                "analystRatingsBuy": 8,
                "analystRatingsHold": 14,
                "analystRatingsSell": 2,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.historical_stock_grades("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-historical", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_stock_grades_with_limit(
        self, analyst_category, mock_client
    ):
        """Test historical stock grades with limit parameter"""
        mock_response = [{"symbol": "AAPL", "analystRatingsBuy": 8}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.historical_stock_grades("AAPL", limit=50)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-historical", {"symbol": "AAPL", "limit": 50}
        )

    @pytest.mark.asyncio
    async def test_stock_grades_summary(self, analyst_category, mock_client):
        """Test stock grades summary"""
        mock_response = [
            {
                "symbol": "AAPL",
                "strongBuy": 1,
                "buy": 29,
                "hold": 11,
                "sell": 4,
                "strongSell": 0,
                "consensus": "Buy",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grades_summary("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-consensus", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_stock_grade_news_basic(self, analyst_category, mock_client):
        """Test stock grade news with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "newsTitle": "Why Apple Shares Are Trading Higher",
                "newGrade": "Buy",
                "previousGrade": "Hold",
                "gradingCompany": "Maxim Group",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grade_news("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-news", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_stock_grade_news_with_optional_params(
        self, analyst_category, mock_client
    ):
        """Test stock grade news with all parameters"""
        mock_response = [{"symbol": "AAPL", "newsTitle": "Test"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grade_news("AAPL", page=1, limit=5)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-news", {"symbol": "AAPL", "page": 1, "limit": 5}
        )

    @pytest.mark.asyncio
    async def test_stock_grade_latest_news_basic(self, analyst_category, mock_client):
        """Test stock grade latest news with no parameters"""
        mock_response = [
            {
                "symbol": "PYPL",
                "newsTitle": "PayPal Beats Q4 Estimates",
                "newGrade": "Overweight",
                "gradingCompany": "J.P. Morgan",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grade_latest_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("grades-latest-news", {})

    @pytest.mark.asyncio
    async def test_stock_grade_latest_news_with_params(
        self, analyst_category, mock_client
    ):
        """Test stock grade latest news with parameters"""
        mock_response = [{"symbol": "PYPL", "newsTitle": "Test"}]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.stock_grade_latest_news(page=2, limit=15)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "grades-latest-news", {"page": 2, "limit": 15}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, analyst_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await analyst_category.financial_estimates("AAPL", "annual")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "analyst-estimates", {"symbol": "AAPL", "period": "annual"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, analyst_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {
                "symbol": "AAPL",
                "date": f"202{i}-01-01",
                "revenueAvg": 100000000000 + i * 10000000000,
            }
            for i in range(100)
        ]
        mock_client._make_request.return_value = large_response

        result = await analyst_category.financial_estimates("AAPL", "annual", limit=100)

        assert len(result) == 100
        assert result[0]["revenueAvg"] == 100000000000
        assert result[99]["revenueAvg"] == 1090000000000
        mock_client._make_request.assert_called_once_with(
            "analyst-estimates", {"symbol": "AAPL", "period": "annual", "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, analyst_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "rating": "A-",
                "overallScore": 4,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await analyst_category.ratings_snapshot("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "ratings-snapshot", {"symbol": "AAPL"}
        )
