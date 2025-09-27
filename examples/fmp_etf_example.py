#!/usr/bin/env python3
"""
Example script demonstrating FMP ETF And Mutual Funds category functionality

This script shows how to use the FMP client to access ETF and mutual fund data including
holdings breakdown, fund information, country allocation, asset exposure, sector weighting, and disclosures.
"""

import asyncio
import os

from aiofmp import FmpClient


async def holdings_examples(client: FmpClient) -> None:
    """Demonstrate ETF holdings functionality"""
    print("\n=== ETF Holdings Examples ===")

    # Get holdings for SPY (S&P 500 ETF)
    print("Fetching holdings for SPY (S&P 500 ETF)...")
    spy_holdings = await client.etf.holdings("SPY")
    print(f"Found {len(spy_holdings)} holdings in SPY")

    if spy_holdings:
        print("\nSPY Holdings Summary:")
        for i, holding in enumerate(spy_holdings[:5]):  # Show first 5 holdings
            print(
                f"  {i + 1}. {holding.get('name', 'N/A')} ({holding.get('asset', 'N/A')})"
            )
            print(f"     Shares: {holding.get('sharesNumber', 0):,}")
            print(f"     Weight: {holding.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holding.get('marketValue', 0):,.2f}")
            print(f"     ISIN: {holding.get('isin', 'N/A')}")
            print(f"     CUSIP: {holding.get('securityCusip', 'N/A')}")
            print()

    # Get holdings for QQQ (Nasdaq-100 ETF)
    print("Fetching holdings for QQQ (Nasdaq-100 ETF)...")
    qqq_holdings = await client.etf.holdings("QQQ")
    print(f"Found {len(qqq_holdings)} holdings in QQQ")

    if qqq_holdings:
        print("\nQQQ Holdings Summary:")
        for i, holding in enumerate(qqq_holdings[:3]):  # Show first 3 holdings
            print(
                f"  {i + 1}. {holding.get('name', 'N/A')} ({holding.get('asset', 'N/A')})"
            )
            print(f"     Shares: {holding.get('sharesNumber', 0):,}")
            print(f"     Weight: {holding.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holding.get('marketValue', 0):,.2f}")
            print()

    # Get holdings for VTI (Total Stock Market ETF)
    print("Fetching holdings for VTI (Total Stock Market ETF)...")
    vti_holdings = await client.etf.holdings("VTI")
    print(f"Found {len(vti_holdings)} holdings in VTI")

    if vti_holdings:
        print("\nVTI Holdings Summary:")
        for i, holding in enumerate(vti_holdings[:3]):  # Show first 3 holdings
            print(
                f"  {i + 1}. {holding.get('name', 'N/A')} ({holding.get('asset', 'N/A')})"
            )
            print(f"     Shares: {holding.get('sharesNumber', 0):,}")
            print(f"     Weight: {holding.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holding.get('marketValue', 0):,.2f}")
            print()


async def info_examples(client: FmpClient) -> None:
    """Demonstrate ETF info functionality"""
    print("\n=== ETF Information Examples ===")

    # Get info for SPY
    print("Fetching information for SPY...")
    spy_info = await client.etf.info("SPY")
    print(f"Found {len(spy_info)} info records for SPY")

    if spy_info:
        print("\nSPY Information Summary:")
        info = spy_info[0]
        print(f"  Name: {info.get('name', 'N/A')}")
        print(f"  Description: {info.get('description', 'N/A')[:100]}...")
        print(f"  Asset Class: {info.get('assetClass', 'N/A')}")
        print(f"  Domicile: {info.get('domicile', 'N/A')}")
        print(f"  ETF Company: {info.get('etfCompany', 'N/A')}")
        print(f"  Expense Ratio: {info.get('expenseRatio', 'N/A')}%")
        print(
            f"  Assets Under Management: ${info.get('assetsUnderManagement', 0):,.0f}"
        )
        print(f"  Average Volume: {info.get('avgVolume', 0):,}")
        print(f"  Inception Date: {info.get('inceptionDate', 'N/A')}")
        print(f"  NAV: ${info.get('nav', 0):.2f} {info.get('navCurrency', 'N/A')}")
        print(f"  Holdings Count: {info.get('holdingsCount', 0):,}")
        print(f"  Website: {info.get('website', 'N/A')}")
        print()

    # Get info for QQQ
    print("Fetching information for QQQ...")
    qqq_info = await client.etf.info("QQQ")
    print(f"Found {len(qqq_info)} info records for QQQ")

    if qqq_info:
        print("\nQQQ Information Summary:")
        info = qqq_info[0]
        print(f"  Name: {info.get('name', 'N/A')}")
        print(f"  Asset Class: {info.get('assetClass', 'N/A')}")
        print(f"  ETF Company: {info.get('etfCompany', 'N/A')}")
        print(f"  Expense Ratio: {info.get('expenseRatio', 'N/A')}%")
        print(
            f"  Assets Under Management: ${info.get('assetsUnderManagement', 0):,.0f}"
        )
        print(f"  Holdings Count: {info.get('holdingsCount', 0):,}")
        print()

    # Get info for VTI
    print("Fetching information for VTI...")
    vti_info = await client.etf.info("VTI")
    print(f"Found {len(vti_info)} info records for VTI")

    if vti_info:
        print("\nVTI Information Summary:")
        info = vti_info[0]
        print(f"  Name: {info.get('name', 'N/A')}")
        print(f"  Asset Class: {info.get('assetClass', 'N/A')}")
        print(f"  ETF Company: {info.get('etfCompany', 'N/A')}")
        print(f"  Expense Ratio: {info.get('expenseRatio', 'N/A')}%")
        print(
            f"  Assets Under Management: ${info.get('assetsUnderManagement', 0):,.0f}"
        )
        print(f"  Holdings Count: {info.get('holdingsCount', 0):,}")
        print()


async def country_weightings_examples(client: FmpClient) -> None:
    """Demonstrate country weightings functionality"""
    print("\n=== Country Weightings Examples ===")

    # Get country weightings for SPY
    print("Fetching country weightings for SPY...")
    spy_countries = await client.etf.country_weightings("SPY")
    print(f"Found {len(spy_countries)} country weightings for SPY")

    if spy_countries:
        print("\nSPY Country Weightings:")
        for i, country in enumerate(spy_countries):
            print(
                f"  {i + 1}. {country.get('country', 'N/A')}: {country.get('weightPercentage', 'N/A')}"
            )
        print()

    # Get country weightings for VTI
    print("Fetching country weightings for VTI...")
    vti_countries = await client.etf.country_weightings("VTI")
    print(f"Found {len(vti_countries)} country weightings for VTI")

    if vti_countries:
        print("\nVTI Country Weightings:")
        for i, country in enumerate(vti_countries):
            print(
                f"  {i + 1}. {country.get('country', 'N/A')}: {country.get('weightPercentage', 'N/A')}"
            )
        print()

    # Get country weightings for IEMG (Emerging Markets)
    print("Fetching country weightings for IEMG (Emerging Markets)...")
    iemg_countries = await client.etf.country_weightings("IEMG")
    print(f"Found {len(iemg_countries)} country weightings for IEMG")

    if iemg_countries:
        print("\nIEMG Country Weightings:")
        for i, country in enumerate(iemg_countries[:10]):  # Show first 10
            print(
                f"  {i + 1}. {country.get('country', 'N/A')}: {country.get('weightPercentage', 'N/A')}"
            )
        if len(iemg_countries) > 10:
            print(f"  ... and {len(iemg_countries) - 10} more countries")
        print()


async def asset_exposure_examples(client: FmpClient) -> None:
    """Demonstrate asset exposure functionality"""
    print("\n=== Asset Exposure Examples ===")

    # Find ETFs that hold AAPL
    print("Finding ETFs that hold AAPL...")
    aapl_exposure = await client.etf.asset_exposure("AAPL")
    print(f"Found {len(aapl_exposure)} ETFs holding AAPL")

    if aapl_exposure:
        print("\nETFs Holding AAPL:")
        for i, etf in enumerate(aapl_exposure[:10]):  # Show first 10
            print(f"  {i + 1}. {etf.get('symbol', 'N/A')}")
            print(f"     Shares: {etf.get('sharesNumber', 0):,}")
            print(f"     Weight: {etf.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${etf.get('marketValue', 0):,.2f}")
            print()
        if len(aapl_exposure) > 10:
            print(f"  ... and {len(aapl_exposure) - 10} more ETFs")

    # Find ETFs that hold MSFT
    print("Finding ETFs that hold MSFT...")
    msft_exposure = await client.etf.asset_exposure("MSFT")
    print(f"Found {len(msft_exposure)} ETFs holding MSFT")

    if msft_exposure:
        print("\nETFs Holding MSFT:")
        for i, etf in enumerate(msft_exposure[:5]):  # Show first 5
            print(f"  {i + 1}. {etf.get('symbol', 'N/A')}")
            print(f"     Shares: {etf.get('sharesNumber', 0):,}")
            print(f"     Weight: {etf.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${etf.get('marketValue', 0):,.2f}")
            print()

    # Find ETFs that hold GOOGL
    print("Finding ETFs that hold GOOGL...")
    googl_exposure = await client.etf.asset_exposure("GOOGL")
    print(f"Found {len(googl_exposure)} ETFs holding GOOGL")

    if googl_exposure:
        print("\nETFs Holding GOOGL:")
        for i, etf in enumerate(googl_exposure[:5]):  # Show first 5
            print(f"  {i + 1}. {etf.get('symbol', 'N/A')}")
            print(f"     Shares: {etf.get('sharesNumber', 0):,}")
            print(f"     Weight: {etf.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${etf.get('marketValue', 0):,.2f}")
            print()


async def sector_weightings_examples(client: FmpClient) -> None:
    """Demonstrate sector weightings functionality"""
    print("\n=== Sector Weightings Examples ===")

    # Get sector weightings for SPY
    print("Fetching sector weightings for SPY...")
    spy_sectors = await client.etf.sector_weightings("SPY")
    print(f"Found {len(spy_sectors)} sector weightings for SPY")

    if spy_sectors:
        print("\nSPY Sector Weightings:")
        for i, sector in enumerate(spy_sectors):
            print(
                f"  {i + 1}. {sector.get('sector', 'N/A')}: {sector.get('weightPercentage', 0):.2f}%"
            )
        print()

    # Get sector weightings for QQQ
    print("Fetching sector weightings for QQQ...")
    qqq_sectors = await client.etf.sector_weightings("QQQ")
    print(f"Found {len(qqq_sectors)} sector weightings for QQQ")

    if qqq_sectors:
        print("\nQQQ Sector Weightings:")
        for i, sector in enumerate(qqq_sectors):
            print(
                f"  {i + 1}. {sector.get('sector', 'N/A')}: {sector.get('weightPercentage', 0):.2f}%"
            )
        print()

    # Get sector weightings for VTI
    print("Fetching sector weightings for VTI...")
    vti_sectors = await client.etf.sector_weightings("VTI")
    print(f"Found {len(vti_sectors)} sector weightings for VTI")

    if vti_sectors:
        print("\nVTI Sector Weightings:")
        for i, sector in enumerate(vti_sectors):
            print(
                f"  {i + 1}. {sector.get('sector', 'N/A')}: {sector.get('weightPercentage', 0):.2f}%"
            )
        print()


async def disclosure_holders_examples(client: FmpClient) -> None:
    """Demonstrate disclosure holders functionality"""
    print("\n=== Disclosure Holders Examples ===")

    # Get latest disclosure holders for AAPL
    print("Fetching latest disclosure holders for AAPL...")
    aapl_disclosures = await client.etf.disclosure_holders_latest("AAPL")
    print(f"Found {len(aapl_disclosures)} disclosure holders for AAPL")

    if aapl_disclosures:
        print("\nLatest Disclosure Holders for AAPL:")
        for i, holder in enumerate(aapl_disclosures[:10]):  # Show first 10
            print(f"  {i + 1}. {holder.get('holder', 'N/A')}")
            print(f"     Shares: {holder.get('shares', 0):,}")
            print(f"     Weight: {holder.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holder.get('marketValue', 0):,.2f}")
            print()
        if len(aapl_disclosures) > 10:
            print(f"  ... and {len(aapl_disclosures) - 10} more holders")

    # Get latest disclosure holders for MSFT
    print("Fetching latest disclosure holders for MSFT...")
    msft_disclosures = await client.etf.disclosure_holders_latest("MSFT")
    print(f"Found {len(msft_disclosures)} disclosure holders for MSFT")

    if msft_disclosures:
        print("\nLatest Disclosure Holders for MSFT:")
        for i, holder in enumerate(msft_disclosures[:5]):  # Show first 5
            print(f"  {i + 1}. {holder.get('holder', 'N/A')}")
            print(f"     Shares: {holder.get('shares', 0):,}")
            print(f"     Weight: {holder.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holder.get('marketValue', 0):,.2f}")
            print()

    # Get latest disclosure holders for GOOGL
    print("Fetching latest disclosure holders for GOOGL...")
    googl_disclosures = await client.etf.disclosure_holders_latest("GOOGL")
    print(f"Found {len(googl_disclosures)} disclosure holders for GOOGL")

    if googl_disclosures:
        print("\nLatest Disclosure Holders for GOOGL:")
        for i, holder in enumerate(googl_disclosures[:5]):  # Show first 5
            print(f"  {i + 1}. {holder.get('holder', 'N/A')}")
            print(f"     Shares: {holder.get('shares', 0):,}")
            print(f"     Weight: {holder.get('weightPercentage', 0):.2f}%")
            print(f"     Market Value: ${holder.get('marketValue', 0):,.2f}")
            print()


async def etf_analysis_examples(client: FmpClient) -> None:
    """Demonstrate ETF analysis functionality"""
    print("\n=== ETF Analysis Examples ===")

    # Analyze SPY vs QQQ
    print("Analyzing SPY vs QQQ...")

    # Get info for both ETFs
    spy_info = await client.etf.info("SPY")
    qqq_info = await client.etf.info("QQQ")

    if spy_info and qqq_info:
        print("\nSPY vs QQQ Comparison:")
        spy = spy_info[0]
        qqq = qqq_info[0]

        print(f"  SPY - {spy.get('name', 'N/A')}:")
        print(f"    Expense Ratio: {spy.get('expenseRatio', 'N/A')}%")
        print(f"    AUM: ${spy.get('assetsUnderManagement', 0):,.0f}")
        print(f"    Holdings Count: {spy.get('holdingsCount', 0):,}")
        print(f"    Inception: {spy.get('inceptionDate', 'N/A')}")

        print(f"  QQQ - {qqq.get('name', 'N/A')}:")
        print(f"    Expense Ratio: {qqq.get('expenseRatio', 'N/A')}%")
        print(f"    AUM: ${qqq.get('assetsUnderManagement', 0):,.0f}")
        print(f"    Holdings Count: {qqq.get('holdingsCount', 0):,}")
        print(f"    Inception: {qqq.get('inceptionDate', 'N/A')}")

        # Compare expense ratios
        spy_expense = spy.get("expenseRatio", 0)
        qqq_expense = qqq.get("expenseRatio", 0)
        if spy_expense > 0 and qqq_expense > 0:
            if spy_expense < qqq_expense:
                print(
                    f"\n  Analysis: SPY has lower expense ratio ({spy_expense}% vs {qqq_expense}%)"
                )
            elif qqq_expense < spy_expense:
                print(
                    f"\n  Analysis: QQQ has lower expense ratio ({qqq_expense}% vs {spy_expense}%)"
                )
            else:
                print(
                    f"\n  Analysis: Both ETFs have the same expense ratio ({spy_expense}%)"
                )

    # Analyze sector concentration
    print("\nAnalyzing sector concentration...")

    spy_sectors = await client.etf.sector_weightings("SPY")
    qqq_sectors = await client.etf.sector_weightings("QQQ")

    if spy_sectors and qqq_sectors:
        print("\nSector Concentration Analysis:")

        # Find top sectors for each ETF
        spy_top_sectors = sorted(
            spy_sectors, key=lambda x: x.get("weightPercentage", 0), reverse=True
        )[:3]
        qqq_top_sectors = sorted(
            qqq_sectors, key=lambda x: x.get("weightPercentage", 0), reverse=True
        )[:3]

        print("  SPY Top Sectors:")
        for i, sector in enumerate(spy_top_sectors):
            print(
                f"    {i + 1}. {sector.get('sector', 'N/A')}: {sector.get('weightPercentage', 0):.2f}%"
            )

        print("  QQQ Top Sectors:")
        for i, sector in enumerate(qqq_top_sectors):
            print(
                f"    {i + 1}. {sector.get('sector', 'N/A')}: {sector.get('weightPercentage', 0):.2f}%"
            )

        # Check for sector concentration
        spy_concentration = sum(s.get("weightPercentage", 0) for s in spy_top_sectors)
        qqq_concentration = sum(s.get("weightPercentage", 0) for s in qqq_top_sectors)

        print("\n  Sector Concentration (Top 3):")
        print(f"    SPY: {spy_concentration:.2f}%")
        print(f"    QQQ: {qqq_concentration:.2f}%")

        if spy_concentration > 50 or qqq_concentration > 50:
            print(
                "    Note: High sector concentration (>50%) indicates concentrated risk"
            )
        else:
            print(
                "    Note: Moderate sector concentration indicates diversified exposure"
            )


async def etf_portfolio_analysis(client: FmpClient) -> None:
    """Demonstrate ETF portfolio analysis functionality"""
    print("\n=== ETF Portfolio Analysis Examples ===")

    # Analyze a hypothetical portfolio
    portfolio = {
        "SPY": 0.40,  # 40% allocation
        "QQQ": 0.30,  # 30% allocation
        "VTI": 0.20,  # 20% allocation
        "IEMG": 0.10,  # 10% allocation
    }

    print(f"Analyzing portfolio: {portfolio}")

    total_expense_ratio = 0
    total_holdings = 0
    sector_exposure = {}
    country_exposure = {}

    for etf, allocation in portfolio.items():
        print(f"\n--- Analyzing {etf} ({allocation * 100:.0f}% allocation) ---")

        try:
            # Get ETF info
            info = await client.etf.info(etf)
            if info:
                info = info[0]
                expense_ratio = info.get("expenseRatio", 0)
                holdings_count = info.get("holdingsCount", 0)

                print(f"  Expense Ratio: {expense_ratio}%")
                print(f"  Holdings Count: {holdings_count:,}")
                print(f"  AUM: ${info.get('assetsUnderManagement', 0):,.0f}")

                # Calculate weighted metrics
                total_expense_ratio += expense_ratio * allocation
                total_holdings += holdings_count * allocation

            # Get sector weightings
            sectors = await client.etf.sector_weightings(etf)
            if sectors:
                print("  Top Sectors:")
                for i, sector in enumerate(sectors[:3]):
                    sector_name = sector.get("sector", "N/A")
                    weight = sector.get("weightPercentage", 0)
                    print(f"    {i + 1}. {sector_name}: {weight:.2f}%")

                    # Aggregate sector exposure
                    if sector_name not in sector_exposure:
                        sector_exposure[sector_name] = 0
                    sector_exposure[sector_name] += weight * allocation

            # Get country weightings
            countries = await client.etf.country_weightings(etf)
            if countries:
                print("  Top Countries:")
                for i, country in enumerate(countries[:3]):
                    country_name = country.get("country", "N/A")
                    weight = country.get("weightPercentage", "N/A")
                    print(f"    {i + 1}. {country_name}: {weight}")

                    # Aggregate country exposure
                    if country_name not in country_exposure:
                        country_exposure[country_name] = 0
                    # Convert percentage string to float
                    try:
                        weight_float = float(str(weight).replace("%", ""))
                        country_exposure[country_name] += weight_float * allocation
                    except ValueError:
                        pass

        except Exception as e:
            print(f"  Error analyzing {etf}: {e}")

    # Portfolio summary
    print("\n=== Portfolio Summary ===")
    print(f"Total Weighted Expense Ratio: {total_expense_ratio:.3f}%")
    print(f"Total Weighted Holdings Count: {total_holdings:,.0f}")

    # Top sector exposures
    top_sectors = sorted(sector_exposure.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop Sector Exposures:")
    for i, (sector, exposure) in enumerate(top_sectors):
        print(f"  {i + 1}. {sector}: {exposure:.2f}%")

    # Top country exposures
    top_countries = sorted(country_exposure.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]
    print("\nTop Country Exposures:")
    for i, (country, exposure) in enumerate(top_countries):
        print(f"  {i + 1}. {country}: {exposure:.2f}%")

    # Risk assessment
    print("\nRisk Assessment:")
    if total_expense_ratio > 0.5:
        print(f"  ⚠️  High expense ratio: {total_expense_ratio:.3f}%")
    elif total_expense_ratio > 0.2:
        print(f"  ⚠️  Moderate expense ratio: {total_expense_ratio:.3f}%")
    else:
        print(f"  ✅ Low expense ratio: {total_expense_ratio:.3f}%")

    if total_holdings > 2000:
        print(f"  ✅ High diversification: {total_holdings:,.0f} holdings")
    elif total_holdings > 500:
        print(f"  ⚠️  Moderate diversification: {total_holdings:,.0f} holdings")
    else:
        print(f"  ⚠️  Low diversification: {total_holdings:,.0f} holdings")


async def main() -> None:
    """Main function demonstrating FMP ETF And Mutual Funds functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP ETF And Mutual Funds Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await holdings_examples(client)
            await info_examples(client)
            await country_weightings_examples(client)
            await asset_exposure_examples(client)
            await sector_weightings_examples(client)
            await disclosure_holders_examples(client)
            await etf_analysis_examples(client)
            await etf_portfolio_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
