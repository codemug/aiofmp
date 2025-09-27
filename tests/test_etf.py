"""
Unit tests for FMP ETF And Mutual Funds category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.etf import EtfAndMutualFundsCategory


class TestEtfAndMutualFundsCategory:
    """Test cases for EtfAndMutualFundsCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def etf_category(self, mock_client):
        """ETF category instance with mocked client"""
        return EtfAndMutualFundsCategory(mock_client)

    @pytest.mark.asyncio
    async def test_holdings_basic(self, etf_category, mock_client):
        """Test holdings with required parameters only"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "AAPL",
                "name": "APPLE INC",
                "isin": "US0378331005",
                "securityCusip": "037833100",
                "sharesNumber": 188106081,
                "weightPercentage": 7.137,
                "marketValue": 44744793487.47,
                "updatedAt": "2025-01-16 05:01:09",
                "updated": "2025-02-04 19:02:31",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.holdings("SPY")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_holdings_response_structure(self, etf_category, mock_client):
        """Test holdings response structure"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "MSFT",
                "name": "MICROSOFT CORP",
                "isin": "US5949181045",
                "securityCusip": "594918104",
                "sharesNumber": 150000000,
                "weightPercentage": 6.5,
                "marketValue": 50000000000.00,
                "updatedAt": "2025-01-16 05:01:09",
                "updated": "2025-02-04 19:02:31",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.holdings("SPY")

        assert len(result) == 1
        assert result[0]["symbol"] == "SPY"
        assert result[0]["asset"] == "MSFT"
        assert result[0]["name"] == "MICROSOFT CORP"
        assert result[0]["sharesNumber"] == 150000000
        assert result[0]["weightPercentage"] == 6.5
        assert result[0]["marketValue"] == 50000000000.00
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_info_basic(self, etf_category, mock_client):
        """Test info with required parameters only"""
        mock_response = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "description": "The Trust seeks to achieve its investment objective by holding a portfolio of the common stocks that are included in the index (the 'Portfolio'), with the weight of each stock in the Portfolio substantially corresponding to the weight of such stock in the index.",
                "isin": "US78462F1030",
                "assetClass": "Equity",
                "securityCusip": "78462F103",
                "domicile": "US",
                "website": "https://www.ssga.com/us/en/institutional/etfs/spdr-sp-500-etf-trust-spy",
                "etfCompany": "SPDR",
                "expenseRatio": 0.0945,
                "assetsUnderManagement": 633120180000,
                "avgVolume": 46396400,
                "inceptionDate": "1993-01-22",
                "nav": 603.64,
                "navCurrency": "USD",
                "holdingsCount": 503,
                "updatedAt": "2024-12-03T20:32:48.873Z",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.info("SPY")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("etf/info", {"symbol": "SPY"})

    @pytest.mark.asyncio
    async def test_info_response_structure(self, etf_category, mock_client):
        """Test info response structure"""
        mock_response = [
            {
                "symbol": "QQQ",
                "name": "Invesco QQQ Trust",
                "description": "The Invesco QQQ Trust is an exchange-traded fund that tracks the Nasdaq-100 Index.",
                "isin": "US46090E1038",
                "assetClass": "Equity",
                "securityCusip": "46090E103",
                "domicile": "US",
                "website": "https://www.invesco.com/us/financial-products/etfs/product-detail?ticker=QQQ",
                "etfCompany": "Invesco",
                "expenseRatio": 0.20,
                "assetsUnderManagement": 200000000000,
                "avgVolume": 25000000,
                "inceptionDate": "1999-03-10",
                "nav": 400.50,
                "navCurrency": "USD",
                "holdingsCount": 100,
                "updatedAt": "2024-12-03T20:32:48.873Z",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.info("QQQ")

        assert len(result) == 1
        assert result[0]["symbol"] == "QQQ"
        assert result[0]["name"] == "Invesco QQQ Trust"
        assert result[0]["expenseRatio"] == 0.20
        assert result[0]["assetsUnderManagement"] == 200000000000
        assert result[0]["holdingsCount"] == 100
        mock_client._make_request.assert_called_once_with("etf/info", {"symbol": "QQQ"})

    @pytest.mark.asyncio
    async def test_country_weightings_basic(self, etf_category, mock_client):
        """Test country weightings with required parameters only"""
        mock_response = [
            {"country": "United States", "weightPercentage": "97.29%"},
            {"country": "United Kingdom", "weightPercentage": "1.45%"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.country_weightings("SPY")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "etf/country-weightings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_country_weightings_response_structure(
        self, etf_category, mock_client
    ):
        """Test country weightings response structure"""
        mock_response = [
            {"country": "United States", "weightPercentage": "95.50%"},
            {"country": "Japan", "weightPercentage": "2.30%"},
            {"country": "Germany", "weightPercentage": "1.20%"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.country_weightings("VTI")

        assert len(result) == 3
        assert result[0]["country"] == "United States"
        assert result[0]["weightPercentage"] == "95.50%"
        assert result[1]["country"] == "Japan"
        assert result[1]["weightPercentage"] == "2.30%"
        assert result[2]["country"] == "Germany"
        assert result[2]["weightPercentage"] == "1.20%"
        mock_client._make_request.assert_called_once_with(
            "etf/country-weightings", {"symbol": "VTI"}
        )

    @pytest.mark.asyncio
    async def test_asset_exposure_basic(self, etf_category, mock_client):
        """Test asset exposure with required parameters only"""
        mock_response = [
            {
                "symbol": "ZECP",
                "asset": "AAPL",
                "sharesNumber": 5482,
                "weightPercentage": 5.86,
                "marketValue": 0,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.asset_exposure("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "etf/asset-exposure", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_asset_exposure_response_structure(self, etf_category, mock_client):
        """Test asset exposure response structure"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "MSFT",
                "sharesNumber": 150000000,
                "weightPercentage": 6.5,
                "marketValue": 50000000000.00,
            },
            {
                "symbol": "QQQ",
                "asset": "MSFT",
                "sharesNumber": 80000000,
                "weightPercentage": 8.2,
                "marketValue": 32000000000.00,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.asset_exposure("MSFT")

        assert len(result) == 2
        assert result[0]["symbol"] == "SPY"
        assert result[0]["asset"] == "MSFT"
        assert result[0]["sharesNumber"] == 150000000
        assert result[0]["weightPercentage"] == 6.5
        assert result[1]["symbol"] == "QQQ"
        assert result[1]["weightPercentage"] == 8.2
        mock_client._make_request.assert_called_once_with(
            "etf/asset-exposure", {"symbol": "MSFT"}
        )

    @pytest.mark.asyncio
    async def test_sector_weightings_basic(self, etf_category, mock_client):
        """Test sector weightings with required parameters only"""
        mock_response = [
            {"symbol": "SPY", "sector": "Basic Materials", "weightPercentage": 1.97},
            {
                "symbol": "SPY",
                "sector": "Communication Services",
                "weightPercentage": 8.87,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.sector_weightings("SPY")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "etf/sector-weightings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_sector_weightings_response_structure(
        self, etf_category, mock_client
    ):
        """Test sector weightings response structure"""
        mock_response = [
            {"symbol": "VTI", "sector": "Technology", "weightPercentage": 25.5},
            {"symbol": "VTI", "sector": "Healthcare", "weightPercentage": 15.2},
            {"symbol": "VTI", "sector": "Financial Services", "weightPercentage": 12.8},
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.sector_weightings("VTI")

        assert len(result) == 3
        assert result[0]["symbol"] == "VTI"
        assert result[0]["sector"] == "Technology"
        assert result[0]["weightPercentage"] == 25.5
        assert result[1]["sector"] == "Healthcare"
        assert result[1]["weightPercentage"] == 15.2
        assert result[2]["sector"] == "Financial Services"
        assert result[2]["weightPercentage"] == 12.8
        mock_client._make_request.assert_called_once_with(
            "etf/sector-weightings", {"symbol": "VTI"}
        )

    @pytest.mark.asyncio
    async def test_disclosure_holders_latest_basic(self, etf_category, mock_client):
        """Test disclosure holders latest with required parameters only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "holder": "Vanguard Total Stock Market ETF",
                "shares": 1000000,
                "weightPercentage": 2.5,
                "marketValue": 150000000.00,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.disclosure_holders_latest("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "funds/disclosure-holders-latest", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_disclosure_holders_latest_response_structure(
        self, etf_category, mock_client
    ):
        """Test disclosure holders latest response structure"""
        mock_response = [
            {
                "symbol": "MSFT",
                "holder": "SPDR S&P 500 ETF Trust",
                "shares": 2000000,
                "weightPercentage": 3.2,
                "marketValue": 800000000.00,
            },
            {
                "symbol": "MSFT",
                "holder": "Invesco QQQ Trust",
                "shares": 1500000,
                "weightPercentage": 4.1,
                "marketValue": 600000000.00,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.disclosure_holders_latest("MSFT")

        assert len(result) == 2
        assert result[0]["symbol"] == "MSFT"
        assert result[0]["holder"] == "SPDR S&P 500 ETF Trust"
        assert result[0]["shares"] == 2000000
        assert result[0]["weightPercentage"] == 3.2
        assert result[1]["holder"] == "Invesco QQQ Trust"
        assert result[1]["shares"] == 1500000
        assert result[1]["weightPercentage"] == 4.1
        mock_client._make_request.assert_called_once_with(
            "funds/disclosure-holders-latest", {"symbol": "MSFT"}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, etf_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await etf_category.holdings("SPY")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, etf_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple holdings
        large_response = [
            {
                "symbol": "SPY",
                "asset": f"STOCK_{i}",
                "name": f"Company {i}",
                "sharesNumber": 1000000 + i * 100000,
                "weightPercentage": 1.0 + i * 0.1,
                "marketValue": 50000000 + i * 1000000,
            }
            for i in range(1, 101)  # 100 holdings
        ]
        mock_client._make_request.return_value = large_response

        result = await etf_category.holdings("SPY")

        assert len(result) == 100
        assert result[0]["asset"] == "STOCK_1"
        assert result[99]["asset"] == "STOCK_100"
        assert result[0]["sharesNumber"] == 1100000
        assert result[99]["sharesNumber"] == 11000000
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, etf_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "AAPL",
                "name": "APPLE INC",
                "sharesNumber": 188106081,
                "weightPercentage": 7.137,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.holdings("SPY")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, etf_category, mock_client):
        """Test ETF functionality with different symbols"""
        mock_response = [{"symbol": "QQQ", "asset": "AAPL", "name": "APPLE INC"}]
        mock_client._make_request.return_value = mock_response

        # Test with QQQ
        result = await etf_category.holdings("QQQ")
        assert result == mock_response
        mock_client._make_request.assert_called_with("etf/holdings", {"symbol": "QQQ"})

        # Test with VTI
        result = await etf_category.holdings("VTI")
        assert result == mock_response
        mock_client._make_request.assert_called_with("etf/holdings", {"symbol": "VTI"})

        # Test with IEMG
        result = await etf_category.holdings("IEMG")
        assert result == mock_response
        mock_client._make_request.assert_called_with("etf/holdings", {"symbol": "IEMG"})

    @pytest.mark.asyncio
    async def test_holdings_response_validation(self, etf_category, mock_client):
        """Test holdings response validation"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "AAPL",
                "name": "APPLE INC",
                "isin": "US0378331005",
                "securityCusip": "037833100",
                "sharesNumber": 188106081,
                "weightPercentage": 7.137,
                "marketValue": 44744793487.47,
                "updatedAt": "2025-01-16 05:01:09",
                "updated": "2025-02-04 19:02:31",
            },
            {
                "symbol": "SPY",
                "asset": "MSFT",
                "name": "MICROSOFT CORP",
                "isin": "US5949181045",
                "securityCusip": "594918104",
                "sharesNumber": 150000000,
                "weightPercentage": 6.5,
                "marketValue": 50000000000.00,
                "updatedAt": "2025-01-16 05:01:09",
                "updated": "2025-02-04 19:02:31",
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.holdings("SPY")

        assert len(result) == 2
        assert result[0]["asset"] == "AAPL"
        assert result[0]["weightPercentage"] == 7.137
        assert result[1]["asset"] == "MSFT"
        assert result[1]["weightPercentage"] == 6.5
        mock_client._make_request.assert_called_once_with(
            "etf/holdings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_info_response_validation(self, etf_category, mock_client):
        """Test info response validation"""
        mock_response = [
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "description": "The Trust seeks to achieve its investment objective by holding a portfolio of the common stocks that are included in the index (the 'Portfolio'), with the weight of each stock in the Portfolio substantially corresponding to the weight of such stock in the index.",
                "isin": "US78462F1030",
                "assetClass": "Equity",
                "securityCusip": "78462F103",
                "domicile": "US",
                "website": "https://www.ssga.com/us/en/institutional/etfs/spdr-sp-500-etf-trust-spy",
                "etfCompany": "SPDR",
                "expenseRatio": 0.0945,
                "assetsUnderManagement": 633120180000,
                "avgVolume": 46396400,
                "inceptionDate": "1993-01-22",
                "nav": 603.64,
                "navCurrency": "USD",
                "holdingsCount": 503,
                "updatedAt": "2024-12-03T20:32:48.873Z",
                "sectorsList": [
                    {"industry": "Basic Materials", "exposure": 1.97},
                    {"industry": "Communication Services", "exposure": 8.87},
                ],
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.info("SPY")

        assert len(result) == 1
        assert result[0]["symbol"] == "SPY"
        assert result[0]["name"] == "SPDR S&P 500 ETF Trust"
        assert result[0]["expenseRatio"] == 0.0945
        assert result[0]["assetsUnderManagement"] == 633120180000
        assert result[0]["holdingsCount"] == 503
        assert len(result[0]["sectorsList"]) == 2
        assert result[0]["sectorsList"][0]["industry"] == "Basic Materials"
        assert result[0]["sectorsList"][0]["exposure"] == 1.97
        mock_client._make_request.assert_called_once_with("etf/info", {"symbol": "SPY"})

    @pytest.mark.asyncio
    async def test_asset_exposure_response_validation(self, etf_category, mock_client):
        """Test asset exposure response validation"""
        mock_response = [
            {
                "symbol": "SPY",
                "asset": "AAPL",
                "sharesNumber": 188106081,
                "weightPercentage": 7.137,
                "marketValue": 44744793487.47,
            },
            {
                "symbol": "QQQ",
                "asset": "AAPL",
                "sharesNumber": 80000000,
                "weightPercentage": 8.2,
                "marketValue": 32000000000.00,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.asset_exposure("AAPL")

        assert len(result) == 2
        assert result[0]["symbol"] == "SPY"
        assert result[0]["sharesNumber"] == 188106081
        assert result[0]["weightPercentage"] == 7.137
        assert result[1]["symbol"] == "QQQ"
        assert result[1]["sharesNumber"] == 80000000
        assert result[1]["weightPercentage"] == 8.2
        mock_client._make_request.assert_called_once_with(
            "etf/asset-exposure", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_sector_weightings_response_validation(
        self, etf_category, mock_client
    ):
        """Test sector weightings response validation"""
        mock_response = [
            {"symbol": "SPY", "sector": "Basic Materials", "weightPercentage": 1.97},
            {
                "symbol": "SPY",
                "sector": "Communication Services",
                "weightPercentage": 8.87,
            },
            {"symbol": "SPY", "sector": "Consumer Cyclical", "weightPercentage": 9.84},
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.sector_weightings("SPY")

        assert len(result) == 3
        assert result[0]["sector"] == "Basic Materials"
        assert result[0]["weightPercentage"] == 1.97
        assert result[1]["sector"] == "Communication Services"
        assert result[1]["weightPercentage"] == 8.87
        assert result[2]["sector"] == "Consumer Cyclical"
        assert result[2]["weightPercentage"] == 9.84
        mock_client._make_request.assert_called_once_with(
            "etf/sector-weightings", {"symbol": "SPY"}
        )

    @pytest.mark.asyncio
    async def test_disclosure_holders_latest_response_validation(
        self, etf_category, mock_client
    ):
        """Test disclosure holders latest response validation"""
        mock_response = [
            {
                "symbol": "AAPL",
                "holder": "Vanguard Total Stock Market ETF",
                "shares": 1000000,
                "weightPercentage": 2.5,
                "marketValue": 150000000.00,
            },
            {
                "symbol": "AAPL",
                "holder": "SPDR S&P 500 ETF Trust",
                "shares": 2000000,
                "weightPercentage": 5.0,
                "marketValue": 300000000.00,
            },
        ]
        mock_client._make_request.return_value = mock_response

        result = await etf_category.disclosure_holders_latest("AAPL")

        assert len(result) == 2
        assert result[0]["holder"] == "Vanguard Total Stock Market ETF"
        assert result[0]["shares"] == 1000000
        assert result[0]["weightPercentage"] == 2.5
        assert result[1]["holder"] == "SPDR S&P 500 ETF Trust"
        assert result[1]["shares"] == 2000000
        assert result[1]["weightPercentage"] == 5.0
        mock_client._make_request.assert_called_once_with(
            "funds/disclosure-holders-latest", {"symbol": "AAPL"}
        )
