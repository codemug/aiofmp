#!/usr/bin/env python3
"""
Example script demonstrating FMP Company category functionality

This script shows how to use the FMP client to access company data including
company profiles, notes, employee counts, market capitalization, shares float,
mergers & acquisitions, executives, and compensation information.
"""

import asyncio
import os
from datetime import datetime, timedelta

from aiofmp import FmpClient


async def company_profile_examples(client: FmpClient) -> None:
    """Demonstrate company profile functionality"""
    print("\n=== Company Profile Examples ===")

    # Get company profile
    print("Fetching company profile for AAPL...")
    profile_data = await client.company.profile("AAPL")
    print(f"Found {len(profile_data)} profile records")

    if profile_data:
        profile = profile_data[0]
        print("\nCompany Profile Summary:")
        print(f"  Company Name: {profile.get('companyName', 'N/A')}")
        print(f"  Symbol: {profile.get('symbol', 'N/A')}")
        print(f"  Sector: {profile.get('sector', 'N/A')}")
        print(f"  Industry: {profile.get('industry', 'N/A')}")
        print(f"  Exchange: {profile.get('exchange', 'N/A')}")
        print(f"  Market Cap: ${profile.get('marketCap', 0):,.0f}")
        print(f"  Current Price: ${profile.get('price', 0):.2f}")
        print(f"  Beta: {profile.get('beta', 'N/A')}")
        print(f"  CEO: {profile.get('ceo', 'N/A')}")
        print(f"  Employees: {profile.get('fullTimeEmployees', 'N/A')}")
        print(f"  Country: {profile.get('country', 'N/A')}")
        print(f"  Website: {profile.get('website', 'N/A')}")
        print(f"  IPO Date: {profile.get('ipoDate', 'N/A')}")
        print(
            f"  Address: {profile.get('address', 'N/A')}, {profile.get('city', 'N/A')}, {profile.get('state', 'N/A')} {profile.get('zip', 'N/A')}"
        )

    # Get company notes
    print("\nFetching company notes for AAPL...")
    notes_data = await client.company.notes("AAPL")
    print(f"Found {len(notes_data)} notes")

    if notes_data:
        print("\nCompany Notes:")
        for i, note in enumerate(notes_data[:5]):
            print(f"  {i + 1}. {note.get('title', 'N/A')}")
            print(f"     Exchange: {note.get('exchange', 'N/A')}")
            print(f"     CIK: {note.get('cik', 'N/A')}")


async def employee_data_examples(client: FmpClient) -> None:
    """Demonstrate employee data functionality"""
    print("\n=== Employee Data Examples ===")

    # Get current employee count
    print("Fetching current employee count for AAPL...")
    employee_data = await client.company.employee_count("AAPL", limit=5)
    print(f"Found {len(employee_data)} employee count records")

    if employee_data:
        print("\nCurrent Employee Count:")
        for i, record in enumerate(employee_data[:3]):
            print(f"  {i + 1}. Period: {record.get('periodOfReport', 'N/A')}")
            print(f"     Employee Count: {record.get('employeeCount', 0):,}")
            print(f"     Filing Date: {record.get('filingDate', 'N/A')}")
            print(f"     Form Type: {record.get('formType', 'N/A')}")
            print(f"     Company: {record.get('companyName', 'N/A')}")

    # Get historical employee count
    print("\nFetching historical employee count for AAPL...")
    historical_employee_data = await client.company.historical_employee_count(
        "AAPL", limit=10
    )
    print(f"Found {len(historical_employee_data)} historical employee count records")

    if historical_employee_data:
        print("\nHistorical Employee Count Trend:")
        for i, record in enumerate(historical_employee_data[:5]):
            print(
                f"  {i + 1}. {record.get('periodOfReport', 'N/A')}: {record.get('employeeCount', 0):,} employees"
            )
            print(f"     Filed: {record.get('filingDate', 'N/A')}")


async def market_cap_examples(client: FmpClient) -> None:
    """Demonstrate market capitalization functionality"""
    print("\n=== Market Capitalization Examples ===")

    # Get current market cap
    print("Fetching current market cap for AAPL...")
    market_cap_data = await client.company.market_cap("AAPL")
    print(f"Found {len(market_cap_data)} market cap records")

    if market_cap_data:
        print("\nCurrent Market Cap:")
        for record in market_cap_data:
            print(f"  Date: {record.get('date', 'N/A')}")
            print(f"  Market Cap: ${record.get('marketCap', 0):,.0f}")

    # Get batch market cap for multiple companies
    print("\nFetching batch market cap for multiple companies...")
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    batch_market_cap = await client.company.batch_market_cap(symbols)
    print(f"Found {len(batch_market_cap)} batch market cap records")

    if batch_market_cap:
        print("\nBatch Market Cap Comparison:")
        for record in batch_market_cap:
            print(
                f"  {record.get('symbol', 'N/A')}: ${record.get('marketCap', 0):,.0f}"
            )

    # Get historical market cap
    print("\nFetching historical market cap for AAPL...")
    today = datetime.now()
    last_month = today - timedelta(days=30)
    from_date = last_month.strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    historical_market_cap = await client.company.historical_market_cap(
        "AAPL", from_date=from_date, to_date=to_date
    )
    print(f"Found {len(historical_market_cap)} historical market cap records")

    if historical_market_cap:
        print("\nHistorical Market Cap (Last 30 days):")
        for i, record in enumerate(historical_market_cap[:5]):
            print(
                f"  {i + 1}. {record.get('date', 'N/A')}: ${record.get('marketCap', 0):,.0f}"
            )


async def shares_float_examples(client: FmpClient) -> None:
    """Demonstrate shares float functionality"""
    print("\n=== Shares Float Examples ===")

    # Get company shares float
    print("Fetching shares float for AAPL...")
    shares_float_data = await client.company.shares_float("AAPL")
    print(f"Found {len(shares_float_data)} shares float records")

    if shares_float_data:
        print("\nShares Float Information:")
        for record in shares_float_data:
            print(f"  Date: {record.get('date', 'N/A')}")
            print(f"  Free Float: {record.get('freeFloat', 0):.2f}%")
            print(f"  Float Shares: {record.get('floatShares', 0):,}")
            print(f"  Outstanding Shares: {record.get('outstandingShares', 0):,}")

    # Get all shares float (limited sample)
    print("\nFetching sample of all shares float data...")
    all_shares_float = await client.company.all_shares_float(limit=10, page=0)
    print(f"Found {len(all_shares_float)} shares float records")

    if all_shares_float:
        print("\nSample Shares Float Data:")
        for i, record in enumerate(all_shares_float[:5]):
            print(f"  {i + 1}. {record.get('symbol', 'N/A')}")
            print(f"     Free Float: {record.get('freeFloat', 0):.2f}%")
            print(f"     Float Shares: {record.get('floatShares', 0):,}")
            print(f"     Outstanding Shares: {record.get('outstandingShares', 0):,}")


async def mergers_acquisitions_examples(client: FmpClient) -> None:
    """Demonstrate mergers and acquisitions functionality"""
    print("\n=== Mergers & Acquisitions Examples ===")

    # Get latest M&A
    print("Fetching latest mergers and acquisitions...")
    latest_ma = await client.company.latest_mergers_acquisitions(page=0, limit=10)
    print(f"Found {len(latest_ma)} latest M&A records")

    if latest_ma:
        print("\nLatest Mergers & Acquisitions:")
        for i, record in enumerate(latest_ma[:5]):
            print(
                f"  {i + 1}. {record.get('companyName', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(
                f"     Target: {record.get('targetedCompanyName', 'N/A')} ({record.get('targetedSymbol', 'N/A')})"
            )
            print(f"     Transaction Date: {record.get('transactionDate', 'N/A')}")
            print(f"     Accepted: {record.get('acceptedDate', 'N/A')}")

    # Search for specific M&A
    print("\nSearching for M&A involving 'Apple'...")
    apple_ma = await client.company.search_mergers_acquisitions("Apple")
    print(f"Found {len(apple_ma)} M&A records involving 'Apple'")

    if apple_ma:
        print("\nApple-Related M&A:")
        for i, record in enumerate(apple_ma[:3]):
            print(
                f"  {i + 1}. {record.get('companyName', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(
                f"     Target: {record.get('targetedCompanyName', 'N/A')} ({record.get('targetedSymbol', 'N/A')})"
            )
            print(f"     Transaction Date: {record.get('transactionDate', 'N/A')}")


async def executives_examples(client: FmpClient) -> None:
    """Demonstrate executives functionality"""
    print("\n=== Executives Examples ===")

    # Get company executives
    print("Fetching executives for AAPL...")
    executives_data = await client.company.executives("AAPL")
    print(f"Found {len(executives_data)} executive records")

    if executives_data:
        print("\nCompany Executives:")
        for i, executive in enumerate(executives_data[:5]):
            print(f"  {i + 1}. {executive.get('name', 'N/A')}")
            print(f"     Title: {executive.get('title', 'N/A')}")
            print(f"     Pay: {executive.get('pay', 'N/A')}")
            print(f"     Currency: {executive.get('currencyPay', 'N/A')}")
            print(f"     Gender: {executive.get('gender', 'N/A')}")
            print(f"     Year Born: {executive.get('yearBorn', 'N/A')}")

    # Get executive compensation
    print("\nFetching executive compensation for AAPL...")
    compensation_data = await client.company.executive_compensation("AAPL")
    print(f"Found {len(compensation_data)} compensation records")

    if compensation_data:
        print("\nExecutive Compensation:")
        for i, record in enumerate(compensation_data[:3]):
            print(f"  {i + 1}. {record.get('nameAndPosition', 'N/A')}")
            print(f"     Year: {record.get('year', 'N/A')}")
            print(f"     Salary: ${record.get('salary', 0):,}")
            print(f"     Bonus: ${record.get('bonus', 0):,}")
            print(f"     Stock Award: ${record.get('stockAward', 0):,}")
            print(f"     Total: ${record.get('total', 0):,}")
            print(f"     Filing Date: {record.get('filingDate', 'N/A')}")

    # Get executive compensation benchmark
    print("\nFetching executive compensation benchmark...")
    benchmark_data = await client.company.executive_compensation_benchmark("2024")
    print(f"Found {len(benchmark_data)} benchmark records")

    if benchmark_data:
        print("\nExecutive Compensation Benchmark (2024):")
        for i, record in enumerate(benchmark_data[:5]):
            print(f"  {i + 1}. {record.get('industryTitle', 'N/A')}")
            print(f"     Year: {record.get('year', 'N/A')}")
            print(
                f"     Average Compensation: ${record.get('averageCompensation', 0):,.0f}"
            )


async def company_analysis_examples(client: FmpClient) -> None:
    """Demonstrate comprehensive company analysis"""
    print("\n=== Company Analysis Examples ===")

    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            # Get comprehensive company data
            profile = await client.company.profile(symbol)
            market_cap = await client.company.market_cap(symbol)
            shares_float = await client.company.shares_float(symbol)
            executives = await client.company.executives(symbol)

            if profile:
                company_info = profile[0]
                print(f"  Company: {company_info.get('companyName', 'N/A')}")
                print(f"  Sector: {company_info.get('sector', 'N/A')}")
                print(f"  Industry: {company_info.get('industry', 'N/A')}")
                print(f"  Market Cap: ${company_info.get('marketCap', 0):,.0f}")
                print(f"  Employees: {company_info.get('fullTimeEmployees', 'N/A')}")
                print(f"  Beta: {company_info.get('beta', 'N/A')}")
                print(f"  Exchange: {company_info.get('exchange', 'N/A')}")

            if market_cap:
                latest_market_cap = market_cap[0]
                print(
                    f"  Latest Market Cap: ${latest_market_cap.get('marketCap', 0):,.0f}"
                )

            if shares_float:
                latest_shares = shares_float[0]
                print(f"  Free Float: {latest_shares.get('freeFloat', 0):.2f}%")
                print(
                    f"  Outstanding Shares: {latest_shares.get('outstandingShares', 0):,}"
                )

            if executives:
                print(f"  Executives: {len(executives)} found")
                if executives:
                    ceo = next(
                        (e for e in executives if "CEO" in e.get("title", "").upper()),
                        None,
                    )
                    if ceo:
                        print(f"  CEO: {ceo.get('name', 'N/A')}")

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")


async def main() -> None:
    """Main function demonstrating FMP Company functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Company Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await company_profile_examples(client)
            await employee_data_examples(client)
            await market_cap_examples(client)
            await shares_float_examples(client)
            await mergers_acquisitions_examples(client)
            await executives_examples(client)
            await company_analysis_examples(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
