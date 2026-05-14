"""Tests for the harvester config module."""

from __future__ import annotations

import pytest

from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    DiscoveryConfig,
    HarvestConfig,
    RetryConfig,
    parse_interval,
)


class TestParseInterval:
    @pytest.mark.parametrize(
        "spec,expected_seconds",
        [
            ("30s", 30),
            ("5m", 300),
            ("30m", 1800),
            ("1h", 3600),
            ("4h", 14400),
            ("24h", 86400),
            ("1d", 86400),
            ("7d", 604800),
            ("30D", 2592000),  # case-insensitive
        ],
    )
    def test_valid_specs(self, spec: str, expected_seconds: int) -> None:
        assert parse_interval(spec) == expected_seconds

    @pytest.mark.parametrize("spec", ["", "30", "30x", "abc", "30 m", "-5m"])
    def test_invalid_specs(self, spec: str) -> None:
        with pytest.raises(ValueError):
            parse_interval(spec)


class TestHarvestConfig:
    def test_defaults(self) -> None:
        cfg = HarvestConfig()
        assert cfg.state_dir == "~/.aiofmp/cache"
        assert cfg.log_level == "INFO"
        assert cfg.budget.monthly_soft_cap_gb == 18
        assert cfg.budget.monthly_hard_cap_gb == 20
        assert cfg.retry.on_429.backoff_seconds == [60, 120, 240, 480]
        assert cfg.discovery.refresh_interval == "7d"
        assert cfg.categories == {}

    def test_category_config_interval_seconds(self) -> None:
        cc = CategoryConfig(enabled=True, interval="6h", extra={})
        assert cc.interval_seconds == 6 * 3600

    def test_retry_defaults(self) -> None:
        r = RetryConfig()
        assert r.on_429.max_attempts == 4
        assert r.on_5xx.max_attempts == 3
        assert r.on_5xx.backoff_seconds == [10, 30, 60]

    def test_discovery_refresh_seconds(self) -> None:
        d = DiscoveryConfig(refresh_interval="7d")
        assert d.refresh_interval_seconds == 7 * 86400

    def test_budget_defaults(self) -> None:
        b = BudgetConfig()
        assert b.soft_cap_behavior == "pause_until_next_month"
