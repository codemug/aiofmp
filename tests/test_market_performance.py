"""
Unit tests for FMP Market Performance category
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.market_performance import MarketPerformanceCategory


class TestMarketPerformanceCategory:
    """Test cases for MarketPerformanceCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def market_performance_category(self, mock_client):
        """Market Performance category instance with mocked client"""
        return MarketPerformanceCategory(mock_client)

    @pytest.mark.asyncio
    async def test_sector_performance_snapshot_basic(
        self, market_performance_category, mock_client
    ):
        """Test sector performance snapshot with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Basic Materials",
                "exchange": "NASDAQ",
                "averageChange": -0.31481377464310634,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_sector_performance_snapshot_with_optional_params(
        self, market_performance_category, mock_client
    ):
        """Test sector performance snapshot with all parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="NASDAQ", sector="Energy"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot",
            {"date": "2024-02-01", "exchange": "NASDAQ", "sector": "Energy"},
        )

    @pytest.mark.asyncio
    async def test_industry_performance_snapshot_basic(
        self, market_performance_category, mock_client
    ):
        """Test industry performance snapshot with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Advertising Agencies",
                "exchange": "NASDAQ",
                "averageChange": 3.8660194344955996,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_performance_snapshot(
            snapshot_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "industry-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_industry_performance_snapshot_with_optional_params(
        self, market_performance_category, mock_client
    ):
        """Test industry performance snapshot with all parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "averageChange": 1.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_performance_snapshot(
            snapshot_date, exchange="NASDAQ", industry="Biotechnology"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "industry-performance-snapshot",
            {"date": "2024-02-01", "exchange": "NASDAQ", "industry": "Biotechnology"},
        )

    @pytest.mark.asyncio
    async def test_historical_sector_performance_basic(
        self, market_performance_category, mock_client
    ):
        """Test historical sector performance with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.6397534025664513,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.historical_sector_performance(
            "Energy"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-sector-performance", {"sector": "Energy"}
        )

    @pytest.mark.asyncio
    async def test_historical_sector_performance_with_dates(
        self, market_performance_category, mock_client
    ):
        """Test historical sector performance with date parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.6398,
            }
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2024, 2, 1)
        to_date = date(2024, 3, 1)

        result = await market_performance_category.historical_sector_performance(
            "Energy", from_date=from_date, to_date=to_date, exchange="NASDAQ"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-sector-performance",
            {
                "sector": "Energy",
                "from": "2024-02-01",
                "to": "2024-03-01",
                "exchange": "NASDAQ",
            },
        )

    @pytest.mark.asyncio
    async def test_historical_industry_performance_basic(
        self, market_performance_category, mock_client
    ):
        """Test historical industry performance with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "averageChange": 1.1479066960358322,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.historical_industry_performance(
            "Biotechnology"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-industry-performance", {"industry": "Biotechnology"}
        )

    @pytest.mark.asyncio
    async def test_historical_industry_performance_with_dates(
        self, market_performance_category, mock_client
    ):
        """Test historical industry performance with date parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "averageChange": 1.1479,
            }
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2024, 2, 1)
        to_date = date(2024, 3, 1)

        result = await market_performance_category.historical_industry_performance(
            "Biotechnology", from_date=from_date, to_date=to_date, exchange="NASDAQ"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-industry-performance",
            {
                "industry": "Biotechnology",
                "from": "2024-02-01",
                "to": "2024-03-01",
                "exchange": "NASDAQ",
            },
        )

    @pytest.mark.asyncio
    async def test_sector_pe_snapshot_basic(
        self, market_performance_category, mock_client
    ):
        """Test sector P/E snapshot with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Basic Materials",
                "exchange": "NASDAQ",
                "pe": 15.687711758428254,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_pe_snapshot(snapshot_date)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "sector-pe-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_sector_pe_snapshot_with_optional_params(
        self, market_performance_category, mock_client
    ):
        """Test sector P/E snapshot with all parameters"""
        mock_response = [
            {"date": "2024-02-01", "sector": "Energy", "exchange": "NASDAQ", "pe": 14.5}
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_pe_snapshot(
            snapshot_date, exchange="NASDAQ", sector="Energy"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "sector-pe-snapshot",
            {"date": "2024-02-01", "exchange": "NASDAQ", "sector": "Energy"},
        )

    @pytest.mark.asyncio
    async def test_industry_pe_snapshot_basic(
        self, market_performance_category, mock_client
    ):
        """Test industry P/E snapshot with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Advertising Agencies",
                "exchange": "NASDAQ",
                "pe": 71.09601665201151,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_pe_snapshot(snapshot_date)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "industry-pe-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_industry_pe_snapshot_with_optional_params(
        self, market_performance_category, mock_client
    ):
        """Test industry P/E snapshot with all parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "pe": 10.2,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_pe_snapshot(
            snapshot_date, exchange="NASDAQ", industry="Biotechnology"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "industry-pe-snapshot",
            {"date": "2024-02-01", "exchange": "NASDAQ", "industry": "Biotechnology"},
        )

    @pytest.mark.asyncio
    async def test_historical_sector_pe_basic(
        self, market_performance_category, mock_client
    ):
        """Test historical sector P/E with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "pe": 14.411400922841464,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.historical_sector_pe("Energy")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-sector-pe", {"sector": "Energy"}
        )

    @pytest.mark.asyncio
    async def test_historical_sector_pe_with_dates(
        self, market_performance_category, mock_client
    ):
        """Test historical sector P/E with date parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "pe": 14.4114,
            }
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2024, 2, 1)
        to_date = date(2024, 3, 1)

        result = await market_performance_category.historical_sector_pe(
            "Energy", from_date=from_date, to_date=to_date, exchange="NASDAQ"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-sector-pe",
            {
                "sector": "Energy",
                "from": "2024-02-01",
                "to": "2024-03-01",
                "exchange": "NASDAQ",
            },
        )

    @pytest.mark.asyncio
    async def test_historical_industry_pe_basic(
        self, market_performance_category, mock_client
    ):
        """Test historical industry P/E with required parameter only"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "pe": 10.181600321811821,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.historical_industry_pe(
            "Biotechnology"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-industry-pe", {"industry": "Biotechnology"}
        )

    @pytest.mark.asyncio
    async def test_historical_industry_pe_with_dates(
        self, market_performance_category, mock_client
    ):
        """Test historical industry P/E with date parameters"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "pe": 10.1816,
            }
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2024, 2, 1)
        to_date = date(2024, 3, 1)

        result = await market_performance_category.historical_industry_pe(
            "Biotechnology", from_date=from_date, to_date=to_date, exchange="NASDAQ"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "historical-industry-pe",
            {
                "industry": "Biotechnology",
                "from": "2024-02-01",
                "to": "2024-03-01",
                "exchange": "NASDAQ",
            },
        )

    @pytest.mark.asyncio
    async def test_biggest_gainers_basic(
        self, market_performance_category, mock_client
    ):
        """Test biggest gainers with no parameters"""
        mock_response = [
            {
                "symbol": "LTRY",
                "price": 0.5876,
                "name": "Lottery.com Inc.",
                "change": 0.2756,
                "changesPercentage": 88.3333,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.biggest_gainers()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("biggest-gainers")

    @pytest.mark.asyncio
    async def test_biggest_losers_basic(self, market_performance_category, mock_client):
        """Test biggest losers with no parameters"""
        mock_response = [
            {
                "symbol": "IDEX",
                "price": 0.0021,
                "name": "Ideanomics, Inc.",
                "change": -0.0029,
                "changesPercentage": -58,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.biggest_losers()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("biggest-losers")

    @pytest.mark.asyncio
    async def test_most_active_stocks_basic(
        self, market_performance_category, mock_client
    ):
        """Test most active stocks with no parameters"""
        mock_response = [
            {
                "symbol": "LUCY",
                "price": 5.03,
                "name": "Innovative Eyewear, Inc.",
                "change": -0.01,
                "changesPercentage": -0.1984,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.most_active_stocks()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("most-actives")

    @pytest.mark.asyncio
    async def test_empty_response_handling(
        self, market_performance_category, mock_client
    ):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(
        self, market_performance_category, mock_client
    ):
        """Test handling of large responses"""
        # Create a large mock response with multiple sectors
        large_response = [
            {
                "date": "2024-02-01",
                "sector": f"Sector {i:03d}",
                "exchange": "NASDAQ",
                "averageChange": 0.1 + (i * 0.01),
            }
            for i in range(1, 101)  # 100 sectors
        ]
        mock_client._make_request.return_value = large_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )

        assert len(result) == 100
        assert result[0]["sector"] == "Sector 001"
        assert result[99]["sector"] == "Sector 100"
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(
        self, market_performance_category, mock_client
    ):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Basic Materials",
                "exchange": "NASDAQ",
                "averageChange": -0.3148,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_different_sectors(self, market_performance_category, mock_client):
        """Test market performance functionality with different sectors"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        # Test with Energy sector
        result = await market_performance_category.historical_sector_performance(
            "Energy"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Energy"}
        )

        # Test with Technology sector
        result = await market_performance_category.historical_sector_performance(
            "Technology"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Technology"}
        )

        # Test with Healthcare sector
        result = await market_performance_category.historical_sector_performance(
            "Healthcare"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Healthcare"}
        )

    @pytest.mark.asyncio
    async def test_different_industries(self, market_performance_category, mock_client):
        """Test market performance functionality with different industries"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Biotechnology",
                "exchange": "NASDAQ",
                "averageChange": 1.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        # Test with Biotechnology industry
        result = await market_performance_category.historical_industry_performance(
            "Biotechnology"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-industry-performance", {"industry": "Biotechnology"}
        )

        # Test with Software industry
        result = await market_performance_category.historical_industry_performance(
            "Software"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-industry-performance", {"industry": "Software"}
        )

        # Test with Banking industry
        result = await market_performance_category.historical_industry_performance(
            "Banking"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-industry-performance", {"industry": "Banking"}
        )

    @pytest.mark.asyncio
    async def test_different_exchanges(self, market_performance_category, mock_client):
        """Test market performance functionality with different exchanges"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)

        # Test with NASDAQ
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="NASDAQ"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01", "exchange": "NASDAQ"}
        )

        # Test with NYSE
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="NYSE"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01", "exchange": "NYSE"}
        )

        # Test with AMEX
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="AMEX"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01", "exchange": "AMEX"}
        )

    @pytest.mark.asyncio
    async def test_date_edge_cases(self, market_performance_category, mock_client):
        """Test date handling edge cases"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        # Test with leap year date
        leap_date = date(2024, 2, 29)
        result = await market_performance_category.sector_performance_snapshot(
            leap_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-29"}
        )

        # Test with year boundary
        year_boundary = date(2024, 12, 31)
        result = await market_performance_category.sector_performance_snapshot(
            year_boundary
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-12-31"}
        )

        # Test with beginning of year
        year_beginning = date(2024, 1, 1)
        result = await market_performance_category.sector_performance_snapshot(
            year_beginning
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-01-01"}
        )

    @pytest.mark.asyncio
    async def test_sector_performance_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test sector performance response validation"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Basic Materials",
                "exchange": "NASDAQ",
                "averageChange": -0.31481377464310634,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )

        assert len(result) == 1
        assert result[0]["date"] == "2024-02-01"
        assert result[0]["sector"] == "Basic Materials"
        assert result[0]["exchange"] == "NASDAQ"
        assert result[0]["averageChange"] == -0.31481377464310634
        mock_client._make_request.assert_called_once_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_industry_performance_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test industry performance response validation"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Advertising Agencies",
                "exchange": "NASDAQ",
                "averageChange": 3.8660194344955996,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_performance_snapshot(
            snapshot_date
        )

        assert len(result) == 1
        assert result[0]["date"] == "2024-02-01"
        assert result[0]["industry"] == "Advertising Agencies"
        assert result[0]["exchange"] == "NASDAQ"
        assert result[0]["averageChange"] == 3.8660194344955996
        mock_client._make_request.assert_called_once_with(
            "industry-performance-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_sector_pe_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test sector P/E response validation"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Basic Materials",
                "exchange": "NASDAQ",
                "pe": 15.687711758428254,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.sector_pe_snapshot(snapshot_date)

        assert len(result) == 1
        assert result[0]["date"] == "2024-02-01"
        assert result[0]["sector"] == "Basic Materials"
        assert result[0]["exchange"] == "NASDAQ"
        assert result[0]["pe"] == 15.687711758428254
        mock_client._make_request.assert_called_once_with(
            "sector-pe-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_industry_pe_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test industry P/E response validation"""
        mock_response = [
            {
                "date": "2024-02-01",
                "industry": "Advertising Agencies",
                "exchange": "NASDAQ",
                "pe": 71.09601665201151,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)
        result = await market_performance_category.industry_pe_snapshot(snapshot_date)

        assert len(result) == 1
        assert result[0]["date"] == "2024-02-01"
        assert result[0]["industry"] == "Advertising Agencies"
        assert result[0]["exchange"] == "NASDAQ"
        assert result[0]["pe"] == 71.09601665201151
        mock_client._make_request.assert_called_once_with(
            "industry-pe-snapshot", {"date": "2024-02-01"}
        )

    @pytest.mark.asyncio
    async def test_biggest_gainers_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test biggest gainers response validation"""
        mock_response = [
            {
                "symbol": "LTRY",
                "price": 0.5876,
                "name": "Lottery.com Inc.",
                "change": 0.2756,
                "changesPercentage": 88.3333,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.biggest_gainers()

        assert len(result) == 1
        assert result[0]["symbol"] == "LTRY"
        assert result[0]["price"] == 0.5876
        assert result[0]["name"] == "Lottery.com Inc."
        assert result[0]["change"] == 0.2756
        assert result[0]["changesPercentage"] == 88.3333
        mock_client._make_request.assert_called_once_with("biggest-gainers")

    @pytest.mark.asyncio
    async def test_biggest_losers_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test biggest losers response validation"""
        mock_response = [
            {
                "symbol": "IDEX",
                "price": 0.0021,
                "name": "Ideanomics, Inc.",
                "change": -0.0029,
                "changesPercentage": -58,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.biggest_losers()

        assert len(result) == 1
        assert result[0]["symbol"] == "IDEX"
        assert result[0]["price"] == 0.0021
        assert result[0]["name"] == "Ideanomics, Inc."
        assert result[0]["change"] == -0.0029
        assert result[0]["changesPercentage"] == -58
        mock_client._make_request.assert_called_once_with("biggest-losers")

    @pytest.mark.asyncio
    async def test_most_active_stocks_response_validation(
        self, market_performance_category, mock_client
    ):
        """Test most active stocks response validation"""
        mock_response = [
            {
                "symbol": "LUCY",
                "price": 5.03,
                "name": "Innovative Eyewear, Inc.",
                "change": -0.01,
                "changesPercentage": -0.1984,
                "exchange": "NASDAQ",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await market_performance_category.most_active_stocks()

        assert len(result) == 1
        assert result[0]["symbol"] == "LUCY"
        assert result[0]["price"] == 5.03
        assert result[0]["name"] == "Innovative Eyewear, Inc."
        assert result[0]["change"] == -0.01
        assert result[0]["changesPercentage"] == -0.1984
        mock_client._make_request.assert_called_once_with("most-actives")

    @pytest.mark.asyncio
    async def test_parameter_combinations(
        self, market_performance_category, mock_client
    ):
        """Test various parameter combinations"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        snapshot_date = date(2024, 2, 1)

        # Test with only date
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01"}
        )

        # Test with date and exchange
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="NASDAQ"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01", "exchange": "NASDAQ"}
        )

        # Test with date and sector
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, sector="Energy"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot", {"date": "2024-02-01", "sector": "Energy"}
        )

        # Test with all parameters
        result = await market_performance_category.sector_performance_snapshot(
            snapshot_date, exchange="NASDAQ", sector="Energy"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "sector-performance-snapshot",
            {"date": "2024-02-01", "exchange": "NASDAQ", "sector": "Energy"},
        )

    @pytest.mark.asyncio
    async def test_historical_date_combinations(
        self, market_performance_category, mock_client
    ):
        """Test historical data with different date combinations"""
        mock_response = [
            {
                "date": "2024-02-01",
                "sector": "Energy",
                "exchange": "NASDAQ",
                "averageChange": 0.5,
            }
        ]
        mock_client._make_request.return_value = mock_response

        # Test with only sector
        result = await market_performance_category.historical_sector_performance(
            "Energy"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Energy"}
        )

        # Test with sector and from_date
        from_date = date(2024, 2, 1)
        result = await market_performance_category.historical_sector_performance(
            "Energy", from_date=from_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Energy", "from": "2024-02-01"}
        )

        # Test with sector and to_date
        to_date = date(2024, 3, 1)
        result = await market_performance_category.historical_sector_performance(
            "Energy", to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Energy", "to": "2024-03-01"}
        )

        # Test with sector and exchange
        result = await market_performance_category.historical_sector_performance(
            "Energy", exchange="NASDAQ"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "historical-sector-performance", {"sector": "Energy", "exchange": "NASDAQ"}
        )
