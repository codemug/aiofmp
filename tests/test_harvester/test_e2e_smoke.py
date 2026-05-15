"""End-to-end smoke test for the harvester."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient import CachedClient, ParquetStorage
from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    HarvestConfig,
    RetryConfig,
)
from aiofmp.harvester.manager import HarvesterManager
from aiofmp.harvester.state import RunStatus


def _eod_record() -> dict[str, Any]:
    return {
        "date": "2025-06-01",
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 1000,
    }


def _earnings_record(symbol: str, d: str) -> dict[str, Any]:
    return {"symbol": symbol, "date": d, "epsEstimated": 1.0, "eps": 1.05}


def _build_fake_fmp() -> MagicMock:
    fmp = MagicMock()
    # Directory + per-category list endpoints
    fmp.directory = MagicMock()
    fmp.directory.financial_symbols = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.directory.actively_trading = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.directory.etf_list = AsyncMock(return_value=[])
    fmp.commodity = MagicMock()
    fmp.commodity.commodities_list = AsyncMock(return_value=[{"symbol": "GCUSD"}])
    fmp.commodity.historical_price_full = AsyncMock(return_value=[_eod_record()])
    fmp.forex = MagicMock()
    fmp.forex.forex_list = AsyncMock(return_value=[{"symbol": "EURUSD"}])
    fmp.forex.historical_price_full = AsyncMock(return_value=[_eod_record()])
    fmp.indexes = MagicMock()
    fmp.indexes.index_list = AsyncMock(return_value=[{"symbol": "^GSPC"}])
    fmp.indexes.historical_price_eod_full = AsyncMock(return_value=[_eod_record()])

    # Chart EOD endpoints
    fmp.chart = MagicMock()
    fmp.chart.historical_price_full = AsyncMock(return_value=[_eod_record()])

    # Statements endpoints — wired with a single canned return
    fmp.statements = MagicMock()
    for m in [
        "income_statement",
        "balance_sheet_statement",
        "cash_flow_statement",
        "key_metrics",
        "financial_ratios",
        "enterprise_values",
        "income_statement_growth",
        "balance_sheet_statement_growth",
        "cash_flow_statement_growth",
        "financial_statement_growth",
        "owner_earnings",
        "revenue_product_segmentation",
        "revenue_geographic_segmentation",
    ]:
        setattr(
            fmp.statements,
            m,
            AsyncMock(return_value=[{"date": "2024-12-31", "symbol": "AAPL"}]),
        )

    # Calendar — earnings_calendar is the discovery probe for statements
    fmp.calendar = MagicMock()
    fmp.calendar.earnings_calendar = AsyncMock(
        return_value=[_earnings_record("AAPL", date.today().isoformat())]
    )

    # News endpoints
    fmp.news = MagicMock()
    for v in (
        "general_news",
        "press_releases",
        "stock_news",
        "crypto_news",
        "forex_news",
    ):
        setattr(fmp.news, v, AsyncMock(return_value=[]))

    # Economics
    fmp.economics = MagicMock()
    fmp.economics.treasury_rates = AsyncMock(return_value=[])
    fmp.economics.economic_indicators = AsyncMock(return_value=[])

    # Analyst
    fmp.analyst = MagicMock()
    fmp.analyst.financial_estimates = AsyncMock(
        side_effect=[
            [{"symbol": "AAPL", "date": "2025-12-31", "revenueAvg": 100}],
            [],
        ]
    )
    fmp.analyst.ratings_snapshot = AsyncMock(
        return_value=[{"symbol": "AAPL", "rating": "A"}]
    )
    fmp.analyst.price_target_consensus = AsyncMock(
        return_value=[{"symbol": "AAPL", "targetConsensus": 250}]
    )
    fmp.analyst.price_target_summary = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.analyst.stock_grades_summary = AsyncMock(
        return_value=[{"symbol": "AAPL", "consensus": "Buy"}]
    )

    # Insider trades
    fmp.insider_trades = MagicMock()
    fmp.insider_trades.latest_insider_trades = AsyncMock(
        side_effect=[
            [
                {
                    "symbol": "AAPL",
                    "filingDate": "2026-05-01",
                    "transactionType": "P-Purchase",
                }
            ],
            [],
        ]
    )

    # Form 13F
    fmp.form13f = MagicMock()
    fmp.form13f.latest_filings = AsyncMock(
        side_effect=[
            [{"cik": "0001067983", "acceptedDate": "2026-05-01", "name": "Berkshire"}],
            [],
        ]
    )

    # DCF
    fmp.dcf = MagicMock()
    fmp.dcf.dcf_valuation = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 150.0}])
    fmp.dcf.levered_dcf = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 155.0}])

    # Make on_response_size assignable (FmpClient has it; MagicMock too)
    fmp.on_response_size = None
    fmp.start = AsyncMock()
    fmp.close = AsyncMock()
    return fmp


@pytest.mark.asyncio
async def test_one_cycle_per_category(tmp_path: Path) -> None:
    cfg = HarvestConfig(
        state_dir=str(tmp_path),
        budget=BudgetConfig(),
        retry=RetryConfig(),
        categories={
            "chart_eod": CategoryConfig(
                enabled=True, interval="24h", extra={"backfill_years": 1}
            ),
            "commodities_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "forex_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "indexes_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "news": CategoryConfig(enabled=True, interval="30m", extra={}),
            "economics": CategoryConfig(
                enabled=True, interval="24h", extra={"indicators": ["GDP"]}
            ),
            "statements": CategoryConfig(
                enabled=True, interval="6h", extra={"periods": ["annual"]}
            ),
            "analyst_estimates": CategoryConfig(
                enabled=True,
                interval="24h",
                extra={"estimate_periods": ["annual"], "page_size": 1},
            ),
            "analyst_snapshots": CategoryConfig(enabled=True, interval="24h", extra={}),
            "insider_trades": CategoryConfig(
                enabled=True, interval="6h", extra={"page_size": 1, "max_pages": 2}
            ),
            "form13f": CategoryConfig(
                enabled=True, interval="24h", extra={"page_size": 1, "max_pages": 2}
            ),
            "dcf": CategoryConfig(enabled=True, interval="24h", extra={}),
        },
    )
    fmp = _build_fake_fmp()
    cached = CachedClient(fmp, storage=ParquetStorage(tmp_path))

    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()

        # Run one cycle per enabled category, sequentially
        for name in list(mgr._categories.keys()):
            await mgr._categories[name]._run_once_and_record()
            run = mgr.state.get_latest_run(name)
            assert run is not None, f"no run row for {name}"
            assert run.status in (RunStatus.OK, RunStatus.PARTIAL), (
                f"{name} ended in unexpected status {run.status}"
            )

        await mgr.close()

    # Sanity: at least one parquet file should exist
    assert any((tmp_path / "cachedclient_data").rglob("data.parquet"))
