"""
Unit tests for FMP Calendar category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.calendar import CalendarCategory


class TestCalendarCategory:
    """Test cases for CalendarCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def calendar_category(self, mock_client):
        """Calendar category instance with mocked client"""
        return CalendarCategory(mock_client)

    @pytest.mark.asyncio
    async def test_dividends_company_basic(self, calendar_category, mock_client):
        """Test dividends company with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-10",
                "recordDate": "2025-02-10",
                "paymentDate": "2025-02-13",
                "declarationDate": "2025-01-30",
                "adjDividend": 0.25,
                "dividend": 0.25,
                "yield": 0.42955326460481097,
                "frequency": "Quarterly",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.dividends_company("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "dividends", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_dividends_company_with_limit(self, calendar_category, mock_client):
        """Test dividends company with limit parameter"""
        mock_response = [{"symbol": "AAPL", "dividend": 0.25}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.dividends_company("AAPL", limit=50)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "dividends", {"symbol": "AAPL", "limit": 50}
        )

    @pytest.mark.asyncio
    async def test_dividends_calendar_no_dates(self, calendar_category, mock_client):
        """Test dividends calendar with no date parameters"""
        mock_response = [
            {
                "symbol": "1D0.SI",
                "date": "2025-02-04",
                "recordDate": "",
                "paymentDate": "",
                "declarationDate": "",
                "adjDividend": 0.01,
                "dividend": 0.01,
                "yield": 6.25,
                "frequency": "Semi-Annual",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.dividends_calendar()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("dividends-calendar", {})

    @pytest.mark.asyncio
    async def test_dividends_calendar_with_dates(self, calendar_category, mock_client):
        """Test dividends calendar with date parameters"""
        mock_response = [{"symbol": "1D0.SI", "date": "2025-02-04"}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.dividends_calendar("2025-01-01", "2025-03-31")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "dividends-calendar", {"from": "2025-01-01", "to": "2025-03-31"}
        )

    @pytest.mark.asyncio
    async def test_earnings_company_basic(self, calendar_category, mock_client):
        """Test earnings company with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-10-29",
                "epsActual": None,
                "epsEstimated": None,
                "revenueActual": None,
                "revenueEstimated": None,
                "lastUpdated": "2025-02-04",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.earnings_company("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "earnings", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_earnings_company_with_limit(self, calendar_category, mock_client):
        """Test earnings company with limit parameter"""
        mock_response = [{"symbol": "AAPL", "date": "2025-10-29"}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.earnings_company("AAPL", limit=20)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "earnings", {"symbol": "AAPL", "limit": 20}
        )

    @pytest.mark.asyncio
    async def test_earnings_calendar_no_dates(self, calendar_category, mock_client):
        """Test earnings calendar with no date parameters"""
        mock_response = [
            {
                "symbol": "KEC.NS",
                "date": "2024-11-04",
                "epsActual": 3.32,
                "epsEstimated": 4.97,
                "revenueActual": 51133100000,
                "revenueEstimated": 44687400000,
                "lastUpdated": "2024-12-08",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.earnings_calendar()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("earnings-calendar", {})

    @pytest.mark.asyncio
    async def test_earnings_calendar_with_dates(self, calendar_category, mock_client):
        """Test earnings calendar with date parameters"""
        mock_response = [{"symbol": "KEC.NS", "date": "2024-11-04"}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.earnings_calendar("2025-01-01", "2025-03-31")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "earnings-calendar", {"from": "2025-01-01", "to": "2025-03-31"}
        )

    @pytest.mark.asyncio
    async def test_ipos_calendar_no_dates(self, calendar_category, mock_client):
        """Test IPOs calendar with no date parameters"""
        mock_response = [
            {
                "symbol": "PEVC",
                "date": "2025-02-03",
                "daa": "2025-02-03T05:00:00.000Z",
                "company": "Pacer Funds Trust",
                "exchange": "NYSE",
                "actions": "Expected",
                "shares": None,
                "priceRange": None,
                "marketCap": None,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_calendar()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("ipos-calendar", {})

    @pytest.mark.asyncio
    async def test_ipos_calendar_with_dates(self, calendar_category, mock_client):
        """Test IPOs calendar with date parameters"""
        mock_response = [{"symbol": "PEVC", "company": "Pacer Funds Trust"}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_calendar("2025-01-01", "2025-06-30")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ipos-calendar", {"from": "2025-01-01", "to": "2025-06-30"}
        )

    @pytest.mark.asyncio
    async def test_ipos_disclosure_no_dates(self, calendar_category, mock_client):
        """Test IPOs disclosure with no date parameters"""
        mock_response = [
            {
                "symbol": "SCHM",
                "filingDate": "2025-02-03",
                "acceptedDate": "2025-02-03",
                "effectivenessDate": "2025-02-03",
                "cik": "0001454889",
                "form": "CERT",
                "url": "https://www.sec.gov/Archives/edgar/data/1454889/000114336225000044/SCCR020325.pdf",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_disclosure()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("ipos-disclosure", {})

    @pytest.mark.asyncio
    async def test_ipos_disclosure_with_dates(self, calendar_category, mock_client):
        """Test IPOs disclosure with date parameters"""
        mock_response = [{"symbol": "SCHM", "cik": "0001454889"}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_disclosure("2025-01-01", "2025-06-30")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ipos-disclosure", {"from": "2025-01-01", "to": "2025-06-30"}
        )

    @pytest.mark.asyncio
    async def test_ipos_prospectus_no_dates(self, calendar_category, mock_client):
        """Test IPOs prospectus with no date parameters"""
        mock_response = [
            {
                "symbol": "ATAK",
                "acceptedDate": "2025-02-03",
                "filingDate": "2025-02-03",
                "ipoDate": "2022-03-20",
                "cik": "0001883788",
                "pricePublicPerShare": 0.78,
                "pricePublicTotal": 4649936.72,
                "discountsAndCommissionsPerShare": 0.04,
                "discountsAndCommissionsTotal": 254909.67,
                "proceedsBeforeExpensesPerShare": 0.74,
                "proceedsBeforeExpensesTotal": 4395207.05,
                "form": "424B4",
                "url": "https://www.sec.gov/Archives/edgar/data/1883788/000149315225004604/form424b4.htm",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_prospectus()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("ipos-prospectus", {})

    @pytest.mark.asyncio
    async def test_ipos_prospectus_with_dates(self, calendar_category, mock_client):
        """Test IPOs prospectus with date parameters"""
        mock_response = [{"symbol": "ATAK", "pricePublicPerShare": 0.78}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.ipos_prospectus("2025-01-01", "2025-06-30")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "ipos-prospectus", {"from": "2025-01-01", "to": "2025-06-30"}
        )

    @pytest.mark.asyncio
    async def test_stock_splits_company_basic(self, calendar_category, mock_client):
        """Test stock splits company with required parameters only"""
        mock_response = [
            {"symbol": "AAPL", "date": "2020-08-31", "numerator": 4, "denominator": 1}
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.stock_splits_company("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("splits", {"symbol": "AAPL"})

    @pytest.mark.asyncio
    async def test_stock_splits_company_with_limit(
        self, calendar_category, mock_client
    ):
        """Test stock splits company with limit parameter"""
        mock_response = [{"symbol": "AAPL", "numerator": 4, "denominator": 1}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.stock_splits_company("AAPL", limit=20)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "splits", {"symbol": "AAPL", "limit": 20}
        )

    @pytest.mark.asyncio
    async def test_stock_splits_calendar_no_dates(self, calendar_category, mock_client):
        """Test stock splits calendar with no date parameters"""
        mock_response = [
            {"symbol": "EYEN", "date": "2025-02-03", "numerator": 1, "denominator": 80}
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.stock_splits_calendar()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("splits-calendar", {})

    @pytest.mark.asyncio
    async def test_stock_splits_calendar_with_dates(
        self, calendar_category, mock_client
    ):
        """Test stock splits calendar with date parameters"""
        mock_response = [{"symbol": "EYEN", "numerator": 1, "denominator": 80}]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.stock_splits_calendar(
            "2025-01-01", "2025-06-30"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "splits-calendar", {"from": "2025-01-01", "to": "2025-06-30"}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, calendar_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await calendar_category.dividends_company("AAPL")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "dividends", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, calendar_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {"symbol": f"STOCK{i}", "date": f"2025-01-{i:02d}", "dividend": 0.01 * i}
            for i in range(1, 101)
        ]
        mock_client._make_request.return_value = large_response

        result = await calendar_category.dividends_company("AAPL", limit=100)

        assert len(result) == 100
        assert result[0]["dividend"] == 0.01
        assert result[99]["dividend"] == 1.0
        mock_client._make_request.assert_called_once_with(
            "dividends", {"symbol": "AAPL", "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, calendar_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "AAPL",
                "date": "2025-02-10",
                "dividend": 0.25,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await calendar_category.dividends_company("AAPL")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "dividends", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, calendar_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "TEST", "date": "2025-01-01"}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await calendar_category.dividends_calendar("2025-01-01")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "dividends-calendar", {"from": "2025-01-01"}
        )

        # Test with only to_date
        result = await calendar_category.dividends_calendar(to_date="2025-03-31")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "dividends-calendar", {"to": "2025-03-31"}
        )

        # Test with both dates
        result = await calendar_category.dividends_calendar("2025-01-01", "2025-03-31")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "dividends-calendar", {"from": "2025-01-01", "to": "2025-03-31"}
        )
