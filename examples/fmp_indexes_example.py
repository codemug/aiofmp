#!/usr/bin/env python3
"""
Example script demonstrating FMP Indexes category functionality

This script shows how to use the FMP client to access stock market index data including
index lists, real-time quotes, historical data, and intraday charts for various time intervals.
"""

import asyncio
import os
from datetime import date, timedelta

from aiofmp import FmpClient


async def index_list_examples(client: FmpClient) -> None:
    """Demonstrate index list functionality"""
    print("\n=== Stock Market Indexes List Examples ===")

    # Get comprehensive list of stock market indexes
    print("Fetching comprehensive list of stock market indexes...")
    all_indexes = await client.indexes.index_list()
    print(f"Found {len(all_indexes)} stock market indexes")

    if all_indexes:
        print("\nStock Market Indexes Summary:")

        # Show first 10 indexes
        for i, index in enumerate(all_indexes[:10]):
            symbol = index.get("symbol", "N/A")
            name = index.get("name", "N/A")
            exchange = index.get("exchange", "N/A")
            currency = index.get("currency", "N/A")

            print(f"\n  {i + 1}. {symbol} - {name}")
            print(f"     Exchange: {exchange}")
            print(f"     Currency: {currency}")

        # Analyze by exchange
        exchanges = {}
        for index in all_indexes:
            exchange = index.get("exchange", "Unknown")
            exchanges[exchange] = exchanges.get(exchange, 0) + 1

        print("\n📊 Exchange Distribution:")
        for exchange, count in sorted(
            exchanges.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {exchange}: {count} indexes")

        # Analyze by currency
        currencies = {}
        for index in all_indexes:
            currency = index.get("currency", "Unknown")
            currencies[currency] = currencies.get(currency, 0) + 1

        print("\n💰 Currency Distribution:")
        for currency, count in sorted(
            currencies.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {currency}: {count} indexes")

        # Find major US indexes
        us_major_indexes = [
            index
            for index in all_indexes
            if index.get("symbol") in ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"]
        ]

        print("\n🇺🇸 Major US Indexes Found:")
        for index in us_major_indexes:
            symbol = index.get("symbol", "N/A")
            name = index.get("name", "N/A")
            print(f"  {symbol}: {name}")


async def index_quotes_examples(client: FmpClient) -> None:
    """Demonstrate index quotes functionality"""
    print("\n=== Index Quotes Examples ===")

    # Major US indexes to analyze
    major_indexes = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"]

    print("Fetching real-time quotes for major US indexes...")

    for symbol in major_indexes:
        try:
            # Get full quote
            quote = await client.indexes.index_quote(symbol)

            if quote:
                data = quote[0]
                name = data.get("name", "N/A")
                price = data.get("price", 0)
                change = data.get("change", 0)
                change_pct = data.get("changePercentage", 0)
                volume = data.get("volume", 0)

                print(f"\n📈 {symbol} ({name}):")
                print(f"  Current Price: ${price:,.2f}")
                print(f"  Change: {change:+.2f} ({change_pct:+.2%})")
                print(f"  Volume: {volume:,}")

                # Additional metrics if available
                if "dayHigh" in data and "dayLow" in data:
                    day_high = data.get("dayHigh", 0)
                    day_low = data.get("dayLow", 0)
                    print(f"  Day Range: ${day_low:,.2f} - ${day_high:,.2f}")

                if "yearHigh" in data and "yearLow" in data:
                    year_high = data.get("yearHigh", 0)
                    year_low = data.get("yearLow", 0)
                    print(f"  Year Range: ${year_low:,.2f} - ${year_high:,.2f}")

                if "priceAvg50" in data and "priceAvg200" in data:
                    avg_50 = data.get("priceAvg50", 0)
                    avg_200 = data.get("priceAvg200", 0)
                    print(f"  50-Day Avg: ${avg_50:,.2f}")
                    print(f"  200-Day Avg: ${avg_200:,.2f}")

                    # Moving average analysis
                    if avg_50 > avg_200:
                        print("  📊 Above 200-day average (Bullish)")
                    else:
                        print("  📊 Below 200-day average (Bearish)")

        except Exception as e:
            print(f"  ❌ Error fetching {symbol}: {e}")

    # Get short quotes for quick overview
    print("\n📊 Quick Index Overview (Short Quotes):")
    for symbol in major_indexes:
        try:
            short_quote = await client.indexes.index_quote_short(symbol)

            if short_quote:
                data = short_quote[0]
                price = data.get("price", 0)
                change = data.get("change", 0)
                volume = data.get("volume", 0)

                print(f"  {symbol}: ${price:,.2f} ({change:+.2f}) | Vol: {volume:,}")

        except Exception as e:
            print(f"  ❌ Error fetching short quote for {symbol}: {e}")


async def all_index_quotes_examples(client: FmpClient) -> None:
    """Demonstrate all index quotes functionality"""
    print("\n=== All Index Quotes Examples ===")

    # Get all index quotes
    print("Fetching quotes for all available indexes...")
    all_quotes = await client.indexes.all_index_quotes()
    print(f"Found quotes for {len(all_quotes)} indexes")

    if all_quotes:
        print("\nAll Indexes Market Overview:")

        # Show first 15 indexes
        for i, quote in enumerate(all_quotes[:15]):
            symbol = quote.get("symbol", "N/A")
            price = quote.get("price", 0)
            change = quote.get("change", 0)
            volume = quote.get("volume", 0)

            print(
                f"  {i + 1:2d}. {symbol}: ${price:,.2f} ({change:+.2f}) | Vol: {volume:,}"
            )

        # Get short quotes for efficiency
        print("\n📊 Short Quotes for All Indexes:")
        short_quotes = await client.indexes.all_index_quotes(short=True)
        print(f"Found short quotes for {len(short_quotes)} indexes")

        if short_quotes:
            # Show first 20 short quotes
            for i, quote in enumerate(short_quotes[:20]):
                symbol = quote.get("symbol", "N/A")
                price = quote.get("price", 0)
                change = quote.get("change", 0)

                print(f"  {i + 1:2d}. {symbol}: ${price:,.2f} ({change:+.2f})")

            # Market sentiment analysis
            positive_changes = [q for q in short_quotes if q.get("change", 0) > 0]
            negative_changes = [q for q in short_quotes if q.get("change", 0) < 0]
            no_changes = [q for q in short_quotes if q.get("change", 0) == 0]

            print("\n📈 Market Sentiment Analysis:")
            print(f"  🟢 Positive: {len(positive_changes)} indexes")
            print(f"  🔴 Negative: {len(negative_changes)} indexes")
            print(f"  ⚪ No Change: {len(no_changes)} indexes")

            if positive_changes and negative_changes:
                total = len(short_quotes)
                positive_pct = (len(positive_changes) / total) * 100
                print(f"  📊 Bullish Indexes: {positive_pct:.1f}%")


async def historical_data_examples(client: FmpClient) -> None:
    """Demonstrate historical data functionality"""
    print("\n=== Historical Data Examples ===")

    # Set date range for historical analysis
    end_date = date.today()
    start_date = end_date - timedelta(days=30)  # Last 30 days

    print(f"Analyzing historical data from {start_date} to {end_date}")

    # Major indexes to analyze
    indexes_to_analyze = ["^GSPC", "^DJI", "^IXIC"]

    for symbol in indexes_to_analyze:
        print(f"\n📊 Historical Analysis for {symbol}:")

        try:
            # Get light historical data
            light_data = await client.indexes.historical_price_eod_light(
                symbol, from_date=start_date, to_date=end_date
            )

            if light_data:
                print(f"  📈 Light Historical Data: {len(light_data)} records")

                # Calculate basic statistics
                prices = [record.get("price", 0) for record in light_data]
                volumes = [record.get("volume", 0) for record in light_data]

                if prices:
                    min_price = min(prices)
                    max_price = max(prices)
                    avg_price = sum(prices) / len(prices)
                    price_change = prices[-1] - prices[0] if len(prices) > 1 else 0
                    price_change_pct = (
                        (price_change / prices[0]) * 100 if prices[0] != 0 else 0
                    )

                    print(f"    Price Range: ${min_price:,.2f} - ${max_price:,.2f}")
                    print(f"    Average Price: ${avg_price:,.2f}")
                    print(
                        f"    Total Change: {price_change:+.2f} ({price_change_pct:+.2f}%)"
                    )

                if volumes:
                    avg_volume = sum(volumes) / len(volumes)
                    print(f"    Average Volume: {avg_volume:,.0f}")

            # Get full historical data
            full_data = await client.indexes.historical_price_eod_full(
                symbol, from_date=start_date, to_date=end_date
            )

            if full_data:
                print(f"  📊 Full Historical Data: {len(full_data)} records")

                # Calculate OHLC statistics
                opens = [record.get("open", 0) for record in full_data]
                highs = [record.get("high", 0) for record in full_data]
                lows = [record.get("low", 0) for record in full_data]
                closes = [record.get("close", 0) for record in full_data]

                if opens and highs and lows and closes:
                    avg_open = sum(opens) / len(opens)
                    avg_high = sum(highs) / len(highs)
                    avg_low = sum(lows) / len(lows)
                    avg_close = sum(closes) / len(closes)

                    print("    Average OHLC:")
                    print(f"      Open: ${avg_open:,.2f}")
                    print(f"      High: ${avg_high:,.2f}")
                    print(f"      Low: ${avg_low:,.2f}")
                    print(f"      Close: ${avg_close:,.2f}")

                    # Volatility analysis
                    daily_ranges = [h - l for h, l in zip(highs, lows, strict=False)]
                    avg_daily_range = sum(daily_ranges) / len(daily_ranges)
                    print(f"    Average Daily Range: ${avg_daily_range:,.2f}")

        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")


async def intraday_data_examples(client: FmpClient) -> None:
    """Demonstrate intraday data functionality"""
    print("\n=== Intraday Data Examples ===")

    # Set date range for intraday analysis (last 5 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=5)

    print(f"Analyzing intraday data from {start_date} to {end_date}")

    # Focus on S&P 500 for intraday analysis
    symbol = "^GSPC"

    try:
        # Get 1-minute intraday data
        print(f"\n⏱️  1-Minute Intraday Analysis for {symbol}:")
        intraday_1min = await client.indexes.intraday_1min(
            symbol, from_date=start_date, to_date=end_date
        )

        if intraday_1min:
            print(f"  📊 1-Minute Data: {len(intraday_1min)} records")

            # Show sample data
            print("  Sample 1-Minute Data:")
            for i, record in enumerate(intraday_1min[:5]):
                timestamp = record.get("date", "N/A")
                open_price = record.get("open", 0)
                high = record.get("high", 0)
                low = record.get("low", 0)
                close = record.get("close", 0)
                volume = record.get("volume", 0)

                print(f"    {i + 1}. {timestamp}")
                print(
                    f"       OHLC: ${open_price:.2f} | ${high:.2f} | ${low:.2f} | ${close:.2f}"
                )
                print(f"       Volume: {volume:,}")

            # Calculate intraday statistics
            prices = [record.get("close", 0) for record in intraday_1min]
            volumes = [record.get("volume", 0) for record in intraday_1min]

            if prices:
                min_price = min(prices)
                max_price = max(prices)
                price_range = max_price - min_price
                print("\n  📈 Intraday Price Analysis:")
                print(f"    Price Range: ${min_price:.2f} - ${max_price:.2f}")
                print(f"    Total Range: ${price_range:.2f}")

            if volumes:
                total_volume = sum(volumes)
                avg_volume = total_volume / len(volumes)
                print(f"    Total Volume: {total_volume:,}")
                print(f"    Average Volume: {avg_volume:,.0f}")

        # Get 5-minute intraday data
        print(f"\n⏱️  5-Minute Intraday Analysis for {symbol}:")
        intraday_5min = await client.indexes.intraday_5min(
            symbol, from_date=start_date, to_date=end_date
        )

        if intraday_5min:
            print(f"  📊 5-Minute Data: {len(intraday_5min)} records")

            # Show sample data
            print("  Sample 5-Minute Data:")
            for i, record in enumerate(intraday_5min[:3]):
                timestamp = record.get("date", "N/A")
                open_price = record.get("open", 0)
                close = record.get("close", 0)
                volume = record.get("volume", 0)

                print(f"    {i + 1}. {timestamp}")
                print(f"       Open: ${open_price:.2f} | Close: ${close:.2f}")
                print(f"       Volume: {volume:,}")

        # Get 1-hour intraday data
        print(f"\n⏱️  1-Hour Intraday Analysis for {symbol}:")
        intraday_1hour = await client.indexes.intraday_1hour(
            symbol, from_date=start_date, to_date=end_date
        )

        if intraday_1hour:
            print(f"  📊 1-Hour Data: {len(intraday_1hour)} records")

            # Show sample data
            print("  Sample 1-Hour Data:")
            for i, record in enumerate(intraday_1hour[:3]):
                timestamp = record.get("date", "N/A")
                open_price = record.get("open", 0)
                close = record.get("close", 0)
                volume = record.get("volume", 0)

                print(f"    {i + 1}. {timestamp}")
                print(f"       Open: ${open_price:.2f} | Close: ${close:.2f}")
                print(f"       Volume: {volume:,}")

    except Exception as e:
        print(f"  ❌ Error analyzing intraday data: {e}")


async def market_analysis_examples(client: FmpClient) -> None:
    """Demonstrate comprehensive market analysis functionality"""
    print("\n=== Comprehensive Market Analysis Examples ===")

    # Perform comprehensive market analysis
    print("Performing comprehensive market analysis...")

    # Major market indexes
    major_indexes = ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"]

    print("\n📊 Major Market Indexes Analysis:")

    for symbol in major_indexes:
        print(f"\n🔍 Analyzing {symbol}...")

        try:
            # Get current quote
            quote = await client.indexes.index_quote(symbol)

            if quote:
                data = quote[0]
                name = data.get("name", "N/A")
                price = data.get("price", 0)
                change = data.get("change", 0)
                change_pct = data.get("changePercentage", 0)

                print(f"  📈 {symbol} ({name}):")
                print(f"    Current: ${price:,.2f} ({change:+.2f}, {change_pct:+.2%})")

                # Technical analysis
                if "priceAvg50" in data and "priceAvg200" in data:
                    avg_50 = data.get("priceAvg50", 0)
                    avg_200 = data.get("priceAvg200", 0)

                    if avg_50 > avg_200:
                        print("    📊 Above 200-day average (Bullish trend)")
                    else:
                        print("    📊 Below 200-day average (Bearish trend)")

                    # Golden/Death cross analysis
                    if avg_50 > avg_200 and price > avg_50:
                        print("    🟢 Golden Cross: Strong bullish momentum")
                    elif avg_50 < avg_200 and price < avg_50:
                        print("    🔴 Death Cross: Strong bearish momentum")

                # Support/Resistance levels
                if "dayLow" in data and "dayHigh" in data:
                    day_low = data.get("dayLow", 0)
                    day_high = data.get("dayHigh", 0)

                    if price > (day_high + day_low) / 2:
                        print("    📈 Trading above daily midpoint")
                    else:
                        print("    📉 Trading below daily midpoint")

                # Volume analysis
                volume = data.get("volume", 0)
                if volume > 0:
                    print(f"    📊 Volume: {volume:,}")

                # Historical context (last 7 days)
                end_date = date.today()
                start_date = end_date - timedelta(days=7)

                historical = await client.indexes.historical_price_eod_light(
                    symbol, from_date=start_date, to_date=end_date
                )

                if historical:
                    prices = [record.get("price", 0) for record in historical]
                    if len(prices) >= 2:
                        week_change = prices[-1] - prices[0]
                        week_change_pct = (
                            (week_change / prices[0]) * 100 if prices[0] != 0 else 0
                        )

                        print(
                            f"    📅 7-Day Change: {week_change:+.2f} ({week_change_pct:+.2f}%)"
                        )

                        # Trend analysis
                        if week_change > 0:
                            print("    📈 Weekly trend: Bullish")
                        elif week_change < 0:
                            print("    📉 Weekly trend: Bearish")
                        else:
                            print("    ➡️  Weekly trend: Sideways")

        except Exception as e:
            print(f"  ❌ Error analyzing {symbol}: {e}")

    # Market breadth analysis
    print("\n🌐 Market Breadth Analysis:")

    try:
        # Get all index quotes for breadth analysis
        all_quotes = await client.indexes.all_index_quotes(short=True)

        if all_quotes:
            total_indexes = len(all_quotes)
            positive_changes = len([q for q in all_quotes if q.get("change", 0) > 0])
            negative_changes = len([q for q in all_quotes if q.get("change", 0) < 0])
            no_changes = len([q for q in all_quotes if q.get("change", 0) == 0])

            print(f"  📊 Total Indexes: {total_indexes}")
            print(
                f"  🟢 Advancing: {positive_changes} ({positive_changes / total_indexes * 100:.1f}%)"
            )
            print(
                f"  🔴 Declining: {negative_changes} ({negative_changes / total_indexes * 100:.1f}%)"
            )
            print(
                f"  ⚪ Unchanged: {no_changes} ({no_changes / total_indexes * 100:.1f}%)"
            )

            # Market sentiment
            if positive_changes > negative_changes:
                print("  📈 Market Sentiment: Bullish")
            elif negative_changes > positive_changes:
                print("  📉 Market Sentiment: Bearish")
            else:
                print("  ➡️  Market Sentiment: Neutral")

            # Volatility analysis
            changes = [abs(q.get("change", 0)) for q in all_quotes]
            if changes:
                avg_change = sum(changes) / len(changes)
                print(f"  📊 Average Change: {avg_change:.2f}")

                if avg_change > 10:
                    print("  ⚠️  High volatility detected")
                elif avg_change > 5:
                    print("  📊 Moderate volatility")
                else:
                    print("  📈 Low volatility")

    except Exception as e:
        print(f"  ❌ Error in market breadth analysis: {e}")


async def main() -> None:
    """Main function demonstrating FMP Indexes functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Indexes Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await index_list_examples(client)
            await index_quotes_examples(client)
            await all_index_quotes_examples(client)
            await historical_data_examples(client)
            await intraday_data_examples(client)
            await market_analysis_examples(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
