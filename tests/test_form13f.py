"""
Unit tests for FMP Form 13F category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.form13f import Form13FCategory


class TestForm13FCategory:
    """Test cases for Form13FCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def form13f_category(self, mock_client):
        """Form 13F category instance with mocked client"""
        return Form13FCategory(mock_client)

    @pytest.mark.asyncio
    async def test_latest_filings_basic(self, form13f_category, mock_client):
        """Test latest filings with no parameters"""
        mock_response = [
            {
                "cik": "0001963967",
                "name": "CPA ASSET MANAGEMENT LLC",
                "date": "2024-12-31",
                "filingDate": "2025-02-04 00:00:00",
                "acceptedDate": "2025-02-04 17:28:36",
                "formType": "13F-HR",
                "link": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/0001963967-25-000001-index.htm",
                "finalLink": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/boc2024q413f.xml",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.latest_filings()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {}
        )

    @pytest.mark.asyncio
    async def test_latest_filings_with_optional_params(
        self, form13f_category, mock_client
    ):
        """Test latest filings with optional parameters"""
        mock_response = [{"cik": "0001963967", "name": "CPA ASSET MANAGEMENT LLC"}]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.latest_filings(page=0, limit=100)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_filings_extract_basic(self, form13f_category, mock_client):
        """Test filings extract with required parameters"""
        mock_response = [
            {
                "date": "2023-09-30",
                "filingDate": "2023-11-13",
                "acceptedDate": "2023-11-13",
                "cik": "0001388838",
                "securityCusip": "674215207",
                "symbol": "CHRD",
                "nameOfIssuer": "CHORD ENERGY CORPORATION",
                "shares": 13280,
                "titleOfClass": "COM NEW",
                "sharesType": "SH",
                "putCallShare": "",
                "value": 2152290,
                "link": "https://www.sec.gov/Archives/edgar/data/1388838/000117266123003760/0001172661-23-003760-index.htm",
                "finalLink": "https://www.sec.gov/Archives/edgar/data/1388838/000117266123003760/infotable.xml",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_extract("0001388838", "2023", "3")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/extract",
            {"cik": "0001388838", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_filings_dates_basic(self, form13f_category, mock_client):
        """Test filings dates with required parameters"""
        mock_response = [{"date": "2024-09-30", "year": 2024, "quarter": 3}]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_dates("0001067983")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/dates", {"cik": "0001067983"}
        )

    @pytest.mark.asyncio
    async def test_filings_extract_analytics_by_holder_basic(
        self, form13f_category, mock_client
    ):
        """Test filings extract analytics by holder with required parameters"""
        mock_response = [
            {
                "date": "2023-09-30",
                "cik": "0000102909",
                "filingDate": "2023-12-18",
                "investorName": "VANGUARD GROUP INC",
                "symbol": "AAPL",
                "securityName": "APPLE INC",
                "typeOfSecurity": "COM",
                "securityCusip": "037833100",
                "sharesType": "SH",
                "putCallShare": "Share",
                "investmentDiscretion": "SOLE",
                "industryTitle": "ELECTRONIC COMPUTERS",
                "weight": 5.4673,
                "lastWeight": 5.996,
                "changeInWeight": -0.5287,
                "changeInWeightPercentage": -8.8175,
                "marketValue": 222572509140,
                "lastMarketValue": 252876459509,
                "changeInMarketValue": -30303950369,
                "changeInMarketValuePercentage": -11.9837,
                "sharesNumber": 1299997133,
                "lastSharesNumber": 1303688506,
                "changeInSharesNumber": -3691373,
                "changeInSharesNumberPercentage": -0.2831,
                "quarterEndPrice": 171.21,
                "avgPricePaid": 95.86,
                "isNew": False,
                "isSoldOut": False,
                "ownership": 8.3336,
                "lastOwnership": 8.305,
                "changeInOwnership": 0.0286,
                "changeInOwnershipPercentage": 0.3445,
                "holdingPeriod": 42,
                "firstAdded": "2013-06-30",
                "performance": -29671950396,
                "performancePercentage": -11.7338,
                "lastPerformance": 38078179274,
                "changeInPerformance": -67750129670,
                "isCountedForPerformance": True,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_extract_analytics_by_holder(
            "AAPL", "2023", "3"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/extract-analytics/holder",
            {"symbol": "AAPL", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_filings_extract_analytics_by_holder_with_optional_params(
        self, form13f_category, mock_client
    ):
        """Test filings extract analytics by holder with optional parameters"""
        mock_response = [{"investorName": "VANGUARD GROUP INC", "symbol": "AAPL"}]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_extract_analytics_by_holder(
            "AAPL", "2023", "3", page=0, limit=10
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/extract-analytics/holder",
            {"symbol": "AAPL", "year": "2023", "quarter": "3", "page": 0, "limit": 10},
        )

    @pytest.mark.asyncio
    async def test_holder_performance_summary_basic(
        self, form13f_category, mock_client
    ):
        """Test holder performance summary with required parameters"""
        mock_response = [
            {
                "date": "2024-09-30",
                "cik": "0001067983",
                "investorName": "BERKSHIRE HATHAWAY INC",
                "portfolioSize": 40,
                "securitiesAdded": 3,
                "securitiesRemoved": 4,
                "marketValue": 266378900503,
                "previousMarketValue": 279969062343,
                "changeInMarketValue": -13590161840,
                "changeInMarketValuePercentage": -4.8542,
                "averageHoldingPeriod": 18,
                "averageHoldingPeriodTop10": 31,
                "averageHoldingPeriodTop20": 27,
                "turnover": 0.175,
                "turnoverAlternateSell": 13.9726,
                "turnoverAlternateBuy": 1.1974,
                "performance": 17707926874,
                "performancePercentage": 6.325,
                "lastPerformance": 38318168662,
                "changeInPerformance": -20610241788,
                "performance1year": 89877376224,
                "performancePercentage1year": 28.5368,
                "performance3year": 91730847239,
                "performancePercentage3year": 31.2597,
                "performance5year": 157058602844,
                "performancePercentage5year": 73.1617,
                "performanceSinceInception": 182067479115,
                "performanceSinceInceptionPercentage": 198.2138,
                "performanceRelativeToSP500Percentage": 6.325,
                "performance1yearRelativeToSP500Percentage": 28.5368,
                "performance3yearRelativeToSP500Percentage": 36.5632,
                "performance5yearRelativeToSP500Percentage": 36.1296,
                "performanceSinceInceptionRelativeToSP500Percentage": 37.0968,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.holder_performance_summary("0001067983")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/holder-performance-summary", {"cik": "0001067983"}
        )

    @pytest.mark.asyncio
    async def test_holder_performance_summary_with_page(
        self, form13f_category, mock_client
    ):
        """Test holder performance summary with page parameter"""
        mock_response = [
            {"investorName": "BERKSHIRE HATHAWAY INC", "portfolioSize": 40}
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.holder_performance_summary("0001067983", page=0)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/holder-performance-summary",
            {"cik": "0001067983", "page": 0},
        )

    @pytest.mark.asyncio
    async def test_holder_industry_breakdown_basic(self, form13f_category, mock_client):
        """Test holder industry breakdown with required parameters"""
        mock_response = [
            {
                "date": "2023-09-30",
                "cik": "0001067983",
                "investorName": "BERKSHIRE HATHAWAY INC",
                "industryTitle": "ELECTRONIC COMPUTERS",
                "weight": 49.7704,
                "lastWeight": 51.0035,
                "changeInWeight": -1.2332,
                "changeInWeightPercentage": -2.4178,
                "performance": -20838154294,
                "performancePercentage": -178.2938,
                "lastPerformance": 26615340304,
                "changeInPerformance": -47453494598,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.holder_industry_breakdown(
            "0001067983", "2023", "3"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/holder-industry-breakdown",
            {"cik": "0001067983", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_symbol_positions_summary_basic(self, form13f_category, mock_client):
        """Test symbol positions summary with required parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "date": "2023-09-30",
                "investorsHolding": 4805,
                "lastInvestorsHolding": 4749,
                "investorsHoldingChange": 56,
                "numberOf13Fshares": 9247670386,
                "lastNumberOf13Fshares": 9345671472,
                "numberOf13FsharesChange": -98001086,
                "totalInvested": 1613733330618,
                "lastTotalInvested": 1825154796061,
                "totalInvestedChange": -211421465443,
                "ownershipPercent": 59.2821,
                "lastOwnershipPercent": 59.5356,
                "ownershipPercentChange": -0.2535,
                "newPositions": 158,
                "lastNewPositions": 188,
                "newPositionsChange": -30,
                "increasedPositions": 1921,
                "lastIncreasedPositions": 1775,
                "increasedPositionsChange": 146,
                "closedPositions": 156,
                "lastClosedPositions": 122,
                "closedPositionsChange": 34,
                "reducedPositions": 2375,
                "lastReducedPositions": 2506,
                "reducedPositionsChange": -131,
                "totalCalls": 173528138,
                "lastTotalCalls": 198746782,
                "totalCallsChange": -25218644,
                "totalPuts": 192878290,
                "lastTotalPuts": 177007062,
                "totalPutsChange": 15871228,
                "putCallRatio": 1.1115,
                "lastPutCallRatio": 0.8906,
                "putCallRatioChange": 22.0894,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.symbol_positions_summary("AAPL", "2023", "3")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/symbol-positions-summary",
            {"symbol": "AAPL", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_industry_performance_summary_basic(
        self, form13f_category, mock_client
    ):
        """Test industry performance summary with required parameters"""
        mock_response = [
            {
                "industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS",
                "industryValue": 10979226300,
                "date": "2023-09-30",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.industry_performance_summary("2023", "3")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/industry-summary", {"year": "2023", "quarter": "3"}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, form13f_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await form13f_category.latest_filings()

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, form13f_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple filings
        large_response = [
            {
                "cik": f"000{1000000 + i:06d}",
                "name": f"Institution {i}",
                "date": "2024-12-31",
                "filingDate": "2025-02-04 00:00:00",
                "acceptedDate": "2025-02-04 17:28:36",
                "formType": "13F-HR",
            }
            for i in range(1, 101)  # 100 filings
        ]
        mock_client._make_request.return_value = large_response

        result = await form13f_category.latest_filings(page=0, limit=100)

        assert len(result) == 100
        assert result[0]["cik"] == "0001000001"
        assert result[99]["cik"] == "0001000100"
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, form13f_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "cik": "0001963967",
                "name": "CPA ASSET MANAGEMENT LLC",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.latest_filings()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {}
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, form13f_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"cik": "0001963967", "name": "CPA ASSET MANAGEMENT LLC"}]
        mock_client._make_request.return_value = mock_response

        # Test with only page
        result = await form13f_category.latest_filings(page=0)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/latest", {"page": 0}
        )

        # Test with only limit
        result = await form13f_category.latest_filings(limit=50)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/latest", {"limit": 50}
        )

        # Test with both parameters
        result = await form13f_category.latest_filings(page=1, limit=25)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/latest", {"page": 1, "limit": 25}
        )

    @pytest.mark.asyncio
    async def test_different_ciks(self, form13f_category, mock_client):
        """Test Form 13F functionality with different CIKs"""
        mock_response = [
            {"cik": "0001067983", "investorName": "BERKSHIRE HATHAWAY INC"}
        ]
        mock_client._make_request.return_value = mock_response

        # Test with Berkshire Hathaway
        result = await form13f_category.filings_dates("0001067983")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/dates", {"cik": "0001067983"}
        )

        # Test with Vanguard
        result = await form13f_category.filings_dates("0000102909")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/dates", {"cik": "0000102909"}
        )

        # Test with BlackRock
        result = await form13f_category.filings_dates("0001100663")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/dates", {"cik": "0001100663"}
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, form13f_category, mock_client):
        """Test Form 13F functionality with different symbols"""
        mock_response = [{"symbol": "AAPL", "investorsHolding": 4805}]
        mock_client._make_request.return_value = mock_response

        # Test with Apple
        result = await form13f_category.symbol_positions_summary("AAPL", "2023", "3")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/symbol-positions-summary",
            {"symbol": "AAPL", "year": "2023", "quarter": "3"},
        )

        # Test with Microsoft
        result = await form13f_category.symbol_positions_summary("MSFT", "2023", "3")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/symbol-positions-summary",
            {"symbol": "MSFT", "year": "2023", "quarter": "3"},
        )

        # Test with Tesla
        result = await form13f_category.symbol_positions_summary("TSLA", "2023", "3")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/symbol-positions-summary",
            {"symbol": "TSLA", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_different_years_and_quarters(self, form13f_category, mock_client):
        """Test Form 13F functionality with different years and quarters"""
        mock_response = [{"year": "2023", "quarter": "3"}]
        mock_client._make_request.return_value = mock_response

        # Test with Q3 2023
        result = await form13f_category.industry_performance_summary("2023", "3")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/industry-summary", {"year": "2023", "quarter": "3"}
        )

        # Test with Q4 2023
        result = await form13f_category.industry_performance_summary("2023", "4")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/industry-summary", {"year": "2023", "quarter": "4"}
        )

        # Test with Q1 2024
        result = await form13f_category.industry_performance_summary("2024", "1")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "institutional-ownership/industry-summary", {"year": "2024", "quarter": "1"}
        )

    @pytest.mark.asyncio
    async def test_latest_filings_response_validation(
        self, form13f_category, mock_client
    ):
        """Test latest filings response validation"""
        mock_response = [
            {
                "cik": "0001963967",
                "name": "CPA ASSET MANAGEMENT LLC",
                "date": "2024-12-31",
                "filingDate": "2025-02-04 00:00:00",
                "acceptedDate": "2025-02-04 17:28:36",
                "formType": "13F-HR",
                "link": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/0001963967-25-000001-index.htm",
                "finalLink": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/boc2024q413f.xml",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.latest_filings()

        assert len(result) == 1
        assert result[0]["cik"] == "0001963967"
        assert result[0]["name"] == "CPA ASSET MANAGEMENT LLC"
        assert result[0]["date"] == "2024-12-31"
        assert result[0]["formType"] == "13F-HR"
        assert "sec.gov" in result[0]["link"]
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/latest", {}
        )

    @pytest.mark.asyncio
    async def test_filings_extract_response_validation(
        self, form13f_category, mock_client
    ):
        """Test filings extract response validation"""
        mock_response = [
            {
                "date": "2023-09-30",
                "cik": "0001388838",
                "securityCusip": "674215207",
                "symbol": "CHRD",
                "nameOfIssuer": "CHORD ENERGY CORPORATION",
                "shares": 13280,
                "value": 2152290,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_extract("0001388838", "2023", "3")

        assert len(result) == 1
        assert result[0]["cik"] == "0001388838"
        assert result[0]["symbol"] == "CHRD"
        assert result[0]["shares"] == 13280
        assert result[0]["value"] == 2152290
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/extract",
            {"cik": "0001388838", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_filings_dates_response_validation(
        self, form13f_category, mock_client
    ):
        """Test filings dates response validation"""
        mock_response = [{"date": "2024-09-30", "year": 2024, "quarter": 3}]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_dates("0001067983")

        assert len(result) == 1
        assert result[0]["date"] == "2024-09-30"
        assert result[0]["year"] == 2024
        assert result[0]["quarter"] == 3
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/dates", {"cik": "0001067983"}
        )

    @pytest.mark.asyncio
    async def test_analytics_by_holder_response_validation(
        self, form13f_category, mock_client
    ):
        """Test analytics by holder response validation"""
        mock_response = [
            {
                "date": "2023-09-30",
                "cik": "0000102909",
                "investorName": "VANGUARD GROUP INC",
                "symbol": "AAPL",
                "weight": 5.4673,
                "marketValue": 222572509140,
                "sharesNumber": 1299997133,
                "ownership": 8.3336,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.filings_extract_analytics_by_holder(
            "AAPL", "2023", "3"
        )

        assert len(result) == 1
        assert result[0]["cik"] == "0000102909"
        assert result[0]["investorName"] == "VANGUARD GROUP INC"
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["weight"] == 5.4673
        assert result[0]["marketValue"] == 222572509140
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/extract-analytics/holder",
            {"symbol": "AAPL", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_performance_summary_response_validation(
        self, form13f_category, mock_client
    ):
        """Test performance summary response validation"""
        mock_response = [
            {
                "date": "2024-09-30",
                "cik": "0001067983",
                "investorName": "BERKSHIRE HATHAWAY INC",
                "portfolioSize": 40,
                "marketValue": 266378900503,
                "performance": 17707926874,
                "performancePercentage": 6.325,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.holder_performance_summary("0001067983")

        assert len(result) == 1
        assert result[0]["cik"] == "0001067983"
        assert result[0]["investorName"] == "BERKSHIRE HATHAWAY INC"
        assert result[0]["portfolioSize"] == 40
        assert result[0]["marketValue"] == 266378900503
        assert result[0]["performance"] == 17707926874
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/holder-performance-summary", {"cik": "0001067983"}
        )

    @pytest.mark.asyncio
    async def test_industry_breakdown_response_validation(
        self, form13f_category, mock_client
    ):
        """Test industry breakdown response validation"""
        mock_response = [
            {
                "date": "2023-09-30",
                "cik": "0001067983",
                "investorName": "BERKSHIRE HATHAWAY INC",
                "industryTitle": "ELECTRONIC COMPUTERS",
                "weight": 49.7704,
                "performance": -20838154294,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.holder_industry_breakdown(
            "0001067983", "2023", "3"
        )

        assert len(result) == 1
        assert result[0]["cik"] == "0001067983"
        assert result[0]["investorName"] == "BERKSHIRE HATHAWAY INC"
        assert result[0]["industryTitle"] == "ELECTRONIC COMPUTERS"
        assert result[0]["weight"] == 49.7704
        assert result[0]["performance"] == -20838154294
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/holder-industry-breakdown",
            {"cik": "0001067983", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_symbol_positions_summary_response_validation(
        self, form13f_category, mock_client
    ):
        """Test symbol positions summary response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "date": "2023-09-30",
                "investorsHolding": 4805,
                "numberOf13Fshares": 9247670386,
                "totalInvested": 1613733330618,
                "ownershipPercent": 59.2821,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.symbol_positions_summary("AAPL", "2023", "3")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["cik"] == "0000320193"
        assert result[0]["investorsHolding"] == 4805
        assert result[0]["numberOf13Fshares"] == 9247670386
        assert result[0]["totalInvested"] == 1613733330618
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/symbol-positions-summary",
            {"symbol": "AAPL", "year": "2023", "quarter": "3"},
        )

    @pytest.mark.asyncio
    async def test_industry_performance_summary_response_validation(
        self, form13f_category, mock_client
    ):
        """Test industry performance summary response validation"""
        mock_response = [
            {
                "industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS",
                "industryValue": 10979226300,
                "date": "2023-09-30",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await form13f_category.industry_performance_summary("2023", "3")

        assert len(result) == 1
        assert (
            result[0]["industryTitle"]
            == "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS"
        )
        assert result[0]["industryValue"] == 10979226300
        assert result[0]["date"] == "2023-09-30"
        mock_client._make_request.assert_called_once_with(
            "institutional-ownership/industry-summary", {"year": "2023", "quarter": "3"}
        )
