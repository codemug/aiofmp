#!/usr/bin/env python3
"""
Example script demonstrating FMP Commodity category functionality

This script shows how to use the FMP client to access commodity data including
commodities list, real-time quotes, historical price data, and intraday charts.
"""

import asyncio
import os

from aiofmp import FmpClient


async def commodities_list_examples(client: FmpClient) -> None:
    """Demonstrate commodities list functionality"""
    print("\n=== Commodities List Examples ===")

    # Get list of all available commodities
    print("Fetching list of all available commodities...")
    commodities = await client.commodity.commodities_list()
    print(f"Found {len(commodities)} commodities")

    if commodities:
        print("\nCommodities Summary:")

        # Group by currency
        currencies = {}
        for commodity in commodities:
            currency = commodity.get("currency", "Unknown")
            if currency not in currencies:
                currencies[currency] = []
            currencies[currency].append(commodity)

        for currency, comm_list in currencies.items():
            print(f"\n  {currency} Commodities ({len(comm_list)}):")
            for i, comm in enumerate(comm_list[:5]):  # Show first 5 per currency
                print(
                    f"    {i + 1}. {comm.get('name', 'N/A')} ({comm.get('symbol', 'N/A')})"
                )
                print(f"       Exchange: {comm.get('exchange', 'N/A')}")
                print(f"       Trade Month: {comm.get('tradeMonth', 'N/A')}")
            if len(comm_list) > 5:
                print(f"       ... and {len(comm_list) - 5} more")

        # Show some specific examples
        print("\nSample Commodities:")
        for i, commodity in enumerate(commodities[:10]):
            print(
                f"  {i + 1:2d}. {commodity.get('name', 'N/A'):<25} - {commodity.get('symbol', 'N/A'):<8} ({commodity.get('currency', 'N/A')})"
            )


async def quote_examples(client: FmpClient) -> None:
    """Demonstrate commodity quote functionality"""
    print("\n=== Commodity Quote Examples ===")

    # Get quote for Gold Futures
    print("Fetching quote for Gold Futures (GCUSD)...")
    gold_quote = await client.commodity.quote("GCUSD")
    print(f"Found {len(gold_quote)} quote records for Gold")

    if gold_quote:
        print("\nGold Futures Quote Summary:")
        quote = gold_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print(
            f"  Day Range: ${quote.get('dayLow', 0):,.2f} - ${quote.get('dayHigh', 0):,.2f}"
        )
        print(
            f"  Year Range: ${quote.get('yearLow', 0):,.2f} - ${quote.get('yearHigh', 0):,.2f}"
        )
        print(f"  Open: ${quote.get('open', 0):,.2f}")
        print(f"  Previous Close: ${quote.get('previousClose', 0):,.2f}")
        print(f"  50-Day Average: ${quote.get('priceAvg50', 0):,.2f}")
        print(f"  200-Day Average: ${quote.get('priceAvg200', 0):,.2f}")
        print(f"  Exchange: {quote.get('exchange', 'N/A')}")
        print()

    # Get quote for Silver Futures
    print("Fetching quote for Silver Futures (SIUSD)...")
    silver_quote = await client.commodity.quote("SIUSD")
    print(f"Found {len(silver_quote)} quote records for Silver")

    if silver_quote:
        print("\nSilver Futures Quote Summary:")
        quote = silver_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print(
            f"  Day Range: ${quote.get('dayLow', 0):,.2f} - ${quote.get('dayHigh', 0):,.2f}"
        )
        print()

    # Get quote for Crude Oil Futures
    print("Fetching quote for Crude Oil Futures (CLUSD)...")
    oil_quote = await client.commodity.quote("CLUSD")
    print(f"Found {len(oil_quote)} quote records for Crude Oil")

    if oil_quote:
        print("\nCrude Oil Futures Quote Summary:")
        quote = oil_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print()


async def quote_short_examples(client: FmpClient) -> None:
    """Demonstrate commodity quote short functionality"""
    print("\n=== Commodity Quote Short Examples ===")

    # Get short quotes for multiple commodities
    commodities_to_quote = ["GCUSD", "SIUSD", "CLUSD", "NGUSD", "HEUSX"]

    for symbol in commodities_to_quote:
        print(f"Fetching short quote for {symbol}...")
        quote = await client.commodity.quote_short(symbol)

        if quote:
            print(
                f"  {symbol}: ${quote[0].get('price', 0):,.2f} ({quote[0].get('change', 0):+.2f}) - Vol: {quote[0].get('volume', 0):,}"
            )
        else:
            print(f"  {symbol}: No data available")

    print()


async def historical_price_examples(client: FmpClient) -> None:
    """Demonstrate historical price functionality"""
    print("\n=== Historical Price Examples ===")

    # Get light historical prices for Gold
    print("Fetching light historical prices for Gold (GCUSD)...")
    gold_light = await client.commodity.historical_price_light(
        "GCUSD", "2025-01-01", "2025-01-31"
    )
    print(f"Found {len(gold_light)} historical price records for Gold in January 2025")

    if gold_light:
        print("\nGold Light Historical Prices (January 2025):")
        for i, record in enumerate(gold_light[:5]):  # Show first 5 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: ${record.get('price', 0):,.2f}")
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get full historical prices for Gold
    print("Fetching full historical prices for Gold (GCUSD)...")
    gold_full = await client.commodity.historical_price_full(
        "GCUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(gold_full)} full historical price records for Gold in January 2025"
    )

    if gold_full:
        print("\nGold Full Historical Prices (January 2025):")
        for i, record in enumerate(gold_full[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print(
                f"     Change: {record.get('change', 0):+.2f} ({record.get('changePercent', 0):+.2f}%)"
            )
            print(f"     VWAP: ${record.get('vwap', 0):,.2f}")
            print()

    # Get historical prices for Silver
    print("Fetching historical prices for Silver (SIUSD)...")
    silver_prices = await client.commodity.historical_price_light(
        "SIUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(silver_prices)} historical price records for Silver in January 2025"
    )

    if silver_prices:
        print("\nSilver Historical Prices (January 2025):")
        for i, record in enumerate(silver_prices[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: ${record.get('price', 0):,.2f}")
            print(f"     Volume: {record.get('volume', 0):,}")
            print()


async def intraday_examples(client: FmpClient) -> None:
    """Demonstrate intraday chart functionality"""
    print("\n=== Intraday Chart Examples ===")

    # Get 1-minute intraday data for Gold
    print("Fetching 1-minute intraday data for Gold (GCUSD)...")
    gold_1min = await client.commodity.intraday_1min(
        "GCUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(gold_1min)} 1-minute records for Gold on January 15, 2025")

    if gold_1min:
        print("\nGold 1-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(gold_1min[:5]):  # Show first 5 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get 5-minute intraday data for Gold
    print("Fetching 5-minute intraday data for Gold (GCUSD)...")
    gold_5min = await client.commodity.intraday_5min(
        "GCUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(gold_5min)} 5-minute records for Gold on January 15, 2025")

    if gold_5min:
        print("\nGold 5-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(gold_5min[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get 1-hour intraday data for Gold
    print("Fetching 1-hour intraday data for Gold (GCUSD)...")
    gold_1hour = await client.commodity.intraday_1hour(
        "GCUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(gold_1hour)} 1-hour records for Gold on January 15, 2025")

    if gold_1hour:
        print("\nGold 1-Hour Intraday Data (January 15, 2025):")
        for i, record in enumerate(gold_1hour[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()


async def commodity_analysis_examples(client: FmpClient) -> None:
    """Demonstrate commodity analysis functionality"""
    print("\n=== Commodity Analysis Examples ===")

    # Analyze Gold vs Silver performance
    print("Analyzing Gold vs Silver performance...")

    # Get quotes for both metals
    gold_quote = await client.commodity.quote("GCUSD")
    silver_quote = await client.commodity.quote("SIUSD")

    if gold_quote and silver_quote:
        print("\nGold vs Silver Comparison:")
        gold = gold_quote[0]
        silver = silver_quote[0]

        print("  Gold (GCUSD):")
        print(f"    Price: ${gold.get('price', 0):,.2f}")
        print(
            f"    Change: {gold.get('change', 0):+.2f} ({gold.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {gold.get('volume', 0):,}")
        print(f"    50-Day Avg: ${gold.get('priceAvg50', 0):,.2f}")
        print(f"    200-Day Avg: ${gold.get('priceAvg200', 0):,.2f}")

        print("  Silver (SIUSD):")
        print(f"    Price: ${silver.get('price', 0):,.2f}")
        print(
            f"    Change: {silver.get('change', 0):+.2f} ({silver.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {silver.get('volume', 0):,}")
        print(f"    50-Day Avg: ${silver.get('priceAvg50', 0):,.2f}")
        print(f"    200-Day Avg: ${silver.get('priceAvg200', 0):,.2f}")

        # Calculate gold-silver ratio
        gold_price = gold.get("price", 0)
        silver_price = silver.get("price", 0)
        if gold_price > 0 and silver_price > 0:
            ratio = gold_price / silver_price
            print(f"\n  Gold-Silver Ratio: {ratio:.2f}")
            if ratio > 80:
                print("    Interpretation: Gold is expensive relative to silver")
            elif ratio < 40:
                print("    Interpretation: Silver is expensive relative to gold")
            else:
                print("    Interpretation: Gold-silver ratio is in normal range")

    # Analyze energy commodities
    print("\nAnalyzing energy commodities...")

    # Get quotes for energy commodities
    oil_quote = await client.commodity.quote("CLUSD")
    gas_quote = await client.commodity.quote("NGUSD")

    if oil_quote and gas_quote:
        print("\nEnergy Commodities Analysis:")
        oil = oil_quote[0]
        gas = gas_quote[0]

        print("  Crude Oil (CLUSD):")
        print(f"    Price: ${oil.get('price', 0):,.2f}")
        print(
            f"    Change: {oil.get('change', 0):+.2f} ({oil.get('changePercentage', 0):+.2f}%)"
        )
        print(
            f"    Day Range: ${oil.get('dayLow', 0):,.2f} - ${oil.get('dayHigh', 0):,.2f}"
        )

        print("  Natural Gas (NGUSD):")
        print(f"    Price: ${gas.get('price', 0):,.2f}")
        print(
            f"    Change: {gas.get('change', 0):+.2f} ({gas.get('changePercentage', 0):+.2f}%)"
        )
        print(
            f"    Day Range: ${gas.get('dayLow', 0):,.2f} - ${gas.get('dayHigh', 0):,.2f}"
        )

        # Check for correlation
        oil_change = oil.get("changePercentage", 0)
        gas_change = gas.get("changePercentage", 0)
        if oil_change > 0 and gas_change > 0:
            print("    Correlation: Both energy commodities moving up")
        elif oil_change < 0 and gas_change < 0:
            print("    Correlation: Both energy commodities moving down")
        else:
            print("    Correlation: Energy commodities moving in opposite directions")


async def commodity_portfolio_analysis(client: FmpClient) -> None:
    """Demonstrate commodity portfolio analysis functionality"""
    print("\n=== Commodity Portfolio Analysis Examples ===")

    # Define a hypothetical commodity portfolio
    portfolio = {
        "GCUSD": 0.40,  # 40% Gold
        "SIUSD": 0.25,  # 25% Silver
        "CLUSD": 0.20,  # 20% Crude Oil
        "NGUSD": 0.15,  # 15% Natural Gas
    }

    print(f"Analyzing commodity portfolio: {portfolio}")

    total_change = 0
    total_volume = 0
    commodity_data = {}

    for symbol, allocation in portfolio.items():
        print(f"\n--- Analyzing {symbol} ({allocation * 100:.0f}% allocation) ---")

        try:
            # Get quote for the commodity
            quote = await client.commodity.quote(symbol)
            if quote:
                quote = quote[0]
                price = quote.get("price", 0)
                change_pct = quote.get("changePercentage", 0)
                volume = quote.get("volume", 0)

                print(f"  Current Price: ${price:,.2f}")
                print(f"  Daily Change: {change_pct:+.2f}%")
                print(f"  Volume: {volume:,}")
                print(f"  50-Day Average: ${quote.get('priceAvg50', 0):,.2f}")
                print(f"  200-Day Average: ${quote.get('priceAvg200', 0):,.2f}")

                # Calculate weighted metrics
                total_change += change_pct * allocation
                total_volume += volume * allocation
                commodity_data[symbol] = {
                    "price": price,
                    "change_pct": change_pct,
                    "allocation": allocation,
                }

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")

    # Portfolio summary
    print("\n=== Portfolio Summary ===")
    print(f"Total Weighted Daily Change: {total_change:+.2f}%")
    print(f"Total Weighted Volume: {total_volume:,.0f}")

    # Performance analysis
    print("\nPerformance Analysis:")
    if total_change > 1:
        print(f"  🟢 Strong positive performance: +{total_change:.2f}%")
    elif total_change > 0:
        print(f"  🟡 Moderate positive performance: +{total_change:.2f}%")
    elif total_change > -1:
        print(f"  🟡 Moderate negative performance: {total_change:.2f}%")
    else:
        print(f"  🔴 Strong negative performance: {total_change:.2f}%")

    # Risk assessment
    print("\nRisk Assessment:")
    high_volatility = [
        sym for sym, data in commodity_data.items() if abs(data["change_pct"]) > 2
    ]
    if high_volatility:
        print(f"  ⚠️  High volatility commodities: {', '.join(high_volatility)}")

    # Diversification check
    if len(portfolio) >= 4:
        print(f"  ✅ Good diversification with {len(portfolio)} commodities")
    else:
        print(f"  ⚠️  Limited diversification with only {len(portfolio)} commodities")


async def main() -> None:
    """Main function demonstrating FMP Commodity functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Commodity Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await commodities_list_examples(client)
            await quote_examples(client)
            await quote_short_examples(client)
            await historical_price_examples(client)
            await intraday_examples(client)
            await commodity_analysis_examples(client)
            await commodity_portfolio_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
