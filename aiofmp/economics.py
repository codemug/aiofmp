"""
Economics category for FMP API

This module provides economics functionality including treasury rates, economic indicators,
economic data releases calendar, and market risk premium data.
"""

from typing import Any

from .base import FMPBaseClient


class EconomicsCategory:
    """Economics category for FMP API endpoints"""

    def __init__(self, client: FMPBaseClient):
        """
        Initialize the economics category

        Args:
            client: Base FMP client instance
        """
        self._client = client

    async def treasury_rates(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get real-time and historical Treasury rates for all maturities

        Endpoint: /treasury-rates

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of treasury rates data with various maturity periods

        Example:
            >>> data = await client.economics.treasury_rates("2025-04-24", "2025-07-24")
            >>> # Returns: [{"date": "2024-02-29", "month1": 5.53, "year10": 4.25, ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("treasury-rates", params)

    async def economic_indicators(
        self, name: str, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get real-time and historical economic data for key indicators

        Endpoint: /economic-indicators

        Args:
            name: Economic indicator name (required)
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of economic indicator data with name, date, and value

        Example:
            >>> data = await client.economics.economic_indicators("GDP", "2024-07-24", "2025-07-24")
            >>> # Returns: [{"name": "GDP", "date": "2024-01-01", "value": 28624.069}]

        Available indicators:
            - GDP, realGDP, nominalPotentialGDP, realGDPPerCapita
            - federalFunds, CPI, inflationRate, inflation
            - retailSales, consumerSentiment, durableGoods
            - unemploymentRate, totalNonfarmPayroll, initialClaims
            - industrialProductionTotalIndex, newPrivatelyOwnedHousingUnitsStartedTotalUnits
            - totalVehicleSales, retailMoneyFunds, smoothedUSRecessionProbabilities
            - 3MonthOr90DayRatesAndYieldsCertificatesOfDeposit
            - commercialBankInterestRateOnCreditCardPlansAllAccounts
            - 30YearFixedRateMortgageAverage, 15YearFixedRateMortgageAverage
        """
        params = {"name": name}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("economic-indicators", params)

    async def economic_calendar(
        self, from_date: str | None = None, to_date: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get comprehensive calendar of upcoming economic data releases

        Endpoint: /economic-calendar

        Args:
            from_date: Start date in YYYY-MM-DD format (optional)
            to_date: End date in YYYY-MM-DD format (optional)

        Returns:
            List of economic calendar events with release details

        Example:
            >>> data = await client.economics.economic_calendar("2025-04-24", "2025-07-24")
            >>> # Returns: [{"date": "2024-03-01 03:35:00", "country": "JP", "event": "3-Month Bill Auction", ...}]
        """
        params = {}
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        return await self._client._make_request("economic-calendar", params)

    async def market_risk_premium(self) -> list[dict[str, Any]]:
        """
        Get market risk premium data for various countries

        Endpoint: /market-risk-premium

        Returns:
            List of market risk premium data with country, continent, and risk metrics

        Example:
            >>> data = await client.economics.market_risk_premium()
            >>> # Returns: [{"country": "Zimbabwe", "continent": "Africa", "countryRiskPremium": 13.17, ...}]
        """
        return await self._client._make_request("market-risk-premium", {})
