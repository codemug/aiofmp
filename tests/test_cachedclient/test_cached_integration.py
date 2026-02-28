"""Integration tests for the CachedClient with mocked FmpClient."""

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient import CachedClient
from aiofmp.cachedclient.storage.parquet import ParquetStorage


def _make_mock_fmp_client():
    """Create a mock FmpClient with the necessary category attributes."""
    fmp = MagicMock()

    # Chart category
    chart = MagicMock()
    chart.historical_price_full = AsyncMock()
    chart.historical_price_light = AsyncMock()
    fmp.chart = chart

    # Statements category
    statements = MagicMock()
    statements.income_statement = AsyncMock()
    fmp.statements = statements

    # Company category (with both cacheable and non-cacheable methods)
    company = MagicMock()
    company.profile = AsyncMock()
    company.historical_market_cap = AsyncMock()
    fmp.company = company

    # Economics
    economics = MagicMock()
    economics.treasury_rates = AsyncMock()
    economics.economic_indicators = AsyncMock()
    fmp.economics = economics

    # All other categories as simple mocks
    for cat in [
        "search", "directory", "analyst", "calendar", "cot", "dcf",
        "etf", "commodity", "crypto", "forex", "form13f", "indexes",
        "insider_trades", "market_performance", "news",
        "technical_indicators", "quote", "senate",
    ]:
        if not hasattr(fmp, cat):
            setattr(fmp, cat, MagicMock())

    # Context manager support
    fmp.start = AsyncMock()
    fmp.close = AsyncMock()

    return fmp


@pytest.fixture
def storage(tmp_path: Path) -> ParquetStorage:
    return ParquetStorage(base_dir=tmp_path)


@pytest.fixture
def mock_fmp():
    return _make_mock_fmp_client()


class TestCachedClientContextManager:
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_fmp, storage):
        cached = CachedClient(mock_fmp, storage)
        async with cached:
            pass
        mock_fmp.start.assert_called_once()
        mock_fmp.close.assert_called_once()


class TestDateRangeCaching:
    @pytest.mark.asyncio
    async def test_first_call_fetches_and_stores(self, mock_fmp, storage):
        """First call should hit API and persist to storage."""
        api_data = [
            {"date": "2024-01-02", "symbol": "AAPL", "close": 185.64},
            {"date": "2024-01-03", "symbol": "AAPL", "close": 184.25},
        ]
        mock_fmp.chart.historical_price_full.return_value = api_data

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            result = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-03")

        assert len(result) == 2
        mock_fmp.chart.historical_price_full.assert_called_once()

        # Verify data was stored
        key = ("historical-price-eod/full", "AAPL")
        stored = await storage.read(key)
        assert len(stored) == 2

    @pytest.mark.asyncio
    async def test_second_call_with_same_range_uses_cache(self, mock_fmp, storage):
        """Second call with same range should not hit API."""
        api_data = [
            {"date": "2024-01-02", "symbol": "AAPL", "close": 185.64},
            {"date": "2024-01-03", "symbol": "AAPL", "close": 184.25},
        ]
        mock_fmp.chart.historical_price_full.return_value = api_data

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            # First call: hits API
            await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-03")
            assert mock_fmp.chart.historical_price_full.call_count == 1

            # Second call with same range: cache hit
            result = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-03")
            assert mock_fmp.chart.historical_price_full.call_count == 1  # no additional call
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_extending_range_fetches_only_gap(self, mock_fmp, storage):
        """Extending the range should only fetch the missing gap."""
        initial_data = [
            {"date": "2024-01-02", "symbol": "AAPL", "close": 185.64},
            {"date": "2024-01-03", "symbol": "AAPL", "close": 184.25},
        ]
        gap_data = [
            {"date": "2024-01-04", "symbol": "AAPL", "close": 181.91},
            {"date": "2024-01-05", "symbol": "AAPL", "close": 181.18},
        ]

        mock_fmp.chart.historical_price_full.side_effect = [initial_data, gap_data]

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            # First call: fetches 2024-01-02 to 2024-01-03
            await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-03")
            assert mock_fmp.chart.historical_price_full.call_count == 1

            # Second call: extends to 2024-01-05, should only fetch gap
            result = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-05")
            assert mock_fmp.chart.historical_price_full.call_count == 2

            # Verify the gap call used the correct date range
            gap_call_kwargs = mock_fmp.chart.historical_price_full.call_args_list[1]
            assert gap_call_kwargs.kwargs.get("from_date") == "2024-01-04"

            # Full result should have all 4 records
            assert len(result) == 4

    @pytest.mark.asyncio
    async def test_no_date_params_fetches_and_stores(self, mock_fmp, storage):
        """Call without date params should fetch everything and persist."""
        api_data = [
            {"date": "2024-01-02", "symbol": "AAPL", "close": 185.64},
        ]
        mock_fmp.chart.historical_price_full.return_value = api_data

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            result = await cached.chart.historical_price_full("AAPL")

        assert len(result) == 1
        mock_fmp.chart.historical_price_full.assert_called_once()


class TestPeriodBasedCaching:
    @pytest.mark.asyncio
    async def test_period_based_merges_data(self, mock_fmp, storage):
        """Pattern B should merge fresh + stored data."""
        first_fetch = [
            {"date": "2024-09-28", "symbol": "AAPL", "revenue": 391035000000},
            {"date": "2023-09-30", "symbol": "AAPL", "revenue": 383285000000},
        ]
        second_fetch = [
            {"date": "2024-09-28", "symbol": "AAPL", "revenue": 391035000001},  # updated
            {"date": "2024-03-30", "symbol": "AAPL", "revenue": 95000000000},  # new quarter
        ]

        mock_fmp.statements.income_statement.side_effect = [first_fetch, second_fetch]

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            # First call
            r1 = await cached.statements.income_statement("AAPL", limit=5, period="annual")
            assert len(r1) == 2

            # Second call — should merge
            r2 = await cached.statements.income_statement("AAPL", limit=5, period="annual")
            assert len(r2) == 3  # 2 from first + 1 new (one was an update)

            # The updated record should have the new value
            sept_2024 = [r for r in r2 if r["date"] == "2024-09-28"][0]
            assert sept_2024["revenue"] == 391035000001

    @pytest.mark.asyncio
    async def test_period_based_respects_limit(self, mock_fmp, storage):
        """Pattern B should respect the caller's limit parameter."""
        records = [
            {"date": f"202{i}-09-28", "symbol": "AAPL", "revenue": i * 100}
            for i in range(5)
        ]
        mock_fmp.statements.income_statement.return_value = records

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            result = await cached.statements.income_statement("AAPL", limit=2, period="annual")
            assert len(result) == 2


class TestNonCacheablePassthrough:
    @pytest.mark.asyncio
    async def test_passthrough(self, mock_fmp, storage):
        """Non-cacheable methods should pass through to the real client."""
        profile_data = [{"symbol": "AAPL", "companyName": "Apple Inc."}]
        mock_fmp.company.profile.return_value = profile_data

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            result = await cached.company.profile("AAPL")

        assert result == profile_data
        mock_fmp.company.profile.assert_called_once_with("AAPL")

    @pytest.mark.asyncio
    async def test_passthrough_does_not_store(self, mock_fmp, storage):
        """Non-cacheable methods should not write to storage."""
        mock_fmp.company.profile.return_value = [{"symbol": "AAPL"}]

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            await cached.company.profile("AAPL")

        keys = await storage.list_keys()
        assert keys == []


class TestStorageKeyDerivation:
    @pytest.mark.asyncio
    async def test_different_symbols_use_different_keys(self, mock_fmp, storage):
        """Different symbols should be stored under different keys."""
        aapl_data = [{"date": "2024-01-02", "symbol": "AAPL", "close": 185.0}]
        msft_data = [{"date": "2024-01-02", "symbol": "MSFT", "close": 375.0}]

        mock_fmp.chart.historical_price_full.side_effect = [aapl_data, msft_data]

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-02")
            await cached.chart.historical_price_full("MSFT", "2024-01-02", "2024-01-02")

        keys = await storage.list_keys()
        assert len(keys) == 2

    @pytest.mark.asyncio
    async def test_economics_global_key(self, mock_fmp, storage):
        """Endpoints with no entity key should use a global storage key."""
        rates_data = [{"date": "2024-01-02", "month1": 5.53}]
        mock_fmp.economics.treasury_rates.return_value = rates_data

        cached = CachedClient(mock_fmp, storage)
        async with cached:
            await cached.economics.treasury_rates("2024-01-02", "2024-01-03")

        meta = await storage.get_stored_range(("treasury-rates",))
        assert meta is not None
