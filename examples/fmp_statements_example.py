#!/usr/bin/env python3
"""
Example script demonstrating FMP Statements category functionality

This script shows how to use the FMP client to access financial statement data including
income statements, balance sheets, cash flow statements, key metrics, financial ratios,
and growth analysis for comprehensive financial analysis.
"""

import asyncio
import os

from aiofmp import FmpClient


async def income_statement_examples(client: FmpClient) -> None:
    """Demonstrate income statement functionality"""
    print("\n=== Income Statement Examples ===")

    # Get income statement for Apple
    print("Fetching income statement for Apple (AAPL)...")
    income_stmt = await client.statements.income_statement(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(income_stmt)} income statement records for AAPL")

    if income_stmt:
        print("\nAAPL Income Statement Summary (Latest 5 Years):")
        for i, record in enumerate(income_stmt):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,}")
            print(f"     Cost of Revenue: ${record.get('costOfRevenue', 0):,}")
            print(f"     Gross Profit: ${record.get('grossProfit', 0):,}")
            print(f"     Operating Expenses: ${record.get('operatingExpenses', 0):,}")
            print(f"     Operating Income: ${record.get('operatingIncome', 0):,}")
            print(f"     Net Income: ${record.get('netIncome', 0):,}")
            print(f"     EPS: ${record.get('eps', 0):.2f}")
            print(f"     EPS Diluted: ${record.get('epsDiluted', 0):.2f}")

    # Get income statement for Microsoft
    print("\nFetching income statement for Microsoft (MSFT)...")
    msft_income = await client.statements.income_statement(
        "MSFT", limit=3, period="annual"
    )
    print(f"Found {len(msft_income)} income statement records for MSFT")

    if msft_income:
        print("\nMSFT Income Statement Summary (Latest 3 Years):")
        for i, record in enumerate(msft_income):
            print(f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')}")
            print(f"     Revenue: ${record.get('revenue', 0):,}")
            print(f"     Net Income: ${record.get('netIncome', 0):,}")
            print(f"     EPS: ${record.get('eps', 0):.2f}")


async def balance_sheet_examples(client: FmpClient) -> None:
    """Demonstrate balance sheet functionality"""
    print("\n=== Balance Sheet Examples ===")

    # Get balance sheet for Apple
    print("Fetching balance sheet for Apple (AAPL)...")
    balance_sheet = await client.statements.balance_sheet_statement(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(balance_sheet)} balance sheet records for AAPL")

    if balance_sheet:
        print("\nAAPL Balance Sheet Summary (Latest 5 Years):")
        for i, record in enumerate(balance_sheet):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Total Assets: ${record.get('totalAssets', 0):,}")
            print(f"     Total Liabilities: ${record.get('totalLiabilities', 0):,}")
            print(
                f"     Total Stockholders' Equity: ${record.get('totalStockholdersEquity', 0):,}"
            )
            print(
                f"     Cash & Cash Equivalents: ${record.get('cashAndCashEquivalents', 0):,}"
            )
            print(f"     Total Debt: ${record.get('totalDebt', 0):,}")
            print(f"     Net Debt: ${record.get('netDebt', 0):,}")

            # Calculate key ratios
            total_assets = record.get("totalAssets", 0)
            total_liabilities = record.get("totalLiabilities", 0)
            total_equity = record.get("totalStockholdersEquity", 0)

            if total_assets > 0:
                debt_to_assets = total_liabilities / total_assets
                print(f"     Debt-to-Assets Ratio: {debt_to_assets:.3f}")

            if total_equity > 0:
                debt_to_equity = total_liabilities / total_equity
                print(f"     Debt-to-Equity Ratio: {debt_to_equity:.3f}")


async def cash_flow_examples(client: FmpClient) -> None:
    """Demonstrate cash flow statement functionality"""
    print("\n=== Cash Flow Statement Examples ===")

    # Get cash flow statement for Apple
    print("Fetching cash flow statement for Apple (AAPL)...")
    cash_flow = await client.statements.cash_flow_statement(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(cash_flow)} cash flow records for AAPL")

    if cash_flow:
        print("\nAAPL Cash Flow Summary (Latest 5 Years):")
        for i, record in enumerate(cash_flow):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Net Income: ${record.get('netIncome', 0):,}")
            print(f"     Operating Cash Flow: ${record.get('operatingCashFlow', 0):,}")
            print(f"     Investing Cash Flow: ${record.get('investingCashFlow', 0):,}")
            print(f"     Financing Cash Flow: ${record.get('financingCashFlow', 0):,}")
            print(f"     Free Cash Flow: ${record.get('freeCashFlow', 0):,}")
            print(f"     Capital Expenditure: ${record.get('capitalExpenditure', 0):,}")

            # Calculate cash flow ratios
            net_income = record.get("netIncome", 0)
            operating_cf = record.get("operatingCashFlow", 0)
            free_cf = record.get("freeCashFlow", 0)

            if net_income > 0 and operating_cf > 0:
                cf_to_income = operating_cf / net_income
                print(f"     Cash Flow to Net Income Ratio: {cf_to_income:.3f}")

            if operating_cf > 0 and free_cf > 0:
                fcf_to_ocf = free_cf / operating_cf
                print(f"     Free Cash Flow to Operating CF Ratio: {fcf_to_ocf:.3f}")


async def key_metrics_examples(client: FmpClient) -> None:
    """Demonstrate key metrics functionality"""
    print("\n=== Key Metrics Examples ===")

    # Get key metrics for Apple
    print("Fetching key metrics for Apple (AAPL)...")
    key_metrics = await client.statements.key_metrics("AAPL", limit=5, period="annual")
    print(f"Found {len(key_metrics)} key metrics records for AAPL")

    if key_metrics:
        print("\nAAPL Key Metrics Summary (Latest 5 Years):")
        for i, record in enumerate(key_metrics):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Market Cap: ${record.get('marketCap', 0):,}")
            print(f"     Enterprise Value: ${record.get('enterpriseValue', 0):,}")
            print(f"     EV/Sales: {record.get('evToSales', 0):.2f}")
            print(f"     EV/EBITDA: {record.get('evToEBITDA', 0):.2f}")
            print(f"     Current Ratio: {record.get('currentRatio', 0):.3f}")
            print(f"     Return on Assets: {record.get('returnOnAssets', 0):.3f}")
            print(f"     Return on Equity: {record.get('returnOnEquity', 0):.3f}")
            print(f"     Working Capital: ${record.get('workingCapital', 0):,}")

            # Calculate additional ratios
            market_cap = record.get("marketCap", 0)
            enterprise_value = record.get("enterpriseValue", 0)

            if market_cap > 0 and enterprise_value > 0:
                ev_to_mc_ratio = enterprise_value / market_cap
                print(
                    f"     Enterprise Value to Market Cap Ratio: {ev_to_mc_ratio:.3f}"
                )


async def financial_ratios_examples(client: FmpClient) -> None:
    """Demonstrate financial ratios functionality"""
    print("\n=== Financial Ratios Examples ===")

    # Get financial ratios for Apple
    print("Fetching financial ratios for Apple (AAPL)...")
    financial_ratios = await client.statements.financial_ratios(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(financial_ratios)} financial ratios records for AAPL")

    if financial_ratios:
        print("\nAAPL Financial Ratios Summary (Latest 5 Years):")
        for i, record in enumerate(financial_ratios):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")

            # Profitability ratios
            print("     Profitability Ratios:")
            print(
                f"       Gross Profit Margin: {record.get('grossProfitMargin', 0):.3f}"
            )
            print(f"       EBIT Margin: {record.get('ebitMargin', 0):.3f}")
            print(f"       Net Profit Margin: {record.get('netProfitMargin', 0):.3f}")

            # Liquidity ratios
            print("     Liquidity Ratios:")
            print(f"       Current Ratio: {record.get('currentRatio', 0):.3f}")
            print(f"       Quick Ratio: {record.get('quickRatio', 0):.3f}")
            print(f"       Cash Ratio: {record.get('cashRatio', 0):.3f}")

            # Efficiency ratios
            print("     Efficiency Ratios:")
            print(f"       Asset Turnover: {record.get('assetTurnover', 0):.3f}")
            print(
                f"       Inventory Turnover: {record.get('inventoryTurnover', 0):.3f}"
            )
            print(
                f"       Receivables Turnover: {record.get('receivablesTurnover', 0):.3f}"
            )

            # Valuation ratios
            print("     Valuation Ratios:")
            print(f"       P/E Ratio: {record.get('priceToEarningsRatio', 0):.2f}")
            print(f"       P/B Ratio: {record.get('priceToBookRatio', 0):.2f}")
            print(f"       P/S Ratio: {record.get('priceToSalesRatio', 0):.2f}")

            # Leverage ratios
            print("     Leverage Ratios:")
            print(f"       Debt-to-Assets: {record.get('debtToAssetsRatio', 0):.3f}")
            print(f"       Debt-to-Equity: {record.get('debtToEquityRatio', 0):.3f}")
            print(
                f"       Financial Leverage: {record.get('financialLeverageRatio', 0):.3f}"
            )


async def financial_scores_examples(client: FmpClient) -> None:
    """Demonstrate financial scores functionality"""
    print("\n=== Financial Scores Examples ===")

    # Get financial scores for Apple
    print("Fetching financial scores for Apple (AAPL)...")
    financial_scores = await client.statements.financial_scores("AAPL")
    print(f"Found {len(financial_scores)} financial scores records for AAPL")

    if financial_scores:
        print("\nAAPL Financial Health Scores:")
        for record in financial_scores:
            print(f"  Symbol: {record.get('symbol', 'N/A')}")
            print(f"  Currency: {record.get('reportedCurrency', 'N/A')}")
            print(f"  Altman Z-Score: {record.get('altmanZScore', 0):.3f}")
            print(f"  Piotroski Score: {record.get('piotroskiScore', 0)}/9")
            print(f"  Working Capital: ${record.get('workingCapital', 0):,}")
            print(f"  Total Assets: ${record.get('totalAssets', 0):,}")
            print(f"  EBIT: ${record.get('ebit', 0):,}")
            print(f"  Market Cap: ${record.get('marketCap', 0):,}")
            print(f"  Total Liabilities: ${record.get('totalLiabilities', 0):,}")
            print(f"  Revenue: ${record.get('revenue', 0):,}")

            # Interpret Altman Z-Score
            altman_score = record.get("altmanZScore", 0)
            if altman_score > 3.0:
                print(f"  🟢 Altman Z-Score: {altman_score:.3f} - Safe Zone (>3.0)")
            elif altman_score > 1.8:
                print(f"  🟡 Altman Z-Score: {altman_score:.3f} - Grey Zone (1.8-3.0)")
            else:
                print(f"  🔴 Altman Z-Score: {altman_score:.3f} - Distress Zone (<1.8)")

            # Interpret Piotroski Score
            piotroski_score = record.get("piotroskiScore", 0)
            if piotroski_score >= 7:
                print(
                    f"  🟢 Piotroski Score: {piotroski_score}/9 - Strong Financial Health (≥7)"
                )
            elif piotroski_score >= 4:
                print(
                    f"  🟡 Piotroski Score: {piotroski_score}/9 - Moderate Financial Health (4-6)"
                )
            else:
                print(
                    f"  🔴 Piotroski Score: {piotroski_score}/9 - Weak Financial Health (<4)"
                )


async def owner_earnings_examples(client: FmpClient) -> None:
    """Demonstrate owner earnings functionality"""
    print("\n=== Owner Earnings Examples ===")

    # Get owner earnings for Apple
    print("Fetching owner earnings for Apple (AAPL)...")
    owner_earnings = await client.statements.owner_earnings("AAPL", limit=5)
    print(f"Found {len(owner_earnings)} owner earnings records for AAPL")

    if owner_earnings:
        print("\nAAPL Owner Earnings Summary (Latest 5 Periods):")
        for i, record in enumerate(owner_earnings):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Average PPE: {record.get('averagePPE', 0):.5f}")
            print(f"     Maintenance Capex: ${record.get('maintenanceCapex', 0):,}")
            print(f"     Growth Capex: ${record.get('growthCapex', 0):,}")
            print(f"     Owner Earnings: ${record.get('ownersEarnings', 0):,}")
            print(
                f"     Owner Earnings Per Share: ${record.get('ownersEarningsPerShare', 0):.2f}"
            )

            # Calculate capex breakdown
            maintenance_capex = record.get("maintenanceCapex", 0)
            growth_capex = record.get("growthCapex", 0)
            total_capex = maintenance_capex + growth_capex

            if total_capex != 0:
                maintenance_ratio = abs(maintenance_capex) / abs(total_capex) * 100
                growth_ratio = abs(growth_capex) / abs(total_capex) * 100
                print("     Capex Breakdown:")
                print(f"       Maintenance: {maintenance_ratio:.1f}%")
                print(f"       Growth: {growth_ratio:.1f}%")


async def enterprise_values_examples(client: FmpClient) -> None:
    """Demonstrate enterprise values functionality"""
    print("\n=== Enterprise Values Examples ===")

    # Get enterprise values for Apple
    print("Fetching enterprise values for Apple (AAPL)...")
    enterprise_values = await client.statements.enterprise_values(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(enterprise_values)} enterprise values records for AAPL")

    if enterprise_values:
        print("\nAAPL Enterprise Values Summary (Latest 5 Years):")
        for i, record in enumerate(enterprise_values):
            print(f"\n  {i + 1}. Date: {record.get('date', 'N/A')}")
            print(f"     Stock Price: ${record.get('stockPrice', 0):.2f}")
            print(f"     Number of Shares: {record.get('numberOfShares', 0):,}")
            print(
                f"     Market Capitalization: ${record.get('marketCapitalization', 0):,}"
            )
            print(
                f"     Minus Cash & Cash Equivalents: ${record.get('minusCashAndCashEquivalents', 0):,}"
            )
            print(f"     Add Total Debt: ${record.get('addTotalDebt', 0):,}")
            print(f"     Enterprise Value: ${record.get('enterpriseValue', 0):,}")

            # Calculate key ratios
            market_cap = record.get("marketCapitalization", 0)
            enterprise_value = record.get("enterpriseValue", 0)
            stock_price = record.get("stockPrice", 0)

            if market_cap > 0 and enterprise_value > 0:
                ev_to_mc_ratio = enterprise_value / market_cap
                print(f"     EV/Market Cap Ratio: {ev_to_mc_ratio:.3f}")

            if stock_price > 0:
                shares_outstanding = record.get("numberOfShares", 0)
                if shares_outstanding > 0:
                    book_value_per_share = enterprise_value / shares_outstanding
                    print(
                        f"     Enterprise Value Per Share: ${book_value_per_share:.2f}"
                    )


async def growth_analysis_examples(client: FmpClient) -> None:
    """Demonstrate growth analysis functionality"""
    print("\n=== Growth Analysis Examples ===")

    # Get income statement growth for Apple
    print("Fetching income statement growth for Apple (AAPL)...")
    income_growth = await client.statements.income_statement_growth(
        "AAPL", limit=5, period="annual"
    )
    print(f"Found {len(income_growth)} income statement growth records for AAPL")

    if income_growth:
        print("\nAAPL Income Statement Growth Summary (Latest 5 Years):")
        for i, record in enumerate(income_growth):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Date: {record.get('date', 'N/A')}")
            print(f"     Revenue Growth: {record.get('growthRevenue', 0):.2%}")
            print(f"     Gross Profit Growth: {record.get('growthGrossProfit', 0):.2%}")
            print(
                f"     Operating Income Growth: {record.get('growthOperatingIncome', 0):.2%}"
            )
            print(f"     Net Income Growth: {record.get('growthNetIncome', 0):.2%}")
            print(f"     EPS Growth: {record.get('growthEPS', 0):.2%}")

            # Growth trend analysis
            revenue_growth = record.get("growthRevenue", 0)
            net_income_growth = record.get("growthNetIncome", 0)

            if revenue_growth > 0 and net_income_growth > 0:
                print("     ✅ Both revenue and net income growing")
            elif revenue_growth > 0 and net_income_growth < 0:
                print("     ⚠️  Revenue growing but net income declining")
            elif revenue_growth < 0 and net_income_growth < 0:
                print("     🔴 Both revenue and net income declining")
            else:
                print("     🔄 Mixed growth patterns")

    # Get comprehensive financial growth for Apple
    print("\nFetching comprehensive financial growth for Apple (AAPL)...")
    financial_growth = await client.statements.financial_statement_growth(
        "AAPL", limit=3, period="annual"
    )
    print(f"Found {len(financial_growth)} comprehensive growth records for AAPL")

    if financial_growth:
        print("\nAAPL Comprehensive Growth Analysis (Latest 3 Years):")
        for i, record in enumerate(financial_growth):
            print(
                f"\n  {i + 1}. Fiscal Year: {record.get('fiscalYear', 'N/A')} ({record.get('period', 'N/A')})"
            )
            print(f"     Revenue Growth: {record.get('revenueGrowth', 0):.2%}")
            print(
                f"     Operating Cash Flow Growth: {record.get('operatingCashFlowGrowth', 0):.2%}"
            )
            print(
                f"     Free Cash Flow Growth: {record.get('freeCashFlowGrowth', 0):.2%}"
            )
            print(f"     Asset Growth: {record.get('assetGrowth', 0):.2%}")
            print(f"     Debt Growth: {record.get('debtGrowth', 0):.2%}")

            # Long-term growth trends
            print("     Long-term Growth Trends:")
            print(
                f"       10Y Revenue Growth Per Share: {record.get('tenYRevenueGrowthPerShare', 0):.2%}"
            )
            print(
                f"       5Y Revenue Growth Per Share: {record.get('fiveYRevenueGrowthPerShare', 0):.2%}"
            )
            print(
                f"       3Y Revenue Growth Per Share: {record.get('threeYRevenueGrowthPerShare', 0):.2%}"
            )


async def revenue_segmentation_examples(client: FmpClient) -> None:
    """Demonstrate revenue segmentation functionality"""
    print("\n=== Revenue Segmentation Examples ===")

    # Get revenue product segmentation for Apple
    print("Fetching revenue product segmentation for Apple (AAPL)...")
    product_segmentation = await client.statements.revenue_product_segmentation(
        "AAPL", period="annual"
    )
    print(f"Found {len(product_segmentation)} product segmentation records for AAPL")

    if product_segmentation:
        print("\nAAPL Revenue Product Segmentation (Annual):")
        for record in product_segmentation:
            print(f"  Fiscal Year: {record.get('fiscalYear', 'N/A')}")
            print(f"  Period: {record.get('period', 'N/A')}")
            print(f"  Date: {record.get('date', 'N/A')}")

            data = record.get("data", {})
            if data:
                total_revenue = sum(data.values())
                print(f"  Total Revenue: ${total_revenue:,}")
                print("  Product Breakdown:")

                # Sort products by revenue (descending)
                sorted_products = sorted(data.items(), key=lambda x: x[1], reverse=True)

                for product, revenue in sorted_products:
                    percentage = (revenue / total_revenue) * 100
                    print(f"    {product}: ${revenue:,} ({percentage:.1f}%)")

    # Get revenue geographic segmentation for Apple
    print("\nFetching revenue geographic segmentation for Apple (AAPL)...")
    geographic_segmentation = await client.statements.revenue_geographic_segmentation(
        "AAPL", period="annual"
    )
    print(
        f"Found {len(geographic_segmentation)} geographic segmentation records for AAPL"
    )

    if geographic_segmentation:
        print("\nAAPL Revenue Geographic Segmentation (Annual):")
        for record in geographic_segmentation:
            print(f"  Fiscal Year: {record.get('fiscalYear', 'N/A')}")
            print(f"  Period: {record.get('period', 'N/A')}")
            print(f"  Date: {record.get('date', 'N/A')}")

            data = record.get("data", {})
            if data:
                total_revenue = sum(data.values())
                print(f"  Total Revenue: ${total_revenue:,}")
                print("  Geographic Breakdown:")

                # Sort regions by revenue (descending)
                sorted_regions = sorted(data.items(), key=lambda x: x[1], reverse=True)

                for region, revenue in sorted_regions:
                    percentage = (revenue / total_revenue) * 100
                    print(f"    {region}: ${revenue:,} ({percentage:.1f}%)")


async def financial_analysis_examples(client: FmpClient) -> None:
    """Demonstrate comprehensive financial analysis functionality"""
    print("\n=== Comprehensive Financial Analysis Examples ===")

    # Analyze Apple's financial health comprehensively
    print("Performing comprehensive financial analysis for Apple (AAPL)...")

    # Get all key financial data
    income_stmt = await client.statements.income_statement(
        "AAPL", limit=1, period="annual"
    )
    balance_sheet = await client.statements.balance_sheet_statement(
        "AAPL", limit=1, period="annual"
    )
    cash_flow = await client.statements.cash_flow_statement(
        "AAPL", limit=1, period="annual"
    )
    key_metrics = await client.statements.key_metrics("AAPL", limit=1, period="annual")
    financial_ratios = await client.statements.financial_ratios(
        "AAPL", limit=1, period="annual"
    )
    financial_scores = await client.statements.financial_scores("AAPL")

    if (
        income_stmt
        and balance_sheet
        and cash_flow
        and key_metrics
        and financial_ratios
        and financial_scores
    ):
        print("\n📊 AAPL Comprehensive Financial Analysis:")

        # Extract latest data
        income = income_stmt[0]
        balance = balance_sheet[0]
        cf = cash_flow[0]
        metrics = key_metrics[0]
        ratios = financial_ratios[0]
        scores = financial_scores[0]

        # Revenue and Profitability Analysis
        print("\n💰 Revenue & Profitability:")
        revenue = income.get("revenue", 0)
        net_income = income.get("netIncome", 0)
        gross_profit = income.get("grossProfit", 0)

        print(f"  Revenue: ${revenue:,}")
        print(f"  Gross Profit: ${gross_profit:,}")
        print(f"  Net Income: ${net_income:,}")
        print(
            f"  Gross Margin: {(gross_profit / revenue) * 100:.1f}%"
            if revenue > 0
            else "  Gross Margin: N/A"
        )
        print(
            f"  Net Margin: {(net_income / revenue) * 100:.1f}%"
            if revenue > 0
            else "  Net Margin: N/A"
        )

        # Balance Sheet Analysis
        print("\n🏦 Balance Sheet Strength:")
        total_assets = balance.get("totalAssets", 0)
        total_liabilities = balance.get("totalLiabilities", 0)
        total_equity = balance.get("totalStockholdersEquity", 0)
        cash = balance.get("cashAndCashEquivalents", 0)
        total_debt = balance.get("totalDebt", 0)

        print(f"  Total Assets: ${total_assets:,}")
        print(f"  Total Liabilities: ${total_liabilities:,}")
        print(f"  Total Equity: ${total_equity:,}")
        print(f"  Cash & Equivalents: ${cash:,}")
        print(f"  Total Debt: ${total_debt:,}")

        if total_assets > 0:
            debt_to_assets = total_liabilities / total_assets
            print(f"  Debt-to-Assets: {debt_to_assets:.3f}")

        if total_equity > 0:
            debt_to_equity = total_liabilities / total_equity
            print(f"  Debt-to-Equity: {debt_to_equity:.3f}")

        # Cash Flow Analysis
        print("\n💵 Cash Flow Analysis:")
        operating_cf = cf.get("operatingCashFlow", 0)
        investing_cf = cf.get("investingCashFlow", 0)
        financing_cf = cf.get("financingCashFlow", 0)
        free_cf = cf.get("freeCashFlow", 0)

        print(f"  Operating Cash Flow: ${operating_cf:,}")
        print(f"  Investing Cash Flow: ${investing_cf:,}")
        print(f"  Financing Cash Flow: ${financing_cf:,}")
        print(f"  Free Cash Flow: ${free_cf:,}")

        if operating_cf > 0 and net_income > 0:
            cf_quality = operating_cf / net_income
            print(f"  Cash Flow Quality: {cf_quality:.3f}")

        # Valuation Metrics
        print("\n📈 Valuation Metrics:")
        market_cap = metrics.get("marketCap", 0)
        enterprise_value = metrics.get("enterpriseValue", 0)

        print(f"  Market Cap: ${market_cap:,}")
        print(f"  Enterprise Value: ${enterprise_value:,}")

        if revenue > 0:
            price_to_sales = market_cap / revenue
            print(f"  P/S Ratio: {price_to_sales:.2f}")

        if net_income > 0:
            price_to_earnings = market_cap / net_income
            print(f"  P/E Ratio: {price_to_earnings:.2f}")

        # Financial Health Scores
        print("\n🏥 Financial Health Scores:")
        altman_score = scores.get("altmanZScore", 0)
        piotroski_score = scores.get("piotroskiScore", 0)

        print(f"  Altman Z-Score: {altman_score:.3f}")
        print(f"  Piotroski Score: {piotroski_score}/9")

        # Overall Assessment
        print("\n🎯 Overall Financial Assessment:")

        # Profitability assessment
        if net_income > 0 and revenue > 0:
            net_margin = (net_income / revenue) * 100
            if net_margin > 15:
                print(f"  ✅ Strong profitability (Net margin: {net_margin:.1f}%)")
            elif net_margin > 10:
                print(f"  🟡 Good profitability (Net margin: {net_margin:.1f}%)")
            else:
                print(f"  ⚠️  Moderate profitability (Net margin: {net_margin:.1f}%)")

        # Financial strength assessment
        if total_assets > 0 and total_liabilities > 0:
            debt_ratio = total_liabilities / total_assets
            if debt_ratio < 0.3:
                print(
                    f"  ✅ Strong financial position (Low debt ratio: {debt_ratio:.3f})"
                )
            elif debt_ratio < 0.5:
                print(
                    f"  🟡 Moderate financial position (Debt ratio: {debt_ratio:.3f})"
                )
            else:
                print(f"  ⚠️  High leverage (Debt ratio: {debt_ratio:.3f})")

        # Cash flow assessment
        if operating_cf > 0 and free_cf > 0:
            print(
                f"  ✅ Strong cash generation (Operating CF: ${operating_cf:,}, Free CF: ${free_cf:,})"
            )
        elif operating_cf > 0:
            print(f"  🟡 Positive operating cash flow (${operating_cf:,})")
        else:
            print(f"  ⚠️  Negative operating cash flow (${operating_cf:,})")

        # Growth assessment
        if revenue > 0 and net_income > 0:
            print(f"  📊 Revenue: ${revenue:,} | Net Income: ${net_income:,}")
            print("  💡 Strong fundamentals with solid cash flow generation")


async def main() -> None:
    """Main function demonstrating FMP Statements functionality"""
    # Get API key from environment variable
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("Error: FMP_API_KEY environment variable not set")
        print("Please set your FMP API key:")
        print("export FMP_API_KEY='your_api_key_here'")
        return

    print("FMP Statements Category Example")
    print("=" * 60)

    # Initialize client
    async with FmpClient(api_key=api_key) as client:
        try:
            # Run examples
            await income_statement_examples(client)
            await balance_sheet_examples(client)
            await cash_flow_examples(client)
            await key_metrics_examples(client)
            await financial_ratios_examples(client)
            await financial_scores_examples(client)
            await owner_earnings_examples(client)
            await enterprise_values_examples(client)
            await growth_analysis_examples(client)
            await revenue_segmentation_examples(client)
            await financial_analysis_examples(client)

        except Exception as e:
            print(f"Error occurred: {e}")
            print("This might be due to:")
            print("- Invalid API key")
            print("- Rate limiting")
            print("- Network issues")
            print("- API endpoint changes")


if __name__ == "__main__":
    asyncio.run(main())
