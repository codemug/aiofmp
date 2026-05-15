"""Tests for the harvester CLI."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from unittest.mock import AsyncMock, patch

import pytest
from click.testing import CliRunner

from aiofmp.cli import cli


def _write_yaml(path: Path, body: str) -> None:
    path.write_text(dedent(body).strip() + "\n")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def env_with_key(monkeypatch) -> None:
    monkeypatch.setenv("FMP_API_KEY", "test_key_xxxx")


@pytest.fixture
def minimal_config(tmp_path: Path) -> Path:
    state = tmp_path / "state"
    state.mkdir()
    cfg = tmp_path / "h.yaml"
    _write_yaml(
        cfg,
        f"""
        state_dir: {state}
        categories:
          news:
            enabled: true
            interval: 30m
    """,
    )
    return cfg


class TestHarvestCli:
    def test_missing_api_key(self, runner: CliRunner, minimal_config: Path) -> None:
        # Ensure FMP_API_KEY is NOT in env
        result = runner.invoke(
            cli,
            ["harvest", "--config", str(minimal_config), "--once"],
            env={"FMP_API_KEY": ""},
        )
        assert result.exit_code != 0
        assert "FMP_API_KEY" in result.output

    def test_dry_run_prints_plan(
        self, env_with_key, runner: CliRunner, minimal_config: Path
    ) -> None:
        result = runner.invoke(
            cli,
            ["harvest", "--config", str(minimal_config), "--dry-run"],
        )
        assert result.exit_code == 0
        assert "news" in result.output
        assert "enabled" in result.output.lower()

    def test_once_runs_and_exits(
        self,
        env_with_key,
        runner: CliRunner,
        minimal_config: Path,
    ) -> None:
        with patch("aiofmp.harvester.cli._build_cached_client") as m:
            fake_cached = AsyncMock()
            fake_cached.__aenter__ = AsyncMock(return_value=fake_cached)
            fake_cached.__aexit__ = AsyncMock(return_value=None)
            fake_cached.news = type("X", (), {})()
            for v in (
                "general_news",
                "press_releases",
                "stock_news",
                "crypto_news",
                "forex_news",
            ):
                setattr(fake_cached.news, v, AsyncMock(return_value=[]))
            fake_cached.storage = AsyncMock()
            m.return_value = (AsyncMock(), fake_cached)

            result = runner.invoke(
                cli,
                ["harvest", "--config", str(minimal_config), "--once"],
            )
            assert result.exit_code == 0, result.output

    def test_once_with_specific_category(
        self,
        env_with_key,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        cfg = tmp_path / "h.yaml"
        state = tmp_path / "state"
        state.mkdir()
        _write_yaml(
            cfg,
            f"""
            state_dir: {state}
            categories:
              news:
                enabled: true
                interval: 30m
              economics:
                enabled: true
                interval: 24h
        """,
        )
        with patch("aiofmp.harvester.cli._build_cached_client") as m:
            fake_cached = AsyncMock()
            fake_cached.__aenter__ = AsyncMock(return_value=fake_cached)
            fake_cached.__aexit__ = AsyncMock(return_value=None)
            fake_cached.news = type("X", (), {})()
            for v in (
                "general_news",
                "press_releases",
                "stock_news",
                "crypto_news",
                "forex_news",
            ):
                setattr(fake_cached.news, v, AsyncMock(return_value=[]))
            fake_cached.economics = type("X", (), {})()
            fake_cached.economics.treasury_rates = AsyncMock(return_value=[])
            fake_cached.economics.economic_indicators = AsyncMock(return_value=[])
            fake_cached.storage = AsyncMock()
            m.return_value = (AsyncMock(), fake_cached)

            result = runner.invoke(
                cli,
                ["harvest", "--config", str(cfg), "--once", "--category", "news"],
            )
            assert result.exit_code == 0, result.output
            # Economics should NOT have been called when filtered to news
            fake_cached.economics.treasury_rates.assert_not_awaited()


class TestHarvestStatusCli:
    def test_empty_status(
        self, env_with_key, runner: CliRunner, minimal_config: Path
    ) -> None:
        result = runner.invoke(cli, ["harvest-status", "--config", str(minimal_config)])
        assert result.exit_code == 0
        # Header should mention categories columns
        assert "category" in result.output.lower()
