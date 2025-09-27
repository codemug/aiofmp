"""
Unit tests for FMP Company category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.company import CompanyCategory


class TestCompanyCategory:
    """Test cases for CompanyCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def company_category(self, mock_client):
        """Company category instance with mocked client"""
        return CompanyCategory(mock_client)

    @pytest.mark.asyncio
    async def test_profile_basic(self, company_category, mock_client):
        """Test company profile with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "price": 232.8,
                "marketCap": 3500823120000,
                "beta": 1.24,
                "lastDividend": 0.99,
                "range": "164.08-260.1",
                "change": 4.79,
                "changePercentage": 2.1008,
                "volume": 0,
                "averageVolume": 50542058,
                "companyName": "Apple Inc.",
                "currency": "USD",
                "cik": "0000320193",
                "isin": "US0378331005",
                "cusip": "037833100",
                "exchangeFullName": "NASDAQ Global Select",
                "exchange": "NASDAQ",
                "industry": "Consumer Electronics",
                "website": "https://www.apple.com",
                "description": "Apple Inc. designs, manufactures, and markets smartphones...",
                "ceo": "Mr. Timothy D. Cook",
                "sector": "Technology",
                "country": "US",
                "fullTimeEmployees": "164000",
                "phone": "(408) 996-1010",
                "address": "One Apple Park Way",
                "city": "Cupertino",
                "state": "CA",
                "zip": "95014",
                "image": "https://images.financialmodelingprep.com/symbol/AAPL.png",
                "ipoDate": "1980-12-12",
                "defaultImage": False,
                "isEtf": False,
                "isActivelyTrading": True,
                "isAdr": False,
                "isFund": False,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.profile("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("profile", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_notes_basic(self, company_category, mock_client):
        """Test company notes with required parameters only"""
        mock_response = [
            {
                "cik": "0000320193",
                "symbol": "AAPL",
                "title": "1.000% Notes due 2022",
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.notes("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "company-notes", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_employee_count_basic(self, company_category, mock_client):
        """Test employee count with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "acceptanceTime": "2024-11-01 06:01:36",
                "periodOfReport": "2024-09-28",
                "companyName": "Apple Inc.",
                "formType": "10-K",
                "filingDate": "2024-11-01",
                "employeeCount": 164000,
                "source": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/0000320193-24-000123-index.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.employee_count("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "employee-count", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_employee_count_with_limit(self, company_category, mock_client):
        """Test employee count with limit parameter"""
        mock_response = [{"symbol": "AAPL", "employeeCount": 164000}]
        mock_client._make_request.return_value = mock_response

        result = await company_category.employee_count("AAPL", limit=10)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "employee-count", {"symbol": "AAPL", "limit": 10}
        )

    @pytest.mark.asyncio
    async def test_historical_employee_count_basic(self, company_category, mock_client):
        """Test historical employee count with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "acceptanceTime": "2024-11-01 06:01:36",
                "periodOfReport": "2024-09-28",
                "companyName": "Apple Inc.",
                "formType": "10-K",
                "filingDate": "2024-11-01",
                "employeeCount": 164000,
                "source": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/0000320193-24-000123-index.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.historical_employee_count("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-employee-count", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_employee_count_with_limit(
        self, company_category, mock_client
    ):
        """Test historical employee count with limit parameter"""
        mock_response = [{"symbol": "AAPL", "employeeCount": 164000}]
        mock_client._make_request.return_value = mock_response

        result = await company_category.historical_employee_count("AAPL", limit=20)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-employee-count", {"symbol": "AAPL", "limit": 20}
        )

    @pytest.mark.asyncio
    async def test_market_cap_basic(self, company_category, mock_client):
        """Test market cap with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2025-02-04", "marketCap": 3500823120000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.market_cap("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "market-capitalization", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_batch_market_cap_basic(self, company_category, mock_client):
        """Test batch market cap with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2025-02-04", "marketCap": 3500823120000},
            {"symbol": "MSFT", "date": "2025-02-04", "marketCap": 3000000000000},
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.batch_market_cap(["AAPL", "MSFT", "GOOGL"])

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "market-capitalization-batch", {"symbols": "AAPL,MSFT,GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_historical_market_cap_basic(self, company_category, mock_client):
        """Test historical market cap with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2024-02-29", "marketCap": 2784608472000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.historical_market_cap("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-market-capitalization", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_historical_market_cap_with_all_params(
        self, company_category, mock_client
    ):
        """Test historical market cap with all parameters"""
        mock_response = [
            {"symbol": "AAPL", "date": "2024-02-29", "marketCap": 2784608472000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.historical_market_cap(
            "AAPL", limit=100, from_date="2025-01-01", to_date="2025-03-31"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-market-capitalization",
            {"symbol": "AAPL", "limit": 100, "from": "2025-01-01", "to": "2025-03-31"},
        )

    @pytest.mark.asyncio
    async def test_shares_float_basic(self, company_category, mock_client):
        """Test shares float with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-04 17:01:35",
                "freeFloat": 99.9095,
                "floatShares": 15024290700,
                "outstandingShares": 15037900000,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.shares_float("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "shares-float", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_all_shares_float_basic(self, company_category, mock_client):
        """Test all shares float with no parameters"""
        mock_response = [
            {
                "symbol": "6898.HK",
                "date": "2025-02-04 17:27:01",
                "freeFloat": 33.2536,
                "floatShares": 318128880,
                "outstandingShares": 956675009,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.all_shares_float()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("shares-float-all", {})

    @pytest.mark.asyncio
    async def test_all_shares_float_with_params(self, company_category, mock_client):
        """Test all shares float with limit and page parameters"""
        mock_response = [{"symbol": "6898.HK", "freeFloat": 33.2536}]
        mock_client._make_request.return_value = mock_response

        result = await company_category.all_shares_float(limit=1000, page=0)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "shares-float-all", {"limit": 1000, "page": 0}
        )

    @pytest.mark.asyncio
    async def test_latest_mergers_acquisitions_basic(
        self, company_category, mock_client
    ):
        """Test latest M&A with no parameters"""
        mock_response = [
            {
                "symbol": "NLOK",
                "companyName": "NortonLifeLock Inc.",
                "cik": "0000849399",
                "targetedCompanyName": "MoneyLion Inc.",
                "targetedCik": "0001807846",
                "targetedSymbol": "ML",
                "transactionDate": "2025-02-03",
                "acceptedDate": "2025-02-03 06:01:10",
                "link": "https://www.sec.gov/Archives/edgar/data/849399/000114036125002752/ny20039778x6_s4.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.latest_mergers_acquisitions()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "mergers-acquisitions-latest", {}
        )

    @pytest.mark.asyncio
    async def test_latest_mergers_acquisitions_with_params(
        self, company_category, mock_client
    ):
        """Test latest M&A with page and limit parameters"""
        mock_response = [{"symbol": "NLOK", "companyName": "NortonLifeLock Inc."}]
        mock_client._make_request.return_value = mock_response

        result = await company_category.latest_mergers_acquisitions(page=0, limit=100)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "mergers-acquisitions-latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_search_mergers_acquisitions_basic(
        self, company_category, mock_client
    ):
        """Test search M&A with required parameters only"""
        mock_response = [
            {
                "symbol": "PEGY",
                "companyName": "Pineapple Energy Inc.",
                "cik": "0000022701",
                "targetedCompanyName": "Communications Systems, Inc.",
                "targetedCik": "0000022701",
                "targetedSymbol": "JCS",
                "transactionDate": "2021-11-12",
                "acceptedDate": "2021-11-12 09:54:22",
                "link": "https://www.sec.gov/Archives/edgar/data/22701/000089710121000932/a211292_s-4.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.search_mergers_acquisitions("Apple")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "mergers-acquisitions-search", {"name": "Apple"}
        )

    @pytest.mark.asyncio
    async def test_executives_basic(self, company_category, mock_client):
        """Test executives with required parameters only"""
        mock_response = [
            {
                "title": "Vice President of Worldwide Sales",
                "name": "Mr. Michael Fenger",
                "pay": None,
                "currencyPay": "USD",
                "gender": "male",
                "yearBorn": None,
                "active": None,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.executives("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "key-executives", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_executives_with_active(self, company_category, mock_client):
        """Test executives with active parameter"""
        mock_response = [{"title": "Vice President", "name": "Mr. Michael Fenger"}]
        mock_client._make_request.return_value = mock_response

        result = await company_category.executives("AAPL", active="true")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "key-executives", {"symbol": "AAPL", "active": "true"}
        )

    @pytest.mark.asyncio
    async def test_executive_compensation_basic(self, company_category, mock_client):
        """Test executive compensation with required parameters only"""
        mock_response = [
            {
                "cik": "0000320193",
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "filingDate": "2025-01-10",
                "acceptedDate": "2025-01-10 16:31:18",
                "nameAndPosition": "Kate Adams Senior Vice President, General Counsel and Secretary",
                "year": 2023,
                "salary": 1000000,
                "bonus": 0,
                "stockAward": 22323641,
                "optionAward": 0,
                "incentivePlanCompensation": 3571150,
                "allOtherCompensation": 46914,
                "total": 26941705,
                "link": "https://www.sec.gov/Archives/edgar/data/320193/000130817925000008/0001308179-25-000008-index.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.executive_compensation("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "governance-executive-compensation", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_executive_compensation_benchmark_basic(
        self, company_category, mock_client
    ):
        """Test executive compensation benchmark with no parameters"""
        mock_response = [
            {
                "industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS",
                "year": 2023,
                "averageCompensation": 694313.1666666666,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.executive_compensation_benchmark()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "executive-compensation-benchmark", {}
        )

    @pytest.mark.asyncio
    async def test_executive_compensation_benchmark_with_year(
        self, company_category, mock_client
    ):
        """Test executive compensation benchmark with year parameter"""
        mock_response = [
            {"industryTitle": "TECHNOLOGY", "year": 2024, "averageCompensation": 800000}
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.executive_compensation_benchmark("2024")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "executive-compensation-benchmark", {"year": "2024"}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, company_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await company_category.profile("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with("profile", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, company_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {
                "symbol": f"SYMBOL_{i}",
                "companyName": f"Company {i}",
                "marketCap": 1000000000 + i * 100000000,
            }
            for i in range(1, 101)
        ]
        mock_client._make_request.return_value = large_response

        result = await company_category.all_shares_float(limit=100)

        assert len(result) == 100
        assert result[0]["symbol"] == "SYMBOL_1"
        assert result[99]["symbol"] == "SYMBOL_100"
        mock_client._make_request.assert_called_once_with(
            "shares-float-all", {"limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, company_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "marketCap": 3500823120000,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await company_category.profile("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("profile", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, company_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"symbol": "AAPL", "marketCap": 3500823120000}]
        mock_client._make_request.return_value = mock_response

        # Test with only limit
        result = await company_category.employee_count("AAPL", limit=10)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "employee-count", {"symbol": "AAPL", "limit": 10}
        )

        # Test with only active
        result = await company_category.executives("AAPL", active="true")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "key-executives", {"symbol": "AAPL", "active": "true"}
        )

        # Test with only year
        result = await company_category.executive_compensation_benchmark("2024")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "executive-compensation-benchmark", {"year": "2024"}
        )

    @pytest.mark.asyncio
    async def test_list_parameter_handling(self, company_category, mock_client):
        """Test handling of list parameters"""
        mock_response = [
            {"symbol": "AAPL", "marketCap": 3500823120000},
            {"symbol": "MSFT", "marketCap": 3000000000000},
        ]
        mock_client._make_request.return_value = mock_response

        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = await company_category.batch_market_cap(symbols)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "market-capitalization-batch", {"symbols": "AAPL,MSFT,GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, company_category, mock_client):
        """Test various date parameter combinations for historical market cap"""
        mock_response = [
            {"symbol": "AAPL", "date": "2024-02-29", "marketCap": 2784608472000}
        ]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await company_category.historical_market_cap(
            "AAPL", from_date="2025-01-01"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-market-capitalization", {"symbol": "AAPL", "from": "2025-01-01"}
        )

        # Test with only to_date
        result = await company_category.historical_market_cap(
            "AAPL", to_date="2025-03-31"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-market-capitalization", {"symbol": "AAPL", "to": "2025-03-31"}
        )

        # Test with both dates
        result = await company_category.historical_market_cap(
            "AAPL", from_date="2025-01-01", to_date="2025-03-31"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-market-capitalization",
            {"symbol": "AAPL", "from": "2025-01-01", "to": "2025-03-31"},
        )
