"""
Unit tests for FMP Insider Trades category
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.insider_trades import InsiderTradesCategory


class TestInsiderTradesCategory:
    """Test cases for InsiderTradesCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def insider_trades_category(self, mock_client):
        """Insider Trades category instance with mocked client"""
        return InsiderTradesCategory(mock_client)

    @pytest.mark.asyncio
    async def test_latest_insider_trades_basic(
        self, insider_trades_category, mock_client
    ):
        """Test latest insider trades with no parameters"""
        mock_response = [
            {
                "symbol": "APA",
                "filingDate": "2025-02-04",
                "transactionDate": "2025-02-01",
                "reportingCik": "0001380034",
                "companyCik": "0001841666",
                "transactionType": "M-Exempt",
                "securitiesOwned": 104398,
                "reportingName": "Hoyt Rebecca A",
                "typeOfOwner": "officer: Sr. VP, Chief Acct Officer",
                "acquisitionOrDisposition": "A",
                "directOrIndirect": "D",
                "formType": "4",
                "securitiesTransacted": 3450,
                "price": 0,
                "securityName": "Common Stock",
                "url": "https://www.sec.gov/Archives/edgar/data/1841666/000194906025000035/0001949060-25-000035-index.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.latest_insider_trades()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("insider-trading/latest", {})

    @pytest.mark.asyncio
    async def test_latest_insider_trades_with_optional_params(
        self, insider_trades_category, mock_client
    ):
        """Test latest insider trades with optional parameters"""
        mock_response = [{"symbol": "APA", "reportingName": "Hoyt Rebecca A"}]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.latest_insider_trades(page=0, limit=100)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_latest_insider_trades_with_date(
        self, insider_trades_category, mock_client
    ):
        """Test latest insider trades with date parameter"""
        mock_response = [{"symbol": "APA", "filingDate": "2025-02-04"}]
        mock_client._make_request.return_value = mock_response

        trade_date = date(2025, 2, 4)
        result = await insider_trades_category.latest_insider_trades(
            trade_date=trade_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/latest", {"date": "2025-02-04"}
        )

    @pytest.mark.asyncio
    async def test_search_insider_trades_basic(
        self, insider_trades_category, mock_client
    ):
        """Test search insider trades with no parameters"""
        mock_response = [
            {
                "symbol": "AAPL",
                "filingDate": "2025-02-04",
                "transactionDate": "2025-02-03",
                "reportingCik": "0001214128",
                "companyCik": "0000320193",
                "transactionType": "S-Sale",
                "securitiesOwned": 4159576,
                "reportingName": "LEVINSON ARTHUR D",
                "typeOfOwner": "director",
                "acquisitionOrDisposition": "D",
                "directOrIndirect": "D",
                "formType": "4",
                "securitiesTransacted": 1516,
                "price": 226.3501,
                "securityName": "Common Stock",
                "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019325000019/0000320193-25-000019-index.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_insider_trades()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("insider-trading/search", {})

    @pytest.mark.asyncio
    async def test_search_insider_trades_with_symbol(
        self, insider_trades_category, mock_client
    ):
        """Test search insider trades with symbol parameter"""
        mock_response = [{"symbol": "AAPL", "transactionType": "S-Sale"}]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_insider_trades(symbol="AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/search", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_search_insider_trades_with_all_params(
        self, insider_trades_category, mock_client
    ):
        """Test search insider trades with all parameters"""
        mock_response = [{"symbol": "AAPL", "transactionType": "S-Sale"}]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_insider_trades(
            symbol="AAPL",
            page=0,
            limit=100,
            reporting_cik="0001214128",
            company_cik="0000320193",
            transaction_type="S-Sale",
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/search",
            {
                "symbol": "AAPL",
                "page": 0,
                "limit": 100,
                "reportingCik": "0001214128",
                "companyCik": "0000320193",
                "transactionType": "S-Sale",
            },
        )

    @pytest.mark.asyncio
    async def test_search_by_reporting_name_basic(
        self, insider_trades_category, mock_client
    ):
        """Test search by reporting name with required parameter"""
        mock_response = [
            {"reportingCik": "0001548760", "reportingName": "Zuckerberg Mark"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_by_reporting_name("Zuckerberg")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/reporting-name", {"name": "Zuckerberg"}
        )

    @pytest.mark.asyncio
    async def test_all_transaction_types_basic(
        self, insider_trades_category, mock_client
    ):
        """Test all transaction types with no parameters"""
        mock_response = [
            {"transactionType": "A-Award"},
            {"transactionType": "P-Purchase"},
            {"transactionType": "S-Sale"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.all_transaction_types()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading-transaction-type"
        )

    @pytest.mark.asyncio
    async def test_insider_trade_statistics_basic(
        self, insider_trades_category, mock_client
    ):
        """Test insider trade statistics with required parameter"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "year": 2024,
                "quarter": 4,
                "acquiredTransactions": 6,
                "disposedTransactions": 38,
                "acquiredDisposedRatio": 0.1579,
                "totalAcquired": 994544,
                "totalDisposed": 2297088,
                "averageAcquired": 165757.3333,
                "averageDisposed": 60449.6842,
                "totalPurchases": 0,
                "totalSales": 22,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.insider_trade_statistics("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "insider-trading/statistics", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_acquisition_ownership_basic(
        self, insider_trades_category, mock_client
    ):
        """Test acquisition ownership with required parameter only"""
        mock_response = [
            {
                "cik": "0000320193",
                "symbol": "AAPL",
                "filingDate": "2024-02-14",
                "acceptedDate": "2024-02-14",
                "cusip": "037833100",
                "nameOfReportingPerson": "National Indemnity Company",
                "citizenshipOrPlaceOfOrganization": "State of Nebraska",
                "soleVotingPower": "0",
                "sharedVotingPower": "755059877",
                "soleDispositivePower": "0",
                "sharedDispositivePower": "755059877",
                "amountBeneficiallyOwned": "755059877",
                "percentOfClass": "4.8",
                "typeOfReportingPerson": "IC, EP, IN, CO",
                "url": "https://www.sec.gov/Archives/edgar/data/320193/000119312524036431/d751537dsc13ga.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.acquisition_ownership("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "acquisition-of-beneficial-ownership", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_acquisition_ownership_with_limit(
        self, insider_trades_category, mock_client
    ):
        """Test acquisition ownership with limit parameter"""
        mock_response = [{"symbol": "AAPL", "cik": "0000320193"}]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.acquisition_ownership("AAPL", limit=1000)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "acquisition-of-beneficial-ownership", {"symbol": "AAPL", "limit": 1000}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, insider_trades_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await insider_trades_category.latest_insider_trades()

        assert result == []
        mock_client._make_request.assert_called_once_with("insider-trading/latest", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, insider_trades_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple insider trades
        large_response = [
            {
                "symbol": f"STOCK{i:03d}",
                "filingDate": "2025-02-04",
                "reportingName": f"Person {i}",
                "transactionType": "S-Sale" if i % 2 == 0 else "P-Purchase",
            }
            for i in range(1, 101)  # 100 insider trades
        ]
        mock_client._make_request.return_value = large_response

        result = await insider_trades_category.latest_insider_trades(page=0, limit=100)

        assert len(result) == 100
        assert result[0]["symbol"] == "STOCK001"
        assert result[99]["symbol"] == "STOCK100"
        mock_client._make_request.assert_called_once_with(
            "insider-trading/latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(
        self, insider_trades_category, mock_client
    ):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "APA",
                "reportingName": "Hoyt Rebecca A",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.latest_insider_trades()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("insider-trading/latest", {})

    @pytest.mark.asyncio
    async def test_different_symbols(self, insider_trades_category, mock_client):
        """Test insider trades functionality with different symbols"""
        mock_response = [{"symbol": "AAPL", "transactionType": "S-Sale"}]
        mock_client._make_request.return_value = mock_response

        # Test with Apple
        result = await insider_trades_category.search_insider_trades(symbol="AAPL")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"symbol": "AAPL"}
        )

        # Test with Microsoft
        result = await insider_trades_category.search_insider_trades(symbol="MSFT")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"symbol": "MSFT"}
        )

        # Test with Tesla
        result = await insider_trades_category.search_insider_trades(symbol="TSLA")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"symbol": "TSLA"}
        )

    @pytest.mark.asyncio
    async def test_different_transaction_types(
        self, insider_trades_category, mock_client
    ):
        """Test insider trades functionality with different transaction types"""
        mock_response = [{"symbol": "AAPL", "transactionType": "S-Sale"}]
        mock_client._make_request.return_value = mock_response

        # Test with Sale
        result = await insider_trades_category.search_insider_trades(
            transaction_type="S-Sale"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"transactionType": "S-Sale"}
        )

        # Test with Purchase
        result = await insider_trades_category.search_insider_trades(
            transaction_type="P-Purchase"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"transactionType": "P-Purchase"}
        )

        # Test with Award
        result = await insider_trades_category.search_insider_trades(
            transaction_type="A-Award"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"transactionType": "A-Award"}
        )

    @pytest.mark.asyncio
    async def test_different_names(self, insider_trades_category, mock_client):
        """Test search by reporting name with different names"""
        mock_response = [
            {"reportingCik": "0001548760", "reportingName": "Zuckerberg Mark"}
        ]
        mock_client._make_request.return_value = mock_response

        # Test with Zuckerberg
        result = await insider_trades_category.search_by_reporting_name("Zuckerberg")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/reporting-name", {"name": "Zuckerberg"}
        )

        # Test with Musk
        result = await insider_trades_category.search_by_reporting_name("Musk")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/reporting-name", {"name": "Musk"}
        )

        # Test with Cook
        result = await insider_trades_category.search_by_reporting_name("Cook")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/reporting-name", {"name": "Cook"}
        )

    @pytest.mark.asyncio
    async def test_date_edge_cases(self, insider_trades_category, mock_client):
        """Test date handling edge cases"""
        mock_response = [{"symbol": "APA", "filingDate": "2025-02-04"}]
        mock_client._make_request.return_value = mock_response

        # Test with leap year date
        leap_date = date(2024, 2, 29)
        result = await insider_trades_category.latest_insider_trades(
            trade_date=leap_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"date": "2024-02-29"}
        )

        # Test with year boundary
        year_boundary = date(2025, 12, 31)
        result = await insider_trades_category.latest_insider_trades(
            trade_date=year_boundary
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"date": "2025-12-31"}
        )

        # Test with beginning of year
        year_beginning = date(2025, 1, 1)
        result = await insider_trades_category.latest_insider_trades(
            trade_date=year_beginning
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"date": "2025-01-01"}
        )

    @pytest.mark.asyncio
    async def test_latest_insider_trades_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test latest insider trades response validation"""
        mock_response = [
            {
                "symbol": "APA",
                "filingDate": "2025-02-04",
                "transactionDate": "2025-02-01",
                "reportingCik": "0001380034",
                "reportingName": "Hoyt Rebecca A",
                "transactionType": "M-Exempt",
                "securitiesTransacted": 3450,
                "price": 0,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.latest_insider_trades()

        assert len(result) == 1
        assert result[0]["symbol"] == "APA"
        assert result[0]["filingDate"] == "2025-02-04"
        assert result[0]["reportingName"] == "Hoyt Rebecca A"
        assert result[0]["transactionType"] == "M-Exempt"
        assert result[0]["securitiesTransacted"] == 3450
        mock_client._make_request.assert_called_once_with("insider-trading/latest", {})

    @pytest.mark.asyncio
    async def test_search_insider_trades_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test search insider trades response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "filingDate": "2025-02-04",
                "transactionDate": "2025-02-03",
                "reportingCik": "0001214128",
                "companyCik": "0000320193",
                "transactionType": "S-Sale",
                "securitiesOwned": 4159576,
                "reportingName": "LEVINSON ARTHUR D",
                "typeOfOwner": "director",
                "acquisitionOrDisposition": "D",
                "directOrIndirect": "D",
                "formType": "4",
                "securitiesTransacted": 1516,
                "price": 226.3501,
                "securityName": "Common Stock",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_insider_trades(symbol="AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["transactionType"] == "S-Sale"
        assert result[0]["reportingName"] == "LEVINSON ARTHUR D"
        assert result[0]["securitiesTransacted"] == 1516
        assert result[0]["price"] == 226.3501
        mock_client._make_request.assert_called_once_with(
            "insider-trading/search", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_search_by_reporting_name_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test search by reporting name response validation"""
        mock_response = [
            {"reportingCik": "0001548760", "reportingName": "Zuckerberg Mark"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.search_by_reporting_name("Zuckerberg")

        assert len(result) == 1
        assert result[0]["reportingCik"] == "0001548760"
        assert result[0]["reportingName"] == "Zuckerberg Mark"
        mock_client._make_request.assert_called_once_with(
            "insider-trading/reporting-name", {"name": "Zuckerberg"}
        )

    @pytest.mark.asyncio
    async def test_all_transaction_types_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test all transaction types response validation"""
        mock_response = [
            {"transactionType": "A-Award"},
            {"transactionType": "P-Purchase"},
            {"transactionType": "S-Sale"},
            {"transactionType": "M-Exempt"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.all_transaction_types()

        assert len(result) == 4
        transaction_types = [item["transactionType"] for item in result]
        assert "A-Award" in transaction_types
        assert "P-Purchase" in transaction_types
        assert "S-Sale" in transaction_types
        assert "M-Exempt" in transaction_types
        mock_client._make_request.assert_called_once_with(
            "insider-trading-transaction-type"
        )

    @pytest.mark.asyncio
    async def test_insider_trade_statistics_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test insider trade statistics response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "cik": "0000320193",
                "year": 2024,
                "quarter": 4,
                "acquiredTransactions": 6,
                "disposedTransactions": 38,
                "acquiredDisposedRatio": 0.1579,
                "totalAcquired": 994544,
                "totalDisposed": 2297088,
                "averageAcquired": 165757.3333,
                "averageDisposed": 60449.6842,
                "totalPurchases": 0,
                "totalSales": 22,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.insider_trade_statistics("AAPL")

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["year"] == 2024
        assert result[0]["quarter"] == 4
        assert result[0]["acquiredTransactions"] == 6
        assert result[0]["disposedTransactions"] == 38
        assert result[0]["acquiredDisposedRatio"] == 0.1579
        mock_client._make_request.assert_called_once_with(
            "insider-trading/statistics", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_acquisition_ownership_response_validation(
        self, insider_trades_category, mock_client
    ):
        """Test acquisition ownership response validation"""
        mock_response = [
            {
                "cik": "0000320193",
                "symbol": "AAPL",
                "filingDate": "2024-02-14",
                "acceptedDate": "2024-02-14",
                "cusip": "037833100",
                "nameOfReportingPerson": "National Indemnity Company",
                "citizenshipOrPlaceOfOrganization": "State of Nebraska",
                "soleVotingPower": "0",
                "sharedVotingPower": "755059877",
                "soleDispositivePower": "0",
                "sharedDispositivePower": "755059877",
                "amountBeneficiallyOwned": "755059877",
                "percentOfClass": "4.8",
                "typeOfReportingPerson": "IC, EP, IN, CO",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await insider_trades_category.acquisition_ownership("AAPL")

        assert len(result) == 1
        assert result[0]["cik"] == "0000320193"
        assert result[0]["symbol"] == "AAPL"
        assert result[0]["filingDate"] == "2024-02-14"
        assert result[0]["nameOfReportingPerson"] == "National Indemnity Company"
        assert result[0]["amountBeneficiallyOwned"] == "755059877"
        assert result[0]["percentOfClass"] == "4.8"
        mock_client._make_request.assert_called_once_with(
            "acquisition-of-beneficial-ownership", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, insider_trades_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"symbol": "AAPL", "transactionType": "S-Sale"}]
        mock_client._make_request.return_value = mock_response

        # Test with only symbol
        result = await insider_trades_category.search_insider_trades(symbol="AAPL")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"symbol": "AAPL"}
        )

        # Test with only transaction type
        result = await insider_trades_category.search_insider_trades(
            transaction_type="S-Sale"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"transactionType": "S-Sale"}
        )

        # Test with only reporting CIK
        result = await insider_trades_category.search_insider_trades(
            reporting_cik="0001214128"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"reportingCik": "0001214128"}
        )

        # Test with only company CIK
        result = await insider_trades_category.search_insider_trades(
            company_cik="0000320193"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/search", {"companyCik": "0000320193"}
        )

    @pytest.mark.asyncio
    async def test_pagination_handling(self, insider_trades_category, mock_client):
        """Test pagination parameter handling"""
        mock_response = [{"symbol": "AAPL", "page": 0}]
        mock_client._make_request.return_value = mock_response

        # Test with only page
        result = await insider_trades_category.latest_insider_trades(page=0)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"page": 0}
        )

        # Test with only limit
        result = await insider_trades_category.latest_insider_trades(limit=50)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"limit": 50}
        )

        # Test with both page and limit
        result = await insider_trades_category.latest_insider_trades(page=1, limit=25)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "insider-trading/latest", {"page": 1, "limit": 25}
        )
