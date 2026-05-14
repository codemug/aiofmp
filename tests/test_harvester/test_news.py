"""Tests for the news category."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.news import build_news
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.cached_client = MagicMock()
    m.cached_client.news = MagicMock()
    for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
        setattr(m.cached_client.news, v, AsyncMock(return_value=[]))
    return m


class TestNews:
    @pytest.mark.asyncio
    async def test_default_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="30m", extra={})
        h = build_news(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        # five variants, each called once
        for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
            getattr(manager.cached_client.news, v).assert_awaited_once()

    @pytest.mark.asyncio
    async def test_custom_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="30m",
            extra={"variants": ["general_news"], "backfill_days_initial": 7, "page_size": 50},
        )
        h = build_news(cfg, manager)
        await h.run_cycle()
        call = manager.cached_client.news.general_news.await_args_list[0]
        # called as general_news(page=0, limit=50, from_date=<date>, to_date=<date>)
        assert call.kwargs["limit"] == 50
        assert isinstance(call.kwargs["from_date"], date)
        assert isinstance(call.kwargs["to_date"], date)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "news" in _REGISTRY
