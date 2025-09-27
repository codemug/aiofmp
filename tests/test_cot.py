"""
Unit tests for FMP Commitment of Traders (COT) category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.cot import CommitmentOfTradersCategory


class TestCommitmentOfTradersCategory:
    """Test cases for CommitmentOfTradersCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def cot_category(self, mock_client):
        """COT category instance with mocked client"""
        return CommitmentOfTradersCategory(mock_client)

    @pytest.mark.asyncio
    async def test_cot_report_basic(self, cot_category, mock_client):
        """Test COT report with required parameters only"""
        mock_response = [
            {
                "symbol": "KC",
                "date": "2024-02-27 00:00:00",
                "name": "Coffee (KC)",
                "sector": "SOFTS",
                "marketAndExchangeNames": "COFFEE C - ICE FUTURES U.S.",
                "cftcContractMarketCode": "083731",
                "cftcMarketCode": "ICUS",
                "cftcRegionCode": "1",
                "cftcCommodityCode": "83",
                "openInterestAll": 209453,
                "noncommPositionsLongAll": 75330,
                "noncommPositionsShortAll": 23630,
                "noncommPositionsSpreadAll": 47072,
                "commPositionsLongAll": 79690,
                "commPositionsShortAll": 132114,
                "totReptPositionsLongAll": 202092,
                "totReptPositionsShortAll": 202816,
                "nonreptPositionsLongAll": 7361,
                "nonreptPositionsShortAll": 6637,
                "openInterestOld": 179986,
                "noncommPositionsLongOld": 75483,
                "noncommPositionsShortOld": 35395,
                "noncommPositionsSpreadOld": 27067,
                "commPositionsLongOld": 70693,
                "commPositionsShortOld": 111666,
                "totReptPositionsLongOld": 173243,
                "totReptPositionsShortOld": 174128,
                "nonreptPositionsLongOld": 6743,
                "nonreptPositionsShortOld": 5858,
                "openInterestOther": 29467,
                "noncommPositionsLongOther": 18754,
                "noncommPositionsShortOther": 7142,
                "noncommPositionsSpreadOther": 1098,
                "commPositionsLongOther": 8997,
                "commPositionsShortOther": 20448,
                "totReptPositionsLongOther": 28849,
                "totReptPositionsShortOther": 28688,
                "nonreptPositionsLongOther": 618,
                "nonreptPositionsShortOther": 779,
                "changeInOpenInterestAll": 2957,
                "changeInNoncommLongAll": -3545,
                "changeInNoncommShortAll": 618,
                "changeInNoncommSpeadAll": 1575,
                "changeInCommLongAll": 4978,
                "changeInCommShortAll": 802,
                "changeInTotReptLongAll": 3008,
                "changeInTotReptShortAll": 2995,
                "changeInNonreptLongAll": -51,
                "changeInNonreptShortAll": -38,
                "pctOfOpenInterestAll": 100,
                "pctOfOiNoncommLongAll": 36,
                "pctOfOiNoncommShortAll": 11.3,
                "pctOfOiNoncommSpreadAll": 22.5,
                "pctOfOiCommLongAll": 38,
                "pctOfOiCommShortAll": 63.1,
                "pctOfOiTotReptLongAll": 96.5,
                "pctOfOiTotReptShortAll": 96.8,
                "pctOfOiNonreptLongAll": 3.5,
                "pctOfOiNonreptShortAll": 3.2,
                "pctOfOpenInterestOl": 100,
                "pctOfOiNoncommLongOl": 41.9,
                "pctOfOiNoncommShortOl": 19.7,
                "pctOfOiNoncommSpreadOl": 15,
                "pctOfOiCommLongOl": 39.3,
                "pctOfOiCommShortOl": 62,
                "pctOfOiTotReptLongOl": 96.3,
                "pctOfOiTotReptShortOl": 96.7,
                "pctOfOiNonreptLongOl": 3.7,
                "pctOfOiNonreptShortOl": 3.3,
                "pctOfOpenInterestOther": 100,
                "pctOfOiNoncommLongOther": 63.6,
                "pctOfOiNoncommShortOther": 24.2,
                "pctOfOiNoncommSpreadOther": 3.7,
                "pctOfOiCommLongOther": 30.5,
                "pctOfOiCommShortOther": 69.4,
                "pctOfOiTotReptLongOther": 97.9,
                "pctOfOiTotReptShortOther": 97.4,
                "pctOfOiNonreptLongOther": 2.1,
                "pctOfOiNonreptShortOther": 2.6,
                "tradersTotAll": 357,
                "tradersNoncommLongAll": 132,
                "tradersNoncommShortAll": 77,
                "tradersNoncommSpreadAll": 94,
                "tradersCommLongAll": 106,
                "tradersCommShortAll": 119,
                "tradersTotReptLongAll": 286,
                "tradersTotReptShortAll": 250,
                "tradersTotOl": 351,
                "tradersNoncommLongOl": 136,
                "tradersNoncommShortOl": 72,
                "tradersNoncommSpeadOl": 88,
                "tradersCommLongOl": 94,
                "tradersCommShortOl": 114,
                "tradersTotReptLongOl": 269,
                "tradersTotReptShortOl": 239,
                "tradersTotOther": 164,
                "tradersNoncommLongOther": 31,
                "tradersNoncommShortOther": 34,
                "tradersNoncommSpreadOther": 16,
                "tradersCommLongOther": 59,
                "tradersCommShortOther": 68,
                "tradersTotReptLongOther": 102,
                "tradersTotReptShortOther": 106,
                "concGrossLe4TdrLongAll": 16,
                "concGrossLe4TdrShortAll": 23.7,
                "concGrossLe8TdrLongAll": 25.8,
                "concGrossLe8TdrShortAll": 38.9,
                "concNetLe4TdrLongAll": 9.8,
                "concNetLe4TdrShortAll": 16.2,
                "concNetLe8TdrLongAll": 17.7,
                "concNetLe8TdrShortAll": 25.4,
                "concGrossLe4TdrLongOl": 13.6,
                "concGrossLe4TdrShortOl": 24.7,
                "concGrossLe8TdrLongOl": 23.2,
                "concGrossLe8TdrShortOl": 40.3,
                "concNetLe4TdrLongOl": 11.3,
                "concNetLe4TdrShortOl": 18.2,
                "concNetLe8TdrLongOl": 20.3,
                "concNetLe8TdrShortOl": 31.9,
                "concGrossLe4TdrLongOther": 68.2,
                "concGrossLe4TdrShortOther": 29.1,
                "concGrossLe8TdrLongOther": 77.8,
                "concGrossLe8TdrShortOther": 47.3,
                "concNetLe4TdrLongOther": 64.7,
                "concNetLe4TdrShortOther": 26.7,
                "concNetLe8TdrLongOther": 73.9,
                "concNetLe8TdrShortOther": 44.2,
                "contractUnits": "(CONTRACTS OF 37,500 POUNDS)",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_report("KC")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report", {"symbol": "KC"}
        )

    @pytest.mark.asyncio
    async def test_cot_report_with_dates(self, cot_category, mock_client):
        """Test COT report with date parameters"""
        mock_response = [{"symbol": "KC", "name": "Coffee (KC)", "sector": "SOFTS"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_report("KC", "2024-01-01", "2024-03-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report",
            {"symbol": "KC", "from": "2024-01-01", "to": "2024-03-01"},
        )

    @pytest.mark.asyncio
    async def test_cot_report_with_from_date_only(self, cot_category, mock_client):
        """Test COT report with only from_date parameter"""
        mock_response = [{"symbol": "KC", "name": "Coffee (KC)"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_report("KC", from_date="2024-01-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report", {"symbol": "KC", "from": "2024-01-01"}
        )

    @pytest.mark.asyncio
    async def test_cot_report_with_to_date_only(self, cot_category, mock_client):
        """Test COT report with only to_date parameter"""
        mock_response = [{"symbol": "KC", "name": "Coffee (KC)"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_report("KC", to_date="2024-03-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report", {"symbol": "KC", "to": "2024-03-01"}
        )

    @pytest.mark.asyncio
    async def test_cot_analysis_basic(self, cot_category, mock_client):
        """Test COT analysis with required parameters only"""
        mock_response = [
            {
                "symbol": "B6",
                "date": "2024-02-27 00:00:00",
                "name": "British Pound (B6)",
                "sector": "CURRENCIES",
                "exchange": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
                "currentLongMarketSituation": 66.85,
                "currentShortMarketSituation": 33.15,
                "marketSituation": "Bullish",
                "previousLongMarketSituation": 67.97,
                "previousShortMarketSituation": 32.03,
                "previousMarketSituation": "Bullish",
                "netPostion": 46358,
                "previousNetPosition": 46312,
                "changeInNetPosition": 0.1,
                "marketSentiment": "Increasing Bullish",
                "reversalTrend": False,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_analysis("B6")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-analysis", {"symbol": "B6"}
        )

    @pytest.mark.asyncio
    async def test_cot_analysis_with_dates(self, cot_category, mock_client):
        """Test COT analysis with date parameters"""
        mock_response = [{"symbol": "B6", "marketSituation": "Bullish"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_analysis("B6", "2024-01-01", "2024-03-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-analysis",
            {"symbol": "B6", "from": "2024-01-01", "to": "2024-03-01"},
        )

    @pytest.mark.asyncio
    async def test_cot_analysis_with_from_date_only(self, cot_category, mock_client):
        """Test COT analysis with only from_date parameter"""
        mock_response = [{"symbol": "B6", "marketSituation": "Bullish"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_analysis("B6", from_date="2024-01-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-analysis", {"symbol": "B6", "from": "2024-01-01"}
        )

    @pytest.mark.asyncio
    async def test_cot_analysis_with_to_date_only(self, cot_category, mock_client):
        """Test COT analysis with only to_date parameter"""
        mock_response = [{"symbol": "B6", "marketSituation": "Bullish"}]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_analysis("B6", to_date="2024-03-01")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-analysis", {"symbol": "B6", "to": "2024-03-01"}
        )

    @pytest.mark.asyncio
    async def test_cot_list_basic(self, cot_category, mock_client):
        """Test COT list with no parameters"""
        mock_response = [
            {"symbol": "NG", "name": "Natural Gas (NG)"},
            {"symbol": "KC", "name": "Coffee (KC)"},
            {"symbol": "B6", "name": "British Pound (B6)"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_list()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-list", {}
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, cot_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await cot_category.cot_report("KC")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report", {"symbol": "KC"}
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(self, cot_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response
        large_response = [
            {
                "symbol": f"SYMBOL_{i}",
                "name": f"Commodity {i}",
                "sector": f"SECTOR_{i % 5}",
                "openInterestAll": 100000 + i * 1000,
            }
            for i in range(1, 101)
        ]
        mock_client._make_request.return_value = large_response

        result = await cot_category.cot_report("KC", "2024-01-01", "2024-03-01")

        assert len(result) == 100
        assert result[0]["symbol"] == "SYMBOL_1"
        assert result[99]["symbol"] == "SYMBOL_100"
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report",
            {"symbol": "KC", "from": "2024-01-01", "to": "2024-03-01"},
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, cot_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "symbol": "KC",
                "name": "Coffee (KC)",
                "sector": "SOFTS",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_report("KC")

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-report", {"symbol": "KC"}
        )

    @pytest.mark.asyncio
    async def test_date_parameter_combinations(self, cot_category, mock_client):
        """Test various date parameter combinations"""
        mock_response = [{"symbol": "KC", "name": "Coffee (KC)"}]
        mock_client._make_request.return_value = mock_response

        # Test with only from_date
        result = await cot_category.cot_report("KC", "2024-01-01")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "commitment-of-traders-report", {"symbol": "KC", "from": "2024-01-01"}
        )

        # Test with only to_date
        result = await cot_category.cot_report("KC", to_date="2024-03-01")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "commitment-of-traders-report", {"symbol": "KC", "to": "2024-03-01"}
        )

        # Test with both dates
        result = await cot_category.cot_report("KC", "2024-01-01", "2024-03-01")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "commitment-of-traders-report",
            {"symbol": "KC", "from": "2024-01-01", "to": "2024-03-01"},
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, cot_category, mock_client):
        """Test COT functionality with different symbols"""
        mock_response = [{"symbol": "NG", "name": "Natural Gas (NG)"}]
        mock_client._make_request.return_value = mock_response

        # Test with Natural Gas
        result = await cot_category.cot_report("NG")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "commitment-of-traders-report", {"symbol": "NG"}
        )

        # Test with British Pound
        result = await cot_category.cot_analysis("B6")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "commitment-of-traders-analysis", {"symbol": "B6"}
        )

    @pytest.mark.asyncio
    async def test_cot_list_response_validation(self, cot_category, mock_client):
        """Test COT list response validation"""
        mock_response = [
            {"symbol": "NG", "name": "Natural Gas (NG)"},
            {"symbol": "KC", "name": "Coffee (KC)"},
            {"symbol": "B6", "name": "British Pound (B6)"},
            {"symbol": "GC", "name": "Gold (GC)"},
            {"symbol": "SI", "name": "Silver (SI)"},
        ]
        mock_client._make_request.return_value = mock_response

        result = await cot_category.cot_list()

        assert len(result) == 5
        assert result[0]["symbol"] == "NG"
        assert result[0]["name"] == "Natural Gas (NG)"
        assert result[4]["symbol"] == "SI"
        assert result[4]["name"] == "Silver (SI)"
        mock_client._make_request.assert_called_once_with(
            "commitment-of-traders-list", {}
        )
