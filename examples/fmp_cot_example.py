#!/usr/bin/env python3
"""
Example script demonstrating FMP Commitment of Traders (COT) category functionality

This script shows how to use the FMP client to access COT data including
comprehensive COT reports, market sentiment analysis, and available COT symbols.
"""

import asyncio
import os

from aiofmp import FmpClient


async def cot_report_examples(client: FmpClient) -> None:
    """Demonstrate COT report functionality"""
    print("\n=== COT Report Examples ===")

    # Get COT report for Coffee
    print("Fetching COT report for Coffee (KC)...")
    cot_report = await client.cot.cot_report("KC", "2024-01-01", "2024-03-01")
    print(f"Found {len(cot_report)} COT report records")

    if cot_report:
        print("\nCOT Report Summary:")
        for i, record in enumerate(cot_report[:3]):
            print(
                f"  {i + 1}. {record.get('name', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Sector: {record.get('sector', 'N/A')}")
            print(f"     Exchange: {record.get('marketAndExchangeNames', 'N/A')}")
            print(f"     Open Interest (All): {record.get('openInterestAll', 0):,}")
            print(
                f"     Non-Commercial Long: {record.get('noncommPositionsLongAll', 0):,}"
            )
            print(
                f"     Non-Commercial Short: {record.get('noncommPositionsShortAll', 0):,}"
            )
            print(f"     Commercial Long: {record.get('commPositionsLongAll', 0):,}")
            print(f"     Commercial Short: {record.get('commPositionsShortAll', 0):,}")
            print(
                f"     Total Reportable Long: {record.get('totReptPositionsLongAll', 0):,}"
            )
            print(
                f"     Total Reportable Short: {record.get('totReptPositionsShortAll', 0):,}"
            )
            print()

    # Get COT report for Natural Gas
    print("Fetching COT report for Natural Gas (NG)...")
    ng_cot = await client.cot.cot_report("NG", "2024-01-01", "2024-03-01")
    print(f"Found {len(ng_cot)} Natural Gas COT records")

    if ng_cot:
        print("\nNatural Gas COT Summary:")
        for i, record in enumerate(ng_cot[:2]):
            print(
                f"  {i + 1}. {record.get('name', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Open Interest: {record.get('openInterestAll', 0):,}")
            print("     Non-Commercial Positions:")
            print(f"       Long: {record.get('noncommPositionsLongAll', 0):,}")
            print(f"       Short: {record.get('noncommPositionsShortAll', 0):,}")
            print(f"       Spread: {record.get('noncommPositionsSpreadAll', 0):,}")
            print("     Commercial Positions:")
            print(f"       Long: {record.get('commPositionsLongAll', 0):,}")
            print(f"       Short: {record.get('commPositionsShortAll', 0):,}")
            print()


async def cot_analysis_examples(client: FmpClient) -> None:
    """Demonstrate COT analysis functionality"""
    print("\n=== COT Analysis Examples ===")

    # Get COT analysis for British Pound
    print("Fetching COT analysis for British Pound (B6)...")
    cot_analysis = await client.cot.cot_analysis("B6", "2024-01-01", "2024-03-01")
    print(f"Found {len(cot_analysis)} COT analysis records")

    if cot_analysis:
        print("\nCOT Analysis Summary:")
        for i, record in enumerate(cot_analysis[:3]):
            print(
                f"  {i + 1}. {record.get('name', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Sector: {record.get('sector', 'N/A')}")
            print(f"     Exchange: {record.get('exchange', 'N/A')}")
            print(
                f"     Current Market Situation: {record.get('marketSituation', 'N/A')}"
            )
            print(
                f"     Current Long: {record.get('currentLongMarketSituation', 0):.2f}%"
            )
            print(
                f"     Current Short: {record.get('currentShortMarketSituation', 0):.2f}%"
            )
            print(
                f"     Previous Market Situation: {record.get('previousMarketSituation', 'N/A')}"
            )
            print(
                f"     Previous Long: {record.get('previousLongMarketSituation', 0):.2f}%"
            )
            print(
                f"     Previous Short: {record.get('previousShortMarketSituation', 0):.2f}%"
            )
            print(f"     Net Position: {record.get('netPostion', 0):,}")
            print(
                f"     Previous Net Position: {record.get('previousNetPosition', 0):,}"
            )
            print(
                f"     Change in Net Position: {record.get('changeInNetPosition', 0):.1f}%"
            )
            print(f"     Market Sentiment: {record.get('marketSentiment', 'N/A')}")
            print(f"     Reversal Trend: {record.get('reversalTrend', 'N/A')}")
            print()

    # Get COT analysis for Gold
    print("Fetching COT analysis for Gold (GC)...")
    gc_analysis = await client.cot.cot_analysis("GC", "2024-01-01", "2024-03-01")
    print(f"Found {len(gc_analysis)} Gold COT analysis records")

    if gc_analysis:
        print("\nGold COT Analysis Summary:")
        for i, record in enumerate(gc_analysis[:2]):
            print(
                f"  {i + 1}. {record.get('name', 'N/A')} ({record.get('symbol', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Market Situation: {record.get('marketSituation', 'N/A')}")
            print(f"     Market Sentiment: {record.get('marketSentiment', 'N/A')}")
            print(
                f"     Long vs Short Ratio: {record.get('currentLongMarketSituation', 0):.2f}% / {record.get('currentShortMarketSituation', 0):.2f}%"
            )
            print()


async def cot_list_examples(client: FmpClient) -> None:
    """Demonstrate COT list functionality"""
    print("\n=== COT List Examples ===")

    # Get list of available COT symbols
    print("Fetching list of available COT symbols...")
    cot_symbols = await client.cot.cot_list()
    print(f"Found {len(cot_symbols)} available COT symbols")

    if cot_symbols:
        print("\nAvailable COT Symbols:")

        # Group by sector if available
        sectors = {}
        for symbol in cot_symbols:
            sector = symbol.get("sector", "UNKNOWN")
            if sector not in sectors:
                sectors[sector] = []
            sectors[sector].append(symbol)

        for sector, symbols in sectors.items():
            print(f"\n  {sector} Sector:")
            for i, symbol in enumerate(symbols[:10]):  # Limit to first 10 per sector
                print(
                    f"    {i + 1}. {symbol.get('name', 'N/A')} ({symbol.get('symbol', 'N/A')})"
                )
            if len(symbols) > 10:
                print(f"    ... and {len(symbols) - 10} more")

        # Show some specific examples
        print("\nSample COT Symbols:")
        for i, symbol in enumerate(cot_symbols[:15]):
            print(
                f"  {i + 1:2d}. {symbol.get('symbol', 'N/A'):<6} - {symbol.get('name', 'N/A')}"
            )


async def cot_market_sentiment_analysis(client: FmpClient) -> None:
    """Demonstrate COT market sentiment analysis"""
    print("\n=== COT Market Sentiment Analysis ===")

    # Analyze multiple commodities for market sentiment
    commodities = [
        "KC",
        "NG",
        "B6",
        "GC",
        "SI",
    ]  # Coffee, Natural Gas, British Pound, Gold, Silver

    for commodity in commodities:
        print(f"\n--- Analyzing {commodity} ---")

        try:
            # Get COT analysis
            analysis = await client.cot.cot_analysis(
                commodity, "2024-01-01", "2024-03-01"
            )

            if analysis:
                latest = analysis[0]
                print(f"  Market Situation: {latest.get('marketSituation', 'N/A')}")
                print(f"  Market Sentiment: {latest.get('marketSentiment', 'N/A')}")
                print(
                    f"  Long Position: {latest.get('currentLongMarketSituation', 0):.2f}%"
                )
                print(
                    f"  Short Position: {latest.get('currentShortMarketSituation', 0):.2f}%"
                )
                print(f"  Reversal Trend: {latest.get('reversalTrend', 'N/A')}")

                # Determine sentiment strength
                long_pct = latest.get("currentLongMarketSituation", 50)
                if long_pct > 60:
                    sentiment = "Strongly Bullish"
                elif long_pct > 55:
                    sentiment = "Moderately Bullish"
                elif long_pct < 40:
                    sentiment = "Strongly Bearish"
                elif long_pct < 45:
                    sentiment = "Moderately Bearish"
                else:
                    sentiment = "Neutral"

                print(f"  Sentiment Strength: {sentiment}")
            else:
                print("  No analysis data available")

        except Exception as e:
            print(f"  Error analyzing {commodity}: {e}")


async def cot_position_analysis(client: FmpClient) -> None:
    """Demonstrate COT position analysis"""
    print("\n=== COT Position Analysis ===")

    # Analyze positions for a specific commodity
    commodity = "KC"  # Coffee

    print(f"Analyzing positions for {commodity} (Coffee)...")

    try:
        # Get COT report
        report = await client.cot.cot_report(commodity, "2024-01-01", "2024-03-01")

        if report:
            latest = report[0]
            print(f"\nPosition Analysis for {latest.get('name', 'N/A')}:")
            print(f"  Date: {latest.get('date', 'N/A')}")
            print(f"  Total Open Interest: {latest.get('openInterestAll', 0):,}")

            # Non-commercial positions
            noncomm_long = latest.get("noncommPositionsLongAll", 0)
            noncomm_short = latest.get("noncommPositionsShortAll", 0)
            noncomm_spread = latest.get("noncommPositionsSpreadAll", 0)

            print("\n  Non-Commercial Positions:")
            print(
                f"    Long: {noncomm_long:,} ({noncomm_long / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )
            print(
                f"    Short: {noncomm_short:,} ({noncomm_short / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )
            print(
                f"    Spread: {noncomm_spread:,} ({noncomm_spread / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )

            # Commercial positions
            comm_long = latest.get("commPositionsLongAll", 0)
            comm_short = latest.get("commPositionsShortAll", 0)

            print("\n  Commercial Positions:")
            print(
                f"    Long: {comm_long:,} ({comm_long / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )
            print(
                f"    Short: {comm_short:,} ({comm_short / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )

            # Total reportable positions
            total_long = latest.get("totReptPositionsLongAll", 0)
            total_short = latest.get("totReptPositionsShortAll", 0)

            print("\n  Total Reportable Positions:")
            print(
                f"    Long: {total_long:,} ({total_long / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )
            print(
                f"    Short: {total_short:,} ({total_short / latest.get('openInterestAll', 1) * 100:.1f}%)"
            )

            # Position changes
            print("\n  Position Changes:")
            print(
                f"    Change in Open Interest: {latest.get('changeInOpenInterestAll', 0):+,}"
            )
            print(
                f"    Change in Non-Commercial Long: {latest.get('changeInNoncommLongAll', 0):+,}"
            )
            print(
                f"    Change in Non-Commercial Short: {latest.get('changeInNoncommShortAll', 0):+,}"
            )
            print(
                f"    Change in Commercial Long: {latest.get('changeInCommLongAll', 0):+,}"
            )
            print(
                f"    Change in Commercial Short: {latest.get('changeInCommShortAll', 0):+,}"
            )

            # Trader counts
            print("\n  Trader Counts:")
            print(f"    Total Traders: {latest.get('tradersTotAll', 0)}")
            print(
                f"    Non-Commercial Traders: {latest.get('tradersNoncommLongAll', 0)} long, {latest.get('tradersNoncommShortAll', 0)} short"
            )
            print(
                f"    Commercial Traders: {latest.get('tradersCommLongAll', 0)} long, {latest.get('tradersCommShortAll', 0)} short"
            )

        else:
            print(f"No position data available for {commodity}")

    except Exception as e:
        print(f"Error analyzing positions for {commodity}: {e}")


async def main() -> None:
    """Main function demonstrating FMP COT functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Commitment of Traders (COT) Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await cot_list_examples(client)
            await cot_report_examples(client)
            await cot_analysis_examples(client)
            await cot_market_sentiment_analysis(client)
            await cot_position_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
