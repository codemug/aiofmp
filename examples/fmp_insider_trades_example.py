#!/usr/bin/env python3
"""
Example script demonstrating FMP Insider Trades category functionality

This script shows how to use the FMP client to access insider trading data including
latest trades, search capabilities, transaction types, statistics, and acquisition ownership.
"""

import asyncio
import os
from datetime import date

from aiofmp import FmpClient


async def latest_insider_trades_examples(client: FmpClient) -> None:
    """Demonstrate latest insider trades functionality"""
    print("\n=== Latest Insider Trading Examples ===")

    # Get latest insider trading activity
    print("Fetching latest insider trading activity...")
    latest_trades = await client.insider_trades.latest_insider_trades(page=0, limit=50)
    print(f"Found {len(latest_trades)} latest insider trades")

    if latest_trades:
        print("\nLatest Insider Trading Activity Summary:")

        # Show first 10 trades
        for i, trade in enumerate(latest_trades[:10]):
            symbol = trade.get("symbol", "N/A")
            reporting_name = trade.get("reportingName", "N/A")
            transaction_type = trade.get("transactionType", "N/A")
            filing_date = trade.get("filingDate", "N/A")
            transaction_date = trade.get("transactionDate", "N/A")
            securities_transacted = trade.get("securitiesTransacted", 0)
            price = trade.get("price", 0)
            type_of_owner = trade.get("typeOfOwner", "N/A")

            print(f"\n  {i + 1}. {symbol} - {reporting_name}")
            print(f"     Transaction Type: {transaction_type}")
            print(f"     Filing Date: {filing_date}")
            print(f"     Transaction Date: {transaction_date}")
            print(f"     Securities: {securities_transacted:,}")
            print(f"     Price: ${price:.2f}" if price > 0 else "     Price: N/A")
            print(f"     Owner Type: {type_of_owner}")

        # Analyze transaction types
        transaction_types = {}
        for trade in latest_trades:
            trans_type = trade.get("transactionType", "Unknown")
            transaction_types[trans_type] = transaction_types.get(trans_type, 0) + 1

        print("\n📊 Transaction Type Distribution:")
        for trans_type, count in sorted(
            transaction_types.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {trans_type}: {count} trades")

        # Analyze by acquisition/disposition
        acquisitions = [
            t for t in latest_trades if t.get("acquisitionOrDisposition") == "A"
        ]
        dispositions = [
            t for t in latest_trades if t.get("acquisitionOrDisposition") == "D"
        ]

        print("\n📈 Acquisition vs Disposition:")
        print(f"  🟢 Acquisitions: {len(acquisitions)} trades")
        print(f"  🔴 Dispositions: {len(dispositions)} trades")

        # Find recent trades (last 7 days)
        today = date.today()
        recent_trades = []
        for trade in latest_trades:
            try:
                filing_date = date.fromisoformat(trade.get("filingDate", "2000-01-01"))
                if (today - filing_date).days <= 7:
                    recent_trades.append(trade)
            except ValueError:
                continue

        print(f"\n📅 Recent Trades (Last 7 Days): {len(recent_trades)}")

        # Analyze by company
        companies = {}
        for trade in latest_trades:
            symbol = trade.get("symbol", "Unknown")
            companies[symbol] = companies.get(symbol, 0) + 1

        print("\n🏢 Top Companies by Insider Activity:")
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
        for symbol, count in top_companies:
            print(f"  {symbol}: {count} trades")


async def search_insider_trades_examples(client: FmpClient) -> None:
    """Demonstrate search insider trades functionality"""
    print("\n=== Search Insider Trades Examples ===")

    # Search for Apple insider trades
    print("Searching for Apple insider trades...")
    apple_trades = await client.insider_trades.search_insider_trades(
        symbol="AAPL", page=0, limit=100
    )
    print(f"Found {len(apple_trades)} Apple insider trades")

    if apple_trades:
        print("\nApple Insider Trading Summary:")

        # Show first 10 Apple trades
        for i, trade in enumerate(apple_trades[:10]):
            reporting_name = trade.get("reportingName", "N/A")
            transaction_type = trade.get("transactionType", "N/A")
            filing_date = trade.get("filingDate", "N/A")
            securities_transacted = trade.get("securitiesTransacted", 0)
            price = trade.get("price", 0)
            type_of_owner = trade.get("typeOfOwner", "N/A")

            print(f"\n  {i + 1}. {reporting_name}")
            print(f"     Transaction Type: {transaction_type}")
            print(f"     Filing Date: {filing_date}")
            print(f"     Securities: {securities_transacted:,}")
            print(f"     Price: ${price:.2f}" if price > 0 else "     Price: N/A")
            print(f"     Owner Type: {type_of_owner}")

        # Analyze Apple insider activity
        apple_transaction_types = {}
        for trade in apple_trades:
            trans_type = trade.get("transactionType", "Unknown")
            apple_transaction_types[trans_type] = (
                apple_transaction_types.get(trans_type, 0) + 1
            )

        print("\n📊 Apple Insider Trading by Type:")
        for trans_type, count in sorted(
            apple_transaction_types.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {trans_type}: {count} trades")

        # Search for specific transaction types
        print("\n🔍 Searching for Apple sales transactions...")
        apple_sales = await client.insider_trades.search_insider_trades(
            symbol="AAPL", transaction_type="S-Sale"
        )
        print(f"Found {len(apple_sales)} Apple sales transactions")

        if apple_sales:
            print("  Recent Apple Sales:")
            for i, sale in enumerate(apple_sales[:5]):
                name = sale.get("reportingName", "N/A")
                date = sale.get("filingDate", "N/A")
                shares = sale.get("securitiesTransacted", 0)
                price = sale.get("price", 0)
                print(
                    f"    {i + 1}. {name}: {shares:,} shares at ${price:.2f}"
                    if price > 0
                    else f"    {i + 1}. {name}: {shares:,} shares"
                )

        # Search for Apple purchases
        print("\n🔍 Searching for Apple purchase transactions...")
        apple_purchases = await client.insider_trades.search_insider_trades(
            symbol="AAPL", transaction_type="P-Purchase"
        )
        print(f"Found {len(apple_purchases)} Apple purchase transactions")

        if apple_purchases:
            print("  Recent Apple Purchases:")
            for i, purchase in enumerate(apple_purchases[:5]):
                name = purchase.get("reportingName", "N/A")
                date = purchase.get("filingDate", "N/A")
                shares = purchase.get("securitiesTransacted", 0)
                price = purchase.get("price", 0)
                print(
                    f"    {i + 1}. {name}: {shares:,} shares at ${price:.2f}"
                    if price > 0
                    else f"    {i + 1}. {name}: {shares:,} shares"
                )

    # Search for Microsoft insider trades
    print("\n🔍 Searching for Microsoft insider trades...")
    msft_trades = await client.insider_trades.search_insider_trades(
        symbol="MSFT", page=0, limit=50
    )
    print(f"Found {len(msft_trades)} Microsoft insider trades")

    if msft_trades:
        print("  Microsoft Insider Trading Summary:")
        msft_transaction_types = {}
        for trade in msft_trades:
            trans_type = trade.get("transactionType", "Unknown")
            msft_transaction_types[trans_type] = (
                msft_transaction_types.get(trans_type, 0) + 1
            )

        for trans_type, count in sorted(
            msft_transaction_types.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"    {trans_type}: {count} trades")


async def search_by_reporting_name_examples(client: FmpClient) -> None:
    """Demonstrate search by reporting name functionality"""
    print("\n=== Search by Reporting Name Examples ===")

    # Search for well-known executives
    well_known_executives = ["Zuckerberg", "Musk", "Cook", "Nadella", "Pichai"]

    for name in well_known_executives:
        print(f"\n🔍 Searching for insider trading by: {name}")

        try:
            results = await client.insider_trades.search_by_reporting_name(name)

            if results:
                print(f"  Found {len(results)} matches:")
                for result in results:
                    cik = result.get("reportingCik", "N/A")
                    full_name = result.get("reportingName", "N/A")
                    print(f"    {full_name} (CIK: {cik})")

                # Get insider trades for the first match
                if results:
                    first_match = results[0]
                    cik = first_match.get("reportingCik")
                    full_name = first_match.get("reportingName")

                    print(f"  \n📊 Getting insider trades for {full_name}...")
                    trades = await client.insider_trades.search_insider_trades(
                        reporting_cik=cik, limit=20
                    )

                    if trades:
                        print(f"    Found {len(trades)} insider trades:")
                        for i, trade in enumerate(trades[:5]):
                            symbol = trade.get("symbol", "N/A")
                            transaction_type = trade.get("transactionType", "N/A")
                            filing_date = trade.get("filingDate", "N/A")
                            securities = trade.get("securitiesTransacted", 0)
                            print(
                                f"      {i + 1}. {symbol}: {transaction_type} on {filing_date} ({securities:,} shares)"
                            )
                    else:
                        print(f"    No insider trades found for {full_name}")
            else:
                print(f"  No matches found for: {name}")

        except Exception as e:
            print(f"  ❌ Error searching for {name}: {e}")


async def transaction_types_examples(client: FmpClient) -> None:
    """Demonstrate transaction types functionality"""
    print("\n=== Transaction Types Examples ===")

    # Get all available transaction types
    print("Fetching all available insider trading transaction types...")
    all_types = await client.insider_trades.all_transaction_types()
    print(f"Found {len(all_types)} transaction types")

    if all_types:
        print("\nAll Insider Trading Transaction Types:")

        # Group by category
        categories = {"Acquisitions": [], "Dispositions": [], "Awards": [], "Other": []}

        for trans_type in all_types:
            type_name = trans_type.get("transactionType", "")

            if type_name.startswith("P-"):
                categories["Acquisitions"].append(type_name)
            elif type_name.startswith("S-"):
                categories["Dispositions"].append(type_name)
            elif type_name.startswith("A-"):
                categories["Awards"].append(type_name)
            else:
                categories["Other"].append(type_name)

        # Display by category
        for category, types in categories.items():
            if types:
                print(f"\n  📊 {category}:")
                for trans_type in sorted(types):
                    print(f"    • {trans_type}")

        # Show most common types
        print("\n📈 Most Common Transaction Types:")
        type_counts = {}
        for trans_type in all_types:
            type_name = trans_type.get("transactionType", "")
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        # This is a mock scenario since we're getting all types, not counts
        print("  Note: All transaction types are equally available")

        # Explain common transaction types
        print("\n📚 Common Transaction Type Explanations:")
        common_types = {
            "P-Purchase": "Purchase of securities",
            "S-Sale": "Sale of securities",
            "A-Award": "Award of securities (e.g., stock options, RSUs)",
            "M-Exempt": "Exempt transaction",
            "G-Gift": "Gift of securities",
            "W-Will": "Transfer by will",
            "D-Dividend": "Dividend reinvestment",
        }

        for trans_type, description in common_types.items():
            if any(t.get("transactionType") == trans_type for t in all_types):
                print(f"  • {trans_type}: {description}")


async def insider_trade_statistics_examples(client: FmpClient) -> None:
    """Demonstrate insider trade statistics functionality"""
    print("\n=== Insider Trade Statistics Examples ===")

    # Companies to analyze
    companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]

    for symbol in companies:
        print(f"\n📊 Insider Trading Statistics for {symbol}:")

        try:
            stats = await client.insider_trades.insider_trade_statistics(symbol)

            if stats:
                for stat in stats:
                    year = stat.get("year", "N/A")
                    quarter = stat.get("quarter", "N/A")
                    acquired_transactions = stat.get("acquiredTransactions", 0)
                    disposed_transactions = stat.get("disposedTransactions", 0)
                    acquired_disposed_ratio = stat.get("acquiredDisposedRatio", 0)
                    total_acquired = stat.get("totalAcquired", 0)
                    total_disposed = stat.get("totalDisposed", 0)
                    average_acquired = stat.get("averageAcquired", 0)
                    average_disposed = stat.get("averageDisposed", 0)
                    total_purchases = stat.get("totalPurchases", 0)
                    total_sales = stat.get("totalSales", 0)

                    print(f"  📅 Q{quarter} {year}:")
                    print(
                        f"    Transactions: {acquired_transactions} acquired, {disposed_transactions} disposed"
                    )
                    print(f"    Ratio: {acquired_disposed_ratio:.4f}")
                    print(
                        f"    Total: {total_acquired:,} acquired, {total_disposed:,} disposed"
                    )
                    print(
                        f"    Average: {average_acquired:,.0f} acquired, {average_disposed:,.0f} disposed"
                    )
                    print(f"    Purchases: {total_purchases}, Sales: {total_sales}")

                    # Sentiment analysis
                    if acquired_disposed_ratio > 1:
                        print(
                            "    🟢 Bullish sentiment (more acquisitions than dispositions)"
                        )
                    elif acquired_disposed_ratio < 1:
                        print(
                            "    🔴 Bearish sentiment (more dispositions than acquisitions)"
                        )
                    else:
                        print(
                            "    ➡️  Neutral sentiment (equal acquisitions and dispositions)"
                        )

                    # Activity level
                    total_transactions = acquired_transactions + disposed_transactions
                    if total_transactions > 20:
                        print("    📈 High insider activity")
                    elif total_transactions > 10:
                        print("    📊 Moderate insider activity")
                    else:
                        print("    📉 Low insider activity")
            else:
                print(f"  ❌ No statistics available for {symbol}")

        except Exception as e:
            print(f"  ❌ Error getting statistics for {symbol}: {e}")


async def acquisition_ownership_examples(client: FmpClient) -> None:
    """Demonstrate acquisition ownership functionality"""
    print("\n=== Acquisition Ownership Examples ===")

    # Companies to analyze
    companies = ["AAPL", "MSFT", "GOOGL"]

    for symbol in companies:
        print(f"\n🏢 Acquisition of Beneficial Ownership for {symbol}:")

        try:
            ownership_changes = await client.insider_trades.acquisition_ownership(
                symbol, limit=100
            )
            print(f"  Found {len(ownership_changes)} ownership changes")

            if ownership_changes:
                print("  Recent Ownership Changes:")

                # Show first 5 changes
                for i, change in enumerate(ownership_changes[:5]):
                    reporting_person = change.get("nameOfReportingPerson", "N/A")
                    filing_date = change.get("filingDate", "N/A")
                    amount_owned = change.get("amountBeneficiallyOwned", "0")
                    percent_of_class = change.get("percentOfClass", "0")
                    type_of_person = change.get("typeOfReportingPerson", "N/A")

                    print(f"    {i + 1}. {reporting_person}")
                    print(f"       Filing Date: {filing_date}")
                    print(f"       Amount Owned: {amount_owned:,}")
                    print(f"       Percent of Class: {percent_of_class}%")
                    print(f"       Type: {type_of_person}")

                # Analyze by type of reporting person
                person_types = {}
                for change in ownership_changes:
                    person_type = change.get("typeOfReportingPerson", "Unknown")
                    person_types[person_type] = person_types.get(person_type, 0) + 1

                print("  \n📊 Ownership Changes by Person Type:")
                for person_type, count in sorted(
                    person_types.items(), key=lambda x: x[1], reverse=True
                ):
                    print(f"    {person_type}: {count} changes")

                # Find significant ownership changes (>5%)
                significant_changes = [
                    change
                    for change in ownership_changes
                    if float(change.get("percentOfClass", "0")) > 5
                ]

                if significant_changes:
                    print("  \n⚠️  Significant Ownership Changes (>5%):")
                    for change in significant_changes:
                        person = change.get("nameOfReportingPerson", "N/A")
                        percent = change.get("percentOfClass", "0")
                        amount = change.get("amountBeneficiallyOwned", "0")
                        print(f"    • {person}: {percent}% ({amount:,} shares)")
                else:
                    print("  \n📊 No significant ownership changes (>5%) found")
            else:
                print(f"  ❌ No ownership changes found for {symbol}")

        except Exception as e:
            print(f"  ❌ Error getting ownership changes for {symbol}: {e}")


async def insider_analysis_examples(client: FmpClient) -> None:
    """Demonstrate comprehensive insider trading analysis"""
    print("\n=== Comprehensive Insider Trading Analysis ===")

    # Perform comprehensive analysis
    print("Performing comprehensive insider trading analysis...")

    # Major companies to analyze
    major_companies = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN", "META"]

    print("\n📊 Insider Trading Analysis for Major Companies:")

    for symbol in major_companies:
        print(f"\n🔍 Analyzing {symbol}...")

        try:
            # Get insider trades
            trades = await client.insider_trades.search_insider_trades(
                symbol, limit=100
            )

            if trades:
                print("  📈 Insider Trading Summary:")
                print(f"    Total Trades: {len(trades)}")

                # Analyze by transaction type
                transaction_types = {}
                for trade in trades:
                    trans_type = trade.get("transactionType", "Unknown")
                    transaction_types[trans_type] = (
                        transaction_types.get(trans_type, 0) + 1
                    )

                print("    Transaction Types:")
                for trans_type, count in sorted(
                    transaction_types.items(), key=lambda x: x[1], reverse=True
                ):
                    print(f"      {trans_type}: {count}")

                # Analyze by acquisition/disposition
                acquisitions = [
                    t for t in trades if t.get("acquisitionOrDisposition") == "A"
                ]
                dispositions = [
                    t for t in trades if t.get("acquisitionOrDisposition") == "D"
                ]

                print(
                    f"    Acquisitions: {len(acquisitions)}, Dispositions: {len(dispositions)}"
                )

                # Sentiment analysis
                if len(acquisitions) > len(dispositions):
                    print("    🟢 Bullish insider sentiment")
                elif len(dispositions) > len(acquisitions):
                    print("    🔴 Bearish insider sentiment")
                else:
                    print("    ➡️  Neutral insider sentiment")

                # Get statistics
                stats = await client.insider_trades.insider_trade_statistics(symbol)
                if stats:
                    latest_stat = stats[0]
                    ratio = latest_stat.get("acquiredDisposedRatio", 0)
                    print(f"    Acquired/Disposed Ratio: {ratio:.4f}")

                    if ratio > 1:
                        print("      📈 More acquisitions than dispositions")
                    elif ratio < 1:
                        print("      📉 More dispositions than acquisitions")
                    else:
                        print("      ➡️  Equal acquisitions and dispositions")

                # Recent activity
                recent_trades = [
                    t for t in trades if t.get("filingDate", "") >= "2024-01-01"
                ]
                print(f"    Recent Trades (2024+): {len(recent_trades)}")

                if recent_trades:
                    print("    Recent Activity:")
                    for trade in recent_trades[:3]:
                        name = trade.get("reportingName", "N/A")
                        trans_type = trade.get("transactionType", "N/A")
                        date = trade.get("filingDate", "N/A")
                        print(f"      • {name}: {trans_type} on {date}")

            else:
                print(f"  ❌ No insider trades found for {symbol}")

        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")

    # Market-wide insider sentiment
    print("\n🌐 Market-Wide Insider Sentiment Analysis:")

    try:
        # Get latest trades across all companies
        latest_trades = await client.insider_trades.latest_insider_trades(
            page=0, limit=200
        )

        if latest_trades:
            total_trades = len(latest_trades)
            acquisitions = [
                t for t in latest_trades if t.get("acquisitionOrDisposition") == "A"
            ]
            dispositions = [
                t for t in latest_trades if t.get("acquisitionOrDisposition") == "D"
            ]

            print(f"  📊 Total Recent Insider Trades: {total_trades}")
            print(
                f"  🟢 Acquisitions: {len(acquisitions)} ({len(acquisitions) / total_trades * 100:.1f}%)"
            )
            print(
                f"  🔴 Dispositions: {len(dispositions)} ({len(dispositions) / total_trades * 100:.1f}%)"
            )

            # Overall sentiment
            if len(acquisitions) > len(dispositions):
                print("  📈 Overall Market Sentiment: Bullish")
            elif len(dispositions) > len(acquisitions):
                print("  📉 Overall Market Sentiment: Bearish")
            else:
                print("  ➡️  Overall Market Sentiment: Neutral")

            # Most active companies
            company_activity = {}
            for trade in latest_trades:
                symbol = trade.get("symbol", "Unknown")
                company_activity[symbol] = company_activity.get(symbol, 0) + 1

            print("  \n🏢 Most Active Companies by Insider Trading:")
            top_companies = sorted(
                company_activity.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for symbol, count in top_companies:
                print(f"    {symbol}: {count} trades")

    except Exception as e:
        print(f"  ❌ Error in market-wide analysis: {e}")


async def main() -> None:
    """Main function demonstrating FMP Insider Trades functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Insider Trades Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await latest_insider_trades_examples(client)
            await search_insider_trades_examples(client)
            await search_by_reporting_name_examples(client)
            await transaction_types_examples(client)
            await insider_trade_statistics_examples(client)
            await acquisition_ownership_examples(client)
            await insider_analysis_examples(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
