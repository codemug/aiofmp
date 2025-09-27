"""
Discounted Cash Flow (DCF) category for FMP API

This module provides DCF functionality including basic DCF valuation, levered DCF analysis,
and custom DCF calculations with detailed financial parameters.
"""

from typing import Any

from .base import FMPBaseClient


class DiscountedCashFlowCategory:
    """Discounted Cash Flow (DCF) category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the DCF category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def dcf_valuation(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get basic DCF valuation for a company

        Endpoint: /discounted-cash-flow

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of DCF valuation data with symbol, date, DCF value, and stock price

        Example:
            >>> data = await client.dcf.dcf_valuation("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "dcf": 147.27, "Stock Price": 231.795}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("discounted-cash-flow", params)

    async def levered_dcf(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get levered DCF valuation incorporating debt impact

        Endpoint: /levered-discounted-cash-flow

        Args:
            symbol: Stock symbol (required)

        Returns:
            List of levered DCF data with post-debt company valuation

        Example:
            >>> data = await client.dcf.levered_dcf("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "date": "2025-02-04", "dcf": 147.27, "Stock Price": 231.795}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("levered-discounted-cash-flow", params)

    async def custom_dcf_advanced(
        self,
        symbol: str,
        revenue_growth_pct: float | None = None,
        ebitda_pct: float | None = None,
        depreciation_and_amortization_pct: float | None = None,
        cash_and_short_term_investments_pct: float | None = None,
        receivables_pct: float | None = None,
        inventories_pct: float | None = None,
        payable_pct: float | None = None,
        ebit_pct: float | None = None,
        capital_expenditure_pct: float | None = None,
        operating_cash_flow_pct: float | None = None,
        selling_general_and_administrative_expenses_pct: float | None = None,
        tax_rate: float | None = None,
        long_term_growth_rate: float | None = None,
        cost_of_debt: float | None = None,
        cost_of_equity: float | None = None,
        market_risk_premium: float | None = None,
        beta: float | None = None,
        risk_free_rate: float | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get custom DCF analysis with detailed financial parameters

        Endpoint: /custom-discounted-cash-flow

        Args:
            symbol: Stock symbol (required)
            revenue_growth_pct: Revenue growth percentage (optional)
            ebitda_pct: EBITDA percentage (optional)
            depreciation_and_amortization_pct: Depreciation and amortization percentage (optional)
            cash_and_short_term_investments_pct: Cash and short-term investments percentage (optional)
            receivables_pct: Receivables percentage (optional)
            inventories_pct: Inventories percentage (optional)
            payable_pct: Payable percentage (optional)
            ebit_pct: EBIT percentage (optional)
            capital_expenditure_pct: Capital expenditure percentage (optional)
            operating_cash_flow_pct: Operating cash flow percentage (optional)
            selling_general_and_administrative_expenses_pct: SG&A expenses percentage (optional)
            tax_rate: Tax rate (optional)
            long_term_growth_rate: Long-term growth rate (optional)
            cost_of_debt: Cost of debt (optional)
            cost_of_equity: Cost of equity (optional)
            market_risk_premium: Market risk premium (optional)
            beta: Beta (optional)
            risk_free_rate: Risk-free rate (optional)

        Returns:
            List of custom DCF analysis data with detailed financial projections

        Example:
            >>> data = await client.dcf.custom_dcf_advanced("AAPL", revenue_growth_pct=0.109, beta=1.244)
            >>> # Returns: [{"year": "2029", "symbol": "AAPL", "revenue": 657173266965, ...}]
        """
        params = {"symbol": symbol}

        # Add optional parameters if provided
        if revenue_growth_pct is not None:
            params["revenueGrowthPct"] = revenue_growth_pct
        if ebitda_pct is not None:
            params["ebitdaPct"] = ebitda_pct
        if depreciation_and_amortization_pct is not None:
            params["depreciationAndAmortizationPct"] = depreciation_and_amortization_pct
        if cash_and_short_term_investments_pct is not None:
            params["cashAndShortTermInvestmentsPct"] = (
                cash_and_short_term_investments_pct
            )
        if receivables_pct is not None:
            params["receivablesPct"] = receivables_pct
        if inventories_pct is not None:
            params["inventoriesPct"] = inventories_pct
        if payable_pct is not None:
            params["payablePct"] = payable_pct
        if ebit_pct is not None:
            params["ebitPct"] = ebit_pct
        if capital_expenditure_pct is not None:
            params["capitalExpenditurePct"] = capital_expenditure_pct
        if operating_cash_flow_pct is not None:
            params["operatingCashFlowPct"] = operating_cash_flow_pct
        if selling_general_and_administrative_expenses_pct is not None:
            params["sellingGeneralAndAdministrativeExpensesPct"] = (
                selling_general_and_administrative_expenses_pct
            )
        if tax_rate is not None:
            params["taxRate"] = tax_rate
        if long_term_growth_rate is not None:
            params["longTermGrowthRate"] = long_term_growth_rate
        if cost_of_debt is not None:
            params["costOfDebt"] = cost_of_debt
        if cost_of_equity is not None:
            params["costOfEquity"] = cost_of_equity
        if market_risk_premium is not None:
            params["marketRiskPremium"] = market_risk_premium
        if beta is not None:
            params["beta"] = beta
        if risk_free_rate is not None:
            params["riskFreeRate"] = risk_free_rate

        return await self._client._make_request("custom-discounted-cash-flow", params)

    async def custom_dcf_levered(
        self,
        symbol: str,
        revenue_growth_pct: float | None = None,
        ebitda_pct: float | None = None,
        depreciation_and_amortization_pct: float | None = None,
        cash_and_short_term_investments_pct: float | None = None,
        receivables_pct: float | None = None,
        inventories_pct: float | None = None,
        payable_pct: float | None = None,
        ebit_pct: float | None = None,
        capital_expenditure_pct: float | None = None,
        operating_cash_flow_pct: float | None = None,
        selling_general_and_administrative_expenses_pct: float | None = None,
        tax_rate: float | None = None,
        long_term_growth_rate: float | None = None,
        cost_of_debt: float | None = None,
        cost_of_equity: float | None = None,
        market_risk_premium: float | None = None,
        beta: float | None = None,
        risk_free_rate: float | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get custom levered DCF analysis with detailed financial parameters

        Endpoint: /custom-levered-discounted-cash-flow

        Args:
            symbol: Stock symbol (required)
            revenue_growth_pct: Revenue growth percentage (optional)
            ebitda_pct: EBITDA percentage (optional)
            depreciation_and_amortization_pct: Depreciation and amortization percentage (optional)
            cash_and_short_term_investments_pct: Cash and short-term investments percentage (optional)
            receivables_pct: Receivables percentage (optional)
            inventories_pct: Inventories percentage (optional)
            payable_pct: Payable percentage (optional)
            ebit_pct: EBIT percentage (optional)
            capital_expenditure_pct: Capital expenditure percentage (optional)
            operating_cash_flow_pct: Operating cash flow percentage (optional)
            selling_general_and_administrative_expenses_pct: SG&A expenses percentage (optional)
            tax_rate: Tax rate (optional)
            long_term_growth_rate: Long-term growth rate (optional)
            cost_of_debt: Cost of debt (optional)
            cost_of_equity: Cost of equity (optional)
            market_risk_premium: Market risk premium (optional)
            beta: Beta (optional)
            risk_free_rate: Risk-free rate (optional)

        Returns:
            List of custom levered DCF analysis data with detailed financial projections

        Example:
            >>> data = await client.dcf.custom_dcf_levered("AAPL", revenue_growth_pct=0.109, beta=1.244)
            >>> # Returns: [{"year": "2029", "symbol": "AAPL", "revenue": 657173266965, ...}]
        """
        params = {"symbol": symbol}

        # Add optional parameters if provided
        if revenue_growth_pct is not None:
            params["revenueGrowthPct"] = revenue_growth_pct
        if ebitda_pct is not None:
            params["ebitdaPct"] = ebitda_pct
        if depreciation_and_amortization_pct is not None:
            params["depreciationAndAmortizationPct"] = depreciation_and_amortization_pct
        if cash_and_short_term_investments_pct is not None:
            params["cashAndShortTermInvestmentsPct"] = (
                cash_and_short_term_investments_pct
            )
        if receivables_pct is not None:
            params["receivablesPct"] = receivables_pct
        if inventories_pct is not None:
            params["inventoriesPct"] = inventories_pct
        if payable_pct is not None:
            params["payablePct"] = payable_pct
        if ebit_pct is not None:
            params["ebitPct"] = ebit_pct
        if capital_expenditure_pct is not None:
            params["capitalExpenditurePct"] = capital_expenditure_pct
        if operating_cash_flow_pct is not None:
            params["operatingCashFlowPct"] = operating_cash_flow_pct
        if selling_general_and_administrative_expenses_pct is not None:
            params["sellingGeneralAndAdministrativeExpensesPct"] = (
                selling_general_and_administrative_expenses_pct
            )
        if tax_rate is not None:
            params["taxRate"] = tax_rate
        if long_term_growth_rate is not None:
            params["longTermGrowthRate"] = long_term_growth_rate
        if cost_of_debt is not None:
            params["costOfDebt"] = cost_of_debt
        if cost_of_equity is not None:
            params["costOfEquity"] = cost_of_equity
        if market_risk_premium is not None:
            params["marketRiskPremium"] = market_risk_premium
        if beta is not None:
            params["beta"] = beta
        if risk_free_rate is not None:
            params["riskFreeRate"] = risk_free_rate

        return await self._client._make_request(
            "custom-levered-discounted-cash-flow", params
        )
