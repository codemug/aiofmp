"""
Unit tests for FMP Technical Indicators category
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.technical_indicators import TechnicalIndicatorsCategory


class TestTechnicalIndicatorsCategory:
    """Test cases for TechnicalIndicatorsCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def technical_indicators_category(self, mock_client):
        """Technical Indicators category instance with mocked client"""
        return TechnicalIndicatorsCategory(mock_client)

    @pytest.mark.asyncio
    async def test_simple_moving_average_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test simple moving average with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "sma": 231.215,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_simple_moving_average_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test simple moving average with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_exponential_moving_average_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test exponential moving average with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "ema": 232.8406611792779,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.exponential_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/ema",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_exponential_moving_average_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test exponential moving average with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "ema": 232.8406611792779}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.exponential_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/ema",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_weighted_moving_average_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test weighted moving average with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "wma": 233.04745454545454,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.weighted_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/wma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_weighted_moving_average_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test weighted moving average with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "wma": 233.04745454545454}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.weighted_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/wma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_double_exponential_moving_average_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test double exponential moving average with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "dema": 232.10592058582725,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.double_exponential_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/dema",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_double_exponential_moving_average_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test double exponential moving average with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "dema": 232.10592058582725}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.double_exponential_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/dema",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_triple_exponential_moving_average_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test triple exponential moving average with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "tema": 233.66383715917516,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.triple_exponential_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/tema",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_triple_exponential_moving_average_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test triple exponential moving average with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "tema": 233.66383715917516}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.triple_exponential_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/tema",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_relative_strength_index_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test relative strength index with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "rsi": 47.64507340768903,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.relative_strength_index(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/rsi",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_relative_strength_index_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test relative strength index with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "rsi": 47.64507340768903}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.relative_strength_index(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/rsi",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_standard_deviation_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test standard deviation with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "standardDeviation": 6.139182763202282,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.standard_deviation(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/standarddeviation",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_standard_deviation_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test standard deviation with date parameters"""
        mock_response = [
            {"date": "2025-02-04 00:00:00", "standardDeviation": 6.139182763202282}
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.standard_deviation(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/standarddeviation",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_williams_percent_r_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test Williams %R with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "williams": -52.51824817518242,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.williams_percent_r(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/williams",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_williams_percent_r_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test Williams %R with date parameters"""
        mock_response = [
            {"date": "2025-02-04 00:00:00", "williams": -52.51824817518242}
        ]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.williams_percent_r(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/williams",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_average_directional_index_basic(
        self, technical_indicators_category, mock_client
    ):
        """Test average directional index with required parameters only"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "adx": 26.414065772772613,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.average_directional_index(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/adx",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_average_directional_index_with_dates(
        self, technical_indicators_category, mock_client
    ):
        """Test average directional index with date parameters"""
        mock_response = [{"date": "2025-02-04 00:00:00", "adx": 26.414065772772613}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await technical_indicators_category.average_directional_index(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/adx",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(
        self, technical_indicators_category, mock_client
    ):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_large_response_handling(
        self, technical_indicators_category, mock_client
    ):
        """Test handling of large responses"""
        # Create a large mock response with multiple data points
        large_response = [
            {
                "date": f"2025-02-{i:02d} 00:00:00",
                "open": 227.2 + (i * 0.1),
                "high": 233.13 + (i * 0.1),
                "low": 226.65 + (i * 0.1),
                "close": 232.8 + (i * 0.1),
                "volume": 44489128 + (i * 1000),
                "sma": 231.215 + (i * 0.01),
            }
            for i in range(1, 101)  # 100 data points
        ]
        mock_client._make_request.return_value = large_response

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )

        assert len(result) == 100
        assert result[0]["date"] == "2025-02-01 00:00:00"
        assert result[99]["date"] == "2025-02-100 00:00:00"
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(
        self, technical_indicators_category, mock_client
    ):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "sma": 231.215,
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_different_symbols(self, technical_indicators_category, mock_client):
        """Test technical indicators functionality with different symbols"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test with AAPL
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

        # Test with MSFT
        result = await technical_indicators_category.simple_moving_average(
            "MSFT", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "MSFT", "periodLength": 10, "timeframe": "1day"},
        )

        # Test with GOOGL
        result = await technical_indicators_category.simple_moving_average(
            "GOOGL", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "GOOGL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_different_period_lengths(
        self, technical_indicators_category, mock_client
    ):
        """Test technical indicators functionality with different period lengths"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test with period length 10
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

        # Test with period length 20
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 20, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 20, "timeframe": "1day"},
        )

        # Test with period length 50
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 50, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 50, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_different_timeframes(
        self, technical_indicators_category, mock_client
    ):
        """Test technical indicators functionality with different timeframes"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test with 1day timeframe
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

        # Test with 1hour timeframe
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1hour"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1hour"},
        )

        # Test with 5min timeframe
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "5min"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "5min"},
        )

    @pytest.mark.asyncio
    async def test_date_edge_cases(self, technical_indicators_category, mock_client):
        """Test date handling edge cases"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test with leap year date
        leap_date = date(2024, 2, 29)
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", from_date=leap_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2024-02-29",
            },
        )

        # Test with year boundary
        year_boundary = date(2024, 12, 31)
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", to_date=year_boundary
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "to": "2024-12-31",
            },
        )

        # Test with beginning of year
        year_beginning = date(2024, 1, 1)
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", from_date=year_beginning
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2024-01-01",
            },
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(
        self, technical_indicators_category, mock_client
    ):
        """Test various parameter combinations"""
        mock_response = [{"date": "2025-02-04 00:00:00", "sma": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test with only required parameters
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

        # Test with from_date
        from_date = date(2025, 2, 1)
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", from_date=from_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
            },
        )

        # Test with to_date
        to_date = date(2025, 2, 28)
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "to": "2025-02-28",
            },
        )

        # Test with both dates
        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day", from_date=from_date, to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "technical-indicators/sma",
            {
                "symbol": "AAPL",
                "periodLength": 10,
                "timeframe": "1day",
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_all_indicators_consistency(
        self, technical_indicators_category, mock_client
    ):
        """Test that all indicators follow the same parameter pattern"""
        mock_response = [{"date": "2025-02-04 00:00:00", "value": 231.215}]
        mock_client._make_request.return_value = mock_response

        # Test all indicators with the same parameters
        indicators = [
            ("simple_moving_average", "technical-indicators/sma"),
            ("exponential_moving_average", "technical-indicators/ema"),
            ("weighted_moving_average", "technical-indicators/wma"),
            ("double_exponential_moving_average", "technical-indicators/dema"),
            ("triple_exponential_moving_average", "technical-indicators/tema"),
            ("relative_strength_index", "technical-indicators/rsi"),
            ("standard_deviation", "technical-indicators/standarddeviation"),
            ("williams_percent_r", "technical-indicators/williams"),
            ("average_directional_index", "technical-indicators/adx"),
        ]

        for method_name, endpoint in indicators:
            method = getattr(technical_indicators_category, method_name)
            result = await method("AAPL", 10, "1day")
            assert result == mock_response
            mock_client._make_request.assert_called_with(
                endpoint, {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"}
            )

    @pytest.mark.asyncio
    async def test_sma_response_validation(
        self, technical_indicators_category, mock_client
    ):
        """Test SMA response validation"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "sma": 231.215,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.simple_moving_average(
            "AAPL", 10, "1day"
        )

        assert len(result) == 1
        assert result[0]["date"] == "2025-02-04 00:00:00"
        assert result[0]["open"] == 227.2
        assert result[0]["high"] == 233.13
        assert result[0]["low"] == 226.65
        assert result[0]["close"] == 232.8
        assert result[0]["volume"] == 44489128
        assert result[0]["sma"] == 231.215
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/sma",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_rsi_response_validation(
        self, technical_indicators_category, mock_client
    ):
        """Test RSI response validation"""
        mock_response = [
            {
                "date": "2025-02-04 00:00:00",
                "open": 227.2,
                "high": 233.13,
                "low": 226.65,
                "close": 232.8,
                "volume": 44489128,
                "rsi": 47.64507340768903,
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await technical_indicators_category.relative_strength_index(
            "AAPL", 10, "1day"
        )

        assert len(result) == 1
        assert result[0]["date"] == "2025-02-04 00:00:00"
        assert result[0]["open"] == 227.2
        assert result[0]["high"] == 233.13
        assert result[0]["low"] == 226.65
        assert result[0]["close"] == 232.8
        assert result[0]["volume"] == 44489128
        assert result[0]["rsi"] == 47.64507340768903
        mock_client._make_request.assert_called_once_with(
            "technical-indicators/rsi",
            {"symbol": "AAPL", "periodLength": 10, "timeframe": "1day"},
        )

    @pytest.mark.asyncio
    async def test_timeframe_validation(self, technical_indicators_category):
        """Test that timeframe parameter accepts valid values"""
        # This test ensures the Timeframe Literal type is working correctly
        valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]

        for timeframe in valid_timeframes:
            # This should not raise a type error
            assert timeframe in TechnicalIndicatorsCategory.Timeframe.__args__
