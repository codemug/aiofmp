#!/usr/bin/env python3
"""
Example script demonstrating FMP Economics category functionality

This script shows how to use the FMP client to access economics data including
treasury rates, economic indicators, economic data releases calendar, and market risk premium.
"""

import asyncio
import os
from datetime import datetime, timedelta

from aiofmp import FmpClient


async def treasury_rates_examples(client: FmpClient) -> None:
    """Demonstrate treasury rates functionality"""
    print("\n=== Treasury Rates Examples ===")

    # Get current treasury rates
    print("Fetching current treasury rates...")
    treasury_rates = await client.economics.treasury_rates()
    print(f"Found {len(treasury_rates)} treasury rates records")

    if treasury_rates:
        print("\nTreasury Rates Summary:")
        for i, record in enumerate(treasury_rates[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print("     Short-term rates:")
            print(f"       1 Month: {record.get('month1', 'N/A')}%")
            print(f"       2 Month: {record.get('month2', 'N/A')}%")
            print(f"       3 Month: {record.get('month3', 'N/A')}%")
            print(f"       6 Month: {record.get('month6', 'N/A')}%")
            print("     Medium-term rates:")
            print(f"       1 Year: {record.get('year1', 'N/A')}%")
            print(f"       2 Year: {record.get('year2', 'N/A')}%")
            print(f"       3 Year: {record.get('year3', 'N/A')}%")
            print(f"       5 Year: {record.get('year5', 'N/A')}%")
            print(f"       7 Year: {record.get('year7', 'N/A')}%")
            print("     Long-term rates:")
            print(f"       10 Year: {record.get('year10', 'N/A')}%")
            print(f"       20 Year: {record.get('year20', 'N/A')}%")
            print(f"       30 Year: {record.get('year30', 'N/A')}%")
            print()

    # Get treasury rates for a specific date range
    print("Fetching treasury rates for Q1 2024...")
    q1_rates = await client.economics.treasury_rates("2024-01-01", "2024-03-31")
    print(f"Found {len(q1_rates)} Q1 2024 treasury rates records")

    if q1_rates:
        print("\nQ1 2024 Treasury Rates Summary:")
        for i, record in enumerate(q1_rates[:2]):  # Show first 2 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     10 Year: {record.get('year10', 'N/A')}%")
            print(f"     30 Year: {record.get('year30', 'N/A')}%")
            print()

    # Get treasury rates for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    print(
        f"Fetching treasury rates for last 30 days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})..."
    )
    recent_rates = await client.economics.treasury_rates(
        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )
    print(f"Found {len(recent_rates)} recent treasury rates records")

    if recent_rates:
        print("\nRecent Treasury Rates Summary:")
        for i, record in enumerate(recent_rates[:2]):  # Show first 2 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     2 Year: {record.get('year2', 'N/A')}%")
            print(f"     10 Year: {record.get('year10', 'N/A')}%")
            print()


async def economic_indicators_examples(client: FmpClient) -> None:
    """Demonstrate economic indicators functionality"""
    print("\n=== Economic Indicators Examples ===")

    # Get GDP data
    print("Fetching GDP data for 2024...")
    gdp_data = await client.economics.economic_indicators(
        "GDP", "2024-01-01", "2024-12-31"
    )
    print(f"Found {len(gdp_data)} GDP records")

    if gdp_data:
        print("\nGDP Data Summary:")
        for i, record in enumerate(gdp_data[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Value: ${record.get('value', 0):,.0f} billion")
            print()

    # Get CPI (Consumer Price Index) data
    print("Fetching CPI data for 2024...")
    cpi_data = await client.economics.economic_indicators(
        "CPI", "2024-01-01", "2024-12-31"
    )
    print(f"Found {len(cpi_data)} CPI records")

    if cpi_data:
        print("\nCPI Data Summary:")
        for i, record in enumerate(cpi_data[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Value: {record.get('value', 0):.3f}")
            print()

    # Get unemployment rate data
    print("Fetching unemployment rate data for 2024...")
    unemployment_data = await client.economics.economic_indicators(
        "unemploymentRate", "2024-01-01", "2024-12-31"
    )
    print(f"Found {len(unemployment_data)} unemployment rate records")

    if unemployment_data:
        print("\nUnemployment Rate Data Summary:")
        for i, record in enumerate(unemployment_data[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Rate: {record.get('value', 0):.1f}%")
            print()

    # Get federal funds rate data
    print("Fetching federal funds rate data for 2024...")
    fed_funds_data = await client.economics.economic_indicators(
        "federalFunds", "2024-01-01", "2024-12-31"
    )
    print(f"Found {len(fed_funds_data)} federal funds rate records")

    if fed_funds_data:
        print("\nFederal Funds Rate Data Summary:")
        for i, record in enumerate(fed_funds_data[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Rate: {record.get('value', 0):.2f}%")
            print()

    # Get inflation rate data
    print("Fetching inflation rate data for 2024...")
    inflation_data = await client.economics.economic_indicators(
        "inflationRate", "2024-01-01", "2024-12-31"
    )
    print(f"Found {len(inflation_data)} inflation rate records")

    if inflation_data:
        print("\nInflation Rate Data Summary:")
        for i, record in enumerate(inflation_data[:3]):  # Show first 3 records
            print(f"  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Rate: {record.get('value', 0):.2f}%")
            print()


async def economic_calendar_examples(client: FmpClient) -> None:
    """Demonstrate economic calendar functionality"""
    print("\n=== Economic Calendar Examples ===")

    # Get economic calendar for the next 30 days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    print(
        f"Fetching economic calendar for next 30 days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})..."
    )
    calendar_data = await client.economics.economic_calendar(
        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )
    print(f"Found {len(calendar_data)} economic calendar events")

    if calendar_data:
        print("\nEconomic Calendar Summary:")
        for i, event in enumerate(calendar_data[:10]):  # Show first 10 events
            print(f"  {i + 1}. Date: {event.get('date', 'N/A')}")
            print(f"     Country: {event.get('country', 'N/A')}")
            print(f"     Event: {event.get('event', 'N/A')}")
            print(f"     Currency: {event.get('currency', 'N/A')}")
            print(f"     Previous: {event.get('previous', 'N/A')}")
            print(f"     Estimate: {event.get('estimate', 'N/A')}")
            print(f"     Actual: {event.get('actual', 'N/A')}")
            print(f"     Change: {event.get('change', 'N/A')}")
            print(f"     Impact: {event.get('impact', 'N/A')}")
            print(f"     Change %: {event.get('changePercentage', 'N/A')}%")
            print()

    # Get economic calendar for a specific month
    print("Fetching economic calendar for March 2024...")
    march_calendar = await client.economics.economic_calendar(
        "2024-03-01", "2024-03-31"
    )
    print(f"Found {len(march_calendar)} March 2024 economic events")

    if march_calendar:
        print("\nMarch 2024 Economic Calendar Summary:")
        for i, event in enumerate(march_calendar[:5]):  # Show first 5 events
            print(f"  {i + 1}. Date: {event.get('date', 'N/A')}")
            print(f"     Country: {event.get('country', 'N/A')}")
            print(f"     Event: {event.get('event', 'N/A')}")
            print(f"     Impact: {event.get('impact', 'N/A')}")
            print()


async def market_risk_premium_examples(client: FmpClient) -> None:
    """Demonstrate market risk premium functionality"""
    print("\n=== Market Risk Premium Examples ===")

    # Get market risk premium data for all countries
    print("Fetching market risk premium data...")
    risk_premium_data = await client.economics.market_risk_premium()
    print(f"Found {len(risk_premium_data)} market risk premium records")

    if risk_premium_data:
        print("\nMarket Risk Premium Summary:")

        # Group by continent
        continents = {}
        for record in risk_premium_data:
            continent = record.get("continent", "Unknown")
            if continent not in continents:
                continents[continent] = []
            continents[continent].append(record)

        for continent, countries in continents.items():
            print(f"\n  {continent} Continent:")
            for i, country in enumerate(countries[:5]):  # Show first 5 per continent
                print(f"    {i + 1}. {country.get('country', 'N/A')}")
                print(
                    f"       Country Risk Premium: {country.get('countryRiskPremium', 'N/A')}%"
                )
                print(
                    f"       Total Equity Risk Premium: {country.get('totalEquityRiskPremium', 'N/A')}%"
                )
            if len(countries) > 5:
                print(f"       ... and {len(countries) - 5} more countries")

        # Show some specific examples
        print("\nSample Market Risk Premium Data:")
        for i, record in enumerate(risk_premium_data[:10]):
            print(
                f"  {i + 1:2d}. {record.get('country', 'N/A'):<20} - CRP: {record.get('countryRiskPremium', 'N/A'):>6}%, TERP: {record.get('totalEquityRiskPremium', 'N/A'):>6}%"
            )


async def economic_analysis_examples(client: FmpClient) -> None:
    """Demonstrate economic analysis functionality"""
    print("\n=== Economic Analysis Examples ===")

    # Analyze yield curve using treasury rates
    print("Analyzing yield curve using treasury rates...")
    treasury_rates = await client.economics.treasury_rates("2024-01-01", "2024-12-31")

    if treasury_rates:
        print(f"\nYield Curve Analysis (based on {len(treasury_rates)} data points):")

        # Get the most recent data
        latest = treasury_rates[0]
        print(f"  Latest Date: {latest.get('date', 'N/A')}")
        print("  Yield Curve:")
        print(f"    2 Year: {latest.get('year2', 'N/A')}%")
        print(f"    5 Year: {latest.get('year5', 'N/A')}%")
        print(f"    10 Year: {latest.get('year10', 'N/A')}%")
        print(f"    30 Year: {latest.get('year30', 'N/A')}%")

        # Calculate yield curve spreads
        year2 = latest.get("year2", 0)
        year10 = latest.get("year10", 0)
        year30 = latest.get("year30", 0)

        if year2 > 0 and year10 > 0:
            spread_2_10 = year10 - year2
            print(f"  2-10 Year Spread: {spread_2_10:+.2f}%")
            if spread_2_10 > 0:
                print("  Yield Curve: Normal (upward sloping)")
            elif spread_2_10 < 0:
                print("  Yield Curve: Inverted (downward sloping)")
            else:
                print("  Yield Curve: Flat")

        if year10 > 0 and year30 > 0:
            spread_10_30 = year30 - year10
            print(f"  10-30 Year Spread: {spread_10_30:+.2f}%")

    # Analyze economic indicators trends
    print("\nAnalyzing economic indicators trends...")

    # Get multiple indicators for comparison
    indicators = ["GDP", "CPI", "unemploymentRate", "federalFunds"]

    for indicator in indicators:
        try:
            data = await client.economics.economic_indicators(
                indicator, "2024-01-01", "2024-12-31"
            )
            if data:
                print(f"\n  {indicator} Trend Analysis:")
                print(f"    Records found: {len(data)}")

                # Show first and last values if available
                if len(data) >= 2:
                    first = data[-1]  # Oldest (last in list)
                    last = data[0]  # Newest (first in list)

                    first_value = first.get("value", 0)
                    last_value = last.get("value", 0)

                    if isinstance(first_value, (int, float)) and isinstance(
                        last_value, (int, float)
                    ):
                        if first_value != 0:
                            change_pct = (
                                (last_value - first_value) / first_value
                            ) * 100
                            print(
                                f"    Change: {first_value} → {last_value} ({change_pct:+.2f}%)"
                            )
                        else:
                            print(f"    Values: {first_value} → {last_value}")
                    else:
                        print(f"    Values: {first_value} → {last_value}")
                else:
                    print(f"    Single value: {data[0].get('value', 'N/A')}")

        except Exception as e:
            print(f"  Error analyzing {indicator}: {e}")


async def economic_calendar_impact_analysis(client: FmpClient) -> None:
    """Demonstrate economic calendar impact analysis"""
    print("\n=== Economic Calendar Impact Analysis ===")

    # Get economic calendar for the next 7 days
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    print(
        f"Analyzing economic calendar impact for next 7 days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})..."
    )

    calendar_data = await client.economics.economic_calendar(
        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    )

    if calendar_data:
        print(f"\nFound {len(calendar_data)} upcoming economic events")

        # Group by impact level
        impact_levels = {}
        for event in calendar_data:
            impact = event.get("impact", "Unknown")
            if impact not in impact_levels:
                impact_levels[impact] = []
            impact_levels[impact].append(event)

        print("\nEvents by Impact Level:")
        for impact, events in impact_levels.items():
            print(f"\n  {impact} Impact Events ({len(events)}):")
            for i, event in enumerate(events[:3]):  # Show first 3 per impact level
                print(
                    f"    {i + 1}. {event.get('date', 'N/A')} - {event.get('country', 'N/A')}: {event.get('event', 'N/A')}"
                )
            if len(events) > 3:
                print(f"    ... and {len(events) - 3} more")

        # Group by country
        countries = {}
        for event in calendar_data:
            country = event.get("country", "Unknown")
            if country not in countries:
                countries[country] = []
            countries[country].append(event)

        print("\nEvents by Country:")
        for country, events in countries.items():
            print(f"  {country}: {len(events)} events")

        # Show high-impact events
        high_impact = [e for e in calendar_data if e.get("impact") == "High"]
        if high_impact:
            print("\nHigh Impact Events to Watch:")
            for i, event in enumerate(high_impact[:5]):
                print(
                    f"  {i + 1}. {event.get('date', 'N/A')} - {event.get('country', 'N/A')}"
                )
                print(f"     Event: {event.get('event', 'N/A')}")
                print(f"     Currency: {event.get('currency', 'N/A')}")
                print(f"     Previous: {event.get('previous', 'N/A')}")
                print(f"     Estimate: {event.get('estimate', 'N/A')}")
                print()


async def main() -> None:
    """Main function demonstrating FMP Economics functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Economics Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await treasury_rates_examples(client)
            await economic_indicators_examples(client)
            await economic_calendar_examples(client)
            await market_risk_premium_examples(client)
            await economic_analysis_examples(client)
            await economic_calendar_impact_analysis(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
