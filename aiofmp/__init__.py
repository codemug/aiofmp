"""
Financial Modeling Prep (FMP) API Client

This module provides a comprehensive async client for the FMP API with
category-based organization for better code management.
"""

from .analyst import AnalystCategory
from .base import (
    FMPAuthenticationError,
    FMPBaseClient,
    FMPError,
    FMPRateLimitError,
    FMPResponseError,
)
from .calendar import CalendarCategory
from .chart import ChartCategory
from .commodity import CommodityCategory
from .company import CompanyCategory
from .cot import CommitmentOfTradersCategory
from .crypto import CryptoCategory
from .dcf import DiscountedCashFlowCategory
from .directory import DirectoryCategory
from .economics import EconomicsCategory
from .etf import EtfAndMutualFundsCategory
from .forex import ForexCategory
from .form13f import Form13FCategory
from .indexes import IndexesCategory
from .insider_trades import InsiderTradesCategory
from .market_performance import MarketPerformanceCategory
from .news import NewsCategory
from .quote import QuoteCategory
from .search import SearchCategory
from .senate import SenateCategory
from .statements import StatementsCategory
from .technical_indicators import TechnicalIndicatorsCategory

__all__ = [
    "FmpClient",
    "FMPError",
    "FMPAuthenticationError",
    "FMPRateLimitError",
    "FMPResponseError",
]


class FmpClient(FMPBaseClient):
    """
    Main FMP API client with category-based organization

    This client provides access to all FMP API endpoints organized by category
    for better code management and maintainability.

    Usage:
        client = FmpClient(api_key="your_api_key")

        # Search category
        symbols = await client.search.symbols("AAPL", limit=10)
        companies = await client.search.companies("Apple", limit=5)
        screener = await client.search.screener(sector="Technology", limit=100)

        # Directory category
        all_symbols = await client.directory.company_symbols()
        etfs = await client.directory.etf_list()
        exchanges = await client.directory.available_exchanges()

        # Analyst category
        estimates = await client.analyst.financial_estimates("AAPL", "annual", limit=10)
        ratings = await client.analyst.ratings_snapshot("AAPL")
        price_targets = await client.analyst.price_target_consensus("AAPL")

        # Calendar category
        dividends = await client.calendar.dividends_company("AAPL", limit=100)
        earnings = await client.calendar.earnings_company("AAPL", limit=20)
        upcoming_ipos = await client.calendar.ipos_calendar("2025-01-01", "2025-06-30")

        # Chart category
        price_data = await client.chart.historical_price_full("AAPL", "2025-01-01", "2025-03-31")
        intraday_data = await client.chart.intraday_1hour("AAPL", "2025-01-01", "2025-01-02")

        # Company category
        profile = await client.company.profile("AAPL")
        executives = await client.company.executives("AAPL")
        market_cap = await client.company.market_cap("AAPL")

        # Commitment of Traders category
        cot_report = await client.cot.cot_report("KC", "2024-01-01", "2024-03-01")
        cot_analysis = await client.cot.cot_analysis("B6", "2024-01-01", "2024-03-01")

        # Discounted Cash Flow category
        dcf_valuation = await client.dcf.dcf_valuation("AAPL")
        levered_dcf = await client.dcf.levered_dcf("AAPL")

        # Economics category
        treasury_rates = await client.economics.treasury_rates("2025-04-24", "2025-07-24")
        gdp_data = await client.economics.economic_indicators("GDP", "2024-07-24", "2025-07-24")

        # ETF And Mutual Funds category
        etf_holdings = await client.etf.holdings("SPY")
        etf_info = await client.etf.info("SPY")

        # Commodity category
        commodities = await client.commodity.commodities_list()
        gold_quote = await client.commodity.quote("GCUSD")

        # Crypto category
        crypto_list = await client.crypto.cryptocurrency_list()
        btc_quote = await client.crypto.quote("BTCUSD")

        # Forex category
        forex_list = await client.forex.forex_list()
        eur_usd_quote = await client.forex.quote("EURUSD")

        # Statements category
        income_stmt = await client.statements.income_statement("AAPL", limit=5)
        balance_sheet = await client.statements.balance_sheet_statement("AAPL", limit=5)

        # Form 13F category
        latest_filings = await client.form13f.latest_filings(page=0, limit=100)
        berkshire_holdings = await client.form13f.filings_extract("0001067983", "2023", "3")

        # Indexes category
        sp500_quote = await client.indexes.index_quote("^GSPC")
        all_indexes = await client.indexes.index_list()

        # Insider Trades category
        latest_trades = await client.insider_trades.latest_insider_trades(page=0, limit=100)
        apple_insider_stats = await client.insider_trades.insider_trade_statistics("AAPL")

        # Market Performance category
        sector_performance = await client.market_performance.sector_performance_snapshot(date.today())
        biggest_gainers = await client.market_performance.biggest_gainers()

        # News category
        fmp_articles = await client.news.fmp_articles(page=0, limit=20)
        stock_news = await client.news.stock_news(page=0, limit=10)

        # Technical Indicators category
        sma_data = await client.technical_indicators.simple_moving_average("AAPL", 10, "1day")
        rsi_data = await client.technical_indicators.relative_strength_index("AAPL", 14, "1day")

        # Quote category
        stock_quote = await client.quote.stock_quote("AAPL")
        price_changes = await client.quote.stock_price_change("AAPL")

        # Senate category
        senate_disclosures = await client.senate.latest_senate_disclosures(page=0, limit=100)
        house_trades = await client.senate.house_trading_activity("AAPL")
    """

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the FMP client

        Args:
            api_key: FMP API key (required)
            **kwargs: Additional arguments passed to base client
        """
        super().__init__(api_key, **kwargs)

        # Initialize category modules
        self.search = SearchCategory(self)
        self.directory = DirectoryCategory(self)
        self.analyst = AnalystCategory(self)
        self.calendar = CalendarCategory(self)
        self.chart = ChartCategory(self)
        self.company = CompanyCategory(self)
        self.cot = CommitmentOfTradersCategory(self)
        self.dcf = DiscountedCashFlowCategory(self)
        self.economics = EconomicsCategory(self)
        self.etf = EtfAndMutualFundsCategory(self)
        self.commodity = CommodityCategory(self)
        self.crypto = CryptoCategory(self)
        self.forex = ForexCategory(self)
        self.statements = StatementsCategory(self)
        self.form13f = Form13FCategory(self)
        self.indexes = IndexesCategory(self)
        self.insider_trades = InsiderTradesCategory(self)
        self.market_performance = MarketPerformanceCategory(self)
        self.news = NewsCategory(self)
        self.technical_indicators = TechnicalIndicatorsCategory(self)
        self.quote = QuoteCategory(self)
        self.senate = SenateCategory(self)

        # Future categories will be added here:
        # self.financial = FinancialCategory(self)
