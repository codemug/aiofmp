"""
Statements category for FMP API

This module provides financial statement functionality including income statements,
balance sheets, cash flow statements, key metrics, financial ratios, and growth analysis.
"""

from typing import Any

from .base import FMPBaseClient


class StatementsCategory:
    """Statements category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the statements category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def income_statement(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get income statement data for a company

        Endpoint: /income-statement

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of income statement data with revenue, expenses, and profitability metrics

        Example:
            >>> data = await client.statements.income_statement("AAPL", limit=5, period="annual")
            >>> # Returns: [{"date": "2024-09-28", "symbol": "AAPL", "revenue": 391035000000, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("income-statement", params)

    async def balance_sheet_statement(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get balance sheet statement data for a company

        Endpoint: /balance-sheet-statement

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of balance sheet data with assets, liabilities, and equity

        Example:
            >>> data = await client.statements.balance_sheet_statement("AAPL", limit=5, period="annual")
            >>> # Returns: [{"date": "2024-09-28", "symbol": "AAPL", "totalAssets": 364980000000, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("balance-sheet-statement", params)

    async def cash_flow_statement(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get cash flow statement data for a company

        Endpoint: /cash-flow-statement

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of cash flow data with operating, investing, and financing activities

        Example:
            >>> data = await client.statements.cash_flow_statement("AAPL", limit=5, period="annual")
            >>> # Returns: [{"date": "2024-09-28", "symbol": "AAPL", "operatingCashFlow": 118254000000, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("cash-flow-statement", params)

    async def key_metrics(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get key financial metrics for a company

        Endpoint: /key-metrics

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of key metrics data with ratios and performance indicators

        Example:
            >>> data = await client.statements.key_metrics("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "marketCap": 3495160329570, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("key-metrics", params)

    async def financial_ratios(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get financial ratios for a company

        Endpoint: /ratios

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of financial ratios data with profitability, liquidity, and efficiency metrics

        Example:
            >>> data = await client.statements.financial_ratios("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "grossProfitMargin": 0.462, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("ratios", params)

    async def financial_scores(self, symbol: str) -> list[dict[str, Any]]:
        """
        Get financial health scores for a company

        Endpoint: /financial-scores

        Args:
            symbol: Company symbol (required)

        Returns:
            List of financial scores data including Altman Z-Score and Piotroski Score

        Example:
            >>> data = await client.statements.financial_scores("AAPL")
            >>> # Returns: [{"symbol": "AAPL", "altmanZScore": 9.32, "piotroskiScore": 8, ...}]
        """
        params = {"symbol": symbol}
        return await self._client._make_request("financial-scores", params)

    async def owner_earnings(
        self, symbol: str, limit: int | None = None
    ) -> list[dict[str, Any]]:
        """
        Get owner earnings data for a company

        Endpoint: /owner-earnings

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)

        Returns:
            List of owner earnings data with cash flow adjustments and per-share metrics

        Example:
            >>> data = await client.statements.owner_earnings("AAPL", limit=5)
            >>> # Returns: [{"symbol": "AAPL", "fiscalYear": "2025", "ownersEarnings": 27655035250, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit

        return await self._client._make_request("owner-earnings", params)

    async def enterprise_values(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get enterprise value data for a company

        Endpoint: /enterprise-values

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of enterprise value data with market cap, debt, and cash adjustments

        Example:
            >>> data = await client.statements.enterprise_values("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "enterpriseValue": 3571846329570, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("enterprise-values", params)

    async def income_statement_growth(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get income statement growth metrics for a company

        Endpoint: /income-statement-growth

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of growth metrics data showing year-over-year changes in income statement items

        Example:
            >>> data = await client.statements.income_statement_growth("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "growthRevenue": 0.0202, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("income-statement-growth", params)

    async def balance_sheet_statement_growth(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get balance sheet statement growth metrics for a company

        Endpoint: /balance-sheet-statement-growth

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of growth metrics data showing year-over-year changes in balance sheet items

        Example:
            >>> data = await client.statements.balance_sheet_statement_growth("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "growthTotalAssets": 0.0352, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request(
            "balance-sheet-statement-growth", params
        )

    async def cash_flow_statement_growth(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get cash flow statement growth metrics for a company

        Endpoint: /cash-flow-statement-growth

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of growth metrics data showing year-over-year changes in cash flow items

        Example:
            >>> data = await client.statements.cash_flow_statement_growth("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "growthNetIncome": -0.0336, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("cash-flow-statement-growth", params)

    async def financial_statement_growth(
        self, symbol: str, limit: int | None = None, period: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get comprehensive financial statement growth metrics for a company

        Endpoint: /financial-growth

        Args:
            symbol: Company symbol (required)
            limit: Number of periods to retrieve (optional)
            period: Period type - Q1,Q2,Q3,Q4,FY,annual,quarter (optional)

        Returns:
            List of comprehensive growth metrics across income, balance sheet, and cash flow statements

        Example:
            >>> data = await client.statements.financial_statement_growth("AAPL", limit=5, period="annual")
            >>> # Returns: [{"symbol": "AAPL", "date": "2024-09-28", "revenueGrowth": 0.0202, ...}]
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        if period is not None:
            params["period"] = period

        return await self._client._make_request("financial-growth", params)

    async def revenue_product_segmentation(
        self, symbol: str, period: str | None = None, structure: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get revenue breakdown by product line for a company

        Endpoint: /revenue-product-segmentation

        Args:
            symbol: Company symbol (required)
            period: Period type - annual,quarter (optional)
            structure: Data structure - flat (optional)

        Returns:
            List of revenue segmentation data by product categories

        Example:
            >>> data = await client.statements.revenue_product_segmentation("AAPL", period="annual")
            >>> # Returns: [{"symbol": "AAPL", "fiscalYear": 2024, "data": {"iPhone": 201183000000, ...}}]
        """
        params = {"symbol": symbol}
        if period is not None:
            params["period"] = period
        if structure is not None:
            params["structure"] = structure

        return await self._client._make_request("revenue-product-segmentation", params)

    async def revenue_geographic_segmentation(
        self, symbol: str, period: str | None = None, structure: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get revenue breakdown by geographic region for a company

        Endpoint: /revenue-geographic-segmentation

        Args:
            symbol: Company symbol (required)
            period: Period type - annual,quarter (optional)
            structure: Data structure - flat (optional)

        Returns:
            List of revenue segmentation data by geographic regions

        Example:
            >>> data = await client.statements.revenue_geographic_segmentation("AAPL", period="annual")
            >>> # Returns: [{"symbol": "AAPL", "fiscalYear": 2024, "data": {"Americas": 167045000000, ...}}]
        """
        params = {"symbol": symbol}
        if period is not None:
            params["period"] = period
        if structure is not None:
            params["structure"] = structure

        return await self._client._make_request(
            "revenue-geographic-segmentation", params
        )
