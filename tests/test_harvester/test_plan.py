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
    PLAN_LIMITS,
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
        assert get_plan_limits("STARTER").calls_per_minute == 300
        assert get_plan_limits("Premium").calls_per_minute == 750

    def test_starter_caps(self) -> None:
        s = get_plan_limits("starter")
        assert s.calls_per_minute == 300
        assert s.monthly_bandwidth_gb == 20
        assert s.historical_years == 5
        assert s.has_quarterly_fundamentals is False
        assert s.us_only_coverage is True

    def test_ultimate_caps(self) -> None:
        u = get_plan_limits("ultimate")
        assert u.calls_per_minute == 3000
        assert u.historical_years == 30
        assert u.has_quarterly_fundamentals is True
        assert u.us_only_coverage is False

    def test_unknown_plan_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown plan"):
            get_plan_limits("nonexistent")

    def test_premium_has_quarterly(self) -> None:
        assert get_plan_limits("premium").has_quarterly_fundamentals is True

    def test_basic_us_only(self) -> None:
        assert get_plan_limits("basic").us_only_coverage is True


class TestIsUsSymbol:
    @pytest.mark.parametrize(
        "symbol",
        ["AAPL", "MSFT", "BRK-B", "^GSPC", "^DJI", "SPY", "QQQ"],
    )
    def test_us_symbols_kept(self, symbol: str) -> None:
        assert is_us_symbol(symbol) is True

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

    def test_threshold_default_is_5(self, tmp_path) -> None:
        h = self._make_harvester(tmp_path)
        # 4 paywalls — below threshold, returns False each time
        for _ in range(4):
            assert h.note_paywall() is False
        # 5th paywall trips the threshold
        assert h.note_paywall() is True

    def test_note_success_resets_counter(self, tmp_path) -> None:
        h = self._make_harvester(tmp_path)
        for _ in range(4):
            h.note_paywall()
        h.note_success()
        # After reset, takes 5 paywalls again to trip
        for _ in range(4):
            assert h.note_paywall() is False
        assert h.note_paywall() is True

    def test_reset_paywall_state(self, tmp_path) -> None:
        h = self._make_harvester(tmp_path)
        for _ in range(4):
            h.note_paywall()
        h._reset_paywall_state()
        assert h.note_paywall() is False


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
