"""
Unit tests for FMP Economics category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.economics import EconomicsCategory


class TestEconomicsCategory:
    """Test cases for EconomicsCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def economics_category(self, mock_client):
        """Economics category instance with mocked client"""
        return EconomicsCategory(mock_client)

    @pytest.mark.asyncio
    async def test_treasury_rates_basic(self, economics_category, mock_client):
        """Test treasury rates with no parameters"""
        mock_response = [
            {
                "date": "2024-02-29",
                "month1": 5.53,
                "month2": 5.5,
                "month3": 5.45,
                "month6": 5.3,
                "year1": 5.01,
                "year2": 4.64,
                "year3": 4.43,
                "year5": 4.26,
                "year7": 4.28,
                "year10": 4.25,
                "year20": 4.51,
                "year30": 4.38,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("treasury-rates", {})

    @pytest.mark.asyncio
    async def test_treasury_rates_with_dates(self, economics_category, mock_client):
        """Test treasury rates with date parameters"""
        mock_response = [{"date": "2024-02-29", "year10": 4.25}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates("2025-04-24", "2025-07-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "treasury-rates", {"from": "2025-04-24", "to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_treasury_rates_with_from_date_only(
        self, economics_category, mock_client
    ):
        """Test treasury rates with only from_date parameter"""
        mock_response = [{"date": "2024-02-29", "year10": 4.25}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates(from_date="2025-04-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "treasury-rates", {"from": "2025-04-24"}
        )

    @pytest.mark.asyncio
    async def test_treasury_rates_with_to_date_only(
        self, economics_category, mock_client
    ):
        """Test treasury rates with only to_date parameter"""
        mock_response = [{"date": "2024-02-29", "year10": 4.25}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates(to_date="2025-07-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "treasury-rates", {"to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_basic(self, economics_category, mock_client):
        """Test economic indicators with required parameters only"""
        mock_response = [{"name": "GDP", "date": "2024-01-01", "value": 28624.069}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_indicators("GDP")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-indicators", {"name": "GDP"}
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_with_dates(
        self, economics_category, mock_client
    ):
        """Test economic indicators with date parameters"""
        mock_response = [{"name": "GDP", "date": "2024-01-01", "value": 28624.069}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_indicators(
            "GDP", "2024-07-24", "2025-07-24"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-indicators",
            {"name": "GDP", "from": "2024-07-24", "to": "2025-07-24"},
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_with_from_date_only(
        self, economics_category, mock_client
    ):
        """Test economic indicators with only from_date parameter"""
        mock_response = [{"name": "CPI", "date": "2024-01-01", "value": 308.417}]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_indicators(
            "CPI", from_date="2024-07-24"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-indicators", {"name": "CPI", "from": "2024-07-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_with_to_date_only(
        self, economics_category, mock_client
    ):
        """Test economic indicators with only to_date parameter"""
        mock_response = [
            {"name": "unemploymentRate", "date": "2024-01-01", "value": 3.7}
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_indicators(
            "unemploymentRate", to_date="2025-07-24"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-indicators", {"name": "unemploymentRate", "to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_different_names(
        self, economics_category, mock_client
    ):
        """Test economic indicators with different indicator names"""
        mock_response = [{"name": "federalFunds", "date": "2024-01-01", "value": 5.33}]
        mock_client._make_request.return_value = mock_response

        # Test with federal funds rate
        result = await economics_category.economic_indicators("federalFunds")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "federalFunds"}
        )

        # Test with inflation rate
        result = await economics_category.economic_indicators("inflationRate")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "inflationRate"}
        )

        # Test with retail sales
        result = await economics_category.economic_indicators("retailSales")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "retailSales"}
        )

    @pytest.mark.asyncio
    async def test_economic_calendar_basic(self, economics_category, mock_client):
        """Test economic calendar with no parameters"""
        mock_response = [
            {
                "date": "2024-03-01 03:35:00",
                "country": "JP",
                "event": "3-Month Bill Auction",
                "currency": "JPY",
                "previous": -0.112,
                "estimate": None,
                "actual": -0.096,
                "change": 0.016,
                "impact": "Low",
                "changePercentage": 14.286,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_calendar()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("economic-calendar", {})

    @pytest.mark.asyncio
    async def test_economic_calendar_with_dates(self, economics_category, mock_client):
        """Test economic calendar with date parameters"""
        mock_response = [
            {"date": "2024-03-01 03:35:00", "event": "3-Month Bill Auction"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_calendar("2025-04-24", "2025-07-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-calendar", {"from": "2025-04-24", "to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_calendar_with_from_date_only(
        self, economics_category, mock_client
    ):
        """Test economic calendar with only from_date parameter"""
        mock_response = [
            {"date": "2024-03-01 03:35:00", "event": "3-Month Bill Auction"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_calendar(from_date="2025-04-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-calendar", {"from": "2025-04-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_calendar_with_to_date_only(
        self, economics_category, mock_client
    ):
        """Test economic calendar with only to_date parameter"""
        mock_response = [
            {"date": "2024-03-01 03:35:00", "event": "3-Month Bill Auction"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_calendar(to_date="2025-07-24")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "economic-calendar", {"to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_market_risk_premium_basic(self, economics_category, mock_client):
        """Test market risk premium with no parameters"""
        mock_response = [
            {
                "country": "Zimbabwe",
                "continent": "Africa",
                "countryRiskPremium": 13.17,
                "totalEquityRiskPremium": 17.77,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.market_risk_premium()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("market-risk-premium", {})

    @pytest.mark.asyncio
    async def test_market_risk_premium_response_structure(
        self, economics_category, mock_client
    ):
        """Test market risk premium response structure"""
        mock_response = [
            {
                "country": "United States",
                "continent": "North America",
                "countryRiskPremium": 0.0,
                "totalEquityRiskPremium": 4.72,
            },
            {
                "country": "Germany",
                "continent": "Europe",
                "countryRiskPremium": 0.0,
                "totalEquityRiskPremium": 4.72,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.market_risk_premium()

        assert len(result) == 2
        assert result[0]["country"] == "United States"
        assert result[0]["continent"] == "North America"
        assert result[0]["countryRiskPremium"] == 0.0
        assert result[0]["totalEquityRiskPremium"] == 4.72
        assert result[1]["country"] == "Germany"
        assert result[1]["continent"] == "Europe"
        mock_client._make_request.assert_called_once_with("market-risk-premium", {})

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, economics_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await economics_category.treasury_rates()

        assert result == []
        mock_client._make_request.assert_called_once_with("treasury-rates", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, economics_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple dates
        large_response = [
            {
                "date": f"2024-{i:02d}-01",
                "month1": 5.0 + i * 0.1,
                "year10": 4.0 + i * 0.05,
                "year30": 4.5 + i * 0.03,
            }
            for i in range(1, 13)  # 12 months
        ]
        mock_client._make_request.return_value = large_response

        result = await economics_category.treasury_rates("2024-01-01", "2024-12-31")

        assert len(result) == 12
        assert result[0]["date"] == "2024-01-01"
        assert result[11]["date"] == "2024-12-01"
        assert result[0]["month1"] == 5.1
        assert result[11]["month1"] == 6.2
        mock_client._make_request.assert_called_once_with(
            "treasury-rates", {"from": "2024-01-01", "to": "2024-12-31"}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, economics_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "date": "2024-02-29",
                "month1": 5.53,
                "year10": 4.25,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("treasury-rates", {})

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, economics_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"date": "2024-02-29", "year10": 4.25}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await economics_category.treasury_rates("2025-04-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "treasury-rates", {"from": "2025-04-24"}
        )

        # Test with only to_date
        result = await economics_category.treasury_rates(to_date="2025-07-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "treasury-rates", {"to": "2025-07-24"}
        )

        # Test with both dates
        result = await economics_category.treasury_rates("2025-04-24", "2025-07-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "treasury-rates", {"from": "2025-04-24", "to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_economic_indicators_parameter_combinations(
        self, economics_category, mock_client
    ):
        """Test various parameter combinations for economic indicators"""
        mock_response = [{"name": "GDP", "date": "2024-01-01", "value": 28624.069}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await economics_category.economic_indicators("GDP", "2024-07-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "GDP", "from": "2024-07-24"}
        )

        # Test with only to_date
        result = await economics_category.economic_indicators(
            "GDP", to_date="2025-07-24"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "GDP", "to": "2025-07-24"}
        )

        # Test with both dates
        result = await economics_category.economic_indicators(
            "GDP", "2024-07-24", "2025-07-24"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators",
            {"name": "GDP", "from": "2024-07-24", "to": "2025-07-24"},
        )

    @pytest.mark.asyncio
    async def test_economic_calendar_parameter_combinations(
        self, economics_category, mock_client
    ):
        """Test various parameter combinations for economic calendar"""
        mock_response = [
            {"date": "2024-03-01 03:35:00", "event": "3-Month Bill Auction"}
        ]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await economics_category.economic_calendar("2025-04-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-calendar", {"from": "2025-04-24"}
        )

        # Test with only to_date
        result = await economics_category.economic_calendar(to_date="2025-07-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-calendar", {"to": "2025-07-24"}
        )

        # Test with both dates
        result = await economics_category.economic_calendar("2025-04-24", "2025-07-24")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-calendar", {"from": "2025-04-24", "to": "2025-07-24"}
        )

    @pytest.mark.asyncio
    async def test_different_economic_indicators(self, economics_category, mock_client):
        """Test economic indicators with different indicator types"""
        mock_response = [{"name": "CPI", "date": "2024-01-01", "value": 308.417}]
        mock_client._make_request.return_value = mock_response

        # Test with CPI
        result = await economics_category.economic_indicators("CPI")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "CPI"}
        )

        # Test with unemployment rate
        result = await economics_category.economic_indicators("unemploymentRate")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "unemploymentRate"}
        )

        # Test with federal funds rate
        result = await economics_category.economic_indicators("federalFunds")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "economic-indicators", {"name": "federalFunds"}
        )

    @pytest.mark.asyncio
    async def test_treasury_rates_response_validation(
        self, economics_category, mock_client
    ):
        """Test treasury rates response validation"""
        mock_response = [
            {
                "date": "2024-02-29",
                "month1": 5.53,
                "month2": 5.5,
                "month3": 5.45,
                "month6": 5.3,
                "year1": 5.01,
                "year2": 4.64,
                "year3": 4.43,
                "year5": 4.26,
                "year7": 4.28,
                "year10": 4.25,
                "year20": 4.51,
                "year30": 4.38,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.treasury_rates()

        assert len(result) == 1
        assert result[0]["date"] == "2024-02-29"
        assert result[0]["month1"] == 5.53
        assert result[0]["month2"] == 5.5
        assert result[0]["year10"] == 4.25
        assert result[0]["year30"] == 4.38
        mock_client._make_request.assert_called_once_with("treasury-rates", {})

    @pytest.mark.asyncio
    async def test_economic_calendar_response_validation(
        self, economics_category, mock_client
    ):
        """Test economic calendar response validation"""
        mock_response = [
            {
                "date": "2024-03-01 03:35:00",
                "country": "JP",
                "event": "3-Month Bill Auction",
                "currency": "JPY",
                "previous": -0.112,
                "estimate": None,
                "actual": -0.096,
                "change": 0.016,
                "impact": "Low",
                "changePercentage": 14.286,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await economics_category.economic_calendar()

        assert len(result) == 1
        assert result[0]["date"] == "2024-03-01 03:35:00"
        assert result[0]["country"] == "JP"
        assert result[0]["event"] == "3-Month Bill Auction"
        assert result[0]["currency"] == "JPY"
        assert result[0]["previous"] == -0.112
        assert result[0]["estimate"] is None
        assert result[0]["actual"] == -0.096
        assert result[0]["change"] == 0.016
        assert result[0]["impact"] == "Low"
        assert result[0]["changePercentage"] == 14.286
        mock_client._make_request.assert_called_once_with("economic-calendar", {})
