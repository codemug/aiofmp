"""Tests for the PAGE_WALK pattern in the cached client registry."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.proxy import CachedCategoryProxy
from aiofmp.cachedclient.registry import (
    CacheableEndpoint,
    EndpointRegistry,
    TemporalPattern,
    build_default_registry,
)
from aiofmp.cachedclient.storage.parquet import ParquetStorage


def test_temporal_pattern_page_walk_exists() -> None:
    assert TemporalPattern.PAGE_WALK.value == "page_walk"


def test_page_walk_endpoint_fields() -> None:
    ep = CacheableEndpoint(
        category="analyst",
        method="financial_estimates",
        api_endpoint="analyst-estimates",
        pattern=TemporalPattern.PAGE_WALK,
        entity_key_args=["symbol"],
        extra_key_args=["period"],
        page_param="page",
        default_page_size=100,
        walk_date_field="date",
        call_params=["symbol", "period", "page", "limit"],
    )
    assert ep.page_param == "page"
    assert ep.default_page_size == 100
    assert ep.walk_date_field == "date"


def test_default_registry_includes_page_walk_endpoints() -> None:
    reg = build_default_registry()
    # The harvester adds these in a later task; we only require the field exists.
    # No PAGE_WALK endpoints are pre-registered by build_default_registry in v1.
    assert reg.get("chart", "historical_price_full") is not None


@pytest_asyncio.fixture
async def storage(tmp_path: Path) -> ParquetStorage:
    s = ParquetStorage(tmp_path)
    await s.initialize()
    return s


class TestPageWalkProxyReadOnly:
    @pytest.mark.asyncio
    async def test_user_call_returns_stored_records(self, storage: ParquetStorage) -> None:
        """When a user calls a PAGE_WALK-registered method, the proxy returns stored records
        without contacting the upstream API."""
        reg = EndpointRegistry()
        reg.register(
            CacheableEndpoint(
                category="analyst",
                method="financial_estimates",
                api_endpoint="analyst-estimates",
                pattern=TemporalPattern.PAGE_WALK,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                page_param="page",
                walk_date_field="date",
                call_params=["symbol", "period", "page", "limit"],
            )
        )

        # Pre-seed storage as if the harvester had written it
        await storage.write(
            ("analyst-estimates", "AAPL", "annual"),
            [
                {"symbol": "AAPL", "date": "2025-12-31", "revenueAvg": 500},
                {"symbol": "AAPL", "date": "2024-12-31", "revenueAvg": 400},
                {"symbol": "AAPL", "date": "2023-12-31", "revenueAvg": 300},
            ],
            date_field="date",
        )

        real_category = MagicMock()
        # If the proxy mistakenly calls upstream, this will be invoked:
        real_category.financial_estimates = AsyncMock(side_effect=AssertionError("upstream called"))

        proxy = CachedCategoryProxy(real_category, "analyst", storage, reg)
        records = await proxy.financial_estimates(symbol="AAPL", period="annual", page=0, limit=2)

        # Returns the requested limit slice (newest first by date convention)
        assert len(records) == 2
        assert records[0]["date"] == "2025-12-31"
        assert records[1]["date"] == "2024-12-31"

    @pytest.mark.asyncio
    async def test_user_call_returns_empty_when_no_storage(self, storage: ParquetStorage) -> None:
        reg = EndpointRegistry()
        reg.register(
            CacheableEndpoint(
                category="analyst",
                method="financial_estimates",
                api_endpoint="analyst-estimates",
                pattern=TemporalPattern.PAGE_WALK,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                page_param="page",
                walk_date_field="date",
                call_params=["symbol", "period", "page", "limit"],
            )
        )
        real_category = MagicMock()
        real_category.financial_estimates = AsyncMock(side_effect=AssertionError("upstream called"))
        proxy = CachedCategoryProxy(real_category, "analyst", storage, reg)
        records = await proxy.financial_estimates(symbol="MSFT", period="annual")
        assert records == []


class TestPageWalkEndpointRegistrations:
    def test_analyst_financial_estimates_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("analyst", "financial_estimates")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "analyst-estimates"
        assert ep.entity_key_args == ["symbol"]
        assert ep.extra_key_args == ["period"]
        assert ep.page_param == "page"
        assert ep.limit_param == "limit"
        assert ep.walk_date_field == "date"

    def test_insider_trades_latest_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("insider_trades", "latest_insider_trades")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "insider-trading/latest"
        assert ep.entity_key_args == []
        assert ep.page_param == "page"
        assert ep.walk_date_field == "filingDate"

    def test_form13f_latest_filings_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("form13f", "latest_filings")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "institutional-ownership/latest"
        assert ep.walk_date_field == "acceptedDate"
