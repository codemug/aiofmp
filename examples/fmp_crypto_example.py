#!/usr/bin/env python3
"""
Example script demonstrating FMP Crypto category functionality

This script shows how to use the FMP client to access cryptocurrency data including
cryptocurrency list, real-time quotes, historical price data, and intraday charts.
"""

import asyncio
import os

from aiofmp import FmpClient


async def cryptocurrency_list_examples(client: FmpClient) -> None:
    """Demonstrate cryptocurrency list functionality"""
    print("\n=== Cryptocurrency List Examples ===")

    # Get list of all available cryptocurrencies
    print("Fetching list of all available cryptocurrencies...")
    cryptocurrencies = await client.crypto.cryptocurrency_list()
    print(f"Found {len(cryptocurrencies)} cryptocurrencies")

    if cryptocurrencies:
        print("\nCryptocurrencies Summary:")

        # Group by exchange
        exchanges = {}
        for crypto in cryptocurrencies:
            exchange = crypto.get("exchange", "Unknown")
            if exchange not in exchanges:
                exchanges[exchange] = []
            exchanges[exchange].append(crypto)

        for exchange, crypto_list in exchanges.items():
            print(f"\n  {exchange} Exchange ({len(crypto_list)}):")
            for i, crypto in enumerate(crypto_list[:5]):  # Show first 5 per exchange
                print(
                    f"    {i + 1}. {crypto.get('name', 'N/A')} ({crypto.get('symbol', 'N/A')})"
                )
                print(f"       ICO Date: {crypto.get('icoDate', 'N/A')}")
                print(
                    f"       Circulating Supply: {crypto.get('circulatingSupply', 0):,}"
                )
                if crypto.get("totalSupply"):
                    print(f"       Total Supply: {crypto.get('totalSupply', 0):,}")
            if len(crypto_list) > 5:
                print(f"       ... and {len(crypto_list) - 5} more")

        # Show some specific examples
        print("\nSample Cryptocurrencies:")
        for i, crypto in enumerate(cryptocurrencies[:10]):
            print(
                f"  {i + 1:2d}. {crypto.get('name', 'N/A'):<25} - {crypto.get('symbol', 'N/A'):<8} ({crypto.get('exchange', 'N/A')})"
            )


async def quote_examples(client: FmpClient) -> None:
    """Demonstrate cryptocurrency quote functionality"""
    print("\n=== Cryptocurrency Quote Examples ===")

    # Get quote for Bitcoin
    print("Fetching quote for Bitcoin (BTCUSD)...")
    btc_quote = await client.crypto.quote("BTCUSD")
    print(f"Found {len(btc_quote)} quote records for Bitcoin")

    if btc_quote:
        print("\nBitcoin Quote Summary:")
        quote = btc_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,.0f}")
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
        print(f"  Market Cap: ${quote.get('marketCap', 0):,.0f}")
        print(f"  Exchange: {quote.get('exchange', 'N/A')}")
        print()

    # Get quote for Ethereum
    print("Fetching quote for Ethereum (ETHUSD)...")
    eth_quote = await client.crypto.quote("ETHUSD")
    print(f"Found {len(eth_quote)} quote records for Ethereum")

    if eth_quote:
        print("\nEthereum Quote Summary:")
        quote = eth_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.2f}")
        print(
            f"  Change: {quote.get('change', 0):+.2f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,.0f}")
        print(
            f"  Day Range: ${quote.get('dayLow', 0):,.2f} - ${quote.get('dayHigh', 0):,.2f}"
        )
        print(f"  Market Cap: ${quote.get('marketCap', 0):,.0f}")
        print()

    # Get quote for Cardano
    print("Fetching quote for Cardano (ADAUSD)...")
    ada_quote = await client.crypto.quote("ADAUSD")
    print(f"Found {len(ada_quote)} quote records for Cardano")

    if ada_quote:
        print("\nCardano Quote Summary:")
        quote = ada_quote[0]
        print(f"  Symbol: {quote.get('symbol', 'N/A')}")
        print(f"  Name: {quote.get('name', 'N/A')}")
        print(f"  Current Price: ${quote.get('price', 0):,.4f}")
        print(
            f"  Change: {quote.get('change', 0):+.4f} ({quote.get('changePercentage', 0):+.2f}%)"
        )
        print(f"  Volume: {quote.get('volume', 0):,.0f}")
        print()


async def quote_short_examples(client: FmpClient) -> None:
    """Demonstrate cryptocurrency quote short functionality"""
    print("\n=== Cryptocurrency Quote Short Examples ===")

    # Get short quotes for multiple cryptocurrencies
    cryptocurrencies_to_quote = ["BTCUSD", "ETHUSD", "ADAUSD", "SOLUSD", "DOTUSD"]

    for symbol in cryptocurrencies_to_quote:
        print(f"Fetching short quote for {symbol}...")
        quote = await client.crypto.quote_short(symbol)

        if quote:
            print(
                f"  {symbol}: ${quote[0].get('price', 0):,.4f} ({quote[0].get('change', 0):+.4f}) - Vol: {quote[0].get('volume', 0):,.0f}"
            )
        else:
            print(f"  {symbol}: No data available")

    print()


async def batch_quotes_examples(client: FmpClient) -> None:
    """Demonstrate batch quotes functionality"""
    print("\n=== Batch Quotes Examples ===")

    # Get batch quotes (short format)
    print("Fetching batch quotes (short format)...")
    batch_quotes_short = await client.crypto.batch_quotes(short=True)
    print(f"Found {len(batch_quotes_short)} batch quotes in short format")

    if batch_quotes_short:
        print("\nSample Batch Quotes (Short Format):")
        for i, quote in enumerate(batch_quotes_short[:10]):  # Show first 10
            print(
                f"  {i + 1:2d}. {quote.get('symbol', 'N/A'):<10} - ${quote.get('price', 0):<12,.4f} ({quote.get('change', 0):+.4f})"
            )

    # Get batch quotes (full format)
    print("\nFetching batch quotes (full format)...")
    batch_quotes_full = await client.crypto.batch_quotes(short=False)
    print(f"Found {len(batch_quotes_full)} batch quotes in full format")

    if batch_quotes_full:
        print("\nSample Batch Quotes (Full Format):")
        for i, quote in enumerate(batch_quotes_full[:5]):  # Show first 5
            print(f"  {i + 1}. {quote.get('symbol', 'N/A')}")
            print(f"     Price: ${quote.get('price', 0):,.4f}")
            print(f"     Change: {quote.get('change', 0):+.4f}")
            print(f"     Volume: {quote.get('volume', 0):,.0f}")
            print()


async def historical_price_examples(client: FmpClient) -> None:
    """Demonstrate historical price functionality"""
    print("\n=== Historical Price Examples ===")

    # Get light historical prices for Bitcoin
    print("Fetching light historical prices for Bitcoin (BTCUSD)...")
    btc_light = await client.crypto.historical_price_light(
        "BTCUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(btc_light)} historical price records for Bitcoin in January 2025"
    )

    if btc_light:
        print("\nBitcoin Light Historical Prices (January 2025):")
        for i, record in enumerate(btc_light[:5]):  # Show first 5 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: ${record.get('price', 0):,.2f}")
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print()

    # Get full historical prices for Bitcoin
    print("Fetching full historical prices for Bitcoin (BTCUSD)...")
    btc_full = await client.crypto.historical_price_full(
        "BTCUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(btc_full)} full historical price records for Bitcoin in January 2025"
    )

    if btc_full:
        print("\nBitcoin Full Historical Prices (January 2025):")
        for i, record in enumerate(btc_full[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print(
                f"     Change: {record.get('change', 0):+.2f} ({record.get('changePercent', 0):+.2f}%)"
            )
            print(f"     VWAP: ${record.get('vwap', 0):,.2f}")
            print()

    # Get historical prices for Ethereum
    print("Fetching historical prices for Ethereum (ETHUSD)...")
    eth_prices = await client.crypto.historical_price_light(
        "ETHUSD", "2025-01-01", "2025-01-31"
    )
    print(
        f"Found {len(eth_prices)} historical price records for Ethereum in January 2025"
    )

    if eth_prices:
        print("\nEthereum Historical Prices (January 2025):")
        for i, record in enumerate(eth_prices[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Price: ${record.get('price', 0):,.2f}")
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print()


async def intraday_examples(client: FmpClient) -> None:
    """Demonstrate intraday chart functionality"""
    print("\n=== Intraday Chart Examples ===")

    # Get 1-minute intraday data for Bitcoin
    print("Fetching 1-minute intraday data for Bitcoin (BTCUSD)...")
    btc_1min = await client.crypto.intraday_1min("BTCUSD", "2025-01-15", "2025-01-15")
    print(f"Found {len(btc_1min)} 1-minute records for Bitcoin on January 15, 2025")

    if btc_1min:
        print("\nBitcoin 1-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(btc_1min[:5]):  # Show first 5 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print()

    # Get 5-minute intraday data for Bitcoin
    print("Fetching 5-minute intraday data for Bitcoin (BTCUSD)...")
    btc_5min = await client.crypto.intraday_5min("BTCUSD", "2025-01-15", "2025-01-15")
    print(f"Found {len(btc_5min)} 5-minute records for Bitcoin on January 15, 2025")

    if btc_5min:
        print("\nBitcoin 5-Minute Intraday Data (January 15, 2025):")
        for i, record in enumerate(btc_5min[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print()

    # Get 1-hour intraday data for Bitcoin
    print("Fetching 1-hour intraday data for Bitcoin (BTCUSD)...")
    btc_1hour = await client.crypto.intraday_1hour("BTCUSD", "2025-01-15", "2025-01-15")
    print(f"Found {len(btc_1hour)} 1-hour records for Bitcoin on January 15, 2025")

    if btc_1hour:
        print("\nBitcoin 1-Hour Intraday Data (January 15, 2025):")
        for i, record in enumerate(btc_1hour[:3]):  # Show first 3 records
            print(f"  {i + 1}. Time: {record.get('date', 'N/A')}")
            print(
                f"     OHLC: ${record.get('open', 0):,.2f} / ${record.get('high', 0):,.2f} / ${record.get('low', 0):,.2f} / ${record.get('close', 0):,.2f}"
            )
            print(f"     Volume: {record.get('volume', 0):,.0f}")
            print()


async def crypto_analysis_examples(client: FmpClient) -> None:
    """Demonstrate cryptocurrency analysis functionality"""
    print("\n=== Cryptocurrency Analysis Examples ===")

    # Analyze Bitcoin vs Ethereum performance
    print("Analyzing Bitcoin vs Ethereum performance...")

    # Get quotes for both cryptocurrencies
    btc_quote = await client.crypto.quote("BTCUSD")
    eth_quote = await client.crypto.quote("ETHUSD")

    if btc_quote and eth_quote:
        print("\nBitcoin vs Ethereum Comparison:")
        btc = btc_quote[0]
        eth = eth_quote[0]

        print("  Bitcoin (BTCUSD):")
        print(f"    Price: ${btc.get('price', 0):,.2f}")
        print(
            f"    Change: {btc.get('change', 0):+.2f} ({btc.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {btc.get('volume', 0):,.0f}")
        print(f"    50-Day Avg: ${btc.get('priceAvg50', 0):,.2f}")
        print(f"    200-Day Avg: ${btc.get('priceAvg200', 0):,.2f}")
        print(f"    Market Cap: ${btc.get('marketCap', 0):,.0f}")

        print("  Ethereum (ETHUSD):")
        print(f"    Price: ${eth.get('price', 0):,.2f}")
        print(
            f"    Change: {eth.get('change', 0):+.2f} ({eth.get('changePercentage', 0):+.2f}%)"
        )
        print(f"    Volume: {eth.get('volume', 0):,.0f}")
        print(f"    50-Day Avg: ${eth.get('priceAvg50', 0):,.2f}")
        print(f"    200-Day Avg: ${eth.get('priceAvg200', 0):,.2f}")
        print(f"    Market Cap: ${eth.get('marketCap', 0):,.0f}")

        # Calculate BTC dominance
        btc_market_cap = btc.get("marketCap", 0)
        eth_market_cap = eth.get("marketCap", 0)
        if btc_market_cap > 0 and eth_market_cap > 0:
            total_market_cap = btc_market_cap + eth_market_cap
            btc_dominance = (btc_market_cap / total_market_cap) * 100
            eth_dominance = (eth_market_cap / total_market_cap) * 100
            print("\n  Market Cap Analysis:")
            print(f"    Bitcoin Dominance: {btc_dominance:.2f}%")
            print(f"    Ethereum Dominance: {eth_dominance:.2f}%")

    # Analyze altcoin performance
    print("\nAnalyzing altcoin performance...")

    # Get quotes for altcoins
    altcoins = ["ADAUSD", "SOLUSD", "DOTUSD"]
    altcoin_data = {}

    for symbol in altcoins:
        try:
            quote = await client.crypto.quote(symbol)
            if quote:
                altcoin_data[symbol] = quote[0]
        except Exception as e:
            print(f"  Error fetching {symbol}: {e}")

    if altcoin_data:
        print("\nAltcoin Performance Analysis:")
        for symbol, quote in altcoin_data.items():
            print(f"  {symbol}:")
            print(f"    Price: ${quote.get('price', 0):,.4f}")
            print(
                f"    Change: {quote.get('change', 0):+.4f} ({quote.get('changePercentage', 0):+.2f}%)"
            )
            print(f"    Volume: {quote.get('volume', 0):,.0f}")
            print(f"    Market Cap: ${quote.get('marketCap', 0):,.0f}")
            print()


async def crypto_portfolio_analysis(client: FmpClient) -> None:
    """Demonstrate cryptocurrency portfolio analysis functionality"""
    print("\n=== Cryptocurrency Portfolio Analysis Examples ===")

    # Define a hypothetical cryptocurrency portfolio
    portfolio = {
        "BTCUSD": 0.50,  # 50% Bitcoin
        "ETHUSD": 0.30,  # 30% Ethereum
        "ADAUSD": 0.10,  # 10% Cardano
        "SOLUSD": 0.10,  # 10% Solana
    }

    print(f"Analyzing cryptocurrency portfolio: {portfolio}")

    total_change = 0
    total_volume = 0
    crypto_data = {}

    for symbol, allocation in portfolio.items():
        print(f"\n--- Analyzing {symbol} ({allocation * 100:.0f}% allocation) ---")

        try:
            # Get quote for the cryptocurrency
            quote = await client.crypto.quote(symbol)
            if quote:
                quote = quote[0]
                price = quote.get("price", 0)
                change_pct = quote.get("changePercentage", 0)
                volume = quote.get("volume", 0)
                market_cap = quote.get("marketCap", 0)

                print(f"  Current Price: ${price:,.4f}")
                print(f"  Daily Change: {change_pct:+.2f}%")
                print(f"  Volume: {volume:,.0f}")
                print(f"  Market Cap: ${market_cap:,.0f}")
                print(f"  50-Day Average: ${quote.get('priceAvg50', 0):,.4f}")
                print(f"  200-Day Average: ${quote.get('priceAvg200', 0):,.4f}")

                # Calculate weighted metrics
                total_change += change_pct * allocation
                total_volume += volume * allocation
                crypto_data[symbol] = {
                    "price": price,
                    "change_pct": change_pct,
                    "allocation": allocation,
                    "market_cap": market_cap,
                }

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")

    # Portfolio summary
    print("\n=== Portfolio Summary ===")
    print(f"Total Weighted Daily Change: {total_change:+.2f}%")
    print(f"Total Weighted Volume: {total_volume:,.0f}")

    # Performance analysis
    print("\nPerformance Analysis:")
    if total_change > 2:
        print(f"  🟢 Strong positive performance: +{total_change:.2f}%")
    elif total_change > 0:
        print(f"  🟡 Moderate positive performance: +{total_change:.2f}%")
    elif total_change > -2:
        print(f"  🟡 Moderate negative performance: {total_change:.2f}%")
    else:
        print(f"  🔴 Strong negative performance: {total_change:.2f}%")

    # Risk assessment
    print("\nRisk Assessment:")
    high_volatility = [
        sym for sym, data in crypto_data.items() if abs(data["change_pct"]) > 5
    ]
    if high_volatility:
        print(f"  ⚠️  High volatility cryptocurrencies: {', '.join(high_volatility)}")

    # Market cap analysis
    if crypto_data:
        total_portfolio_market_cap = sum(
            data["market_cap"] * data["allocation"] for data in crypto_data.values()
        )
        print("\nMarket Cap Analysis:")
        print(f"  Total Portfolio Market Cap: ${total_portfolio_market_cap:,.0f}")

        # Check for large cap vs small cap exposure
        large_cap_exposure = sum(
            data["allocation"]
            for data in crypto_data.values()
            if data["market_cap"] > 100000000000
        )  # >$100B
        if large_cap_exposure > 0.7:
            print(f"  ✅ High large-cap exposure: {large_cap_exposure * 100:.1f}%")
        elif large_cap_exposure > 0.4:
            print(f"  ⚠️  Moderate large-cap exposure: {large_cap_exposure * 100:.1f}%")
        else:
            print(f"  ⚠️  Low large-cap exposure: {large_cap_exposure * 100:.1f}%")

    # Diversification check
    if len(portfolio) >= 4:
        print(f"  ✅ Good diversification with {len(portfolio)} cryptocurrencies")
    else:
        print(
            f"  ⚠️  Limited diversification with only {len(portfolio)} cryptocurrencies"
        )


async def main() -> None:
    """Main function demonstrating FMP Crypto functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Crypto Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await cryptocurrency_list_examples(client)
            await quote_examples(client)
            await quote_short_examples(client)
            await batch_quotes_examples(client)
            await historical_price_examples(client)
            await intraday_examples(client)
            await crypto_analysis_examples(client)
            await crypto_portfolio_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
