#!/usr/bin/env python3
"""
Example script demonstrating the CachedClient — a caching wrapper for FmpClient.

The CachedClient intercepts time-series API calls, stores results locally in
Parquet files, and only fetches missing date ranges on subsequent calls. This
dramatically reduces API usage when working with historical data.

Requirements:
    pip install aiofmp
"""

import asyncio
import os

from aiofmp import FmpClient
from aiofmp.cachedclient import CachedClient


async def date_range_caching_example(cached: CachedClient) -> None:
    """Demonstrate date-range caching (Pattern A) with chart data."""
    print("\n=== Date-Range Caching (Chart Data) ===")

    # First call: fetches all data from the API and stores it locally
    print("1. Fetching AAPL daily prices for Jan 2024...")
    data = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-31")
    print(f"   Got {len(data)} records (fetched from API)")

    # Second call with the same range: served entirely from cache, no API call
    print("2. Fetching same range again...")
    data = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-01-31")
    print(f"   Got {len(data)} records (served from cache, zero API calls)")

    # Third call with an extended range: only fetches the gap (Feb 2024)
    print("3. Extending range to include Feb 2024...")
    data = await cached.chart.historical_price_full("AAPL", "2024-01-02", "2024-02-29")
    print(f"   Got {len(data)} records (only Feb gap fetched from API)")

    if data:
        first = data[-1]
        last = data[0]
        print(f"   Range: {first.get('date')} to {last.get('date')}")


async def period_based_caching_example(cached: CachedClient) -> None:
    """Demonstrate period-based caching (Pattern B) with financial statements."""
    print("\n=== Period-Based Caching (Financial Statements) ===")

    # First call: fetches from API and stores locally
    print("1. Fetching AAPL annual income statements (last 5 years)...")
    stmts = await cached.statements.income_statement("AAPL", limit=5, period="annual")
    print(f"   Got {len(stmts)} records")

    if stmts:
        for s in stmts[:3]:
            print(f"   {s.get('date')}: revenue=${s.get('revenue', 0):,}")

    # Second call: fetches fresh data, merges with stored, deduplicates by date
    print("2. Fetching again — merges fresh data with stored historical records...")
    stmts = await cached.statements.income_statement("AAPL", limit=5, period="annual")
    print(f"   Got {len(stmts)} records (merged: fresh API data + stored history)")


async def multiple_symbols_example(cached: CachedClient) -> None:
    """Demonstrate caching across different symbols."""
    print("\n=== Multiple Symbols ===")

    symbols = ["AAPL", "MSFT", "GOOGL"]
    for symbol in symbols:
        data = await cached.chart.historical_price_full(
            symbol, "2024-06-01", "2024-06-30"
        )
        print(f"   {symbol}: {len(data)} daily records for June 2024")

    # Second pass — all served from cache
    print("   (Fetching all again — fully cached, zero API calls)")
    for symbol in symbols:
        data = await cached.chart.historical_price_full(
            symbol, "2024-06-01", "2024-06-30"
        )
        print(f"   {symbol}: {len(data)} records (cache hit)")


async def economics_example(cached: CachedClient) -> None:
    """Demonstrate caching of global (non-symbol) endpoints."""
    print("\n=== Global Endpoints (Economics) ===")

    print("1. Fetching treasury rates for Q1 2024...")
    rates = await cached.economics.treasury_rates("2024-01-01", "2024-03-31")
    print(f"   Got {len(rates)} records")

    print("2. Extending to Q2 2024 — only the gap is fetched...")
    rates = await cached.economics.treasury_rates("2024-01-01", "2024-06-30")
    print(f"   Got {len(rates)} records (Q1 from cache, Q2 from API)")


async def passthrough_example(cached: CachedClient) -> None:
    """Demonstrate that non-cacheable endpoints pass through unchanged."""
    print("\n=== Non-Cacheable Passthrough ===")

    print("Fetching AAPL company profile (not cached, passes through to API)...")
    profile = await cached.company.profile("AAPL")
    if profile:
        name = profile[0].get("companyName", "N/A") if isinstance(profile, list) else profile.get("companyName", "N/A")
        print(f"   Company: {name}")
    print("   (Non-cacheable methods work exactly like FmpClient)")


async def inspect_storage_example(cached: CachedClient) -> None:
    """Demonstrate storage inspection utilities."""
    print("\n=== Storage Inspection ===")

    keys = await cached.storage.list_keys()
    print(f"Total cached datasets: {len(keys)}")

    for key in keys[:10]:
        meta = await cached.storage.get_stored_range(key)
        if meta:
            print(f"   {'/'.join(key)}: {meta.min_date} to {meta.max_date} ({meta.record_count} records)")
        else:
            print(f"   {'/'.join(key)}: (no metadata)")

    if len(keys) > 10:
        print(f"   ... and {len(keys) - 10} more")


async def main() -> None:
    """Main function demonstrating CachedClient functionality."""
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("  export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP CachedClient Example")
    print("=" * 50)

    # Create the FmpClient + CachedClient
    # By default, data is cached in ~/.aiofmp/cache (override with AIOFMP_CACHE_FILE_PATH env var)
    fmp = FmpClient(api_key=api_key)
    cached = CachedClient(fmp)

    async with cached:
        await date_range_caching_example(cached)
        await period_based_caching_example(cached)
        await multiple_symbols_example(cached)
        await economics_example(cached)
        await passthrough_example(cached)
        await inspect_storage_example(cached)

    print("\nDone! Cached data is stored in ~/.aiofmp/cache/")
    print("(Override with AIOFMP_CACHE_FILE_PATH environment variable)")
    print("Run this script again to see that all calls are served from cache.")


if __name__ == "__main__":
    asyncio.run(main())
