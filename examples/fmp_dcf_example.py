#!/usr/bin/env python3
"""
Example script demonstrating FMP Discounted Cash Flow (DCF) category functionality

This script shows how to use the FMP client to access DCF data including
basic DCF valuation, levered DCF analysis, and custom DCF calculations.
"""

import asyncio
import os

from aiofmp import FmpClient


async def basic_dcf_examples(client: FmpClient) -> None:
    """Demonstrate basic DCF functionality"""
    print("\n=== Basic DCF Examples ===")

    # Get basic DCF valuation for Apple
    print("Fetching basic DCF valuation for AAPL...")
    dcf_data = await client.dcf.dcf_valuation("AAPL")
    print(f"Found {len(dcf_data)} DCF valuation records")

    if dcf_data:
        print("\nBasic DCF Valuation Summary:")
        for i, record in enumerate(dcf_data):
            print(f"  {i + 1}. Symbol: {record.get('symbol', 'N/A')}")
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     DCF Value: ${record.get('dcf', 0):.2f}")
            print(f"     Stock Price: ${record.get('Stock Price', 0):.3f}")

            # Calculate potential upside/downside
            dcf_value = record.get("dcf", 0)
            stock_price = record.get("Stock Price", 0)
            if dcf_value > 0 and stock_price > 0:
                upside = ((dcf_value - stock_price) / stock_price) * 100
                print(f"     Potential Upside: {upside:+.2f}%")
                if upside > 0:
                    print("     Investment Thesis: Undervalued")
                elif upside < 0:
                    print("     Investment Thesis: Overvalued")
                else:
                    print("     Investment Thesis: Fairly Valued")

    # Get basic DCF valuation for Microsoft
    print("\nFetching basic DCF valuation for MSFT...")
    msft_dcf = await client.dcf.dcf_valuation("MSFT")
    print(f"Found {len(msft_dcf)} Microsoft DCF records")

    if msft_dcf:
        print("\nMicrosoft DCF Summary:")
        for record in msft_dcf:
            print(f"  Symbol: {record.get('symbol', 'N/A')}")
            print(f"  DCF Value: ${record.get('dcf', 0):.2f}")
            print(f"  Stock Price: ${record.get('Stock Price', 0):.3f}")


async def levered_dcf_examples(client: FmpClient) -> None:
    """Demonstrate levered DCF functionality"""
    print("\n=== Levered DCF Examples ===")

    # Get levered DCF for Apple
    print("Fetching levered DCF for AAPL...")
    levered_dcf = await client.dcf.levered_dcf("AAPL")
    print(f"Found {len(levered_dcf)} levered DCF records")

    if levered_dcf:
        print("\nLevered DCF Summary:")
        for i, record in enumerate(levered_dcf):
            print(f"  {i + 1}. Symbol: {record.get('symbol', 'N/A')}")
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     DCF Value: ${record.get('dcf', 0):.2f}")
            print(f"     Stock Price: ${record.get('Stock Price', 0):.3f}")

            # Calculate potential upside/downside
            dcf_value = record.get("dcf", 0)
            stock_price = record.get("Stock Price", 0)
            if dcf_value > 0 and stock_price > 0:
                upside = ((dcf_value - stock_price) / stock_price) * 100
                print(f"     Potential Upside: {upside:+.2f}%")

    # Get levered DCF for Google
    print("\nFetching levered DCF for GOOGL...")
    googl_dcf = await client.dcf.levered_dcf("GOOGL")
    print(f"Found {len(googl_dcf)} Google levered DCF records")

    if googl_dcf:
        print("\nGoogle Levered DCF Summary:")
        for record in googl_dcf:
            print(f"  Symbol: {record.get('symbol', 'N/A')}")
            print(f"  DCF Value: ${record.get('dcf', 0):.2f}")
            print(f"  Stock Price: ${record.get('Stock Price', 0):.3f}")


async def custom_dcf_advanced_examples(client: FmpClient) -> None:
    """Demonstrate custom DCF advanced functionality"""
    print("\n=== Custom DCF Advanced Examples ===")

    # Get custom DCF with minimal parameters
    print("Fetching custom DCF advanced for AAPL with minimal parameters...")
    custom_dcf = await client.dcf.custom_dcf_advanced(
        "AAPL", revenue_growth_pct=0.109, beta=1.244
    )
    print(f"Found {len(custom_dcf)} custom DCF records")

    if custom_dcf:
        print("\nCustom DCF Advanced Summary (Minimal Parameters):")
        for i, record in enumerate(custom_dcf[:3]):  # Show first 3 years
            print(f"  {i + 1}. Year: {record.get('year', 'N/A')}")
            print(f"     Symbol: {record.get('symbol', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,.0f}")
            print(f"     Revenue Growth: {record.get('revenuePercentage', 0):.2f}%")
            print(f"     EBITDA: ${record.get('ebitda', 0):,.0f}")
            print(f"     EBIT: ${record.get('ebit', 0):,.0f}")
            print(f"     Beta: {record.get('beta', 'N/A')}")
            print(f"     WACC: {record.get('wacc', 'N/A')}%")
            print(
                f"     Equity Value Per Share: ${record.get('equityValuePerShare', 0):.2f}"
            )
            print()

    # Get custom DCF with more parameters
    print("Fetching custom DCF advanced for AAPL with more parameters...")
    custom_dcf_detailed = await client.dcf.custom_dcf_advanced(
        "AAPL",
        revenue_growth_pct=0.109,
        ebitda_pct=0.313,
        beta=1.244,
        tax_rate=0.149,
        long_term_growth_rate=4.0,
        cost_of_debt=3.64,
        cost_of_equity=9.512,
        market_risk_premium=4.72,
        risk_free_rate=3.64,
    )
    print(f"Found {len(custom_dcf_detailed)} detailed custom DCF records")

    if custom_dcf_detailed:
        print("\nCustom DCF Advanced Summary (Detailed Parameters):")
        for i, record in enumerate(custom_dcf_detailed[:2]):  # Show first 2 years
            print(f"  {i + 1}. Year: {record.get('year', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,.0f}")
            print(f"     EBITDA: ${record.get('ebitda', 0):,.0f}")
            print(f"     EBIT: ${record.get('ebit', 0):,.0f}")
            print(f"     Total Cash: ${record.get('totalCash', 0):,.0f}")
            print(f"     Total Debt: ${record.get('totalDebt', 0):,.0f}")
            print(f"     Enterprise Value: ${record.get('enterpriseValue', 0):,.0f}")
            print(f"     Equity Value: ${record.get('equityValue', 0):,.0f}")
            print(
                f"     Equity Value Per Share: ${record.get('equityValuePerShare', 0):.2f}"
            )
            print(f"     Free Cash Flow T1: ${record.get('freeCashFlowT1', 0):,.0f}")
            print()


async def custom_dcf_levered_examples(client: FmpClient) -> None:
    """Demonstrate custom DCF levered functionality"""
    print("\n=== Custom DCF Levered Examples ===")

    # Get custom levered DCF with minimal parameters
    print("Fetching custom levered DCF for AAPL with minimal parameters...")
    custom_levered = await client.dcf.custom_dcf_levered(
        "AAPL", revenue_growth_pct=0.109, beta=1.244
    )
    print(f"Found {len(custom_levered)} custom levered DCF records")

    if custom_levered:
        print("\nCustom DCF Levered Summary (Minimal Parameters):")
        for i, record in enumerate(custom_levered[:3]):  # Show first 3 years
            print(f"  {i + 1}. Year: {record.get('year', 'N/A')}")
            print(f"     Symbol: {record.get('symbol', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,.0f}")
            print(f"     Revenue Growth: {record.get('revenuePercentage', 0):.2f}%")
            print(
                f"     Capital Expenditure: ${record.get('capitalExpenditure', 0):,.0f}"
            )
            print(f"     Beta: {record.get('beta', 'N/A')}")
            print(f"     Cost of Debt: {record.get('costofDebt', 'N/A')}%")
            print(f"     Cost of Equity: {record.get('costOfEquity', 'N/A')}%")
            print(f"     WACC: {record.get('wacc', 'N/A')}%")
            print(
                f"     Operating Cash Flow: ${record.get('operatingCashFlow', 0):,.0f}"
            )
            print(f"     Free Cash Flow: ${record.get('freeCashFlow', 0):,.0f}")
            print(f"     Enterprise Value: ${record.get('enterpriseValue', 0):,.0f}")
            print(f"     Equity Value: ${record.get('equityValue', 0):,.0f}")
            print(
                f"     Equity Value Per Share: ${record.get('equityValuePerShare', 0):.2f}"
            )
            print()

    # Get custom levered DCF with more parameters
    print("Fetching custom levered DCF for AAPL with more parameters...")
    custom_levered_detailed = await client.dcf.custom_dcf_levered(
        "AAPL",
        revenue_growth_pct=0.109,
        ebitda_pct=0.313,
        beta=1.244,
        tax_rate=0.149,
        long_term_growth_rate=4.0,
        cost_of_debt=3.64,
        cost_of_equity=9.512,
        market_risk_premium=4.72,
        risk_free_rate=3.64,
    )
    print(f"Found {len(custom_levered_detailed)} detailed custom levered DCF records")

    if custom_levered_detailed:
        print("\nCustom DCF Levered Summary (Detailed Parameters):")
        for i, record in enumerate(custom_levered_detailed[:2]):  # Show first 2 years
            print(f"  {i + 1}. Year: {record.get('year', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,.0f}")
            print(
                f"     Capital Expenditure: ${record.get('capitalExpenditure', 0):,.0f}"
            )
            print(f"     Total Debt: ${record.get('totalDebt', 0):,.0f}")
            print(f"     Total Equity: ${record.get('totalEquity', 0):,.0f}")
            print(f"     Total Capital: ${record.get('totalCapital', 0):,.0f}")
            print(f"     Debt Weighting: {record.get('debtWeighting', 0):.2f}%")
            print(f"     Equity Weighting: {record.get('equityWeighting', 0):.2f}%")
            print(f"     WACC: {record.get('wacc', 'N/A')}%")
            print(
                f"     Operating Cash Flow: ${record.get('operatingCashFlow', 0):,.0f}"
            )
            print(f"     Free Cash Flow: ${record.get('freeCashFlow', 0):,.0f}")
            print(f"     Terminal Value: ${record.get('terminalValue', 0):,.0f}")
            print(f"     Enterprise Value: ${record.get('enterpriseValue', 0):,.0f}")
            print(f"     Equity Value: ${record.get('equityValue', 0):,.0f}")
            print(
                f"     Equity Value Per Share: ${record.get('equityValuePerShare', 0):.2f}"
            )
            print()


async def dcf_comparison_analysis(client: FmpClient) -> None:
    """Demonstrate DCF comparison analysis"""
    print("\n=== DCF Comparison Analysis ===")

    # Compare different DCF methods for the same company
    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        print(f"\n--- Analyzing {symbol} ---")

        try:
            # Get basic DCF
            basic_dcf = await client.dcf.dcf_valuation(symbol)

            # Get levered DCF
            levered_dcf = await client.dcf.levered_dcf(symbol)

            # Get custom DCF with reasonable assumptions
            custom_dcf = await client.dcf.custom_dcf_advanced(
                symbol,
                revenue_growth_pct=0.10,  # 10% growth
                beta=1.2,  # Moderate beta
                tax_rate=0.25,  # 25% tax rate
                long_term_growth_rate=3.0,  # 3% long-term growth
            )

            print(f"  Basic DCF: {len(basic_dcf)} records found")
            print(f"  Levered DCF: {len(levered_dcf)} records found")
            print(f"  Custom DCF: {len(custom_dcf)} records found")

            # Compare basic vs levered DCF
            if basic_dcf and levered_dcf:
                basic_value = basic_dcf[0].get("dcf", 0)
                levered_value = levered_dcf[0].get("dcf", 0)
                stock_price = basic_dcf[0].get("Stock Price", 0)

                if basic_value > 0 and levered_value > 0 and stock_price > 0:
                    basic_upside = ((basic_value - stock_price) / stock_price) * 100
                    levered_upside = ((levered_value - stock_price) / stock_price) * 100

                    print(f"  Stock Price: ${stock_price:.2f}")
                    print(
                        f"  Basic DCF Value: ${basic_value:.2f} (Upside: {basic_upside:+.2f}%)"
                    )
                    print(
                        f"  Levered DCF Value: ${levered_value:.2f} (Upside: {levered_upside:+.2f}%)"
                    )

                    # Determine which method shows higher value
                    if basic_upside > levered_upside:
                        print(
                            "  Analysis: Basic DCF shows higher upside (debt impact considered)"
                        )
                    elif levered_upside > basic_upside:
                        print(
                            "  Analysis: Levered DCF shows higher upside (debt impact beneficial)"
                        )
                    else:
                        print("  Analysis: Both methods show similar upside")

            # Show custom DCF projections if available
            if custom_dcf:
                print("  Custom DCF Projections:")
                for i, record in enumerate(custom_dcf[:3]):  # Show first 3 years
                    year = record.get("year", "N/A")
                    revenue = record.get("revenue", 0)
                    equity_value = record.get("equityValuePerShare", 0)
                    print(
                        f"    {year}: Revenue ${revenue:,.0f}, Equity Value ${equity_value:.2f}"
                    )

        except Exception as e:
            print(f"  Error analyzing {symbol}: {e}")


async def dcf_parameter_sensitivity_analysis(client: FmpClient) -> None:
    """Demonstrate DCF parameter sensitivity analysis"""
    print("\n=== DCF Parameter Sensitivity Analysis ===")

    symbol = "AAPL"
    print(f"Analyzing parameter sensitivity for {symbol}...")

    # Test different revenue growth rates
    growth_rates = [0.05, 0.10, 0.15, 0.20]  # 5%, 10%, 15%, 20%

    print("\nRevenue Growth Rate Sensitivity:")
    for growth_rate in growth_rates:
        try:
            custom_dcf = await client.dcf.custom_dcf_advanced(
                symbol,
                revenue_growth_pct=growth_rate,
                beta=1.244,
                tax_rate=0.149,
                long_term_growth_rate=4.0,
            )

            if custom_dcf:
                latest = custom_dcf[0]
                equity_value = latest.get("equityValuePerShare", 0)
                print(
                    f"  {growth_rate * 100:2.0f}% Growth: Equity Value = ${equity_value:.2f}"
                )
            else:
                print(f"  {growth_rate * 100:2.0f}% Growth: No data available")

        except Exception as e:
            print(f"  {growth_rate * 100:2.0f}% Growth: Error - {e}")

    # Test different beta values
    beta_values = [0.8, 1.0, 1.2, 1.5, 2.0]

    print("\nBeta Sensitivity (with 10% revenue growth):")
    for beta in beta_values:
        try:
            custom_dcf = await client.dcf.custom_dcf_advanced(
                symbol,
                revenue_growth_pct=0.10,
                beta=beta,
                tax_rate=0.149,
                long_term_growth_rate=4.0,
            )

            if custom_dcf:
                latest = custom_dcf[0]
                equity_value = latest.get("equityValuePerShare", 0)
                print(f"  Beta {beta:3.1f}: Equity Value = ${equity_value:.2f}")
            else:
                print(f"  Beta {beta:3.1f}: No data available")

        except Exception as e:
            print(f"  Beta {beta:3.1f}: Error - {e}")

    # Test different tax rates
    tax_rates = [0.15, 0.20, 0.25, 0.30, 0.35]

    print("\nTax Rate Sensitivity (with 10% revenue growth, beta 1.2):")
    for tax_rate in tax_rates:
        try:
            custom_dcf = await client.dcf.custom_dcf_advanced(
                symbol,
                revenue_growth_pct=0.10,
                beta=1.2,
                tax_rate=tax_rate,
                long_term_growth_rate=4.0,
            )

            if custom_dcf:
                latest = custom_dcf[0]
                equity_value = latest.get("equityValuePerShare", 0)
                print(
                    f"  Tax Rate {tax_rate * 100:2.0f}%: Equity Value = ${equity_value:.2f}"
                )
            else:
                print(f"  Tax Rate {tax_rate * 100:2.0f}%: No data available")

        except Exception as e:
            print(f"  Tax Rate {tax_rate * 100:2.0f}%: Error - {e}")


async def main() -> None:
    """Main function demonstrating FMP DCF functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Discounted Cash Flow (DCF) Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await basic_dcf_examples(client)
            await levered_dcf_examples(client)
            await custom_dcf_advanced_examples(client)
            await custom_dcf_levered_examples(client)
            await dcf_comparison_analysis(client)
            await dcf_parameter_sensitivity_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
