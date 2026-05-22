"""Tests for the plan capability matrix and sliding-window rate limiter."""

from __future__ import annotations

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import (
    FMPPaywallError,
    _SlidingWindowRateLimiter,
)
from aiofmp.harvester.plan import (
    get_plan_limits,
    is_us_symbol,
)


class TestGetPlanLimits:
    @pytest.mark.parametrize("plan", ["basic", "starter", "premium", "ultimate"])
    def test_known_plans(self, plan: str) -> None:
        limits = get_plan_limits(plan)
        assert limits.name == plan
        assert limits.calls_per_minute > 0

    def test_case_insensitive(self) -> None:
        # RPMs are paced ~17% below FMP's documented caps (300/750/3000) to
        # absorb residual server-side 429s. Keep these as exact assertions so
        # accidental drift gets caught.
        assert get_plan_limits("STARTER").calls_per_minute == 250
        assert get_plan_limits("Premium").calls_per_minute == 625

    def test_starter_caps(self) -> None:
        s = get_plan_limits("starter")
        assert s.calls_per_minute == 250
        assert s.monthly_bandwidth_gb == 20
        assert s.historical_years == 5
        assert s.us_only_coverage is True
        # Probed 2026-05 against a Starter key:
        assert "form13f" in s.paywalled_categories
        assert "key_metrics" in s.quarterly_paywalled_statement_endpoints
        assert "financial_ratios" in s.quarterly_paywalled_statement_endpoints
        assert "1min" in s.intraday_paywalled_timeframes
        assert "press_releases" in s.paywalled_news_variants
        assert s.quarterly_analyst_estimates_paywalled is True

    def test_ultimate_caps(self) -> None:
        u = get_plan_limits("ultimate")
        assert u.calls_per_minute == 2500
        assert u.historical_years == 30
        assert u.us_only_coverage is False
        # Ultimate has none of Starter's paywall restrictions.
        assert u.paywalled_categories == frozenset()
        assert u.quarterly_paywalled_statement_endpoints == frozenset()
        assert u.intraday_paywalled_timeframes == frozenset()
        assert u.paywalled_news_variants == frozenset()
        assert u.quarterly_analyst_estimates_paywalled is False

    def test_unknown_plan_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown plan"):
            get_plan_limits("nonexistent")

    def test_premium_unrestricted(self) -> None:
        p = get_plan_limits("premium")
        assert p.quarterly_paywalled_statement_endpoints == frozenset()
        assert p.us_only_coverage is False

    def test_basic_us_only(self) -> None:
        assert get_plan_limits("basic").us_only_coverage is True

    def test_valid_economic_indicators_starts_with_GDP(self) -> None:
        from aiofmp.harvester.plan import VALID_ECONOMIC_INDICATORS

        # Probed 2026-05: these are FMP's actual indicator names.
        assert "GDP" in VALID_ECONOMIC_INDICATORS
        assert "inflationRate" in VALID_ECONOMIC_INDICATORS
        assert "unemploymentRate" in VALID_ECONOMIC_INDICATORS
        assert "federalFunds" in VALID_ECONOMIC_INDICATORS
        # FRED codes are NOT valid here.
        assert "UNRATE" not in VALID_ECONOMIC_INDICATORS
        assert "FEDFUNDS" not in VALID_ECONOMIC_INDICATORS


class TestIsUsSymbol:
    @pytest.mark.parametrize(
        "symbol",
        ["AAPL", "MSFT", "BRK-B", "^GSPC", "^DJI", "SPY", "QQQ"],
    )
    def test_us_symbols_kept(self, symbol: str) -> None:
        assert is_us_symbol(symbol) is True

    def test_currency_usd_in_payload_keeps_symbol(self) -> None:
        # Even when the symbol shape would normally pass, the currency
        # field in the payload (when present) is the authoritative signal.
        assert is_us_symbol("^GSPC", {"currency": "USD"}) is True

    def test_non_usd_currency_drops_symbol(self) -> None:
        # ^AVFOCGRW / ^AFLI / ^AEX etc. — symbol-only heuristic misses them
        # (no dot, no 0P prefix) but the FMP record carries a non-USD currency.
        assert is_us_symbol("^AVFOCGRW", {"currency": "GBP"}) is False
        assert is_us_symbol("^AEX", {"currency": "EUR"}) is False
        assert is_us_symbol("^N225", {"currency": "JPY"}) is False

    def test_missing_currency_falls_back_to_symbol_heuristic(self) -> None:
        # If payload lacks a usable currency, behave as if payload=None.
        assert is_us_symbol("^GSPC", {}) is True
        assert is_us_symbol("AAPL", {"currency": ""}) is True
        assert is_us_symbol("6898.HK", {}) is False  # dot still kicks in

    @pytest.mark.parametrize(
        "symbol",
        [
            "GOOG.L",  # London
            "6898.HK",  # Hong Kong
            "000001.SS",  # Shanghai
            "399967.SZ",  # Shenzhen
            "XU100.IS",  # Istanbul
            "KOSPI200.KS",  # Korea
            "IDX30.JK",  # Jakarta
            "0P00000RNB",  # Morningstar fund ID
            "0P0000GATU",  # Morningstar fund ID
        ],
    )
    def test_non_us_symbols_dropped(self, symbol: str) -> None:
        assert is_us_symbol(symbol) is False

    def test_empty(self) -> None:
        assert is_us_symbol("") is False


class TestSlidingWindowRateLimiter:
    @pytest.mark.asyncio
    async def test_first_acquire_is_immediate(self) -> None:
        rl = _SlidingWindowRateLimiter(max_per_minute=600)  # 100ms interval
        t0 = time.monotonic()
        await rl.acquire()
        elapsed = time.monotonic() - t0
        # First call shouldn't wait — wait was for _next_slot=0 vs now
        assert elapsed < 0.05

    @pytest.mark.asyncio
    async def test_paces_subsequent_requests(self) -> None:
        # 6000 RPM = 10ms between requests. 5 sequential calls should take >= 40ms.
        rl = _SlidingWindowRateLimiter(max_per_minute=6000)
        t0 = time.monotonic()
        for _ in range(5):
            await rl.acquire()
        elapsed = time.monotonic() - t0
        # 5 acquires at 10ms interval ≈ 40ms minimum (first is free, then 4 × 10ms)
        assert elapsed >= 0.030
        # Generous upper bound — shouldn't blow the wait
        assert elapsed < 0.5

    @pytest.mark.asyncio
    async def test_concurrent_acquires_serialise(self) -> None:
        rl = _SlidingWindowRateLimiter(max_per_minute=6000)  # 10ms interval
        t0 = time.monotonic()
        await asyncio.gather(*[rl.acquire() for _ in range(10)])
        elapsed = time.monotonic() - t0
        # 10 acquires at 10ms interval ≈ 90ms minimum
        assert elapsed >= 0.060

    def test_zero_rate_rejected(self) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            _SlidingWindowRateLimiter(max_per_minute=0)

    def test_negative_rate_rejected(self) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            _SlidingWindowRateLimiter(max_per_minute=-5)


class TestFMPPaywallError:
    @pytest.mark.asyncio
    async def test_402_raises_fmp_paywall_error(self) -> None:
        from aiofmp.base import FMPBaseClient

        client = FMPBaseClient(api_key="test")
        fake_resp = MagicMock()
        fake_resp.status = 402
        fake_resp.reason = "Payment Required"
        with pytest.raises(FMPPaywallError, match="402"):
            await client._handle_response(fake_resp)

    def test_inherits_from_fmp_error(self) -> None:
        from aiofmp.base import FMPError

        assert issubclass(FMPPaywallError, FMPError)


class TestNotePaywallThreshold:
    """Verify CategoryHarvester.note_paywall() threshold + reset behavior."""

    def _make_harvester(self, tmp_path):
        from aiofmp.harvester.base import CategoryHarvester, RunOutcome
        from aiofmp.harvester.budget import BudgetTracker
        from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
        from aiofmp.harvester.state import RunStatus, StateStore

        class _NoopCategory(CategoryHarvester):
            async def run_cycle(self) -> RunOutcome:
                return RunOutcome(status=RunStatus.OK)

        store = StateStore(tmp_path / "h.sqlite")
        store.initialize()
        cfg = CategoryConfig(enabled=True, interval="1s", extra={})
        budget = BudgetTracker(store, BudgetConfig())
        retry = RetryConfig()
        return _NoopCategory("test", cfg, store, budget, retry)

    def test_threshold_default(self, tmp_path) -> None:
        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        # (threshold - 1) paywalls stay below the line.
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD - 1):
            assert h.note_paywall() is False
        # One more trips it.
        assert h.note_paywall() is True

    def test_note_success_resets_counter(self, tmp_path) -> None:
        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD - 1):
            h.note_paywall()
        h.note_success()
        # After reset, takes the full threshold-count again to trip.
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD - 1):
            assert h.note_paywall() is False
        assert h.note_paywall() is True

    def test_reset_paywall_state(self, tmp_path) -> None:
        h = self._make_harvester(tmp_path)
        for _ in range(4):
            h.note_paywall()
        h._reset_paywall_state()
        assert h.note_paywall() is False

    def test_paywall_marker_set_when_threshold_trips(self, tmp_path) -> None:
        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        assert h._paywalled_at is None
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD):
            h.note_paywall()
        # Marker is now set; next cycle should skip.
        assert h._paywalled_at is not None
        assert h._paywall_skip_remaining_seconds() > 0

    def test_paywall_marker_not_set_below_threshold(self, tmp_path) -> None:
        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD - 1):
            h.note_paywall()
        assert h._paywalled_at is None
        assert h._paywall_skip_remaining_seconds() == 0

    def test_paywall_marker_cleared_on_success(self, tmp_path) -> None:
        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        for _ in range(CategoryHarvester.PAYWALL_THRESHOLD):
            h.note_paywall()
        assert h._paywalled_at is not None
        h.note_success()
        assert h._paywalled_at is None
        assert h._paywall_skip_remaining_seconds() == 0

    def test_paywall_skip_window_expires(self, tmp_path) -> None:
        from datetime import UTC, datetime, timedelta

        from aiofmp.harvester.base import CategoryHarvester

        h = self._make_harvester(tmp_path)
        # Forge an old paywall marker — older than the re-probe window.
        h._paywalled_at = datetime.now(UTC) - timedelta(
            seconds=CategoryHarvester.PAYWALL_REPROBE_SECONDS + 1,
        )
        assert h._paywall_skip_remaining_seconds() == 0


class TestRateLimiterPlumbedIntoFmpClient:
    @pytest.mark.asyncio
    async def test_client_with_rate_limiter(self) -> None:
        from aiofmp.base import FMPBaseClient

        client = FMPBaseClient(api_key="test", requests_per_minute=300)
        assert client._rate_limiter is not None
        # The limiter is callable (basic sanity)
        await client._rate_limiter.acquire()

    @pytest.mark.asyncio
    async def test_client_without_rate_limiter(self) -> None:
        from aiofmp.base import FMPBaseClient

        client = FMPBaseClient(api_key="test")
        assert client._rate_limiter is None


class TestEmptyResponseBodyHandling:
    """Some FMP endpoints return 200 + empty body for paywalled resources."""

    @pytest.mark.asyncio
    async def test_empty_body_returns_none_not_error(self) -> None:
        from aiofmp.base import FMPBaseClient

        client = FMPBaseClient(api_key="test")
        fake_resp = MagicMock()
        fake_resp.status = 200
        fake_resp.read = AsyncMock(return_value=b"")
        assert await client._handle_response(fake_resp) is None

    @pytest.mark.asyncio
    async def test_whitespace_only_body_returns_none(self) -> None:
        from aiofmp.base import FMPBaseClient

        client = FMPBaseClient(api_key="test")
        fake_resp = MagicMock()
        fake_resp.status = 200
        fake_resp.read = AsyncMock(return_value=b"   \n  \t  \n")
        assert await client._handle_response(fake_resp) is None


class TestSymbolCatalogReadSideFilter:
    """Plan changes apply to cached universes on the next read, not next refresh."""

    @pytest.mark.asyncio
    async def test_filter_applies_on_read_to_cached_data(self, tmp_path) -> None:
        from aiofmp.harvester.catalog import SymbolCatalog
        from aiofmp.harvester.plan import is_us_symbol
        from aiofmp.harvester.state import StateStore

        store = StateStore(tmp_path / "h.sqlite")
        store.initialize()

        # Pretend a previous run (on a different plan) stored a mixed universe.
        store.replace_universe(
            "indexes",
            [
                ("^GSPC", {"symbol": "^GSPC"}),
                ("^DJI", {"symbol": "^DJI"}),
                ("DX-Y.NYB", {"symbol": "DX-Y.NYB"}),  # foreign exchange suffix
                ("6898.HK", {"symbol": "6898.HK"}),  # foreign exchange suffix
                ("0P0000RNB", {"symbol": "0P0000RNB"}),  # Morningstar fund ID
            ],
        )
        # Pretend it's fresh so .symbols() doesn't trigger a refresh.
        from datetime import UTC, datetime

        store.set_last_refresh("indexes", datetime.now(UTC))

        # Build a catalog with the US-only filter (Starter behaviour).
        fake_fmp = MagicMock()
        catalog = SymbolCatalog(
            store,
            fake_fmp,
            refresh_interval_seconds=86_400,
            symbol_filter=is_us_symbol,
        )

        # The cached universe has 5 symbols; the filter should drop the 3
        # non-US ones AT READ TIME (the refresh did not run).
        result = await catalog.symbols("indexes")
        assert set(result) == {"^GSPC", "^DJI"}
        # The non-US symbols remain physically stored — only the read is filtered.
        assert set(store.list_symbols("indexes")) == {
            "^GSPC",
            "^DJI",
            "DX-Y.NYB",
            "6898.HK",
            "0P0000RNB",
        }

    @pytest.mark.asyncio
    async def test_no_filter_returns_everything_stored(self, tmp_path) -> None:
        from aiofmp.harvester.catalog import SymbolCatalog
        from aiofmp.harvester.state import StateStore

        store = StateStore(tmp_path / "h.sqlite")
        store.initialize()
        store.replace_universe(
            "indexes",
            [
                ("^GSPC", {"symbol": "^GSPC"}),
                ("DX-Y.NYB", {"symbol": "DX-Y.NYB"}),
            ],
        )
        from datetime import UTC, datetime

        store.set_last_refresh("indexes", datetime.now(UTC))

        fake_fmp = MagicMock()
        catalog = SymbolCatalog(
            store, fake_fmp, refresh_interval_seconds=86_400, symbol_filter=None
        )
        result = await catalog.symbols("indexes")
        assert set(result) == {"^GSPC", "DX-Y.NYB"}
