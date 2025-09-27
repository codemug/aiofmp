"""
Unit tests for FMP Discounted Cash Flow (DCF) category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.dcf import DiscountedCashFlowCategory


class TestDiscountedCashFlowCategory:
    """Test cases for DiscountedCashFlowCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def dcf_category(self, mock_client):
        """DCF category instance with mocked client"""
        return DiscountedCashFlowCategory(mock_client)

    @pytest.mark.asyncio
    async def test_dcf_valuation_basic(self, dcf_category, mock_client):
        """Test DCF valuation with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "dcf": 147.2669883190846,
                "Stock Price": 231.795,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.dcf_valuation("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_dcf_valuation_response_structure(self, dcf_category, mock_client):
        """Test DCF valuation response structure"""
        mock_response = [
            {
                "symbol": "MSFT",
                "date": "2025-02-04",
                "dcf": 350.50,
                "Stock Price": 400.25,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.dcf_valuation("MSFT")

        assert len(result) == 1
        assert result[0]["symbol"] == "MSFT"
        assert result[0]["date"] == "2025-02-04"
        assert result[0]["dcf"] == 350.50
        assert result[0]["Stock Price"] == 400.25
        mock_client._make_request.assert_called_once_with(
            "discounted-cash-flow", {"symbol": "MSFT"}
        )

    @pytest.mark.asyncio
    async def test_levered_dcf_basic(self, dcf_category, mock_client):
        """Test levered DCF with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "dcf": 147.2669883190846,
                "Stock Price": 231.795,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.levered_dcf("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "levered-discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_levered_dcf_response_structure(self, dcf_category, mock_client):
        """Test levered DCF response structure"""
        mock_response = [
            {
                "symbol": "GOOGL",
                "date": "2025-02-04",
                "dcf": 125.75,
                "Stock Price": 140.50,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.levered_dcf("GOOGL")

        assert len(result) == 1
        assert result[0]["symbol"] == "GOOGL"
        assert result[0]["date"] == "2025-02-04"
        assert result[0]["dcf"] == 125.75
        assert result[0]["Stock Price"] == 140.50
        mock_client._make_request.assert_called_once_with(
            "levered-discounted-cash-flow", {"symbol": "GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_advanced_basic(self, dcf_category, mock_client):
        """Test custom DCF advanced with required parameters only"""
        mock_response = [
            {
                "year": "2029",
                "symbol": "AAPL",
                "revenue": 657173266965,
                "revenuePercentage": 10.94,
                "ebitda": 205521399637,
                "ebitdaPercentage": 31.27,
                "ebit": 182813984515,
                "ebitPercentage": 27.82,
                "depreciation": 22707415125,
                "depreciationPercentage": 3.46,
                "totalCash": 154056011356,
                "totalCashPercentage": 23.44,
                "receivables": 100795299078,
                "receivablesPercentage": 15.34,
                "inventories": 10202330691,
                "inventoriesPercentage": 1.55,
                "payable": 106124867281,
                "payablePercentage": 16.15,
                "capitalExpenditure": 20111200574,
                "capitalExpenditurePercentage": 3.06,
                "price": 232.8,
                "beta": 1.244,
                "dilutedSharesOutstanding": 15408095000,
                "costofDebt": 3.64,
                "taxRate": 24.09,
                "afterTaxCostOfDebt": 2.76,
                "riskFreeRate": 3.64,
                "marketRiskPremium": 4.72,
                "costOfEquity": 9.51,
                "totalDebt": 106629000000,
                "totalEquity": 3587004516000,
                "totalCapital": 3693633516000,
                "debtWeighting": 2.89,
                "equityWeighting": 97.11,
                "wacc": 9.33,
                "taxRateCash": 14919580,
                "ebiat": 155538906468,
                "ufcf": 197876962552,
                "sumPvUfcf": 616840860880,
                "longTermGrowthRate": 4,
                "terminalValue": 3863553224578,
                "presentTerminalValue": 2473772391290,
                "enterpriseValue": 3090613252170,
                "netDebt": 76686000000,
                "equityValue": 3013927252170,
                "equityValuePerShare": 195.61,
                "freeCashFlowT1": 205792041054,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_advanced("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_advanced_with_parameters(self, dcf_category, mock_client):
        """Test custom DCF advanced with various parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029", "revenue": 657173266965}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_advanced(
            "AAPL",
            revenue_growth_pct=0.109,
            beta=1.244,
            tax_rate=0.149,
            long_term_growth_rate=4.0,
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.109,
            "beta": 1.244,
            "taxRate": 0.149,
            "longTermGrowthRate": 4.0,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", expected_params
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_advanced_with_all_parameters(
        self, dcf_category, mock_client
    ):
        """Test custom DCF advanced with all parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_advanced(
            "AAPL",
            revenue_growth_pct=0.109,
            ebitda_pct=0.313,
            depreciation_and_amortization_pct=0.035,
            cash_and_short_term_investments_pct=0.234,
            receivables_pct=0.153,
            inventories_pct=0.016,
            payable_pct=0.161,
            ebit_pct=0.278,
            capital_expenditure_pct=0.031,
            operating_cash_flow_pct=0.289,
            selling_general_and_administrative_expenses_pct=0.066,
            tax_rate=0.149,
            long_term_growth_rate=4.0,
            cost_of_debt=3.64,
            cost_of_equity=9.512,
            market_risk_premium=4.72,
            beta=1.244,
            risk_free_rate=3.64,
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.109,
            "ebitdaPct": 0.313,
            "depreciationAndAmortizationPct": 0.035,
            "cashAndShortTermInvestmentsPct": 0.234,
            "receivablesPct": 0.153,
            "inventoriesPct": 0.016,
            "payablePct": 0.161,
            "ebitPct": 0.278,
            "capitalExpenditurePct": 0.031,
            "operatingCashFlowPct": 0.289,
            "sellingGeneralAndAdministrativeExpensesPct": 0.066,
            "taxRate": 0.149,
            "longTermGrowthRate": 4.0,
            "costOfDebt": 3.64,
            "costOfEquity": 9.512,
            "marketRiskPremium": 4.72,
            "beta": 1.244,
            "riskFreeRate": 3.64,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", expected_params
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_levered_basic(self, dcf_category, mock_client):
        """Test custom DCF levered with required parameters only"""
        mock_response = [
            {
                "year": "2029",
                "symbol": "AAPL",
                "revenue": 657173266965,
                "revenuePercentage": 10.94,
                "capitalExpenditure": 20111200574,
                "capitalExpenditurePercentage": 3.06,
                "price": 232.8,
                "beta": 1.244,
                "dilutedSharesOutstanding": 15408095000,
                "costofDebt": 3.64,
                "taxRate": 24.09,
                "afterTaxCostOfDebt": 2.76,
                "riskFreeRate": 3.64,
                "marketRiskPremium": 4.72,
                "costOfEquity": 9.51,
                "totalDebt": 106629000000,
                "totalEquity": 3587004516000,
                "totalCapital": 3693633516000,
                "debtWeighting": 2.89,
                "equityWeighting": 97.11,
                "wacc": 9.33,
                "operatingCashFlow": 189682120638,
                "pvLfcf": 134327365439,
                "sumPvLfcf": 652368547936,
                "longTermGrowthRate": 4,
                "freeCashFlow": 209793321212,
                "terminalValue": 4096220460472,
                "presentTerminalValue": 2622745564702,
                "enterpriseValue": 3275114112638,
                "netDebt": 76686000000,
                "equityValue": 3198428112638,
                "equityValuePerShare": 207.58,
                "freeCashFlowT1": 218185054060,
                "operatingCashFlowPercentage": 28.86,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_levered("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "custom-levered-discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_levered_with_parameters(self, dcf_category, mock_client):
        """Test custom DCF levered with various parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029", "revenue": 657173266965}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_levered(
            "AAPL",
            revenue_growth_pct=0.109,
            beta=1.244,
            cost_of_debt=3.64,
            cost_of_equity=9.512,
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.109,
            "beta": 1.244,
            "costOfDebt": 3.64,
            "costOfEquity": 9.512,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-levered-discounted-cash-flow", expected_params
        )

    @pytest.mark.asyncio
    async def test_custom_dcf_levered_with_all_parameters(
        self, dcf_category, mock_client
    ):
        """Test custom DCF levered with all parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_levered(
            "AAPL",
            revenue_growth_pct=0.109,
            ebitda_pct=0.313,
            depreciation_and_amortization_pct=0.035,
            cash_and_short_term_investments_pct=0.234,
            receivables_pct=0.153,
            inventories_pct=0.016,
            payable_pct=0.161,
            ebit_pct=0.278,
            capital_expenditure_pct=0.031,
            operating_cash_flow_pct=0.289,
            selling_general_and_administrative_expenses_pct=0.066,
            tax_rate=0.149,
            long_term_growth_rate=4.0,
            cost_of_debt=3.64,
            cost_of_equity=9.512,
            market_risk_premium=4.72,
            beta=1.244,
            risk_free_rate=3.64,
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.109,
            "ebitdaPct": 0.313,
            "depreciationAndAmortizationPct": 0.035,
            "cashAndShortTermInvestmentsPct": 0.234,
            "receivablesPct": 0.153,
            "inventoriesPct": 0.016,
            "payablePct": 0.161,
            "ebitPct": 0.278,
            "capitalExpenditurePct": 0.031,
            "operatingCashFlowPct": 0.289,
            "sellingGeneralAndAdministrativeExpensesPct": 0.066,
            "taxRate": 0.149,
            "longTermGrowthRate": 4.0,
            "costOfDebt": 3.64,
            "costOfEquity": 9.512,
            "marketRiskPremium": 4.72,
            "beta": 1.244,
            "riskFreeRate": 3.64,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-levered-discounted-cash-flow", expected_params
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, dcf_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await dcf_category.dcf_valuation("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, dcf_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple years
        large_response = [
            {
                "year": f"202{i}",
                "symbol": "AAPL",
                "revenue": 500000000000 + (i - 5) * 50000000000,
                "dcf": 100.0 + (i - 5) * 10.0,
                "equityValuePerShare": 150.0 + (i - 5) * 15.0,
            }
            for i in range(5, 10)
        ]
        mock_client._make_request.return_value = large_response

        result = await dcf_category.custom_dcf_advanced(
            "AAPL", revenue_growth_pct=0.109
        )

        assert len(result) == 5
        assert result[0]["year"] == "2025"
        assert result[4]["year"] == "2029"
        assert result[0]["revenue"] == 500000000000
        assert result[4]["revenue"] == 700000000000
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL", "revenueGrowthPct": 0.109}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, dcf_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04",
                "dcf": 147.27,
                "Stock Price": 231.795,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.dcf_valuation("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, dcf_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        # Test with only revenue growth
        result = await dcf_category.custom_dcf_advanced(
            "AAPL", revenue_growth_pct=0.109
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL", "revenueGrowthPct": 0.109}
        )

        # Test with only beta
        result = await dcf_category.custom_dcf_advanced("AAPL", beta=1.244)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL", "beta": 1.244}
        )

        # Test with only tax rate
        result = await dcf_category.custom_dcf_advanced("AAPL", tax_rate=0.149)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL", "taxRate": 0.149}
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, dcf_category, mock_client):
        """Test DCF functionality with different symbols"""
        mock_response = [{"symbol": "MSFT", "dcf": 350.50}]
        mock_client._make_request.return_value = mock_response

        # Test with Microsoft
        result = await dcf_category.dcf_valuation("MSFT")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "discounted-cash-flow", {"symbol": "MSFT"}
        )

        # Test with Google
        result = await dcf_category.levered_dcf("GOOGL")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "levered-discounted-cash-flow", {"symbol": "GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_float_parameter_handling(self, dcf_category, mock_client):
        """Test handling of float parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        # Test with various float values
        result = await dcf_category.custom_dcf_advanced(
            "AAPL",
            revenue_growth_pct=0.1094119804597946,
            ebitda_pct=0.31273548388,
            beta=1.244,
            tax_rate=0.14919579658453103,
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.1094119804597946,
            "ebitdaPct": 0.31273548388,
            "beta": 1.244,
            "taxRate": 0.14919579658453103,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", expected_params
        )

    @pytest.mark.asyncio
    async def test_none_parameter_handling(self, dcf_category, mock_client):
        """Test that None parameters are not included in the request"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_advanced(
            "AAPL", revenue_growth_pct=None, beta=None, tax_rate=None
        )

        assert result == mock_response
        # Only symbol should be included, None values should be filtered out
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_zero_parameter_handling(self, dcf_category, mock_client):
        """Test handling of zero values in parameters"""
        mock_response = [{"symbol": "AAPL", "year": "2029"}]
        mock_client._make_request.return_value = mock_response

        result = await dcf_category.custom_dcf_advanced(
            "AAPL", revenue_growth_pct=0.0, beta=0.0, tax_rate=0.0
        )

        assert result == mock_response
        expected_params = {
            "symbol": "AAPL",
            "revenueGrowthPct": 0.0,
            "beta": 0.0,
            "taxRate": 0.0,
        }
        mock_client._make_request.assert_called_once_with(
            "custom-discounted-cash-flow", expected_params
        )
