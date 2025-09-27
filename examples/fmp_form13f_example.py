#!/usr/bin/env python3
"""
Example script demonstrating FMP Form 13F category functionality

This script shows how to use the FMP client to access Form 13F and institutional ownership
data including latest filings, extracts, analytics, performance summaries, and industry breakdowns.
"""

import asyncio
import os

from aiofmp import FmpClient


async def latest_filings_examples(client: FmpClient) -> None:
    """Demonstrate latest filings functionality"""
    print("\n=== Latest Form 13F Filings Examples ===")

    # Get latest institutional ownership filings
    print("Fetching latest Form 13F filings...")
    latest_filings = await client.form13f.latest_filings(page=0, limit=50)
    print(f"Found {len(latest_filings)} latest filings")

    if latest_filings:
        print("\nLatest Form 13F Filings Summary:")
        for i, filing in enumerate(latest_filings[:10]):  # Show first 10
            print(f"\n  {i + 1}. Institution: {filing.get('name', 'N/A')}")
            print(f"     CIK: {filing.get('cik', 'N/A')}")
            print(f"     Date: {filing.get('date', 'N/A')}")
            print(f"     Filing Date: {filing.get('filingDate', 'N/A')}")
            print(f"     Form Type: {filing.get('formType', 'N/A')}")
            print(f"     SEC Link: {filing.get('link', 'N/A')}")

        # Analyze filing types
        form_types = {}
        for filing in latest_filings:
            form_type = filing.get("formType", "Unknown")
            form_types[form_type] = form_types.get(form_type, 0) + 1

        print("\n📊 Filing Type Distribution:")
        for form_type, count in form_types.items():
            print(f"  {form_type}: {count} filings")

        # Find recent filings
        recent_filings = [
            f for f in latest_filings if f.get("date", "") >= "2024-12-01"
        ]
        print(f"\n📅 Recent Filings (Dec 2024+): {len(recent_filings)}")


async def filings_extract_examples(client: FmpClient) -> None:
    """Demonstrate filings extract functionality"""
    print("\n=== Form 13F Filings Extract Examples ===")

    # Extract Berkshire Hathaway holdings for Q3 2023
    print("Fetching Berkshire Hathaway holdings for Q3 2023...")
    berkshire_holdings = await client.form13f.filings_extract("0001067983", "2023", "3")
    print(f"Found {len(berkshire_holdings)} holdings for Berkshire Hathaway")

    if berkshire_holdings:
        print("\nBerkshire Hathaway Holdings Summary (Q3 2023):")

        # Calculate total portfolio value
        total_value = sum(holding.get("value", 0) for holding in berkshire_holdings)
        total_shares = sum(holding.get("shares", 0) for holding in berkshire_holdings)

        print(f"  Total Portfolio Value: ${total_value:,}")
        print(f"  Total Shares Held: {total_shares:,}")
        print(f"  Number of Positions: {len(berkshire_holdings)}")

        # Show top holdings by value
        sorted_holdings = sorted(
            berkshire_holdings, key=lambda x: x.get("value", 0), reverse=True
        )
        print("\n  Top 10 Holdings by Value:")
        for i, holding in enumerate(sorted_holdings[:10]):
            symbol = holding.get("symbol", "N/A")
            name = holding.get("nameOfIssuer", "N/A")
            shares = holding.get("shares", 0)
            value = holding.get("value", 0)
            percentage = (value / total_value * 100) if total_value > 0 else 0

            print(f"    {i + 1}. {symbol} ({name})")
            print(f"       Shares: {shares:,}")
            print(f"       Value: ${value:,}")
            print(f"       Portfolio Weight: {percentage:.2f}%")

        # Analyze by security type
        security_types = {}
        for holding in berkshire_holdings:
            sec_type = holding.get("titleOfClass", "Unknown")
            security_types[sec_type] = security_types.get(sec_type, 0) + 1

        print("\n  Security Type Breakdown:")
        for sec_type, count in security_types.items():
            print(f"    {sec_type}: {count} positions")

    # Extract Vanguard holdings for Q3 2023
    print("\nFetching Vanguard holdings for Q3 2023...")
    vanguard_holdings = await client.form13f.filings_extract("0000102909", "2023", "3")
    print(f"Found {len(vanguard_holdings)} holdings for Vanguard")

    if vanguard_holdings:
        vanguard_value = sum(holding.get("value", 0) for holding in vanguard_holdings)
        print(f"  Vanguard Total Portfolio Value: ${vanguard_value:,}")
        print(f"  Vanguard Number of Positions: {len(vanguard_holdings)}")


async def filings_dates_examples(client: FmpClient) -> None:
    """Demonstrate filings dates functionality"""
    print("\n=== Form 13F Filing Dates Examples ===")

    # Get filing dates for Berkshire Hathaway
    print("Fetching filing dates for Berkshire Hathaway...")
    berkshire_dates = await client.form13f.filings_dates("0001067983")
    print(f"Found {len(berkshire_dates)} filing dates for Berkshire Hathaway")

    if berkshire_dates:
        print("\nBerkshire Hathaway Filing Dates:")
        for date_record in berkshire_dates:
            date = date_record.get("date", "N/A")
            year = date_record.get("year", "N/A")
            quarter = date_record.get("quarter", "N/A")
            print(f"  {date} - Q{quarter} {year}")

    # Get filing dates for Vanguard
    print("\nFetching filing dates for Vanguard...")
    vanguard_dates = await client.form13f.filings_dates("0000102909")
    print(f"Found {len(vanguard_dates)} filing dates for Vanguard")

    if vanguard_dates:
        print("\nVanguard Filing Dates:")
        for date_record in vanguard_dates:
            date = date_record.get("date", "N/A")
            year = date_record.get("year", "N/A")
            quarter = date_record.get("quarter", "N/A")
            print(f"  {date} - Q{quarter} {year}")

    # Get filing dates for BlackRock
    print("\nFetching filing dates for BlackRock...")
    blackrock_dates = await client.form13f.filings_dates("0001100663")
    print(f"Found {len(blackrock_dates)} filing dates for BlackRock")

    if blackrock_dates:
        print("\nBlackRock Filing Dates:")
        for date_record in blackrock_dates:
            date = date_record.get("date", "N/A")
            year = date_record.get("year", "N/A")
            quarter = date_record.get("quarter", "N/A")
            print(f"  {date} - Q{quarter} {year}")


async def analytics_by_holder_examples(client: FmpClient) -> None:
    """Demonstrate analytics by holder functionality"""
    print("\n=== Form 13F Analytics by Holder Examples ===")

    # Get Apple institutional holder analytics for Q3 2023
    print("Fetching Apple institutional holder analytics for Q3 2023...")
    apple_analytics = await client.form13f.filings_extract_analytics_by_holder(
        "AAPL", "2023", "3", page=0, limit=20
    )
    print(f"Found {len(apple_analytics)} institutional holders for Apple")

    if apple_analytics:
        print("\nApple Institutional Holder Analytics (Q3 2023):")

        # Calculate total institutional ownership
        total_shares = sum(holder.get("sharesNumber", 0) for holder in apple_analytics)
        total_value = sum(holder.get("marketValue", 0) for holder in apple_analytics)

        print(f"  Total Institutional Shares: {total_shares:,}")
        print(f"  Total Institutional Value: ${total_value:,}")

        # Show top holders by ownership
        sorted_holders = sorted(
            apple_analytics, key=lambda x: x.get("ownership", 0), reverse=True
        )
        print("\n  Top 10 Institutional Holders by Ownership:")
        for i, holder in enumerate(sorted_holders[:10]):
            name = holder.get("investorName", "N/A")
            ownership = holder.get("ownership", 0)
            shares = holder.get("sharesNumber", 0)
            value = holder.get("marketValue", 0)
            weight = holder.get("weight", 0)

            print(f"    {i + 1}. {name}")
            print(f"       Ownership: {ownership:.2f}%")
            print(f"       Shares: {shares:,}")
            print(f"       Value: ${value:,}")
            print(f"       Portfolio Weight: {weight:.2f}%")

        # Analyze position changes
        new_positions = [h for h in apple_analytics if h.get("isNew", False)]
        sold_out = [h for h in apple_analytics if h.get("isSoldOut", False)]
        increased = [h for h in apple_analytics if h.get("changeInSharesNumber", 0) > 0]
        decreased = [h for h in apple_analytics if h.get("changeInSharesNumber", 0) < 0]

        print("\n  Position Changes Summary:")
        print(f"    New Positions: {len(new_positions)}")
        print(f"    Sold Out: {len(sold_out)}")
        print(f"    Increased: {len(increased)}")
        print(f"    Decreased: {len(decreased)}")

        # Show significant changes
        significant_changes = [
            h
            for h in apple_analytics
            if abs(h.get("changeInSharesNumberPercentage", 0)) > 10
        ]
        print("\n  Significant Changes (>10%):")
        for holder in significant_changes[:5]:
            name = holder.get("investorName", "N/A")
            change_pct = holder.get("changeInSharesNumberPercentage", 0)
            print(f"    {name}: {change_pct:+.2f}%")


async def holder_performance_examples(client: FmpClient) -> None:
    """Demonstrate holder performance functionality"""
    print("\n=== Institutional Holder Performance Examples ===")

    # Get Berkshire Hathaway performance summary
    print("Fetching Berkshire Hathaway performance summary...")
    berkshire_performance = await client.form13f.holder_performance_summary(
        "0001067983", page=0
    )
    print(
        f"Found {len(berkshire_performance)} performance records for Berkshire Hathaway"
    )

    if berkshire_performance:
        print("\nBerkshire Hathaway Performance Summary:")
        for record in berkshire_performance:
            date = record.get("date", "N/A")
            portfolio_size = record.get("portfolioSize", 0)
            market_value = record.get("marketValue", 0)
            performance = record.get("performance", 0)
            performance_pct = record.get("performancePercentage", 0)

            print(f"  Date: {date}")
            print(f"  Portfolio Size: {portfolio_size} positions")
            print(f"  Market Value: ${market_value:,}")
            print(f"  Performance: ${performance:,}")
            print(f"  Performance %: {performance_pct:.2f}%")

            # Portfolio changes
            securities_added = record.get("securitiesAdded", 0)
            securities_removed = record.get("securitiesRemoved", 0)
            turnover = record.get("turnover", 0)

            print(f"  Securities Added: {securities_added}")
            print(f"  Securities Removed: {securities_removed}")
            print(f"  Turnover: {turnover:.3f}")

            # Long-term performance
            perf_1y = record.get("performance1year", 0)
            perf_3y = record.get("performance3year", 0)
            perf_5y = record.get("performance5year", 0)
            perf_since_inception = record.get("performanceSinceInception", 0)

            print("  Performance Trends:")
            print(f"    1 Year: ${perf_1y:,}")
            print(f"    3 Year: ${perf_3y:,}")
            print(f"    5 Year: ${perf_5y:,}")
            print(f"    Since Inception: ${perf_since_inception:,}")

            # S&P 500 comparison
            sp500_relative = record.get("performanceRelativeToSP500Percentage", 0)
            print(f"  vs S&P 500: {sp500_relative:+.2f}%")

    # Get Vanguard performance summary
    print("\nFetching Vanguard performance summary...")
    vanguard_performance = await client.form13f.holder_performance_summary(
        "0000102909", page=0
    )
    print(f"Found {len(vanguard_performance)} performance records for Vanguard")

    if vanguard_performance:
        for record in vanguard_performance:
            market_value = record.get("marketValue", 0)
            performance = record.get("performance", 0)
            print(f"  Vanguard Market Value: ${market_value:,}")
            print(f"  Vanguard Performance: ${performance:,}")


async def industry_breakdown_examples(client: FmpClient) -> None:
    """Demonstrate industry breakdown functionality"""
    print("\n=== Institutional Holder Industry Breakdown Examples ===")

    # Get Berkshire Hathaway industry breakdown for Q3 2023
    print("Fetching Berkshire Hathaway industry breakdown for Q3 2023...")
    berkshire_industries = await client.form13f.holder_industry_breakdown(
        "0001067983", "2023", "3"
    )
    print(
        f"Found {len(berkshire_industries)} industry allocations for Berkshire Hathaway"
    )

    if berkshire_industries:
        print("\nBerkshire Hathaway Industry Breakdown (Q3 2023):")

        # Sort by weight
        sorted_industries = sorted(
            berkshire_industries, key=lambda x: x.get("weight", 0), reverse=True
        )

        for i, industry in enumerate(sorted_industries):
            name = industry.get("industryTitle", "N/A")
            weight = industry.get("weight", 0)
            last_weight = industry.get("lastWeight", 0)
            change = industry.get("changeInWeight", 0)
            performance = industry.get("performance", 0)

            print(f"\n  {i + 1}. {name}")
            print(f"     Current Weight: {weight:.2f}%")
            print(f"     Previous Weight: {last_weight:.2f}%")
            print(f"     Weight Change: {change:+.2f}%")
            print(f"     Performance: ${performance:,}")

        # Calculate total allocation
        total_weight = sum(
            industry.get("weight", 0) for industry in berkshire_industries
        )
        print(f"\n  Total Industry Allocation: {total_weight:.2f}%")

        # Find top performing industries
        top_performing = sorted(
            berkshire_industries, key=lambda x: x.get("performance", 0), reverse=True
        )
        print("\n  Top Performing Industries:")
        for industry in top_performing[:3]:
            name = industry.get("industryTitle", "N/A")
            performance = industry.get("performance", 0)
            print(f"    {name}: ${performance:,}")


async def symbol_positions_summary_examples(client: FmpClient) -> None:
    """Demonstrate symbol positions summary functionality"""
    print("\n=== Symbol Positions Summary Examples ===")

    # Get Apple institutional positions summary for Q3 2023
    print("Fetching Apple institutional positions summary for Q3 2023...")
    apple_positions = await client.form13f.symbol_positions_summary("AAPL", "2023", "3")
    print(f"Found {len(apple_positions)} position summary records for Apple")

    if apple_positions:
        print("\nApple Institutional Positions Summary (Q3 2023):")
        for record in apple_positions:
            investors_holding = record.get("investorsHolding", 0)
            shares_13f = record.get("numberOf13Fshares", 0)
            total_invested = record.get("totalInvested", 0)
            ownership_percent = record.get("ownershipPercent", 0)

            print(f"  Investors Holding: {investors_holding:,}")
            print(f"  13F Shares: {shares_13f:,}")
            print(f"  Total Invested: ${total_invested:,}")
            print(f"  Ownership %: {ownership_percent:.2f}%")

            # Position changes
            new_positions = record.get("newPositions", 0)
            increased_positions = record.get("increasedPositions", 0)
            reduced_positions = record.get("reducedPositions", 0)
            closed_positions = record.get("closedPositions", 0)

            print("  Position Changes:")
            print(f"    New: {new_positions}")
            print(f"    Increased: {increased_positions}")
            print(f"    Reduced: {reduced_positions}")
            print(f"    Closed: {closed_positions}")

            # Options activity
            total_calls = record.get("totalCalls", 0)
            total_puts = record.get("totalPuts", 0)
            put_call_ratio = record.get("putCallRatio", 0)

            print("  Options Activity:")
            print(f"    Total Calls: {total_calls:,}")
            print(f"    Total Puts: {total_puts:,}")
            print(f"    Put/Call Ratio: {put_call_ratio:.3f}")

    # Get Microsoft institutional positions summary
    print("\nFetching Microsoft institutional positions summary for Q3 2023...")
    msft_positions = await client.form13f.symbol_positions_summary("MSFT", "2023", "3")
    print(f"Found {len(msft_positions)} position summary records for Microsoft")

    if msft_positions:
        for record in msft_positions:
            investors_holding = record.get("investorsHolding", 0)
            total_invested = record.get("totalInvested", 0)
            print(f"  MSFT Investors Holding: {investors_holding:,}")
            print(f"  MSFT Total Invested: ${total_invested:,}")


async def industry_performance_examples(client: FmpClient) -> None:
    """Demonstrate industry performance functionality"""
    print("\n=== Industry Performance Summary Examples ===")

    # Get industry performance summary for Q3 2023
    print("Fetching industry performance summary for Q3 2023...")
    industry_performance = await client.form13f.industry_performance_summary(
        "2023", "3"
    )
    print(f"Found {len(industry_performance)} industry performance records")

    if industry_performance:
        print("\nIndustry Performance Summary (Q3 2023):")

        # Sort by industry value
        sorted_industries = sorted(
            industry_performance, key=lambda x: x.get("industryValue", 0), reverse=True
        )

        print("  Top 10 Industries by Value:")
        for i, industry in enumerate(sorted_industries[:10]):
            name = industry.get("industryTitle", "N/A")
            value = industry.get("industryValue", 0)
            date = industry.get("date", "N/A")

            print(f"    {i + 1}. {name}")
            print(f"       Value: ${value:,}")
            print(f"       Date: {date}")

        # Calculate total market value
        total_value = sum(
            industry.get("industryValue", 0) for industry in industry_performance
        )
        print(f"\n  Total Market Value: ${total_value:,}")

        # Find largest industries
        largest_industries = sorted_industries[:5]
        print("\n  Largest Industries:")
        for industry in largest_industries:
            name = industry.get("industryTitle", "N/A")
            value = industry.get("industryValue", 0)
            percentage = (value / total_value * 100) if total_value > 0 else 0
            print(f"    {name}: ${value:,} ({percentage:.2f}%)")


async def institutional_analysis_examples(client: FmpClient) -> None:
    """Demonstrate comprehensive institutional analysis functionality"""
    print("\n=== Comprehensive Institutional Analysis Examples ===")

    # Analyze institutional ownership patterns comprehensively
    print("Performing comprehensive institutional ownership analysis...")

    # Get data for multiple companies
    companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    year = "2023"
    quarter = "3"

    print(f"\n📊 Institutional Ownership Analysis for Q{quarter} {year}:")

    for symbol in companies:
        print(f"\n🔍 Analyzing {symbol}...")

        try:
            # Get positions summary
            positions = await client.form13f.symbol_positions_summary(
                symbol, year, quarter
            )

            if positions:
                position = positions[0]
                investors = position.get("investorsHolding", 0)
                shares = position.get("numberOf13Fshares", 0)
                total_invested = position.get("totalInvested", 0)
                ownership = position.get("ownershipPercent", 0)

                print(f"  📈 {symbol} Summary:")
                print(f"    Institutional Investors: {investors:,}")
                print(f"    13F Shares: {shares:,}")
                print(f"    Total Invested: ${total_invested:,}")
                print(f"    Ownership %: {ownership:.2f}%")

                # Get top holders
                analytics = await client.form13f.filings_extract_analytics_by_holder(
                    symbol, year, quarter, page=0, limit=5
                )

                if analytics:
                    print("    Top 5 Institutional Holders:")
                    for i, holder in enumerate(analytics[:5]):
                        name = holder.get("investorName", "N/A")
                        ownership_pct = holder.get("ownership", 0)
                        value = holder.get("marketValue", 0)
                        print(
                            f"      {i + 1}. {name}: {ownership_pct:.2f}% (${value:,})"
                        )

                # Position changes
                new_pos = position.get("newPositions", 0)
                increased = position.get("increasedPositions", 0)
                reduced = position.get("reducedPositions", 0)
                closed = position.get("closedPositions", 0)

                print("    Position Changes:")
                print(
                    f"      New: {new_pos} | Increased: {increased} | Reduced: {reduced} | Closed: {closed}"
                )

                # Sentiment analysis
                if new_pos > closed and increased > reduced:
                    print("      🟢 Bullish institutional sentiment")
                elif closed > new_pos and reduced > increased:
                    print("      🔴 Bearish institutional sentiment")
                else:
                    print("      🟡 Mixed institutional sentiment")

        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")

    # Analyze major institutional investors
    print("\n🏦 Major Institutional Investor Analysis:")

    major_investors = [
        ("0001067983", "Berkshire Hathaway"),
        ("0000102909", "Vanguard Group"),
        ("0001100663", "BlackRock"),
        ("0001364742", "State Street"),
        ("0001166559", "Fidelity"),
    ]

    for cik, name in major_investors:
        print(f"\n  📋 {name} (CIK: {cik}):")

        try:
            # Get performance summary
            performance = await client.form13f.holder_performance_summary(cik, page=0)

            if performance:
                perf = performance[0]
                portfolio_size = perf.get("portfolioSize", 0)
                market_value = perf.get("marketValue", 0)
                performance_val = perf.get("performance", 0)
                performance_pct = perf.get("performancePercentage", 0)

                print(f"    Portfolio Size: {portfolio_size} positions")
                print(f"    Market Value: ${market_value:,}")
                print(
                    f"    Performance: ${performance_val:,} ({performance_pct:+.2f}%)"
                )

                # Get industry breakdown
                industries = await client.form13f.holder_industry_breakdown(
                    cik, year, quarter
                )

                if industries:
                    top_industry = max(industries, key=lambda x: x.get("weight", 0))
                    industry_name = top_industry.get("industryTitle", "N/A")
                    industry_weight = top_industry.get("weight", 0)

                    print(f"    Top Industry: {industry_name} ({industry_weight:.2f}%)")

        except Exception as e:
            print(f"    ❌ Error analyzing {name}: {e}")


async def main() -> None:
    """Main function demonstrating FMP Form 13F functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Form 13F Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await latest_filings_examples(client)
            await filings_extract_examples(client)
            await filings_dates_examples(client)
            await analytics_by_holder_examples(client)
            await holder_performance_examples(client)
            await industry_breakdown_examples(client)
            await symbol_positions_summary_examples(client)
            await industry_performance_examples(client)
            await institutional_analysis_examples(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
