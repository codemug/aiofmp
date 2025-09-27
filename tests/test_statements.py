"""
Unit tests for FMP Statements category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.statements import StatementsCategory


class TestStatementsCategory:
    """Test cases for StatementsCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def statements_category(self, mock_client):
        """Statements category instance with mocked client"""
        return StatementsCategory(mock_client)

    @pytest.mark.asyncio
    async def test_income_statement_basic(self, statements_category, mock_client):
        """Test income statement with required parameters only"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "cik": "0000320193",
                "filingDate": "2024-11-01",
                "acceptedDate": "2024-11-01 06:01:36",
                "fiscalYear": "2024",
                "period": "FY",
                "revenue": 391035000000,
                "costOfRevenue": 210352000000,
                "grossProfit": 180683000000,
                "netIncome": 93736000000,
                "eps": 6.11,
                "epsDiluted": 6.08,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_income_statement_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test income statement with optional parameters"""
        mock_response = [
            {"symbol": "AAPL", "revenue": 391035000000, "netIncome": 93736000000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement(
            "AAPL", limit=5, period="annual"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL", "limit": 5, "period": "annual"}
        )

    @pytest.mark.asyncio
    async def test_balance_sheet_statement_basic(
        self, statements_category, mock_client
    ):
        """Test balance sheet statement with required parameters only"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "cik": "0000320193",
                "fiscalYear": "2024",
                "period": "FY",
                "totalAssets": 364980000000,
                "totalLiabilities": 308030000000,
                "totalStockholdersEquity": 56950000000,
                "cashAndCashEquivalents": 29943000000,
                "totalDebt": 106629000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.balance_sheet_statement("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "balance-sheet-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_balance_sheet_statement_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test balance sheet statement with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "totalAssets": 364980000000,
                "totalLiabilities": 308030000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.balance_sheet_statement(
            "AAPL", limit=3, period="quarter"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "balance-sheet-statement",
            {"symbol": "AAPL", "limit": 3, "period": "quarter"},
        )

    @pytest.mark.asyncio
    async def test_cash_flow_statement_basic(self, statements_category, mock_client):
        """Test cash flow statement with required parameters only"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "fiscalYear": "2024",
                "period": "FY",
                "netIncome": 93736000000,
                "operatingCashFlow": 118254000000,
                "investingCashFlow": 2935000000,
                "financingCashFlow": -121983000000,
                "freeCashFlow": 108807000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.cash_flow_statement("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "cash-flow-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_cash_flow_statement_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test cash flow statement with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "operatingCashFlow": 118254000000,
                "freeCashFlow": 108807000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.cash_flow_statement(
            "AAPL", limit=4, period="Q4"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "cash-flow-statement", {"symbol": "AAPL", "limit": 4, "period": "Q4"}
        )

    @pytest.mark.asyncio
    async def test_key_metrics_basic(self, statements_category, mock_client):
        """Test key metrics with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "marketCap": 3495160329570,
                "enterpriseValue": 3571846329570,
                "evToSales": 9.134339201273542,
                "currentRatio": 0.8673125765340832,
                "returnOnEquity": 1.6459350307287095,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.key_metrics("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "key-metrics", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_key_metrics_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test key metrics with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "marketCap": 3495160329570,
                "enterpriseValue": 3571846329570,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.key_metrics("AAPL", limit=2, period="annual")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "key-metrics", {"symbol": "AAPL", "limit": 2, "period": "annual"}
        )

    @pytest.mark.asyncio
    async def test_financial_ratios_basic(self, statements_category, mock_client):
        """Test financial ratios with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "grossProfitMargin": 0.4620634981523393,
                "ebitMargin": 0.31510222870075566,
                "netProfitMargin": 0.23971255769943867,
                "currentRatio": 0.8673125765340832,
                "debtToEquityRatio": 1.872326602282704,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_ratios("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("ratios", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_financial_ratios_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test financial ratios with optional parameters"""
        mock_response = [
            {"symbol": "AAPL", "grossProfitMargin": 0.462, "netProfitMargin": 0.240}
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_ratios(
            "AAPL", limit=1, period="Q4"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ratios", {"symbol": "AAPL", "limit": 1, "period": "Q4"}
        )

    @pytest.mark.asyncio
    async def test_financial_scores_basic(self, statements_category, mock_client):
        """Test financial scores with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "altmanZScore": 9.322985825443649,
                "piotroskiScore": 8,
                "workingCapital": -11125000000,
                "totalAssets": 344085000000,
                "ebit": 125675000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_scores("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "financial-scores", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_owner_earnings_basic(self, statements_category, mock_client):
        """Test owner earnings with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "fiscalYear": "2025",
                "period": "Q1",
                "date": "2024-12-28",
                "averagePPE": 0.13969,
                "maintenanceCapex": -2279964750,
                "ownersEarnings": 27655035250,
                "ownersEarningsPerShare": 1.83,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.owner_earnings("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "owner-earnings", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_owner_earnings_with_limit(self, statements_category, mock_client):
        """Test owner earnings with limit parameter"""
        mock_response = [
            {
                "symbol": "AAPL",
                "ownersEarnings": 27655035250,
                "ownersEarningsPerShare": 1.83,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.owner_earnings("AAPL", limit=3)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "owner-earnings", {"symbol": "AAPL", "limit": 3}
        )

    @pytest.mark.asyncio
    async def test_enterprise_values_basic(self, statements_category, mock_client):
        """Test enterprise values with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "stockPrice": 227.79,
                "numberOfShares": 15343783000,
                "marketCapitalization": 3495160329570,
                "enterpriseValue": 3571846329570,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.enterprise_values("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "enterprise-values", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_enterprise_values_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test enterprise values with optional parameters"""
        mock_response = [{"symbol": "AAPL", "enterpriseValue": 3571846329570}]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.enterprise_values(
            "AAPL", limit=2, period="quarter"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "enterprise-values", {"symbol": "AAPL", "limit": 2, "period": "quarter"}
        )

    @pytest.mark.asyncio
    async def test_income_statement_growth_basic(
        self, statements_category, mock_client
    ):
        """Test income statement growth with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "growthRevenue": 0.020219940775141214,
                "growthGrossProfit": 0.06819471705252206,
                "growthNetIncome": -0.033599670086086914,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement_growth("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "income-statement-growth", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_income_statement_growth_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test income statement growth with optional parameters"""
        mock_response = [
            {"symbol": "AAPL", "growthRevenue": 0.0202, "growthNetIncome": -0.0336}
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement_growth(
            "AAPL", limit=4, period="annual"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "income-statement-growth",
            {"symbol": "AAPL", "limit": 4, "period": "annual"},
        )

    @pytest.mark.asyncio
    async def test_balance_sheet_statement_growth_basic(
        self, statements_category, mock_client
    ):
        """Test balance sheet statement growth with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "growthTotalAssets": 0.035160515396374756,
                "growthTotalLiabilities": 0.060574238130816666,
                "growthTotalEquity": -0.0836095645737457,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.balance_sheet_statement_growth("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "balance-sheet-statement-growth", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_balance_sheet_statement_growth_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test balance sheet statement growth with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "growthTotalAssets": 0.0352,
                "growthTotalEquity": -0.0836,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.balance_sheet_statement_growth(
            "AAPL", limit=3, period="Q4"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "balance-sheet-statement-growth",
            {"symbol": "AAPL", "limit": 3, "period": "Q4"},
        )

    @pytest.mark.asyncio
    async def test_cash_flow_statement_growth_basic(
        self, statements_category, mock_client
    ):
        """Test cash flow statement growth with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "growthNetIncome": -0.033599670086086914,
                "growthOperatingCashFlow": 0.06975566069312394,
                "growthFreeCashFlow": 0.092615279562982,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.cash_flow_statement_growth("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "cash-flow-statement-growth", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_cash_flow_statement_growth_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test cash flow statement growth with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "growthOperatingCashFlow": 0.0698,
                "growthFreeCashFlow": 0.0926,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.cash_flow_statement_growth(
            "AAPL", limit=2, period="annual"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "cash-flow-statement-growth",
            {"symbol": "AAPL", "limit": 2, "period": "annual"},
        )

    @pytest.mark.asyncio
    async def test_financial_statement_growth_basic(
        self, statements_category, mock_client
    ):
        """Test financial statement growth with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "fiscalYear": "2024",
                "period": "FY",
                "reportedCurrency": "USD",
                "revenueGrowth": 0.020219940775141214,
                "grossProfitGrowth": 0.06819471705252206,
                "netIncomeGrowth": -0.033599670086086914,
                "operatingCashFlowGrowth": 0.06975566069312394,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_statement_growth("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "financial-growth", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_financial_statement_growth_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test financial statement growth with optional parameters"""
        mock_response = [
            {"symbol": "AAPL", "revenueGrowth": 0.0202, "netIncomeGrowth": -0.0336}
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_statement_growth(
            "AAPL", limit=5, period="quarter"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "financial-growth", {"symbol": "AAPL", "limit": 5, "period": "quarter"}
        )

    @pytest.mark.asyncio
    async def test_revenue_product_segmentation_basic(
        self, statements_category, mock_client
    ):
        """Test revenue product segmentation with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "fiscalYear": 2024,
                "period": "FY",
                "reportedCurrency": None,
                "date": "2024-09-28",
                "data": {
                    "Mac": 29984000000,
                    "Service": 96169000000,
                    "iPhone": 201183000000,
                },
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.revenue_product_segmentation("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "revenue-product-segmentation", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_revenue_product_segmentation_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test revenue product segmentation with optional parameters"""
        mock_response = [
            {"symbol": "AAPL", "data": {"iPhone": 201183000000, "Mac": 29984000000}}
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.revenue_product_segmentation(
            "AAPL", period="quarter", structure="flat"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "revenue-product-segmentation",
            {"symbol": "AAPL", "period": "quarter", "structure": "flat"},
        )

    @pytest.mark.asyncio
    async def test_revenue_geographic_segmentation_basic(
        self, statements_category, mock_client
    ):
        """Test revenue geographic segmentation with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "fiscalYear": 2024,
                "period": "FY",
                "reportedCurrency": None,
                "date": "2024-09-28",
                "data": {
                    "Americas Segment": 167045000000,
                    "Europe Segment": 101328000000,
                    "Greater China Segment": 66952000000,
                },
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.revenue_geographic_segmentation("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "revenue-geographic-segmentation", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_revenue_geographic_segmentation_with_optional_params(
        self, statements_category, mock_client
    ):
        """Test revenue geographic segmentation with optional parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "data": {"Americas": 167045000000, "Europe": 101328000000},
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.revenue_geographic_segmentation(
            "AAPL", period="annual", structure="flat"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "revenue-geographic-segmentation",
            {"symbol": "AAPL", "period": "annual", "structure": "flat"},
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, statements_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await statements_category.income_statement("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, statements_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple periods
        large_response = [
            {
                "symbol": "AAPL",
                "date": f"2024-{i:02d}-28",
                "fiscalYear": "2024",
                "period": f"Q{((i - 1) % 4) + 1}",
                "revenue": 391035000000 + (i * 1000000000),
                "netIncome": 93736000000 + (i * 500000000),
            }
            for i in range(1, 21)  # 20 periods
        ]
        mock_client._make_request.return_value = large_response

        result = await statements_category.income_statement("AAPL", limit=20)

        assert len(result) == 20
        assert result[0]["period"] == "Q1"
        assert result[19]["period"] == "Q4"
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL", "limit": 20}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(
        self, statements_category, mock_client
    ):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2024-09-28",
                "revenue": 391035000000,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, statements_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"symbol": "AAPL", "revenue": 391035000000}]
        mock_client._make_request.return_value = mock_response

        # Test with only limit
        result = await statements_category.income_statement("AAPL", limit=5)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "AAPL", "limit": 5}
        )

        # Test with only period
        result = await statements_category.income_statement("AAPL", period="annual")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "AAPL", "period": "annual"}
        )

        # Test with both parameters
        result = await statements_category.income_statement(
            "AAPL", limit=5, period="annual"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "AAPL", "limit": 5, "period": "annual"}
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, statements_category, mock_client):
        """Test statements functionality with different symbols"""
        mock_response = [{"symbol": "MSFT", "revenue": 211915000000}]
        mock_client._make_request.return_value = mock_response

        # Test with Microsoft
        result = await statements_category.income_statement("MSFT")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "MSFT"}
        )

        # Test with Google
        result = await statements_category.income_statement("GOOGL")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "GOOGL"}
        )

        # Test with Tesla
        result = await statements_category.income_statement("TSLA")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "income-statement", {"symbol": "TSLA"}
        )

    @pytest.mark.asyncio
    async def test_income_statement_response_validation(
        self, statements_category, mock_client
    ):
        """Test income statement response validation"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "cik": "0000320193",
                "fiscalYear": "2024",
                "period": "FY",
                "revenue": 391035000000,
                "costOfRevenue": 210352000000,
                "grossProfit": 180683000000,
                "netIncome": 93736000000,
                "eps": 6.11,
                "epsDiluted": 6.08,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.income_statement("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["date"] == "2024-09-28"
        assert result[0]["revenue"] == 391035000000
        assert result[0]["netIncome"] == 93736000000
        assert result[0]["eps"] == 6.11
        mock_client._make_request.assert_called_once_with(
            "income-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_balance_sheet_response_validation(
        self, statements_category, mock_client
    ):
        """Test balance sheet response validation"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "fiscalYear": "2024",
                "period": "FY",
                "totalAssets": 364980000000,
                "totalLiabilities": 308030000000,
                "totalStockholdersEquity": 56950000000,
                "cashAndCashEquivalents": 29943000000,
                "totalDebt": 106629000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.balance_sheet_statement("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["date"] == "2024-09-28"
        assert result[0]["totalAssets"] == 364980000000
        assert result[0]["totalLiabilities"] == 308030000000
        assert result[0]["totalStockholdersEquity"] == 56950000000
        mock_client._make_request.assert_called_once_with(
            "balance-sheet-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_cash_flow_response_validation(
        self, statements_category, mock_client
    ):
        """Test cash flow response validation"""
        mock_response = [
            {
                "date": "2024-09-28",
                "symbol": "AAPL",
                "fiscalYear": "2024",
                "period": "FY",
                "netIncome": 93736000000,
                "operatingCashFlow": 118254000000,
                "investingCashFlow": 2935000000,
                "financingCashFlow": -121983000000,
                "freeCashFlow": 108807000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.cash_flow_statement("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["date"] == "2024-09-28"
        assert result[0]["netIncome"] == 93736000000
        assert result[0]["operatingCashFlow"] == 118254000000
        assert result[0]["freeCashFlow"] == 108807000000
        mock_client._make_request.assert_called_once_with(
            "cash-flow-statement", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_financial_scores_response_validation(
        self, statements_category, mock_client
    ):
        """Test financial scores response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "reportedCurrency": "USD",
                "altmanZScore": 9.322985825443649,
                "piotroskiScore": 8,
                "workingCapital": -11125000000,
                "totalAssets": 344085000000,
                "ebit": 125675000000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.financial_scores("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["altmanZScore"] == 9.322985825443649
        assert result[0]["piotroskiScore"] == 8
        assert result[0]["workingCapital"] == -11125000000
        mock_client._make_request.assert_called_once_with(
            "financial-scores", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_revenue_segmentation_response_validation(
        self, statements_category, mock_client
    ):
        """Test revenue segmentation response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "fiscalYear": 2024,
                "period": "FY",
                "date": "2024-09-28",
                "data": {
                    "Mac": 29984000000,
                    "Service": 96169000000,
                    "iPhone": 201183000000,
                },
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await statements_category.revenue_product_segmentation("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["fiscalYear"] == 2024
        assert result[0]["period"] == "FY"
        assert result[0]["data"]["iPhone"] == 201183000000
        assert result[0]["data"]["Mac"] == 29984000000
        assert result[0]["data"]["Service"] == 96169000000
        mock_client._make_request.assert_called_once_with(
            "revenue-product-segmentation", {"symbol": "AAPL"}
        )
