#!/usr/bin/env python3
"""
Example script demonstrating FMP Forex category functionality

This script shows how to use the FMP client to access forex data including
currency pairs list, real-time quotes, historical price data, and intraday charts.
"""

import asyncio
import os

from aiofmp import FmpClient


async def forex_list_examples(client: FmpClient) -> None:
    """Demonstrate forex list functionality"""
    print("\n=== Forex List Examples ===")

    # Get list of all available forex currency pairs
    print("Fetching list of all available forex currency pairs...")
    forex_pairs = await client.forex.forex_list()
    print(f"Found {len(forex_pairs)} forex currency pairs")

    if forex_pairs:
        print("\nForex Currency Pairs Summary:")

        # Group by base currency
        base_currencies = {}
        for pair in forex_pairs:
            base_currency = pair.get("fromCurrency", "Unknown")
            if base_currency not in base_currencies:
                base_currencies[base_currency] = []
            base_currencies[base_currency].append(pair)

        # Show major currency pairs first
        major_currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]
        for currency in major_currencies:
            if currency in base_currencies:
                pairs = base_currencies[currency]
                print(f"\n  {currency} Pairs ({len(pairs)}):")
                for i, pair in enumerate(pairs[:5]):  # Show first 5 pairs
                    print(
                        f"    {i + 1}. {pair.get('fromName', 'N/A')} → {pair.get('toName', 'N/A')} ({pair.get('symbol', 'N/A')})"
                    )
                if len(pairs) > 5:
                    print(f"       ... and {len(pairs) - 5} more pairs")

        # Show some specific examples
        print("\nSample Forex Pairs:")
        for i, pair in enumerate(forex_pairs[:10]):
            print(
                f"  {i + 1:2d}. {pair.get('fromCurrency', 'N/A')}/{pair.get('toCurrency', 'N/A')} - {pair.get('fromName', 'N/A')} → {pair.get('toName', 'N/A')}"
            )


async def quote_examples(client: FmpClient) -> None:
    """Demonstrate forex quote functionality"""
    print("\n=== Forex Quote Examples ===")

    # Get quote for EUR/USD
    print("Fetching quote for EUR/USD...")
    eur_usd_quote = await client.forex.quote("EURUSD")
    print(f"Found {len(eur_usd_quote)} quote records for EUR/USD")

    if eur_usd_quote:
        print("\nEUR/USD Quote Summary:")
        quote = eur_usd_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: {quote.get('price', 0):.5f}")
        print(
            f"  Change: {quote.get('change', 0):+.5f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print(
            f"  Day Range: {quote.get('dayLow', 0):.5f} - {quote.get('dayHigh', 0):.5f}"
        )
        print(
            f"  Year Range: {quote.get('yearLow', 0):.5f} - {quote.get('yearHigh', 0):.5f}"
        )
        print(f"  Open: {quote.get('open', 0):.5f}")
        print(f"  Previous Close: {quote.get('previousClose', 0):.5f}")
        print(f"  50-Day Average: {quote.get('priceAvg50', 0):.5f}")
        print(f"  200-Day Average: {quote.get('priceAvg200', 0):.5f}")
        print(f"  Exchange: {quote.get('exchange', 'N/A')}")
        print()

    # Get quote for GBP/USD
    print("Fetching quote for GBP/USD...")
    gbp_usd_quote = await client.forex.quote("GBPUSD")
    print(f"Found {len(gbp_usd_quote)} quote records for GBP/USD")

    if gbp_usd_quote:
        print("\nGBP/USD Quote Summary:")
        quote = gbp_usd_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: {quote.get('price', 0):.5f}")
        print(
            f"  Change: {quote.get('change', 0):+.5f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print(
            f"  Day Range: {quote.get('dayLow', 0):.5f} - {quote.get('dayHigh', 0):.5f}"
        )
        print()

    # Get quote for USD/JPY
    print("Fetching quote for USD/JPY...")
    usd_jpy_quote = await client.forex.quote("USDJPY")
    print(f"Found {len(usd_jpy_quote)} quote records for USD/JPY")

    if usd_jpy_quote:
        print("\nUSD/JPY Quote Summary:")
        quote = usd_jpy_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: {quote.get('price', 0):.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,}")
        print()


async def quote_short_examples(client: FmpClient) -> None:
    """Demonstrate forex quote short functionality"""
    print("\n=== Forex Quote Short Examples ===")

    # Get short quotes for multiple forex pairs
    forex_pairs_to_quote = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

    for symbol in forex_pairs_to_quote:
        print(f"Fetching short quote for {symbol}...")
        quote = await client.forex.quote_short(symbol)

        if quote:
            print(
                f"  {symbol}: {quote[0].get('price', 0):.5f} ({quote[0].get('change', 0):+.5f}) - Vol: {quote[0].get('volume', 0):,}"
            )
        else:
            print(f"  {symbol}: No data available")

    print()


async def batch_quotes_examples(client: FmpClient) -> None:
    """Demonstrate batch quotes functionality"""
    print("\n=== Batch Quotes Examples ===")

    # Get batch quotes (short format)
    print("Fetching batch quotes (short format)...")
    batch_quotes_short = await client.forex.batch_quotes(short=True)
    print(f"Found {len(batch_quotes_short)} batch quotes in short format")

    if batch_quotes_short:
        print("\nSample Batch Quotes (Short Format):")
        for i, quote in enumerate(batch_quotes_short[:10]):  # Show first 10
            print(
                f"  {i + 1:2d}. {quote.get('symbol', 'N/A'):<10} - {quote.get('price', 0):<12.5f} ({quote.get('change', 0):+.5f})"
            )

    # Get batch quotes (full format)
    print("\nFetching batch quotes (full format)...")
    batch_quotes_full = await client.forex.batch_quotes(short=False)
    print(f"Found {len(batch_quotes_full)} batch quotes in full format")

    if batch_quotes_full:
        print("\nSample Batch Quotes (Full Format):")
        for i, quote in enumerate(batch_quotes_full[:5]):  # Show first 5
            print(f"  {i + 1}. {quote.get('symbol', 'N/A')}")
            print(f"     Price: {quote.get('price', 0):.5f}")
            print(f"     Change: {quote.get('change', 0):+.5f}")
            print(f"     Volume: {quote.get('volume', 0):,}")
            print()


async def historical_price_examples(client: FmpClient) -> None:
    """Demonstrate historical price functionality"""
    print("\n=== Historical Price Examples ===")

    # Get light historical prices for EUR/USD
    print("Fetching light historical prices for EUR/USD...")
    eur_usd_light = await client.forex.historical_price_light(
        "EURUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(eur_usd_light)} historical price records for EUR/USD in January 2025"
    )

    if eur_usd_light:
        print("\nEUR/USD Light Historical Prices (January 2025):")
        for i, record in enumerate(eur_usd_light[:5]):  # Show first 5 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: {record.get('price', 0):.5f}")
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get full historical prices for EUR/USD
    print("Fetching full historical prices for EUR/USD...")
    eur_usd_full = await client.forex.historical_price_full(
        "EURUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(eur_usd_full)} full historical price records for EUR/USD in January 2025"
    )

    if eur_usd_full:
        print("\nEUR/USD Full Historical Prices (January 2025):")
        for i, record in enumerate(eur_usd_full[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: {record.get('open', 0):.5f} / {record.get('high', 0):.5f} / {record.get('low', 0):.5f} / {record.get('close', 0):.5f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print(
                f"     Change: {record.get('change', 0):+.5f} ({record.get('changePercent', 0):+.2f}%)"
            )
            print(f"     VWAP: {record.get('vwap', 0):.5f}")
            print()

    # Get historical prices for GBP/USD
    print("Fetching historical prices for GBP/USD...")
    gbp_usd_prices = await client.forex.historical_price_light(
        "GBPUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(gbp_usd_prices)} historical price records for GBP/USD in January 2025"
    )

    if gbp_usd_prices:
        print("\nGBP/USD Historical Prices (January 2025):")
        for i, record in enumerate(gbp_usd_prices[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: {record.get('price', 0):.5f}")
            print(f"     Volume: {record.get('volume', 0):,}")
            print()


async def intraday_examples(client: FmpClient) -> None:
    """Demonstrate intraday chart functionality"""
    print("\n=== Intraday Chart Examples ===")

    # Get 1-minute intraday data for EUR/USD
    print("Fetching 1-minute intraday data for EUR/USD...")
    eur_usd_1min = await client.forex.intraday_1min(
        "EURUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(eur_usd_1min)} 1-minute records for EUR/USD on January 15, 2025")

    if eur_usd_1min:
        print("\nEUR/USD 1-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(eur_usd_1min[:5]):  # Show first 5 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: {record.get('open', 0):.5f} / {record.get('high', 0):.5f} / {record.get('low', 0):.5f} / {record.get('close', 0):.5f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get 5-minute intraday data for EUR/USD
    print("Fetching 5-minute intraday data for EUR/USD...")
    eur_usd_5min = await client.forex.intraday_5min(
        "EURUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(eur_usd_5min)} 5-minute records for EUR/USD on January 15, 2025")

    if eur_usd_5min:
        print("\nEUR/USD 5-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(eur_usd_5min[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: {record.get('open', 0):.5f} / {record.get('high', 0):.5f} / {record.get('low', 0):.5f} / {record.get('close', 0):.5f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()

    # Get 1-hour intraday data for EUR/USD
    print("Fetching 1-hour intraday data for EUR/USD...")
    eur_usd_1hour = await client.forex.intraday_1hour(
        "EURUSD", "2025-01-15", "2025-01-15"
    )
    print(f"Found {len(eur_usd_1hour)} 1-hour records for EUR/USD on January 15, 2025")

    if eur_usd_1hour:
        print("\nEUR/USD 1-Hour Intraday Data (January 15, 2025):")
        for i, record in enumerate(eur_usd_1hour[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: {record.get('open', 0):.5f} / {record.get('high', 0):.5f} / {record.get('low', 0):.5f} / {record.get('close', 0):.5f}"
            )
            print(f"     Volume: {record.get('volume', 0):,}")
            print()


async def forex_analysis_examples(client: FmpClient) -> None:
    """Demonstrate forex analysis functionality"""
    print("\n=== Forex Analysis Examples ===")

    # Analyze EUR/USD vs GBP/USD performance
    print("Analyzing EUR/USD vs GBP/USD performance...")

    # Get quotes for both currency pairs
    eur_usd_quote = await client.forex.quote("EURUSD")
    gbp_usd_quote = await client.forex.quote("GBPUSD")

    if eur_usd_quote and gbp_usd_quote:
        print("\nEUR/USD vs GBP/USD Comparison:")
        eur_usd = eur_usd_quote[0]
        gbp_usd = gbp_usd_quote[0]

        print("  EUR/USD:")
        print(f"    Price: {eur_usd.get('price', 0):.5f}")
        print(
            f"    Change: {eur_usd.get('change', 0):+.5f} ({eur_usd.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {eur_usd.get('volume', 0):,}")
        print(f"    50-Day Avg: {eur_usd.get('priceAvg50', 0):.5f}")
        print(f"    200-Day Avg: {eur_usd.get('priceAvg200', 0):.5f}")

        print("  GBP/USD:")
        print(f"    Price: {gbp_usd.get('price', 0):.5f}")
        print(
            f"    Change: {gbp_usd.get('change', 0):+.5f} ({gbp_usd.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {gbp_usd.get('volume', 0):,}")
        print(f"    50-Day Avg: {gbp_usd.get('priceAvg50', 0):.5f}")
        print(f"    200-Day Avg: {gbp_usd.get('priceAvg200', 0):.5f}")

        # Calculate correlation
        eur_change = eur_usd.get("changePercentage", 0)
        gbp_change = gbp_usd.get("changePercentage", 0)
        if eur_change > 0 and gbp_change > 0:
            print("    Correlation: Both pairs moving up")
        elif eur_change < 0 and gbp_change < 0:
            print("    Correlation: Both pairs moving down")
        else:
            print("    Correlation: Pairs moving in opposite directions")

    # Analyze USD crosses
    print("\nAnalyzing USD crosses...")

    # Get quotes for USD crosses
    usd_crosses = ["USDJPY", "USDCAD", "AUDUSD"]
    usd_cross_data = {}

    for symbol in usd_crosses:
        try:
            quote = await client.forex.quote(symbol)
            if quote:
                usd_cross_data[symbol] = quote[0]
        except Exception as e:
            print(f"  Error fetching {symbol}: {e}")

    if usd_cross_data:
        print("\nUSD Cross Performance Analysis:")
        for symbol, quote in usd_cross_data.items():
            print(f"  {symbol}:")
            print(f"    Price: {quote.get('price', 0):.5f}")
            print(
                f"    Change: {quote.get('change', 0):+.5f} ({quote.get('changePercentage', 0):+.2f}%)"
            )
            print(f"    Volume: {quote.get('volume', 0):,}")
            print()


async def forex_portfolio_analysis(client: FmpClient) -> None:
    """Demonstrate forex portfolio analysis functionality"""
    print("\n=== Forex Portfolio Analysis Examples ===")

    # Define a hypothetical forex portfolio
    portfolio = {
        "EURUSD": 0.40,  # 40% EUR/USD
        "GBPUSD": 0.25,  # 25% GBP/USD
        "USDJPY": 0.20,  # 20% USD/JPY
        "AUDUSD": 0.15,  # 15% AUD/USD
    }

    print(f"Analyzing forex portfolio: {portfolio}")

    total_change = 0
    total_volume = 0
    forex_data = {}

    for symbol, allocation in portfolio.items():
        print(f"\n--- Analyzing {symbol} ({allocation * 100:.0f}% allocation) ---")

        try:
            # Get quote for the currency pair
            quote = await client.forex.quote(symbol)
            if quote:
                quote = quote[0]
                price = quote.get("price", 0)
                change_pct = quote.get("changePercentage", 0)
                volume = quote.get("volume", 0)

                print(f"  Current Price: {price:.5f}")
                print(f"  Daily Change: {change_pct:+.2f}%")
                print(f"  Volume: {volume:,}")
                print(f"  50-Day Average: {quote.get('priceAvg50', 0):.5f}")
                print(f"  200-Day Average: {quote.get('priceAvg200', 0):.5f}")

                # Calculate weighted metrics
                total_change += change_pct * allocation
                total_volume += volume * allocation
                forex_data[symbol] = {
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
    if total_change > 0.5:
        print(f"  🟢 Strong positive performance: +{total_change:.2f}%")
    elif total_change > 0:
        print(f"  🟡 Moderate positive performance: +{total_change:.2f}%")
    elif total_change > -0.5:
        print(f"  🟡 Moderate negative performance: {total_change:.2f}%")
    else:
        print(f"  🔴 Strong negative performance: {total_change:.2f}%")

    # Risk assessment
    print("\nRisk Assessment:")
    high_volatility = [
        sym for sym, data in forex_data.items() if abs(data["change_pct"]) > 1
    ]
    if high_volatility:
        print(f"  ⚠️  High volatility pairs: {', '.join(high_volatility)}")

    # Currency exposure analysis
    if forex_data:
        print("\nCurrency Exposure Analysis:")

        # Calculate USD exposure (direct and indirect)
        usd_exposure = 0
        for symbol, data in forex_data.items():
            if symbol.endswith("USD"):  # Direct USD exposure
                usd_exposure += data["allocation"]
            elif symbol.startswith("USD"):  # Indirect USD exposure
                usd_exposure += data["allocation"]

        print(f"  USD Exposure: {usd_exposure * 100:.1f}%")

        # Check for diversification
        if len(portfolio) >= 4:
            print(f"  ✅ Good diversification with {len(portfolio)} currency pairs")
        else:
            print(
                f"  ⚠️  Limited diversification with only {len(portfolio)} currency pairs"
            )

        # Check for major vs minor currency exposure
        major_currencies = ["EUR", "GBP", "JPY", "USD"]
        major_exposure = sum(
            data["allocation"]
            for symbol, data in forex_data.items()
            if any(currency in symbol for currency in major_currencies)
        )

        if major_exposure > 0.8:
            print(f"  ✅ High major currency exposure: {major_exposure * 100:.1f}%")
        elif major_exposure > 0.5:
            print(f"  ⚠️  Moderate major currency exposure: {major_exposure * 100:.1f}%")
        else:
            print(f"  ⚠️  Low major currency exposure: {major_exposure * 100:.1f}%")


async def main() -> None:
    """Main function demonstrating FMP Forex functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Forex Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await forex_list_examples(client)
            await quote_examples(client)
            await quote_short_examples(client)
            await batch_quotes_examples(client)
            await historical_price_examples(client)
            await intraday_examples(client)
            await forex_analysis_examples(client)
            await forex_portfolio_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
