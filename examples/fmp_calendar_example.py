#!/usr/bin/env python3
"""
Example script demonstrating FMP Calendar category functionality

This script shows how to use the FMP client to access calendar data including
dividends, earnings, IPOs, stock splits, and related calendar events.
"""

import asyncio
import os
from datetime import datetime, timedelta

from aiofmp import FmpClient


async def dividends_example(client: FmpClient) -> None:
    """Demonstrate dividends functionality"""
    print("\n=== Dividends Examples ===")

    # Get company-specific dividends
    print("Fetching dividend history for AAPL...")
    dividends = await client.calendar.dividends_company("AAPL", limit=10)
    print(f"Found {len(dividends)} dividend records")

    if dividends:
        print("\nRecent dividend history:")
        for i, dividend in enumerate(dividends[:5]):
            print(f"  {i + 1}. Date: {dividend.get('date', 'N/A')}")
            print(f"     Amount: ${dividend.get('dividend', 0):.2f}")
            print(f"     Yield: {dividend.get('yield', 0):.2%}")
            print(f"     Frequency: {dividend.get('frequency', 'N/A')}")
            print(f"     Record Date: {dividend.get('recordDate', 'N/A')}")
            print(f"     Payment Date: {dividend.get('paymentDate', 'N/A')}")
            print()

    # Get dividend calendar for a date range
    print("Fetching dividend calendar for Q1 2025...")
    dividend_calendar = await client.calendar.dividends_calendar(
        "2025-01-01", "2025-03-31"
    )
    print(f"Found {len(dividend_calendar)} dividend events in Q1 2025")

    if dividend_calendar:
        print("\nSample dividend events:")
        for i, event in enumerate(dividend_calendar[:3]):
            print(
                f"  {i + 1}. {event.get('symbol', 'N/A')}: ${event.get('dividend', 0):.2f}"
            )
            print(f"     Date: {event.get('date', 'N/A')}")
            print(f"     Yield: {event.get('yield', 0):.2%}")
            print(f"     Frequency: {event.get('frequency', 'N/A')}")
            print()


async def earnings_example(client: FmpClient) -> None:
    """Demonstrate earnings functionality"""
    print("\n=== Earnings Examples ===")

    # Get company-specific earnings
    print("Fetching earnings history for AAPL...")
    earnings = await client.calendar.earnings_company("AAPL", limit=10)
    print(f"Found {len(earnings)} earnings records")

    if earnings:
        print("\nRecent earnings history:")
        for i, earning in enumerate(earnings[:5]):
            print(f"  {i + 1}. Date: {earning.get('date', 'N/A')}")

            eps_estimated = earning.get("epsEstimated")
            if eps_estimated is not None:
                print(f"     EPS Estimated: ${eps_estimated:.2f}")

            eps_actual = earning.get("epsActual")
            if eps_actual is not None:
                print(f"     EPS Actual: ${eps_actual:.2f}")

            revenue_estimated = earning.get("revenueEstimated")
            if revenue_estimated is not None:
                revenue_billions = revenue_estimated / 1_000_000_000
                print(f"     Revenue Estimated: ${revenue_billions:.1f}B")

            revenue_actual = earning.get("revenueActual")
            if revenue_actual is not None:
                revenue_billions = revenue_actual / 1_000_000_000
                print(f"     Revenue Actual: ${revenue_billions:.1f}B")

            print(f"     Last Updated: {earning.get('lastUpdated', 'N/A')}")
            print()

    # Get earnings calendar for a date range
    print("Fetching earnings calendar for Q1 2025...")
    earnings_calendar = await client.calendar.earnings_calendar(
        "2025-01-01", "2025-03-31"
    )
    print(f"Found {len(earnings_calendar)} earnings announcements in Q1 2025")

    if earnings_calendar:
        print("\nSample earnings announcements:")
        for i, announcement in enumerate(earnings_calendar[:3]):
            print(
                f"  {i + 1}. {announcement.get('symbol', 'N/A')}: {announcement.get('date', 'N/A')}"
            )

            eps_estimated = announcement.get("epsEstimated")
            if eps_estimated is not None:
                print(f"     EPS Estimated: ${eps_estimated:.2f}")

            eps_actual = announcement.get("epsActual")
            if eps_actual is not None:
                print(f"     EPS Actual: ${eps_actual:.2f}")
            print()


async def ipos_example(client: FmpClient) -> None:
    """Demonstrate IPOs functionality"""
    print("\n=== IPOs Examples ===")

    # Get IPO calendar for upcoming offerings
    print("Fetching IPO calendar for H1 2025...")
    ipos = await client.calendar.ipos_calendar("2025-01-01", "2025-06-30")
    print(f"Found {len(ipos)} upcoming IPOs")

    if ipos:
        print("\nUpcoming IPOs:")
        for i, ipo in enumerate(ipos[:5]):
            print(f"  {i + 1}. {ipo.get('symbol', 'N/A')}: {ipo.get('company', 'N/A')}")
            print(f"     Date: {ipo.get('date', 'N/A')}")
            print(f"     Exchange: {ipo.get('exchange', 'N/A')}")
            print(f"     Status: {ipo.get('actions', 'N/A')}")

            shares = ipo.get("shares")
            if shares is not None:
                print(f"     Shares: {shares:,}")

            price_range = ipo.get("priceRange")
            if price_range is not None:
                print(f"     Price Range: {price_range}")

            market_cap = ipo.get("marketCap")
            if market_cap is not None:
                market_cap_billions = market_cap / 1_000_000_000
                print(f"     Market Cap: ${market_cap_billions:.1f}B")
            print()

    # Get IPO disclosure filings
    print("Fetching IPO disclosure filings for H1 2025...")
    disclosures = await client.calendar.ipos_disclosure("2025-01-01", "2025-06-30")
    print(f"Found {len(disclosures)} disclosure filings")

    if disclosures:
        print("\nIPO Disclosure Filings:")
        for i, disclosure in enumerate(disclosures[:3]):
            print(f"  {i + 1}. {disclosure.get('symbol', 'N/A')}")
            print(f"     Filing Date: {disclosure.get('filingDate', 'N/A')}")
            print(f"     Accepted Date: {disclosure.get('acceptedDate', 'N/A')}")
            print(
                f"     Effectiveness Date: {disclosure.get('effectivenessDate', 'N/A')}"
            )
            print(f"     CIK: {disclosure.get('cik', 'N/A')}")
            print(f"     Form: {disclosure.get('form', 'N/A')}")
            print()

    # Get IPO prospectus information
    print("Fetching IPO prospectus information for H1 2025...")
    prospectuses = await client.calendar.ipos_prospectus("2025-01-01", "2025-06-30")
    print(f"Found {len(prospectuses)} prospectus records")

    if prospectuses:
        print("\nIPO Prospectus Information:")
        for i, prospectus in enumerate(prospectuses[:3]):
            print(f"  {i + 1}. {prospectus.get('symbol', 'N/A')}")
            print(f"     IPO Date: {prospectus.get('ipoDate', 'N/A')}")
            print(
                f"     Price per Share: ${prospectus.get('pricePublicPerShare', 0):.2f}"
            )
            print(f"     Total Price: ${prospectus.get('pricePublicTotal', 0):,.2f}")
            print(f"     Form: {prospectus.get('form', 'N/A')}")
            print(f"     CIK: {prospectus.get('cik', 'N/A')}")
            print()


async def stock_splits_example(client: FmpClient) -> None:
    """Demonstrate stock splits functionality"""
    print("\n=== Stock Splits Examples ===")

    # Get company-specific stock splits
    print("Fetching stock split history for AAPL...")
    splits = await client.calendar.stock_splits_company("AAPL", limit=10)
    print(f"Found {len(splits)} stock split records")

    if splits:
        print("\nStock split history:")
        for i, split in enumerate(splits[:5]):
            print(f"  {i + 1}. Date: {split.get('date', 'N/A')}")
            numerator = split.get("numerator", 0)
            denominator = split.get("denominator", 1)
            print(f"     Ratio: {numerator}:{denominator}")
            print(f"     Split Factor: {numerator / denominator:.1f}x")
            print()

    # Get stock splits calendar for a date range
    print("Fetching stock splits calendar for H1 2025...")
    splits_calendar = await client.calendar.stock_splits_calendar(
        "2025-01-01", "2025-06-30"
    )
    print(f"Found {len(splits_calendar)} upcoming stock splits")

    if splits_calendar:
        print("\nUpcoming stock splits:")
        for i, split in enumerate(splits_calendar[:5]):
            print(
                f"  {i + 1}. {split.get('symbol', 'N/A')}: {split.get('date', 'N/A')}"
            )
            numerator = split.get("numerator", 0)
            denominator = split.get("denominator", 1)
            print(f"     Ratio: {numerator}:{denominator}")
            print(f"     Split Factor: {numerator / denominator:.1f}x")
            print()


async def calendar_analysis_example(client: FmpClient) -> None:
    """Demonstrate comprehensive calendar analysis"""
    print("\n=== Calendar Analysis Examples ===")

    # Get current date and calculate date ranges
    today = datetime.now()
    next_month = today + timedelta(days=30)
    next_quarter = today + timedelta(days=90)

    from_date = today.strftime("%Y-%m-%d")
    to_date_month = next_month.strftime("%Y-%m-%d")
    to_date_quarter = next_quarter.strftime("%Y-%m-%d")

    print(f"Analyzing calendar events from {from_date} to {to_date_quarter}")

    # Get comprehensive calendar data
    print("\nFetching comprehensive calendar data...")

    try:
        # Dividends
        dividends = await client.calendar.dividends_calendar(from_date, to_date_quarter)
        print(f"  Dividends: {len(dividends)} events")

        # Earnings
        earnings = await client.calendar.earnings_calendar(from_date, to_date_quarter)
        print(f"  Earnings: {len(earnings)} announcements")

        # IPOs
        ipos = await client.calendar.ipos_calendar(from_date, to_date_quarter)
        print(f"  IPOs: {len(ipos)} offerings")

        # Stock splits
        splits = await client.calendar.stock_splits_calendar(from_date, to_date_quarter)
        print(f"  Stock Splits: {len(splits)} events")

        # Summary
        total_events = len(dividends) + len(earnings) + len(ipos) + len(splits)
        print(f"\nTotal calendar events: {total_events}")

        # Find high-yield dividend stocks
        if dividends:
            high_yield_dividends = [d for d in dividends if d.get("yield", 0) > 5.0]
            print(f"High-yield dividend stocks (>5%): {len(high_yield_dividends)}")

            if high_yield_dividends:
                print("  Top high-yield stocks:")
                for dividend in high_yield_dividends[:3]:
                    symbol = dividend.get("symbol", "N/A")
                    yield_val = dividend.get("yield", 0)
                    print(f"    {symbol}: {yield_val:.2f}%")

        # Find upcoming earnings surprises
        if earnings:
            upcoming_earnings = [e for e in earnings if e.get("date") >= from_date]
            print(f"Upcoming earnings announcements: {len(upcoming_earnings)}")

            if upcoming_earnings:
                print("  Next few earnings:")
                for earning in upcoming_earnings[:3]:
                    symbol = earning.get("symbol", "N/A")
                    date = earning.get("date", "N/A")
                    print(f"    {symbol}: {date}")

    except Exception as e:
        print(f"Error during calendar analysis: {e}")


async def multi_symbol_calendar_example(client: FmpClient) -> None:
    """Demonstrate analyzing calendar events for multiple symbols"""
    print("\n=== Multi-Symbol Calendar Analysis ===")

    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

    for symbol in symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            # Get dividends
            dividends = await client.calendar.dividends_company(symbol, limit=5)
            if dividends:
                latest_dividend = dividends[0]
                print(f"  Latest Dividend: ${latest_dividend.get('dividend', 0):.2f}")
                print(f"  Dividend Yield: {latest_dividend.get('yield', 0):.2%}")
                print(f"  Frequency: {latest_dividend.get('frequency', 'N/A')}")

            # Get earnings
            earnings = await client.calendar.earnings_company(symbol, limit=5)
            if earnings:
                latest_earnings = earnings[0]
                print(f"  Latest Earnings Date: {latest_earnings.get('date', 'N/A')}")

                eps_estimated = latest_earnings.get("epsEstimated")
                if eps_estimated is not None:
                    print(f"  EPS Estimated: ${eps_estimated:.2f}")

                eps_actual = latest_earnings.get("epsActual")
                if eps_actual is not None:
                    print(f"  EPS Actual: ${eps_actual:.2f}")

            # Get stock splits
            splits = await client.calendar.stock_splits_company(symbol, limit=5)
            if splits:
                latest_split = splits[0]
                numerator = latest_split.get("numerator", 0)
                denominator = latest_split.get("denominator", 1)
                print(
                    f"  Latest Split: {numerator}:{denominator} ({numerator / denominator:.1f}x)"
                )

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")


async def main() -> None:
    """Main function demonstrating FMP Calendar functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Calendar Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await dividends_example(client)
            await earnings_example(client)
            await ipos_example(client)
            await stock_splits_example(client)
            await calendar_analysis_example(client)
            await multi_symbol_calendar_example(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
