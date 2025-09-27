#!/usr/bin/env python3
"""
Example script demonstrating FMP Directory category functionality

This script shows how to use the FMP client to access directory information
including company symbols, ETFs, exchanges, sectors, industries, and countries.
"""

import asyncio
import os

from aiofmp import FmpClient


async def company_symbols_example(client: FmpClient) -> None:
    """Demonstrate company symbols functionality"""
    print("\n=== Company Symbols Examples ===")

    # Get all company symbols
    print("Fetching company symbols list...")
    symbols = await client.directory.company_symbols()
    print(f"Found {len(symbols)} company symbols")

    # Show first few examples
    print("\nFirst 5 company symbols:")
    for i, symbol in enumerate(symbols[:5]):
        print(f"  {i + 1}. {symbol['symbol']}: {symbol.get('companyName', 'N/A')}")

    # Show some international examples
    international_symbols = [s for s in symbols if "." in s["symbol"]]
    if international_symbols:
        print(f"\nFound {len(international_symbols)} international symbols")
        print("Sample international symbols:")
        for i, symbol in enumerate(international_symbols[:3]):
            print(f"  - {symbol['symbol']}: {symbol.get('companyName', 'N/A')}")


async def financial_symbols_example(client: FmpClient) -> None:
    """Demonstrate financial symbols functionality"""
    print("\n=== Financial Symbols Examples ===")

    # Get financial symbols (companies with financial statements)
    print("Fetching financial symbols list...")
    financial_symbols = await client.directory.financial_symbols()
    print(f"Found {len(financial_symbols)} financial symbols")

    # Show first few examples with currency information
    print("\nFirst 5 financial symbols:")
    for i, symbol in enumerate(financial_symbols[:5]):
        trading_currency = symbol.get("tradingCurrency", "N/A")
        reporting_currency = symbol.get("reportingCurrency", "N/A")
        print(f"  {i + 1}. {symbol['symbol']}: {symbol.get('companyName', 'N/A')}")
        print(f"      Trading: {trading_currency}, Reporting: {reporting_currency}")

    # Show currency distribution
    currencies = {}
    for symbol in financial_symbols:
        currency = symbol.get("tradingCurrency", "Unknown")
        currencies[currency] = currencies.get(currency, 0) + 1

    print("\nCurrency distribution:")
    for currency, count in sorted(currencies.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]:
        print(f"  {currency}: {count} companies")


async def etf_list_example(client: FmpClient) -> None:
    """Demonstrate ETF list functionality"""
    print("\n=== ETF List Examples ===")

    # Get ETF list
    print("Fetching ETF list...")
    etfs = await client.directory.etf_list()
    print(f"Found {len(etfs)} ETFs")

    # Show first few examples
    print("\nFirst 10 ETFs:")
    for i, etf in enumerate(etfs[:10]):
        print(f"  {i + 1:2d}. {etf['symbol']}: {etf.get('name', 'N/A')}")

    # Show some popular ETFs
    popular_etf_symbols = ["SPY", "QQQ", "IWM", "VTI", "VEA", "VWO"]
    popular_etfs = [etf for etf in etfs if etf["symbol"] in popular_etf_symbols]

    if popular_etfs:
        print("\nPopular ETFs found:")
        for etf in popular_etfs:
            print(f"  - {etf['symbol']}: {etf.get('name', 'N/A')}")


async def actively_trading_example(client: FmpClient) -> None:
    """Demonstrate actively trading list functionality"""
    print("\n=== Actively Trading Examples ===")

    # Get actively trading list
    print("Fetching actively trading list...")
    active_symbols = await client.directory.actively_trading()
    print(f"Found {len(active_symbols)} actively trading symbols")

    # Show first few examples
    print("\nFirst 10 actively trading symbols:")
    for i, symbol in enumerate(active_symbols[:10]):
        print(f"  {i + 1:2d}. {symbol['symbol']}: {symbol.get('name', 'N/A')}")

    # Compare with total company symbols
    all_symbols = await client.directory.company_symbols()
    active_percentage = (len(active_symbols) / len(all_symbols)) * 100
    print(
        f"\nActively trading: {len(active_symbols):,} out of {len(all_symbols):,} total symbols ({active_percentage:.1f}%)"
    )


async def earnings_transcripts_example(client: FmpClient) -> None:
    """Demonstrate earnings transcripts functionality"""
    print("\n=== Earnings Transcripts Examples ===")

    # Get earnings transcripts list
    print("Fetching earnings transcripts list...")
    transcripts = await client.directory.earnings_transcripts()
    print(f"Found {len(transcripts)} companies with earnings transcripts")

    # Show companies with most transcripts
    sorted_transcripts = sorted(
        transcripts, key=lambda x: int(x.get("noOfTranscripts", 0)), reverse=True
    )

    print("\nTop 10 companies by number of transcripts:")
    for i, company in enumerate(sorted_transcripts[:10]):
        transcript_count = company.get("noOfTranscripts", "0")
        print(
            f"  {i + 1:2d}. {company['symbol']}: {company.get('companyName', 'N/A')} ({transcript_count} transcripts)"
        )

    # Show transcript count distribution
    transcript_counts = [int(t.get("noOfTranscripts", 0)) for t in transcripts]
    if transcript_counts:
        avg_transcripts = sum(transcript_counts) / len(transcript_counts)
        max_transcripts = max(transcript_counts)
        min_transcripts = min(transcript_counts)
        print("\nTranscript statistics:")
        print(f"  Average: {avg_transcripts:.1f}")
        print(f"  Maximum: {max_transcripts}")
        print(f"  Minimum: {min_transcripts}")


async def available_exchanges_example(client: FmpClient) -> None:
    """Demonstrate available exchanges functionality"""
    print("\n=== Available Exchanges Examples ===")

    # Get available exchanges
    print("Fetching available exchanges...")
    exchanges = await client.directory.available_exchanges()
    print(f"Found {len(exchanges)} exchanges")

    # Show all exchanges with details
    print("\nAll available exchanges:")
    for exchange in exchanges:
        print(f"  {exchange['exchange']}: {exchange.get('name', 'N/A')}")
        print(
            f"    Country: {exchange.get('countryName', 'N/A')} ({exchange.get('countryCode', 'N/A')})"
        )
        print(f"    Delay: {exchange.get('delay', 'N/A')}")
        print(f"    Symbol Suffix: {exchange.get('symbolSuffix', 'N/A')}")
        print()

    # Group by country
    countries = {}
    for exchange in exchanges:
        country = exchange.get("countryName", "Unknown")
        if country not in countries:
            countries[country] = []
        countries[country].append(exchange["exchange"])

    print("Exchanges by country:")
    for country, exchange_list in sorted(countries.items()):
        print(f"  {country}: {', '.join(exchange_list)}")


async def available_sectors_example(client: FmpClient) -> None:
    """Demonstrate available sectors functionality"""
    print("\n=== Available Sectors Examples ===")

    # Get available sectors
    print("Fetching available sectors...")
    sectors = await client.directory.available_sectors()
    print(f"Found {len(sectors)} sectors")

    # Show all sectors
    print("\nAll available sectors:")
    for i, sector in enumerate(sectors, 1):
        print(f"  {i:2d}. {sector['sector']}")

    # Show some common sectors
    common_sectors = [
        "Technology",
        "Healthcare",
        "Financial Services",
        "Consumer Cyclical",
        "Basic Materials",
    ]
    available_common = [s for s in sectors if s["sector"] in common_sectors]

    if available_common:
        print("\nCommon sectors available:")
        for sector in available_common:
            print(f"  - {sector['sector']}")


async def available_industries_example(client: FmpClient) -> None:
    """Demonstrate available industries functionality"""
    print("\n=== Available Industries Examples ===")

    # Get available industries
    print("Fetching available industries...")
    industries = await client.directory.available_industries()
    print(f"Found {len(industries)} industries")

    # Show first 20 industries
    print("\nFirst 20 industries:")
    for i, industry in enumerate(industries[:20], 1):
        print(f"  {i:2d}. {industry['industry']}")

    # Show some technology-related industries
    tech_industries = [
        i
        for i in industries
        if any(
            tech_word in i["industry"].lower()
            for tech_word in ["software", "hardware", "technology", "internet"]
        )
    ]

    if tech_industries:
        print(f"\nTechnology-related industries ({len(tech_industries)} found):")
        for industry in tech_industries[:10]:
            print(f"  - {industry['industry']}")


async def available_countries_example(client: FmpClient) -> None:
    """Demonstrate available countries functionality"""
    print("\n=== Available Countries Examples ===")

    # Get available countries
    print("Fetching available countries...")
    countries = await client.directory.available_countries()
    print(f"Found {len(countries)} countries")

    # Show all countries
    print("\nAll available countries:")
    for i, country in enumerate(countries, 1):
        print(f"  {i:2d}. {country['country']}")

    # Show some major markets
    major_markets = ["US", "CA", "GB", "DE", "FR", "JP", "AU", "HK", "SG"]
    available_major = [c for c in countries if c["country"] in major_markets]

    if available_major:
        print("\nMajor markets available:")
        for country in available_major:
            print(f"  - {country['country']}")


async def main() -> None:
    """Main function demonstrating FMP Directory functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Directory Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await company_symbols_example(client)
            await financial_symbols_example(client)
            await etf_list_example(client)
            await actively_trading_example(client)
            await earnings_transcripts_example(client)
            await available_exchanges_example(client)
            await available_sectors_example(client)
            await available_industries_example(client)
            await available_countries_example(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
