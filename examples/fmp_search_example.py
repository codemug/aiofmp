#!/usr/bin/env python3
"""
Example script demonstrating FMP Search category functionality

This script shows how to use the FMP client to search for symbols,
companies, and screen stocks based on various criteria.
"""

import asyncio
import os

from aiofmp import FmpClient


async def search_symbols_example(client: FmpClient) -> None:
    """Demonstrate symbol search functionality"""
    print("\n=== Symbol Search Examples ===")

    # Basic symbol search
    print("Searching for 'AAPL'...")
    symbols = await client.search.symbols("AAPL")
    print(f"Found {len(symbols)} symbols:")
    for symbol in symbols[:3]:  # Show first 3 results
        print(
            f"  - {symbol['symbol']}: {symbol.get('name', 'N/A')} ({symbol.get('exchange', 'N/A')})"
        )

    # Search with limit
    print("\nSearching for 'MSFT' with limit 5...")
    msft_symbols = await client.search.symbols("MSFT", limit=5)
    print(f"Found {len(msft_symbols)} symbols:")
    for symbol in msft_symbols:
        print(f"  - {symbol['symbol']}: {symbol.get('name', 'N/A')}")

    # Search by exchange
    print("\nSearching for 'GOOGL' on NASDAQ...")
    nasdaq_symbols = await client.search.symbols("GOOGL", exchange="NASDAQ")
    print(f"Found {len(nasdaq_symbols)} NASDAQ symbols:")
    for symbol in nasdaq_symbols:
        print(f"  - {symbol['symbol']}: {symbol.get('name', 'N/A')}")


async def search_companies_example(client: FmpClient) -> None:
    """Demonstrate company search functionality"""
    print("\n=== Company Search Examples ===")

    # Search by company name
    print("Searching for companies with 'Apple' in name...")
    companies = await client.search.companies("Apple", limit=5)
    print(f"Found {len(companies)} companies:")
    for company in companies:
        print(
            f"  - {company['symbol']}: {company.get('name', 'N/A')} ({company.get('exchange', 'N/A')})"
        )

    # Search with exchange filter
    print("\nSearching for 'Microsoft' on NASDAQ...")
    msft_companies = await client.search.companies(
        "Microsoft", exchange="NASDAQ", limit=3
    )
    print(f"Found {len(msft_companies)} NASDAQ companies:")
    for company in msft_companies:
        print(f"  - {company['symbol']}: {company.get('name', 'N/A')}")


async def stock_screener_example(client: FmpClient) -> None:
    """Demonstrate stock screener functionality"""
    print("\n=== Stock Screener Examples ===")

    # Basic screener - Technology sector
    print("Screening for Technology sector stocks...")
    tech_stocks = await client.search.screener(sector="Technology", limit=5)
    print(f"Found {len(tech_stocks)} Technology stocks:")
    for stock in tech_stocks:
        print(
            f"  - {stock['symbol']}: {stock.get('companyName', 'N/A')} "
            f"(Market Cap: ${stock.get('marketCap', 0):,})"
        )

    # Screener with market cap filter
    print("\nScreening for large-cap stocks (>$100B)...")
    large_caps = await client.search.screener(
        market_cap_more_than=100000000000,  # $100B
        limit=5,
    )
    print(f"Found {len(large_caps)} large-cap stocks:")
    for stock in large_caps:
        market_cap = stock.get("marketCap", 0)
        market_cap_billions = market_cap / 1_000_000_000
        print(
            f"  - {stock['symbol']}: {stock.get('companyName', 'N/A')} "
            f"(Market Cap: ${market_cap_billions:.1f}B)"
        )

    # Screener with multiple filters
    print("\nScreening for dividend-paying stocks on NYSE...")
    dividend_stocks = await client.search.screener(
        exchange="NYSE", dividend_more_than=0.5, is_etf=False, limit=5
    )
    print(f"Found {len(dividend_stocks)} dividend-paying NYSE stocks:")
    for stock in dividend_stocks:
        dividend = stock.get("lastAnnualDividend", 0)
        print(
            f"  - {stock['symbol']}: {stock.get('companyName', 'N/A')} "
            f"(Dividend: ${dividend:.2f})"
        )

    # Complex screener
    print("\nScreening for mid-cap Technology stocks with high volume...")
    mid_cap_tech = await client.search.screener(
        sector="Technology",
        market_cap_more_than=10000000000,  # $10B
        market_cap_lower_than=100000000000,  # $100B
        volume_more_than=1000000,  # 1M+ volume
        exchange="NASDAQ",
        limit=5,
    )
    print(f"Found {len(mid_cap_tech)} mid-cap Technology stocks:")
    for stock in mid_cap_tech:
        market_cap = stock.get("marketCap", 0)
        market_cap_billions = market_cap / 1_000_000_000
        volume = stock.get("volume", 0)
        print(
            f"  - {stock['symbol']}: {stock.get('companyName', 'N/A')} "
            f"(Market Cap: ${market_cap_billions:.1f}B, Volume: {volume:,})"
        )


async def main() -> None:
    """Main function demonstrating FMP Search functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Search Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await search_symbols_example(client)
            await search_companies_example(client)
            await stock_screener_example(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
