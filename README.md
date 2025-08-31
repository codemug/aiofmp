# aiofmp

A modern, async-first Python client for the Financial Modeling Prep API, designed with clean architecture and
comprehensive functionality.

## Features

- **Async-First Design**: Built with asyncio for high-performance concurrent operations
- **Category-Based Organization**: Clean separation of API endpoints by functionality
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Rate Limiting**: Built-in rate limiting and retry logic
- **Clean API**: Intuitive method names that mirror the FMP API structure

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd aiofmp

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

## Quick Start

```python
import asyncio
from aiofmp import FmpClient


async def main():
    # Initialize client with your API key
    client = FmpClient(api_key="your_api_key_here")

    # Use async context manager for automatic session management
    async with client:
        # Search for symbols
        symbols = await client.search.symbols("AAPL", limit=10)
        print(f"Found {len(symbols)} symbols")

        # Search for companies
        companies = await client.search.companies("Apple", limit=5)
        print(f"Found {len(companies)} companies")

        # Screen stocks
        tech_stocks = await client.search.screener(
            sector="Technology",
            market_cap_more_than=1000000000,  # $1B+
            limit=100
        )
        print(f"Found {len(tech_stocks)} technology stocks")


# Run the example
asyncio.run(main())
```

## API Categories

### Search Category (`client.search`)

The Search category provides functionality for finding stocks and companies:

#### `symbols(query, limit=None, exchange=None)`

Search for stock symbols by query (symbol or company name).

```python
# Basic search
symbols = await client.search.symbols("AAPL")

# With limit and exchange filter
symbols = await client.search.symbols("AAPL", limit=10, exchange="NASDAQ")
```

#### `companies(query, limit=None, exchange=None)`

Search for companies by name.

```python
# Search for companies with "Apple" in the name
companies = await client.search.companies("Apple", limit=5)

# Filter by exchange
nasdaq_companies = await client.search.companies("Microsoft", exchange="NASDAQ")
```

#### `screener(**filters)`

Screen stocks based on various criteria.

```python
# Technology sector stocks
tech_stocks = await client.search.screener(sector="Technology", limit=100)

# Large-cap stocks
large_caps = await client.search.screener(
    market_cap_more_than=100000000000,  # $100B+
    limit=50
)

# Complex screening
dividend_stocks = await client.search.screener(
    sector="Technology",
    dividend_more_than=0.5,
    exchange="NYSE",
    is_etf=False,
    limit=100
)
```

### Directory Category (`client.directory`)

The Directory category provides access to comprehensive lists and reference data:

#### `company_symbols()`

Get a complete list of all available company symbols.

```python
# Get all company symbols
all_symbols = await client.directory.company_symbols()
print(f"Total symbols available: {len(all_symbols)}")
```

#### `financial_symbols()`

Get companies with available financial statements.

```python
# Get companies with financial data
financial_companies = await client.directory.financial_symbols()
print(f"Companies with financial statements: {len(financial_companies)}")
```

#### `etf_list()`

Get a complete list of available ETFs.

```python
# Get all ETFs
etfs = await client.directory.etf_list()
print(f"Total ETFs available: {len(etfs)}")
```

#### `actively_trading()`

Get a list of currently actively trading securities.

```python
# Get actively trading symbols
active_symbols = await client.directory.actively_trading()
print(f"Actively trading: {len(active_symbols)}")
```

#### `earnings_transcripts()`

Get companies with available earnings transcripts.

```python
# Get companies with transcripts
transcript_companies = await client.directory.earnings_transcripts()
print(f"Companies with transcripts: {len(transcript_companies)}")
```

#### `available_exchanges()`

Get a list of all supported stock exchanges.

```python
# Get available exchanges
exchanges = await client.directory.available_exchanges()
for exchange in exchanges:
    print(f"{exchange['exchange']}: {exchange['name']}")
```

#### `available_sectors()`

Get a list of all available industry sectors.

```python
# Get available sectors
sectors = await client.directory.available_sectors()
for sector in sectors:
    print(f"- {sector['sector']}")
```

#### `available_industries()`

Get a list of all available industries.

```python
# Get available industries
industries = await client.directory.available_industries()
for industry in industries:
    print(f"- {industry['industry']}")
```

#### `available_countries()`

Get a list of all available countries.

```python
# Get available countries
countries = await client.directory.available_countries()
for country in countries:
    print(f"- {country['country']}")
```

### Analyst Category (`client.analyst`)

The Analyst category provides access to analyst estimates, ratings, price targets, and stock grades:

#### `financial_estimates(symbol, period, page=None, limit=None)`

Get analyst financial estimates for a stock symbol.

```python
# Get annual estimates
annual_estimates = await client.analyst.financial_estimates("AAPL", "annual", limit=10)

# Get quarterly estimates
quarterly_estimates = await client.analyst.financial_estimates("AAPL", "quarter", page=1, limit=20)
```

#### `ratings_snapshot(symbol, limit=None)`

Get current financial ratings snapshot for a stock symbol.

```python
# Get current ratings
ratings = await client.analyst.ratings_snapshot("AAPL")

# Get multiple ratings
ratings = await client.analyst.ratings_snapshot("AAPL", limit=5)
```

#### `historical_ratings(symbol, limit=None)`

Get historical financial ratings for a stock symbol.

```python
# Get historical ratings
historical = await client.analyst.historical_ratings("AAPL", limit=10)
```

#### `price_target_summary(symbol)`

Get price target summary from analysts for a stock symbol.

```python
# Get price target summary
summary = await client.analyst.price_target_summary("AAPL")
```

#### `price_target_consensus(symbol)`

Get price target consensus from analysts for a stock symbol.

```python
# Get price target consensus
consensus = await client.analyst.price_target_consensus("AAPL")
```

#### `price_target_news(symbol, page=None, limit=None)`

Get news about analyst price targets for a stock symbol.

```python
# Get price target news
news = await client.analyst.price_target_news("AAPL", limit=5)
```

#### `price_target_latest_news(page=None, limit=None)`

Get latest analyst price target news for all stock symbols.

```python
# Get latest price target news
latest_news = await client.analyst.price_target_latest_news(limit=20)
```

#### `stock_grades(symbol)`

Get latest stock grades from analysts for a stock symbol.

```python
# Get stock grades
grades = await client.analyst.stock_grades("AAPL")
```

#### `historical_stock_grades(symbol, limit=None)`

Get historical analyst grades for a stock symbol.

```python
# Get historical grades
historical_grades = await client.analyst.historical_stock_grades("AAPL", limit=50)
```

#### `stock_grades_summary(symbol)`

Get summary of analyst grades consensus for a stock symbol.

```python
# Get grades summary
summary = await client.analyst.stock_grades_summary("AAPL")
```

#### `stock_grade_news(symbol, page=None, limit=None)`

Get news about analyst grade changes for a stock symbol.

```python
# Get grade change news
grade_news = await client.analyst.stock_grade_news("AAPL", limit=5)
```

#### `stock_grade_latest_news(page=None, limit=None)`

Get latest analyst grade change news for all stock symbols.

```python
# Get latest grade change news
latest_grades = await client.analyst.stock_grade_latest_news(limit=20)
```

### Calendar Category (`client.calendar`)

The
Calendar
category
provides
access
to
calendar
events
including
dividends, earnings, IPOs, and stock
splits:

#### `dividends_company(symbol, limit=None)`
Get
dividend
information
for a specific company.

```python
# Get company dividends
dividends = await client.calendar.dividends_company("AAPL", limit=50)

# Get all available dividends
all_dividends = await client.calendar.dividends_company("AAPL")
```

#### `dividends_calendar(from_date=None, to_date=None)`

Get dividend calendar for all stocks within a date range.

```python
# Get dividend calendar for Q1 2025
dividends = await client.calendar.dividends_calendar("2025-01-01", "2025-03-31")

# Get all upcoming dividends
upcoming = await client.calendar.dividends_calendar()
```

#### `earnings_company(symbol, limit=None)`

Get earnings information for a specific company.

```python
# Get company earnings
earnings = await client.calendar.earnings_company("AAPL", limit=20)

# Get all available earnings
all_earnings = await client.calendar.earnings_company("AAPL")
```

#### `earnings_calendar(from_date=None, to_date=None)`

Get earnings calendar for all companies within a date range.

```python
# Get earnings calendar for Q1 2025
earnings = await client.calendar.earnings_calendar("2025-01-01", "2025-03-31")

# Get all upcoming earnings
upcoming = await client.calendar.earnings_calendar()
```

#### `ipos_calendar(from_date=None, to_date=None)`

Get IPO calendar for upcoming initial public offerings.

```python
# Get IPO calendar for H1 2025
ipos = await client.calendar.ipos_calendar("2025-01-01", "2025-06-30")

# Get all upcoming IPOs
upcoming = await client.calendar.ipos_calendar()
```

#### `ipos_disclosure(from_date=None, to_date=None)`

Get IPO disclosure filings for upcoming initial public offerings.

```python
# Get IPO disclosures for H1 2025
disclosures = await client.calendar.ipos_disclosure("2025-01-01", "2025-06-30")
```

#### `ipos_prospectus(from_date=None, to_date=None)`

Get IPO prospectus information for upcoming initial public offerings.

```python
# Get IPO prospectuses for H1 2025
prospectuses = await client.calendar.ipos_prospectus("2025-01-01", "2025-06-30")
```

#### `stock_splits_company(symbol, limit=None)`

Get stock split information for a specific company.

```python
# Get company stock splits
splits = await client.calendar.stock_splits_company("AAPL", limit=20)

# Get all available splits
all_splits = await client.calendar.stock_splits_company("AAPL")
```

#### `stock_splits_calendar(from_date=None, to_date=None)`

Get stock splits calendar for all companies within a date range.

```python
# Get stock splits calendar for H1 2025
splits = await client.calendar.stock_splits_calendar("2025-01-01", "2025-06-30")

# Get all upcoming splits
upcoming = await client.calendar.stock_splits_calendar()
```

### Chart Category (`client.chart`)

The Chart category provides access to historical price data, intraday data, and various time intervals for stock
analysis:

#### `historical_price_light(symbol, from_date=None, to_date=None)`

Get simplified stock chart data with essential information.

```python
# Get light historical price data
light_data = await client.chart.historical_price_light("AAPL", "2025-01-01", "2025-03-31")

# Get all available light data
all_light_data = await client.chart.historical_price_light("AAPL")
```

#### `historical_price_full(symbol, from_date=None, to_date=None)`

Get comprehensive stock price and volume data including OHLC, changes, and VWAP.

```python
# Get full historical price data
full_data = await client.chart.historical_price_full("AAPL", "2025-01-01", "2025-03-31")

# Get all available full data
all_full_data = await client.chart.historical_price_full("AAPL")
```

#### `historical_price_unadjusted(symbol, from_date=None, to_date=None)`

Get stock price data without adjustments for stock splits.

```python
# Get unadjusted historical price data
unadjusted_data = await client.chart.historical_price_unadjusted("AAPL", "2025-01-01", "2025-03-31")
```

#### `historical_price_dividend_adjusted(symbol, from_date=None, to_date=None)`

Get stock price data with dividend adjustments.

```python
# Get dividend-adjusted historical price data
dividend_adjusted_data = await client.chart.historical_price_dividend_adjusted("AAPL", "2025-01-01", "2025-03-31")
```

#### `intraday_1min(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 1-minute interval intraday stock data.

```python
# Get 1-minute intraday data
intraday_1min = await client.chart.intraday_1min("AAPL", "2025-01-01", "2025-01-02")

# Get nonadjusted 1-minute data
nonadjusted_1min = await client.chart.intraday_1min("AAPL", "2025-01-01", "2025-01-02", nonadjusted=True)
```

#### `intraday_5min(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 5-minute interval intraday stock data.

```python
# Get 5-minute intraday data
intraday_5min = await client.chart.intraday_5min("AAPL", "2025-01-01", "2025-01-02")
```

#### `intraday_15min(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 15-minute interval intraday stock data.

```python
# Get 15-minute intraday data
intraday_15min = await client.chart.intraday_15min("AAPL", "2025-01-01", "2025-01-02")
```

#### `intraday_30min(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 30-minute interval intraday stock data.

```python
# Get 30-minute intraday data
intraday_30min = await client.chart.intraday_30min("AAPL", "2025-01-01", "2025-01-02")
```

#### `intraday_1hour(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 1-hour interval intraday stock data.

```python
# Get 1-hour intraday data
intraday_1hour = await client.chart.intraday_1hour("AAPL", "2025-01-01", "2025-01-02")
```

#### `intraday_4hour(symbol, from_date=None, to_date=None, nonadjusted=None)`

Get 4-hour interval intraday stock data.

```python
# Get 4-hour intraday data
intraday_4hour = await client.chart.intraday_4hour("AAPL", "2025-01-01", "2025-01-02")
```

### Company Category (`client.company`)

The Company category provides access to comprehensive company information including profiles, employee data, market
capitalization, shares float, mergers & acquisitions, executives, and compensation:

#### `profile(symbol)`

Get detailed company profile data with comprehensive company information.

```python
# Get company profile
profile = await client.company.profile("AAPL")

# Access profile information
company_name = profile[0]["companyName"]
market_cap = profile[0]["marketCap"]
sector = profile[0]["sector"]
```

#### `notes(symbol)`

Get company-issued notes information with CIK, symbol, title, and exchange.

```python
# Get company notes
notes = await client.company.notes("AAPL")
```

#### `employee_count(symbol, limit=None)`

Get company employee count information with workforce data and SEC filing details.

```python
# Get current employee count
employees = await client.company.employee_count("AAPL", limit=5)

# Get all available employee data
all_employees = await client.company.employee_count("AAPL")
```

#### `historical_employee_count(symbol, limit=None)`

Get historical employee count data showing workforce evolution over time.

```python
# Get historical employee count
historical = await client.company.historical_employee_count("AAPL", limit=20)
```

#### `market_cap(symbol)`

Get company market capitalization data with symbol, date, and market cap value.

```python
# Get current market cap
market_cap = await client.company.market_cap("AAPL")
```

#### `batch_market_cap(symbols)`

Get market capitalization data for multiple companies in a single request.

```python
# Get market cap for multiple companies
symbols = ["AAPL", "MSFT", "GOOGL"]
batch_market_cap = await client.company.batch_market_cap(symbols)
```

#### `historical_market_cap(symbol, limit=None, from_date=None, to_date=None)`

Get historical market capitalization data showing market value changes over time.

```python
# Get historical market cap for specific period
historical = await client.company.historical_market_cap("AAPL", "2025-01-01", "2025-03-31")

# Get with limit
historical = await client.company.historical_market_cap("AAPL", limit=100, from_date="2025-01-01")
```

#### `shares_float(symbol)`

Get company share float and liquidity information including free float and outstanding shares.

```python
# Get shares float data
shares_float = await client.company.shares_float("AAPL")
```

#### `all_shares_float(limit=None, page=None)`

Get shares float data for all available companies with pagination support.

```python
# Get all shares float data
all_shares = await client.company.all_shares_float(limit=1000, page=0)
```

#### `latest_mergers_acquisitions(page=None, limit=None)`

Get latest mergers and acquisitions data with transaction details and SEC filing links.

```python
# Get latest M&A
latest_ma = await client.company.latest_mergers_acquisitions(page=0, limit=100)
```

#### `search_mergers_acquisitions(name)`

Search for specific mergers and acquisitions data by company name.

```python
# Search for M&A involving specific company
apple_ma = await client.company.search_mergers_acquisitions("Apple")
```

#### `executives(symbol, active=None)`

Get company executives information with names, titles, compensation, and demographic details.

```python
# Get all executives
executives = await client.company.executives("AAPL")

# Get only active executives
active_executives = await client.company.executives("AAPL", active="true")
```

#### `executive_compensation(symbol)`

Get executive compensation data with salaries, stock awards, and total compensation.

```python
# Get executive compensation
compensation = await client.company.executive_compensation("AAPL")
```

#### `executive_compensation_benchmark(year=None)`

Get executive compensation benchmark data by industry for comparison.

```python
# Get current year benchmark
benchmark = await client.company.executive_compensation_benchmark("2024")

# Get all available benchmark data
all_benchmarks = await client.company.executive_compensation_benchmark()
```

### Commitment of Traders Category (`client.cot`)

The Commitment of Traders (COT) category provides access to comprehensive COT reports, market sentiment analysis, and
available COT symbols for commodities and futures:

#### `cot_report(symbol, from_date=None, to_date=None)`

Get comprehensive Commitment of Traders (COT) reports with detailed position information.

```python
# Get COT report for Coffee
cot_report = await client.cot.cot_report("KC", "2024-01-01", "2024-03-01")

# Get COT report for Natural Gas
ng_cot = await client.cot.cot_report("NG", "2024-01-01", "2024-03-01")
```

#### `cot_analysis(symbol, from_date=None, to_date=None)`

Get COT analysis with market sentiment insights and trend information.

```python
# Get COT analysis for British Pound
cot_analysis = await client.cot.cot_analysis("B6", "2024-01-01", "2024-03-01")

# Get COT analysis for Gold
gc_analysis = await client.cot.cot_analysis("GC", "2024-01-01", "2024-03-01")
```

#### `cot_list()`

Get list of available COT report symbols for commodities and futures.

```python
# Get all available COT symbols
cot_symbols = await client.cot.cot_list()

# Access symbol information
for symbol in cot_symbols:
    print(f"{symbol['symbol']}: {symbol['name']}")
```

### Discounted Cash Flow Category (`client.dcf`)

The Discounted Cash Flow (DCF) category provides access to comprehensive DCF valuation, levered DCF analysis, and custom
DCF calculations with detailed financial parameters:

#### `dcf_valuation(symbol)`

Get basic DCF valuation for a company with symbol, date, DCF value, and stock price.

```python
# Get basic DCF valuation
dcf_data = await client.dcf.dcf_valuation("AAPL")

# Access DCF information
dcf_value = dcf_data[0]["dcf"]
stock_price = dcf_data[0]["Stock Price"]
```

#### `levered_dcf(symbol)`

Get levered DCF valuation incorporating debt impact for post-debt company valuation.

```python
# Get levered DCF valuation
levered_dcf = await client.dcf.levered_dcf("AAPL")
```

#### `custom_dcf_advanced(symbol, **kwargs)`

Get custom DCF analysis with detailed financial parameters for personalized valuation.

```python
# Get custom DCF with minimal parameters
custom_dcf = await client.dcf.custom_dcf_advanced("AAPL", revenue_growth_pct=0.109, beta=1.244)

# Get custom DCF with comprehensive parameters
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
    risk_free_rate=3.64
)
```

#### `custom_dcf_levered(symbol, **kwargs)`

Get custom levered DCF analysis with detailed financial parameters for debt-adjusted valuation.

```python
# Get custom levered DCF with parameters
custom_levered = await client.dcf.custom_dcf_levered(
    "AAPL",
    revenue_growth_pct=0.109,
    beta=1.244,
    cost_of_debt=3.64,
    cost_of_equity=9.512
)
```

**Available DCF Parameters:**

- `revenue_growth_pct`: Revenue growth percentage
- `ebitda_pct`: EBITDA percentage
- `depreciation_and_amortization_pct`: Depreciation and amortization percentage
- `cash_and_short_term_investments_pct`: Cash and short-term investments percentage
- `receivables_pct`: Receivables percentage
- `inventories_pct`: Inventories percentage
- `payable_pct`: Payable percentage
- `ebit_pct`: EBIT percentage
- `capital_expenditure_pct`: Capital expenditure percentage
- `operating_cash_flow_pct`: Operating cash flow percentage
- `selling_general_and_administrative_expenses_pct`: SG&A expenses percentage
- `tax_rate`: Tax rate
- `long_term_growth_rate`: Long-term growth rate
- `cost_of_debt`: Cost of debt
- `cost_of_equity`: Cost of equity
- `market_risk_premium`: Market risk premium
- `beta`: Beta
- `risk_free_rate`: Risk-free rate

### Available Screener Filters

- **Market Cap**: `market_cap_more_than`, `market_cap_lower_than`
- **Sector/Industry**: `sector`, `industry`
- **Price**: `price_more_than`, `price_lower_than`
- **Volume**: `volume_more_than`, `volume_lower_than`
- **Beta**: `beta_more_than`, `beta_lower_than`
- **Dividend**: `dividend_more_than`, `dividend_lower_than`
- **Exchange/Country**: `exchange`, `country`
- **Security Type**: `is_etf`, `is_fund`, `is_actively_trading`
- **Results**: `limit`, `include_all_share_classes`

## Configuration

The client supports various configuration options:

```python
client = FmpClient(
    api_key="your_api_key",
    base_url="https://financialmodelingprep.com/stable",  # Default
    timeout=60,  # Request timeout in seconds
    max_retries=3,  # Maximum retry attempts
    retry_delay=1.0,  # Base delay between retries
    max_concurrent_requests=10  # Rate limiting
)
```

## Error Handling

The client provides specific exception types for different error scenarios:

```python
from aiofmp import (
    FMPError,
    FMPAuthenticationError,
    FMPRateLimitError,
    FMPResponseError
)

try:
    result = await client.search.symbols("AAPL")
except FMPAuthenticationError:
    print("Invalid API key")
except FMPRateLimitError:
    print("Rate limit exceeded")
except FMPResponseError as e:
    print(f"API error: {e}")
except FMPError as e:
    print(f"General error: {e}")
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/fmp/test_search.py -v

# Run with coverage
uv run pytest --cov=aiofmp
```

### Code Quality

```bash
# Format code
uv run black aiofmp/ tests/

# Sort imports
uv run isort aiofmp/ tests/

# Type checking
uv run mypy aiofmp/
```

## Examples

See the `examples/` directory for complete working examples:

- `examples/fmp_search_example.py` - Comprehensive Search category examples
- `examples/fmp_directory_example.py` - Comprehensive Directory category examples
- `examples/fmp_analyst_example.py` - Comprehensive Analyst category examples
- `examples/fmp_calendar_example.py` - Comprehensive Calendar category examples
- `examples/fmp_chart_example.py` - Comprehensive Chart category examples
- `examples/fmp_company_example.py` - Comprehensive Company category examples
- `examples/fmp_cot_example.py` - Comprehensive Commitment of Traders (COT) category examples
- `examples/fmp_dcf_example.py` - Comprehensive Discounted Cash Flow (DCF) category examples

## API Key

To use this client, you'll need an API key from Financial Modeling Prep:

1. Visit [Financial Modeling Prep](https://financialmodelingprep.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Set it as an environment variable: `export FMP_API_KEY='your_key_here'`

## License

This project is licensed under the Apache 2.0 License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
