#!/usr/bin/env python3
"""
Example script demonstrating FMP Analyst category functionality

This script shows how to use the FMP client to access analyst data including
financial estimates, ratings, price targets, stock grades, and related news.
"""

import asyncio
import os

from aiofmp import FmpClient


async def financial_estimates_example(client: FmpClient) -> None:
    """Demonstrate financial estimates functionality"""
    print("\n=== Financial Estimates Examples ===")

    # Get annual financial estimates for Apple
    print("Fetching annual financial estimates for AAPL...")
    annual_estimates = await client.analyst.financial_estimates(
        "AAPL", "annual", limit=5
    )
    print(f"Found {len(annual_estimates)} annual estimates")

    if annual_estimates:
        print("\nLatest annual estimates:")
        for i, estimate in enumerate(annual_estimates[:3]):
            print(f"  {i + 1}. Date: {estimate.get('date', 'N/A')}")
            revenue_avg = estimate.get("revenueAvg", 0)
            if revenue_avg:
                revenue_billions = revenue_avg / 1_000_000_000
                print(f"     Revenue (Avg): ${revenue_billions:.1f}B")

            eps_avg = estimate.get("epsAvg", 0)
            if eps_avg:
                print(f"     EPS (Avg): ${eps_avg:.2f}")

            num_analysts = estimate.get("numAnalystsRevenue", 0)
            if num_analysts:
                print(f"     Number of Analysts: {num_analysts}")
            print()

    # Get quarterly estimates
    print("Fetching quarterly financial estimates for AAPL...")
    quarterly_estimates = await client.analyst.financial_estimates(
        "AAPL", "quarter", limit=3
    )
    print(f"Found {len(quarterly_estimates)} quarterly estimates")

    if quarterly_estimates:
        print("\nLatest quarterly estimates:")
        for estimate in quarterly_estimates[:2]:
            print(f"  Date: {estimate.get('date', 'N/A')}")
            revenue_avg = estimate.get("revenueAvg", 0)
            if revenue_avg:
                revenue_billions = revenue_avg / 1_000_000_000
                print(f"    Revenue (Avg): ${revenue_billions:.1f}B")
            print()


async def ratings_example(client: FmpClient) -> None:
    """Demonstrate ratings functionality"""
    print("\n=== Ratings Examples ===")

    # Get current ratings snapshot
    print("Fetching current ratings snapshot for AAPL...")
    ratings = await client.analyst.ratings_snapshot("AAPL")
    print(f"Found {len(ratings)} ratings snapshots")

    if ratings:
        rating = ratings[0]
        print(f"\nCurrent Rating: {rating.get('rating', 'N/A')}")
        print(f"Overall Score: {rating.get('overallScore', 'N/A')}/5")
        print(
            f"Discounted Cash Flow Score: {rating.get('discountedCashFlowScore', 'N/A')}/5"
        )
        print(f"Return on Equity Score: {rating.get('returnOnEquityScore', 'N/A')}/5")
        print(f"Return on Assets Score: {rating.get('returnOnAssetsScore', 'N/A')}/5")
        print(f"Debt to Equity Score: {rating.get('debtToEquityScore', 'N/A')}/5")
        print(f"Price to Earnings Score: {rating.get('priceToEarningsScore', 'N/A')}/5")
        print(f"Price to Book Score: {rating.get('priceToBookScore', 'N/A')}/5")

    # Get historical ratings
    print("\nFetching historical ratings for AAPL...")
    historical_ratings = await client.analyst.historical_ratings("AAPL", limit=5)
    print(f"Found {len(historical_ratings)} historical ratings")

    if historical_ratings:
        print("\nHistorical ratings:")
        for rating in historical_ratings[:3]:
            print(f"  Date: {rating.get('date', 'N/A')}")
            print(f"    Rating: {rating.get('rating', 'N/A')}")
            print(f"    Overall Score: {rating.get('overallScore', 'N/A')}/5")
            print()


async def price_targets_example(client: FmpClient) -> None:
    """Demonstrate price targets functionality"""
    print("\n=== Price Targets Examples ===")

    # Get price target summary
    print("Fetching price target summary for AAPL...")
    price_summary = await client.analyst.price_target_summary("AAPL")
    print(f"Found {len(price_summary)} price target summaries")

    if price_summary:
        summary = price_summary[0]
        print("\nPrice Target Summary:")
        print(
            f"  Last Month: {summary.get('lastMonthCount', 0)} analysts, "
            f"Avg: ${summary.get('lastMonthAvgPriceTarget', 0):.2f}"
        )
        print(
            f"  Last Quarter: {summary.get('lastQuarterCount', 0)} analysts, "
            f"Avg: ${summary.get('lastQuarterAvgPriceTarget', 0):.2f}"
        )
        print(
            f"  Last Year: {summary.get('lastYearCount', 0)} analysts, "
            f"Avg: ${summary.get('lastYearAvgPriceTarget', 0):.2f}"
        )
        print(
            f"  All Time: {summary.get('allTimeCount', 0)} analysts, "
            f"Avg: ${summary.get('allTimeAvgPriceTarget', 0):.2f}"
        )

        publishers = summary.get("publishers", "[]")
        if publishers and publishers != "[]":
            print(f"  Publishers: {publishers}")

    # Get price target consensus
    print("\nFetching price target consensus for AAPL...")
    consensus = await client.analyst.price_target_consensus("AAPL")
    print(f"Found {len(consensus)} consensus data points")

    if consensus:
        consensus_data = consensus[0]
        print("\nPrice Target Consensus:")
        print(f"  High: ${consensus_data.get('targetHigh', 0):.2f}")
        print(f"  Low: ${consensus_data.get('targetLow', 0):.2f}")
        print(f"  Consensus: ${consensus_data.get('targetConsensus', 0):.2f}")
        print(f"  Median: ${consensus_data.get('targetMedian', 0):.2f}")

    # Get price target news
    print("\nFetching price target news for AAPL...")
    price_news = await client.analyst.price_target_news("AAPL", limit=3)
    print(f"Found {len(price_news)} price target news articles")

    if price_news:
        print("\nRecent price target news:")
        for i, news in enumerate(price_news[:3]):
            print(f"  {i + 1}. {news.get('newsTitle', 'N/A')}")
            print(
                f"     Analyst: {news.get('analystName', 'N/A')} ({news.get('analystCompany', 'N/A')})"
            )
            print(f"     Price Target: ${news.get('priceTarget', 0):.2f}")
            print(f"     Publisher: {news.get('newsPublisher', 'N/A')}")
            print(f"     Date: {news.get('publishedDate', 'N/A')}")
            print()


async def stock_grades_example(client: FmpClient) -> None:
    """Demonstrate stock grades functionality"""
    print("\n=== Stock Grades Examples ===")

    # Get current stock grades
    print("Fetching current stock grades for AAPL...")
    grades = await client.analyst.stock_grades("AAPL")
    print(f"Found {len(grades)} stock grades")

    if grades:
        print("\nRecent stock grades:")
        for i, grade in enumerate(grades[:3]):
            print(f"  {i + 1}. Date: {grade.get('date', 'N/A')}")
            print(f"     Company: {grade.get('gradingCompany', 'N/A')}")
            print(f"     Previous Grade: {grade.get('previousGrade', 'N/A')}")
            print(f"     New Grade: {grade.get('newGrade', 'N/A')}")
            print(f"     Action: {grade.get('action', 'N/A')}")
            print()

    # Get historical stock grades
    print("Fetching historical stock grades for AAPL...")
    historical_grades = await client.analyst.historical_stock_grades("AAPL", limit=5)
    print(f"Found {len(historical_grades)} historical grade records")

    if historical_grades:
        print("\nHistorical analyst ratings breakdown:")
        for grade in historical_grades[:3]:
            print(f"  Date: {grade.get('date', 'N/A')}")
            print(f"    Buy: {grade.get('analystRatingsBuy', 0)}")
            print(f"    Hold: {grade.get('analystRatingsHold', 0)}")
            print(f"    Sell: {grade.get('analystRatingsSell', 0)}")
            print(f"    Strong Sell: {grade.get('analystRatingsStrongSell', 0)}")
            print()

    # Get stock grades summary
    print("Fetching stock grades summary for AAPL...")
    grades_summary = await client.analyst.stock_grades_summary("AAPL")
    print(f"Found {len(grades_summary)} grade summaries")

    if grades_summary:
        summary = grades_summary[0]
        print("\nAnalyst Consensus Summary:")
        print(f"  Strong Buy: {summary.get('strongBuy', 0)}")
        print(f"  Buy: {summary.get('buy', 0)}")
        print(f"  Hold: {summary.get('hold', 0)}")
        print(f"  Sell: {summary.get('sell', 0)}")
        print(f"  Strong Sell: {summary.get('strongSell', 0)}")
        print(f"  Consensus: {summary.get('consensus', 'N/A')}")

        total_ratings = (
            summary.get("strongBuy", 0)
            + summary.get("buy", 0)
            + summary.get("hold", 0)
            + summary.get("sell", 0)
            + summary.get("strongSell", 0)
        )
        if total_ratings > 0:
            buy_percentage = (
                (summary.get("strongBuy", 0) + summary.get("buy", 0)) / total_ratings
            ) * 100
            print(f"  Buy Rating Percentage: {buy_percentage:.1f}%")


async def latest_news_example(client: FmpClient) -> None:
    """Demonstrate latest news functionality"""
    print("\n=== Latest News Examples ===")

    # Get latest price target news
    print("Fetching latest price target news...")
    latest_price_news = await client.analyst.price_target_latest_news(limit=5)
    print(f"Found {len(latest_price_news)} latest price target news articles")

    if latest_price_news:
        print("\nLatest price target news:")
        for i, news in enumerate(latest_price_news[:3]):
            print(
                f"  {i + 1}. {news.get('symbol', 'N/A')}: {news.get('newsTitle', 'N/A')}"
            )
            print(
                f"     Analyst: {news.get('analystName', 'N/A')} ({news.get('analystCompany', 'N/A')})"
            )
            print(f"     Price Target: ${news.get('priceTarget', 0):.2f}")
            print(f"     Publisher: {news.get('newsPublisher', 'N/A')}")
            print(f"     Date: {news.get('publishedDate', 'N/A')}")
            print()

    # Get latest grade change news
    print("Fetching latest grade change news...")
    latest_grade_news = await client.analyst.stock_grade_latest_news(limit=5)
    print(f"Found {len(latest_grade_news)} latest grade change news articles")

    if latest_grade_news:
        print("\nLatest grade change news:")
        for i, news in enumerate(latest_grade_news[:3]):
            print(
                f"  {i + 1}. {news.get('symbol', 'N/A')}: {news.get('newsTitle', 'N/A')}"
            )
            print(f"     New Grade: {news.get('newGrade', 'N/A')}")
            print(f"     Previous Grade: {news.get('previousGrade', 'N/A')}")
            print(f"     Company: {news.get('gradingCompany', 'N/A')}")
            print(f"     Publisher: {news.get('newsPublisher', 'N/A')}")
            print(f"     Date: {news.get('publishedDate', 'N/A')}")
            print()


async def multi_symbol_analysis_example(client: FmpClient) -> None:
    """Demonstrate analyzing multiple symbols"""
    print("\n=== Multi-Symbol Analysis Examples ===")

    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            # Get ratings snapshot
            ratings = await client.analyst.ratings_snapshot(symbol)
            if ratings:
                rating = ratings[0]
                print(f"  Rating: {rating.get('rating', 'N/A')}")
                print(f"  Overall Score: {rating.get('overallScore', 'N/A')}/5")

            # Get price target consensus
            consensus = await client.analyst.price_target_consensus(symbol)
            if consensus:
                consensus_data = consensus[0]
                print(
                    f"  Price Target Consensus: ${consensus_data.get('targetConsensus', 0):.2f}"
                )
                print(
                    f"  Price Target Range: ${consensus_data.get('targetLow', 0):.2f} - ${consensus_data.get('targetHigh', 0):.2f}"
                )

            # Get grades summary
            grades_summary = await client.analyst.stock_grades_summary(symbol)
            if grades_summary:
                summary = grades_summary[0]
                print(f"  Analyst Consensus: {summary.get('consensus', 'N/A')}")
                total_ratings = (
                    summary.get("strongBuy", 0)
                    + summary.get("buy", 0)
                    + summary.get("hold", 0)
                    + summary.get("sell", 0)
                    + summary.get("strongSell", 0)
                )
                print(f"  Total Analyst Ratings: {total_ratings}")

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")


async def main() -> None:
    """Main function demonstrating FMP Analyst functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Analyst Category Example")
    print("=" * 50)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await financial_estimates_example(client)
            await ratings_example(client)
            await price_targets_example(client)
            await stock_grades_example(client)
            await latest_news_example(client)
            await multi_symbol_analysis_example(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
