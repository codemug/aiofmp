#!/usr/bin/env python3
"""
Example script demonstrating FMP Chart category functionality

This script shows how to use the FMP client to access chart data including
historical price data, intraday data, and various time intervals.
"""

import asyncio
import os
from datetime import datetime, timedelta

from aiofmp import FmpClient


async def historical_price_examples(client: FmpClient) -> None:
    """Demonstrate historical price functionality"""
    print("\n=== Historical Price Examples ===")

    # Get light historical price data
    print("Fetching light historical price data for AAPL...")
    light_data = await client.chart.historical_price_light(
        "AAPL", "2025-01-01", "2025-01-31"
    )
    print(f"Found {len(light_data)} data points")

    if light_data:
        print("\nSample light price data:")
        for i, data in enumerate(light_data[:5]):
            print(f"  {i + 1}. Date: {data.get('date', 'N/A')}")
            print(f"     Price: ${data.get('price', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get full historical price data
    print("Fetching full historical price data for AAPL...")
    full_data = await client.chart.historical_price_full(
        "AAPL", "2025-01-01", "2025-01-31"
    )
    print(f"Found {len(full_data)} data points")

    if full_data:
        print("\nSample full price data:")
        for i, data in enumerate(full_data[:3]):
            print(f"  {i + 1}. Date: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print(f"     Change: ${data.get('change', 0):.2f}")
            print(f"     Change %: {data.get('changePercent', 0):.2f}%")
            print(f"     VWAP: ${data.get('vwap', 0):.2f}")
            print()

    # Get unadjusted historical price data
    print("Fetching unadjusted historical price data for AAPL...")
    unadjusted_data = await client.chart.historical_price_unadjusted(
        "AAPL", "2025-01-01", "2025-01-31"
    )
    print(f"Found {len(unadjusted_data)} data points")

    if unadjusted_data:
        print("\nSample unadjusted price data:")
        for i, data in enumerate(unadjusted_data[:3]):
            print(f"  {i + 1}. Date: {data.get('date', 'N/A')}")
            print(f"     Adj Open: ${data.get('adjOpen', 0):.2f}")
            print(f"     Adj High: ${data.get('adjHigh', 0):.2f}")
            print(f"     Adj Low: ${data.get('adjLow', 0):.2f}")
            print(f"     Adj Close: ${data.get('adjClose', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get dividend-adjusted historical price data
    print("Fetching dividend-adjusted historical price data for AAPL...")
    dividend_adjusted_data = await client.chart.historical_price_dividend_adjusted(
        "AAPL", "2025-01-01", "2025-01-31"
    )
    print(f"Found {len(dividend_adjusted_data)} data points")

    if dividend_adjusted_data:
        print("\nSample dividend-adjusted price data:")
        for i, data in enumerate(dividend_adjusted_data[:3]):
            print(f"  {i + 1}. Date: {data.get('date', 'N/A')}")
            print(f"     Adj Open: ${data.get('adjOpen', 0):.2f}")
            print(f"     Adj High: ${data.get('adjHigh', 0):.2f}")
            print(f"     Adj Low: ${data.get('adjLow', 0):.2f}")
            print(f"     Adj Close: ${data.get('adjClose', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()


async def intraday_examples(client: FmpClient) -> None:
    """Demonstrate intraday functionality"""
    print("\n=== Intraday Examples ===")

    # Get 1-minute intraday data
    print("Fetching 1-minute intraday data for AAPL...")
    intraday_1min = await client.chart.intraday_1min("AAPL", "2025-01-01", "2025-01-02")
    print(f"Found {len(intraday_1min)} 1-minute data points")

    if intraday_1min:
        print("\nSample 1-minute intraday data:")
        for i, data in enumerate(intraday_1min[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get 5-minute intraday data
    print("Fetching 5-minute intraday data for AAPL...")
    intraday_5min = await client.chart.intraday_5min("AAPL", "2025-01-01", "2025-01-02")
    print(f"Found {len(intraday_5min)} 5-minute data points")

    if intraday_5min:
        print("\nSample 5-minute intraday data:")
        for i, data in enumerate(intraday_5min[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get 15-minute intraday data
    print("Fetching 15-minute intraday data for AAPL...")
    intraday_15min = await client.chart.intraday_15min(
        "AAPL", "2025-01-01", "2025-01-02"
    )
    print(f"Found {len(intraday_15min)} 15-minute data points")

    if intraday_15min:
        print("\nSample 15-minute intraday data:")
        for i, data in enumerate(intraday_15min[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get 30-minute intraday data
    print("Fetching 30-minute intraday data for AAPL...")
    intraday_30min = await client.chart.intraday_30min(
        "AAPL", "2025-01-01", "2025-01-02"
    )
    print(f"Found {len(intraday_30min)} 30-minute data points")

    if intraday_30min:
        print("\nSample 30-minute intraday data:")
        for i, data in enumerate(intraday_30min[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get 1-hour intraday data
    print("Fetching 1-hour intraday data for AAPL...")
    intraday_1hour = await client.chart.intraday_1hour(
        "AAPL", "2025-01-01", "2025-01-02"
    )
    print(f"Found {len(intraday_1hour)} 1-hour data points")

    if intraday_1hour:
        print("\nSample 1-hour intraday data:")
        for i, data in enumerate(intraday_1hour[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Get 4-hour intraday data
    print("Fetching 4-hour intraday data for AAPL...")
    intraday_4hour = await client.chart.intraday_4hour(
        "AAPL", "2025-01-01", "2025-01-02"
    )
    print(f"Found {len(intraday_4hour)} 4-hour data points")

    if intraday_4hour:
        print("\nSample 4-hour intraday data:")
        for i, data in enumerate(intraday_4hour[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()


async def chart_analysis_examples(client: FmpClient) -> None:
    """Demonstrate chart analysis functionality"""
    print("\n=== Chart Analysis Examples ===")

    # Get current date and calculate date ranges
    today = datetime.now()
    last_month = today - timedelta(days=30)
    last_week = today - timedelta(days=7)

    from_date_month = last_month.strftime("%Y-%m-%d")
    from_date_week = last_week.strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    print(f"Analyzing chart data from {from_date_month} to {to_date}")

    # Get comprehensive chart data
    print("\nFetching comprehensive chart data...")

    try:
        # Historical price data (light)
        light_data = await client.chart.historical_price_light(
            "AAPL", from_date_month, to_date
        )
        print(f"  Historical Price (Light): {len(light_data)} data points")

        # Historical price data (full)
        full_data = await client.chart.historical_price_full(
            "AAPL", from_date_month, to_date
        )
        print(f"  Historical Price (Full): {len(full_data)} data points")

        # Intraday data (1-hour)
        intraday_data = await client.chart.intraday_1hour(
            "AAPL", from_date_week, to_date
        )
        print(f"  Intraday (1-hour): {len(intraday_data)} data points")

        # Summary
        total_data_points = len(light_data) + len(full_data) + len(intraday_data)
        print(f"\nTotal data points: {total_data_points}")

        # Analyze price trends
        if light_data:
            prices = [data.get("price", 0) for data in light_data if data.get("price")]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                print("\nPrice Analysis:")
                print(f"  Minimum Price: ${min_price:.2f}")
                print(f"  Maximum Price: ${max_price:.2f}")
                print(f"  Average Price: ${avg_price:.2f}")
                print(f"  Price Range: ${max_price - min_price:.2f}")

        # Analyze volume trends
        if light_data:
            volumes = [
                data.get("volume", 0) for data in light_data if data.get("volume")
            ]
            if volumes:
                min_volume = min(volumes)
                max_volume = max(volumes)
                avg_volume = sum(volumes) / len(volumes)
                print("\nVolume Analysis:")
                print(f"  Minimum Volume: {min_volume:,}")
                print(f"  Maximum Volume: {max_volume:,}")
                print(f"  Average Volume: {avg_volume:,.0f}")

        # Compare adjusted vs unadjusted data
        if full_data and light_data:
            print("\nData Comparison:")
            print(f"  Full Data Points: {len(full_data)}")
            print(f"  Light Data Points: {len(light_data)}")

            if len(full_data) > 0 and len(light_data) > 0:
                full_sample = full_data[0]
                light_sample = light_data[0]

                print("  Sample Full Data: OHLC + Volume + Changes + VWAP")
                print("  Sample Light Data: Price + Volume only")

    except Exception as e:
        print(f"Error during chart analysis: {e}")


async def multi_symbol_chart_example(client: FmpClient) -> None:
    """Demonstrate analyzing chart data for multiple symbols"""
    print("\n=== Multi-Symbol Chart Analysis ===")

    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

    for symbol in symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            # Get light historical data
            light_data = await client.chart.historical_price_light(
                symbol, "2025-01-01", "2025-01-31"
            )
            if light_data:
                latest_data = light_data[0]
                print(f"  Latest Price: ${latest_data.get('price', 0):.2f}")
                print(f"  Latest Volume: {latest_data.get('volume', 0):,}")

                # Calculate price change if we have multiple data points
                if len(light_data) > 1:
                    first_price = light_data[-1].get("price", 0)
                    last_price = light_data[0].get("price", 0)
                    if first_price > 0:
                        price_change = ((last_price - first_price) / first_price) * 100
                        print(f"  Monthly Change: {price_change:+.2f}%")

            # Get intraday data
            intraday_data = await client.chart.intraday_1hour(
                symbol, "2025-01-01", "2025-01-02"
            )
            if intraday_data:
                print(f"  Intraday Data Points: {len(intraday_data)}")

                # Show latest intraday data
                latest_intraday = intraday_data[0]
                print(
                    f"  Latest Intraday Close: ${latest_intraday.get('close', 0):.2f}"
                )

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")


async def nonadjusted_data_example(client: FmpClient) -> None:
    """Demonstrate nonadjusted data functionality"""
    print("\n=== Nonadjusted Data Examples ===")

    # Get nonadjusted intraday data
    print("Fetching nonadjusted 1-minute intraday data for AAPL...")
    nonadjusted_data = await client.chart.intraday_1min(
        "AAPL", "2025-01-01", "2025-01-02", nonadjusted=True
    )
    print(f"Found {len(nonadjusted_data)} nonadjusted data points")

    if nonadjusted_data:
        print("\nSample nonadjusted intraday data:")
        for i, data in enumerate(nonadjusted_data[:3]):
            print(f"  {i + 1}. Time: {data.get('date', 'N/A')}")
            print(f"     Open: ${data.get('open', 0):.2f}")
            print(f"     High: ${data.get('high', 0):.2f}")
            print(f"     Low: ${data.get('low', 0):.2f}")
            print(f"     Close: ${data.get('close', 0):.2f}")
            print(f"     Volume: {data.get('volume', 0):,}")
            print()

    # Compare adjusted vs nonadjusted
    print("Fetching adjusted 1-minute intraday data for comparison...")
    adjusted_data = await client.chart.intraday_1min(
        "AAPL", "2025-01-01", "2025-01-02", nonadjusted=False
    )
    print(f"Found {len(adjusted_data)} adjusted data points")

    if nonadjusted_data and adjusted_data:
        print("\nComparison (Adjusted vs Nonadjusted):")
        print(f"  Nonadjusted Data Points: {len(nonadjusted_data)}")
        print(f"  Adjusted Data Points: {len(adjusted_data)}")

        if len(nonadjusted_data) > 0 and len(adjusted_data) > 0:
            nonadj_sample = nonadjusted_data[0]
            adj_sample = adjusted_data[0]

            print(
                f"  Sample Nonadjusted: {nonadj_sample.get('date', 'N/A')} - Close: ${nonadj_sample.get('close', 0):.2f}"
            )
            print(
                f"  Sample Adjusted: {adj_sample.get('date', 'N/A')} - Close: ${adj_sample.get('close', 0):.2f}"
            )


async def main() -> None:
    """Main function demonstrating FMP Chart functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Chart Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await historical_price_examples(client)
            await intraday_examples(client)
            await chart_analysis_examples(client)
            await multi_symbol_chart_example(client)
            await nonadjusted_data_example(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
