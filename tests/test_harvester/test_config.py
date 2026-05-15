"""Tests for the harvester config module."""

from __future__ import annotations

from textwrap import dedent

import pytest

from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    DiscoveryConfig,
    HarvestConfig,
    RetryConfig,
    load_config_from_yaml,
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


class TestLoadConfigFromYaml:
    def test_minimal(self, tmp_path) -> None:
        path = tmp_path / "h.yaml"
        path.write_text("state_dir: /tmp/x\n")
        cfg = load_config_from_yaml(path)
        assert cfg.state_dir == "/tmp/x"
        assert cfg.log_level == "INFO"
        assert cfg.budget.monthly_soft_cap_gb == 18

    def test_full(self, tmp_path) -> None:
        path = tmp_path / "h.yaml"
        path.write_text(
            dedent("""
            state_dir: /var/aiofmp
            log_level: DEBUG
            budget:
              monthly_soft_cap_gb: 10
              monthly_hard_cap_gb: 12
              soft_cap_behavior: warn_only
            retry:
              on_429:
                backoff_seconds: [30, 60]
                max_attempts: 2
              on_5xx:
                backoff_seconds: [5]
                max_attempts: 1
            discovery:
              refresh_interval: 3d
            categories:
              statements:
                enabled: true
                interval: 6h
                periods: [annual, quarter]
                initial_limit: 40
              chart_eod:
                enabled: false
                interval: 24h
        """).strip()
            + "\n"
        )
        cfg = load_config_from_yaml(path)
        assert cfg.state_dir == "/var/aiofmp"
        assert cfg.log_level == "DEBUG"
        assert cfg.budget.monthly_soft_cap_gb == 10
        assert cfg.budget.soft_cap_behavior == "warn_only"
        assert cfg.retry.on_429.backoff_seconds == [30, 60]
        assert cfg.retry.on_429.max_attempts == 2
        assert cfg.discovery.refresh_interval == "3d"
        assert "statements" in cfg.categories
        st = cfg.categories["statements"]
        assert st.enabled is True
        assert st.interval == "6h"
        assert st.extra["periods"] == ["annual", "quarter"]
        assert st.extra["initial_limit"] == 40
        assert cfg.categories["chart_eod"].enabled is False

    def test_missing_file(self, tmp_path) -> None:
        import pytest

        with pytest.raises(FileNotFoundError):
            load_config_from_yaml(tmp_path / "nope.yaml")

    def test_bad_yaml(self, tmp_path) -> None:
        import pytest

        path = tmp_path / "bad.yaml"
        path.write_text("state_dir: [unclosed\n")
        with pytest.raises(ValueError, match="yaml"):
            load_config_from_yaml(path)

    def test_category_missing_required(self, tmp_path) -> None:
        import pytest

        path = tmp_path / "h.yaml"
        path.write_text(
            dedent("""
            categories:
              statements:
                enabled: true
                # interval missing
        """).strip()
            + "\n"
        )
        with pytest.raises(ValueError, match="interval"):
            load_config_from_yaml(path)
