# **Free Stock Market API and Financial Statements API**

FMP is your source for the most reliable and accurate Stock Market API and Financial Data API available. Whether you're looking for [real-time stock prices](https://site.financialmodelingprep.com/developer/docs#real-time-full-price-quote), [financial statements](https://site.financialmodelingprep.com/developer/docs#income-statements-financial-statements), or [historical data](https://site.financialmodelingprep.com/developer/docs#earnings-historical-earnings), we offer a comprehensive solution to meet all your financial data needs.

Our platform provides free stock market data, including audited, standardized, and real-time updates of income statements, balance sheets, and cash flow statements on a quarterly and annual basis.

We also offer a wide range of historical stock prices, from 1 minute, 15 minutes, 30 minutes, 1 hour and daily intervals, ensuring you have the data you need.

*Note: When adding the API key to your requests, ensure to use **\&apikey=** if other query parameters already exist in the endpoint.*

*Any field marked with an \* is required*

## **Search**

[Stock Symbol Search API](https://site.financialmodelingprep.com/developer/docs/stable/search-symbol)

Easily find the ticker symbol of any stock with the FMP Stock Symbol Search API. Search by company name or symbol across multiple global markets.

**Endpoint:**

https://financialmodelingprep.com/stable/search-symbol?*query*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| query\* | string | AAPL |
| limit | number | 50 |
| exchange | string | NASDAQ |

Response   
\[  
	{  
		"symbol": "AAPL",  
		"name": "Apple Inc.",  
		"currency": "USD",  
		"exchangeFullName": "NASDAQ Global Select",  
		"exchange": "NASDAQ"  
	}  
\]

[Company Name Search API](https://site.financialmodelingprep.com/developer/docs/stable/search-name)

Search for ticker symbols, company names, and exchange details for equity securities and ETFs listed on various exchanges with the FMP Name Search API. This endpoint is useful for retrieving ticker symbols when you know the full or partial company or asset name but not the symbol identifier.

**Endpoint:**

https://financialmodelingprep.com/stable/search-name?*query*\=AA

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| query\* | string | AAPL |
| limit | number | 50 |
| exchange | string | NASDAQ |

Response  
\[  
	{  
		"symbol": "AAGUSD",  
		"name": "A	AG USD",  
		"currency": "USD",  
		"exchangeFullName": "CCC",  
		"exchange": "CRYPTO"  
	}  
\]

[Stock Screener API](https://site.financialmodelingprep.com/developer/docs/stable/search-company-screener)

Discover stocks that align with your investment strategy using the FMP Stock Screener API. Filter stocks based on market cap, price, volume, beta, sector, country, and more to identify the best opportunities.

**Endpoint:**

https://financialmodelingprep.com/stable/*company-screener*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| marketCapMoreThan | number | 1000000 |
| marketCapLowerThan | number | 1000000000 |
| sector | string | Technology |
| industry | string | Consumer Electronics |
| betaMoreThan | number | 0.5 |
| betaLowerThan | number | 1.5 |
| priceMoreThan | number | 10 |
| priceLowerThan | number | 200 |
| dividendMoreThan | number | 0.5 |
| dividendLowerThan | number | 2 |
| volumeMoreThan | number | 1000 |
| volumeLowerThan | number | 1000000 |
| exchange | string | NASDAQ |
| country | string | US |
| isEtf | boolean | false |
| isFund | boolean | false |
| isActivelyTrading | boolean | true |
| limit | number | 1000 |
| includeAllShareClasses | boolean | false |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"companyName": "Apple Inc.",  
		"marketCap": 3435062313000,  
		"sector": "Technology",  
		"industry": "Consumer Electronics",  
		"beta": 1.24,  
		"price": 225.93,  
		"lastAnnualDividend": 1,  
		"volume": 43010091,  
		"exchange": "NASDAQ Global Select",  
		"exchangeShortName": "NASDAQ",  
		"country": "US",  
		"isEtf": false,  
		"isFund": false,  
		"isActivelyTrading": true  
	}  
\]

## **Directory**

[Company Symbols List API](https://site.financialmodelingprep.com/developer/docs/stable/company-symbols-list)

Easily retrieve a comprehensive list of financial symbols with the FMP Company Symbols List API. Access a broad range of stock symbols and other tradable financial instruments from various global exchanges, helping you explore the full range of available securities.

Response  
\[  
	{  
		"symbol": "6898.HK",  
		"companyName": "China Aluminum Cans Holdings Limited"  
	}  
\]

[Financial Statement Symbols List API](https://site.financialmodelingprep.com/developer/docs/stable/financial-symbols-list)

Access a comprehensive list of companies with available financial statements through the FMP Financial Statement Symbols List API. Find companies listed on major global exchanges and obtain up-to-date financial data including income statements, balance sheets, and cash flow statements, are provided.

**Endpoint:**

https://financialmodelingprep.com/stable/*financial-statement-symbol-list*

Response  
\[  
	{  
		"symbol": "6898.HK",  
		"companyName": "China Aluminum Cans Holdings Limited",  
		"tradingCurrency": "HKD",  
		"reportingCurrency": "HKD"  
	}  
\]

[ETF Symbol Search API](https://site.financialmodelingprep.com/developer/docs/stable/etfs-list)

Quickly find ticker symbols and company names for Exchange Traded Funds (ETFs) using the FMP ETF Symbol Search API. This tool simplifies identifying specific ETFs by their name or ticker.

**Endpoint:**

https://financialmodelingprep.com/stable/*etf-list*

Response  
\[  
	{  
		"symbol": "GULF",  
		"name": "WisdomTree Middle East Dividend Fund"  
	}  
\]  
[Actively Trading List API](https://site.financialmodelingprep.com/developer/docs/stable/actively-trading-list)

List all actively trading companies and financial instruments with the FMP Actively Trading List API. This endpoint allows users to filter and display securities that are currently being traded on public exchanges, ensuring you access real-time market activity.

**Endpoint:**

https://financialmodelingprep.com/stable/*actively-trading-list*

Response  
\[  
	{  
		"symbol": "6898.HK",  
		"name": "China Aluminum Cans Holdings Limited"  
	}  
\]

[Earnings Transcript List API](https://site.financialmodelingprep.com/developer/docs/stable/earnings-transcript-list)

Access available earnings transcripts for companies with the FMP Earnings Transcript List API. Retrieve a list of companies with earnings transcripts, along with the total number of transcripts available for each company.

**Endpoint:**

https://financialmodelingprep.com/stable/*earnings-transcript-list*

Response  
\[  
	{  
		"symbol": "MCUJF",  
		"companyName": "Medicure Inc.",  
		"noOfTranscripts": "16"  
	}  
\]  
[Available Exchanges API](https://site.financialmodelingprep.com/developer/docs/stable/available-exchanges)

Access a complete list of supported stock exchanges using the FMP Available Exchanges API. This API provides a comprehensive overview of global stock exchanges, allowing users to identify where securities are traded and filter data by specific exchanges for further analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/*available-exchanges*

Response  
\[  
	{  
		"exchange": "AMEX",  
		"name": "New York Stock Exchange Arca",  
		"countryName": "United States of America",  
		"countryCode": "US",  
		"symbolSuffix": "N/A",  
		"delay": "Real-time"  
	}  
\]

[Available Sectors API](https://site.financialmodelingprep.com/developer/docs/stable/available-sectors)

Access a complete list of industry sectors using the FMP Available Sectors API. This API helps users categorize and filter companies based on their respective sectors, enabling deeper analysis and more focused queries across different industries.

**Endpoint:**

https://financialmodelingprep.com/stable/*available-sectors*

Response  
\[  
	{  
		"sector": "Basic Materials"  
	}  
\]  
[Available Industries API](https://site.financialmodelingprep.com/developer/docs/stable/available-industries)

Access a comprehensive list of industries where stock symbols are available using the FMP Available Industries API. This API helps users filter and categorize companies based on their industry for more focused research and analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/*available-industries*

Response  
\[  
	{  
		"industry": "Steel"  
	}  
\]

[Available Countries API](https://site.financialmodelingprep.com/developer/docs/stable/available-countries)

Access a comprehensive list of countries where stock symbols are available with the FMP Available Countries API. This API enables users to filter and analyze stock symbols based on the country of origin or the primary market where the securities are traded.

**Endpoint:**

https://financialmodelingprep.com/stable/*available-countries*

#### 

\[  
	{  
		"country": "FK"  
	}  
\]

## **Analyst**

[Financial Estimates API](https://site.financialmodelingprep.com/developer/docs/stable/financial-estimates)

Retrieve analyst financial estimates for stock symbols with the FMP Financial Estimates API. Access projected figures like revenue, earnings per share (EPS), and other key financial metrics as forecasted by industry analysts to inform your investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/analyst-estimates?*symbol*\=AAPL&*period*\=annual&*page*\=0&*limit*\=10

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| period\* | string | annual,quarter |
| page | number | 0 |
| limit | number | 10 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2029-09-28",  
		"revenueLow": 483092500000,  
		"revenueHigh": 483093500000,  
		"revenueAvg": 483093000000,  
		"ebitdaLow": 155952166036,  
		"ebitdaHigh": 155952488856,  
		"ebitdaAvg": 155952327446,  
		"ebitLow": 140628295747,  
		"ebitHigh": 140628586847,  
		"ebitAvg": 140628441297,  
		"netIncomeLow": 139446957701,  
		"netIncomeHigh": 157185372990,  
		"netIncomeAvg": 149150359609,  
		"sgaExpenseLow": 31694652812,  
		"sgaExpenseHigh": 31694718420,  
		"sgaExpenseAvg": 31694685616,  
		"epsAvg": 9.68,  
		"epsHigh": 10.20148,  
		"epsLow": 9.05024,  
		"numAnalystsRevenue": 16,  
		"numAnalystsEps": 6  
	}  
\]

[Ratings Snapshot API](https://site.financialmodelingprep.com/developer/docs/stable/ratings-snapshot)

Quickly assess the financial health and performance of companies with the FMP Ratings Snapshot API. This API provides a comprehensive snapshot of financial ratings for stock symbols in our database, based on various key financial ratios.

**Endpoint:**

https://financialmodelingprep.com/stable/ratings-snapshot?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 1 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"rating": "A-",  
		"overallScore": 4,  
		"discountedCashFlowScore": 3,  
		"returnOnEquityScore": 5,  
		"returnOnAssetsScore": 5,  
		"debtToEquityScore": 4,  
		"priceToEarningsScore": 2,  
		"priceToBookScore": 1  
	}  
\]

[Historical Ratings API](https://site.financialmodelingprep.com/developer/docs/stable/historical-ratings)

Track changes in financial performance over time with the FMP Historical Ratings API. This API provides access to historical financial ratings for stock symbols in our database, allowing users to view ratings and key financial metric scores for specific dates.

**Endpoint:**

https://financialmodelingprep.com/stable/ratings-historical?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 1 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"rating": "A-",  
		"overallScore": 4,  
		"discountedCashFlowScore": 3,  
		"returnOnEquityScore": 5,  
		"returnOnAssetsScore": 5,  
		"debtToEquityScore": 4,  
		"priceToEarningsScore": 2,  
		"priceToBookScore": 1  
	}  
\]

[Price Target Summary API](https://site.financialmodelingprep.com/developer/docs/stable/price-target-summary)

Gain insights into analysts' expectations for stock prices with the FMP Price Target Summary API. This API provides access to average price targets from analysts across various timeframes, helping investors assess future stock performance based on expert opinions.

**Endpoint:**

https://financialmodelingprep.com/stable/price-target-summary?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"lastMonthCount": 1,  
		"lastMonthAvgPriceTarget": 200.75,  
		"lastQuarterCount": 3,  
		"lastQuarterAvgPriceTarget": 204.2,  
		"lastYearCount": 48,  
		"lastYearAvgPriceTarget": 232.99,  
		"allTimeCount": 167,  
		"allTimeAvgPriceTarget": 201.21,  
		"publishers": "\[\\"Benzinga\\",\\"StreetInsider\\",\\"TheFly\\",\\"Pulse 2.0\\",\\"TipRanks Contributor\\",\\"MarketWatch\\",\\"Investing\\",\\"Barrons\\",\\"Investor's Business Daily\\"\]"  
	}  
\]

[Price Target Consensus API](https://site.financialmodelingprep.com/developer/docs/stable/price-target-consensus)

Access analysts' consensus price targets with the FMP Price Target Consensus API. This API provides high, low, median, and consensus price targets for stocks, offering investors a comprehensive view of market expectations for future stock prices.

**Endpoint:**

https://financialmodelingprep.com/stable/price-target-consensus?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"targetHigh": 300,  
		"targetLow": 200,  
		"targetConsensus": 251.7,  
		"targetMedian": 258  
	}  
\]

[Price Target News API](https://site.financialmodelingprep.com/developer/docs/stable/price-target-news)

Stay informed with real-time updates on analysts' price targets for stocks using the FMP Price Target News API. Access the latest forecasts, stock prices at the time of the update, and direct links to trusted news sources for deeper insights.

**Endpoint:**

https://financialmodelingprep.com/stable/price-target-news?*symbol*\=AAPL&*page*\=0&*limit*\=10

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 10 |
| page | number | 0 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"publishedDate": "2025-01-21T01:24:32.000Z",  
		"newsURL": "https://www.benzinga.com/markets/equities/25/01/43087992/apple-gets-rare-downgrade-from-jefferies-analyst-warns-on-slowing-revenue-growth-missed-forecast",  
		"newsTitle": "Apple Gets Rare Downgrade From Jefferies, Analyst Warns On Slowing Revenue Growth, Missed Forecasts, And Falling iPhone Demand",  
		"analystName": "Edison Lee",  
		"priceTarget": 200.75,  
		"adjPriceTarget": 200.75,  
		"priceWhenPosted": 229.98,  
		"newsPublisher": "Benzinga",  
		"newsBaseURL": "benzinga.com",  
		"analystCompany": "Jefferies"  
	}  
\]

[Price Target Latest News API](https://site.financialmodelingprep.com/developer/docs/stable/price-target-latest-news)

Stay updated with the most recent analyst price target updates for all stock symbols using the FMP Price Target Latest News API. Get access to detailed forecasts, stock prices at the time of the update, analyst insights, and direct links to news sources for deeper analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/price-target-latest-news?*page*\=0&*limit*\=10

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| limit | number | 10 |
| page | number | 0 |

Response

\[  
	{  
		"symbol": "OLN",  
		"publishedDate": "2025-02-03T18:23:58.000Z",  
		"newsURL": "https://www.benzinga.com/25/02/43444520/these-analysts-cut-their-forecasts-on-olin-after-q4-earnings",  
		"newsTitle": "These Analysts Cut Their Forecasts On Olin After Q4 Earnings",  
		"analystName": "Peter Osterland",  
		"priceTarget": 32,  
		"adjPriceTarget": 32,  
		"priceWhenPosted": 27.76,  
		"newsPublisher": "Benzinga",  
		"newsBaseURL": "benzinga.com",  
		"analystCompany": "Truist Financial"  
	}  
\]

[Stock Grades API](https://site.financialmodelingprep.com/developer/docs/stable/grades)

Access the latest stock grades from top analysts and financial institutions with the FMP Grades API. Track grading actions, such as upgrades, downgrades, or maintained ratings, for specific stock symbols, providing valuable insight into how experts evaluate companies over time.

**Endpoint:**

https://financialmodelingprep.com/stable/grades?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-01-31",  
		"gradingCompany": "Morgan Stanley",  
		"previousGrade": "Overweight",  
		"newGrade": "Overweight",  
		"action": "maintain"  
	}  
\]

[Historical Stock Grades API](https://site.financialmodelingprep.com/developer/docs/stable/historical-grades)  
Globe Flag

Access a comprehensive record of analyst grades with the FMP Historical Grades API. This tool allows you to track historical changes in analyst ratings for specific stock symbol

**Endpoint:**

https://financialmodelingprep.com/stable/grades-historical?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-01",  
		"analystRatingsBuy": 8,  
		"analystRatingsHold": 14,  
		"analystRatingsSell": 2,  
		"analystRatingsStrongSell": 2  
	}  
\]

[Stock Grades Summary API](https://site.financialmodelingprep.com/developer/docs/stable/grades-summary)

Quickly access an overall view of analyst ratings with the FMP Grades Summary API. This API provides a consolidated summary of market sentiment for individual stock symbols, including the total number of strong buy, buy, hold, sell, and strong sell ratings. Understand the overall consensus on a stock’s outlook with just a few data points.

**Endpoint:**

https://financialmodelingprep.com/stable/grades-consensus?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"strongBuy": 1,  
		"buy": 29,  
		"hold": 11,  
		"sell": 4,  
		"strongSell": 0,  
		"consensus": "Buy"  
	}  
\]

[Stock Grade News API](https://site.financialmodelingprep.com/developer/docs/stable/grade-news)

Stay informed on the latest analyst grade changes with the FMP Grade News API. This API provides real-time updates on stock rating changes, including the grading company, previous and new grades, and the action taken. Direct links to trusted news sources and stock prices at the time of the update help you stay ahead of market trends and analyst opinions for specific stock symbols.

**Endpoint:**

https://financialmodelingprep.com/stable/grades-news?*symbol*\=AAPL&*page*\=0&*limit*\=1

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| page | number | 0 |
| limit | number | 1 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"publishedDate": "2025-01-31T10:11:47.000Z",  
		"newsURL": "https://www.benzinga.com/25/01/43379061/why-apple-shares-are-trading-higher-here-are-20-stocks-moving-premarket",  
		"newsTitle": "Why Apple Shares Are Trading Higher; Here Are 20 Stocks Moving Premarket",  
		"newsBaseURL": "benzinga.com",  
		"newsPublisher": "Benzinga",  
		"newGrade": "Buy",  
		"previousGrade": "Hold",  
		"gradingCompany": "Maxim Group",  
		"action": "initialise",  
		"priceWhenPosted": 237.59  
	}  
\]

[Stock Grade Latest News API](https://site.financialmodelingprep.com/developer/docs/stable/grade-latest-news)

Stay informed on the latest stock rating changes with the FMP Grade Latest News API. This API provides the most recent updates on analyst ratings for all stock symbols, including links to the original news sources. Track stock price movements, grading firm actions, and market sentiment shifts in real time, sourced from trusted publishers.

**Endpoint:**

https://financialmodelingprep.com/stable/grades-latest-news?*page*\=0&*limit*\=10

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 10 |

Response

\[  
	{  
		"symbol": "PYPL",  
		"publishedDate": "2025-02-04T19:18:04.000Z",  
		"newsURL": "https://www.benzinga.com/25/02/43475080/paypal-beats-q4-estimates-as-transaction-margins-and-payment-volume-drive-growth-eyes-2025-growth-with-strong-tmd",  
		"newsTitle": "PayPal Transaction Margins and Payment Volume Drive Growth, Eyes 2025 Growth With Strong TMD Ahead of Investor Day: Analyst",  
		"newsBaseURL": "benzinga.com",  
		"newsPublisher": "Benzinga",  
		"newGrade": "Overweight",  
		"previousGrade": "Overweight",  
		"gradingCompany": "J.P. Morgan",  
		"action": "hold",  
		"priceWhenPosted": 77.725  
	}  
\]

## **Calendar**

[Dividends Company API](https://site.financialmodelingprep.com/developer/docs/stable/dividends-company)

Stay informed about upcoming dividend payments with the FMP Dividends Company API. This API provides essential dividend data for individual stock symbols, including record dates, payment dates, declaration dates, and more.

**Endpoint:**

https://financialmodelingprep.com/stable/dividends?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-10",  
		"recordDate": "2025-02-10",  
		"paymentDate": "2025-02-13",  
		"declarationDate": "2025-01-30",  
		"adjDividend": 0.25,  
		"dividend": 0.25,  
		"yield": 0.42955326460481097,  
		"frequency": "Quarterly"  
	}  
\]

[Dividends Calendar API](https://site.financialmodelingprep.com/developer/docs/stable/dividends-calendar)

Stay informed on upcoming dividend events with the Dividend Events Calendar API. Access a comprehensive schedule of dividend-related dates for all stocks, including record dates, payment dates, declaration dates, and dividend yields.

**Endpoint:**

https://financialmodelingprep.com/stable/*dividends-calendar*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response  
\[  
	{  
		"symbol": "1D0.SI",  
		"date": "2025-02-04",  
		"recordDate": "",  
		"paymentDate": "",  
		"declarationDate": "",  
		"adjDividend": 0.01,  
		"dividend": 0.01,  
		"yield": 6.25,  
		"frequency": "Semi-Annual"  
	}  
\]

[Earnings Report API](https://site.financialmodelingprep.com/developer/docs/stable/earnings-company)

Retrieve in-depth earnings information with the FMP Earnings Report API. Gain access to key financial data for a specific stock symbol, including earnings report dates, EPS estimates, and revenue projections to help you stay on top of company performance.

**Endpoint:**

https://financialmodelingprep.com/stable/earnings?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-10-29",  
		"epsActual": null,  
		"epsEstimated": null,  
		"revenueActual": null,  
		"revenueEstimated": null,  
		"lastUpdated": "2025-02-04"  
	}  
\]

[Earnings Calendar API](https://site.financialmodelingprep.com/developer/docs/stable/earnings-calendar)

Stay informed on upcoming and past earnings announcements with the FMP Earnings Calendar API. Access key data, including announcement dates, estimated earnings per share (EPS), and actual EPS for publicly traded companies.

**Endpoint:**

https://financialmodelingprep.com/stable/*earnings-calendar*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response

\[  
	{  
		"symbol": "KEC.NS",  
		"date": "2024-11-04",  
		"epsActual": 3.32,  
		"epsEstimated": 4.97,  
		"revenueActual": 51133100000,  
		"revenueEstimated": 44687400000,  
		"lastUpdated": "2024-12-08"  
	}  
\]

[IPOs Calendar API](https://site.financialmodelingprep.com/developer/docs/stable/ipos-calendar)

Access a comprehensive list of all upcoming initial public offerings (IPOs) with the FMP IPO Calendar API. Stay up to date on the latest companies entering the public market, with essential details on IPO dates, company names, expected pricing, and exchange listings.

**Endpoint:**

https://financialmodelingprep.com/stable/*ipos-calendar*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response  
\[  
	{  
		"symbol": "PEVC",  
		"date": "2025-02-03",  
		"daa": "2025-02-03T05:00:00.000Z",  
		"company": "Pacer Funds Trust",  
		"exchange": "NYSE",  
		"actions": "Expected",  
		"shares": null,  
		"priceRange": null,  
		"marketCap": null  
	}  
\]

[IPOs Disclosure API](https://site.financialmodelingprep.com/developer/docs/stable/ipos-disclosure)

Access a comprehensive list of disclosure filings for upcoming initial public offerings (IPOs) with the FMP IPO Disclosures API. Stay updated on regulatory filings, including filing dates, effectiveness dates, CIK numbers, and form types, with direct links to official SEC documents.

**Endpoint:**

https://financialmodelingprep.com/stable/*ipos-disclosure*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response  
\[  
	{  
		"symbol": "SCHM",  
		"filingDate": "2025-02-03",  
		"acceptedDate": "2025-02-03",  
		"effectivenessDate": "2025-02-03",  
		"cik": "0001454889",  
		"form": "CERT",  
		"url": "https://www.sec.gov/Archives/edgar/data/1454889/000114336225000044/SCCR020325.pdf"  
	}  
\]

[IPOs Prospectus API](https://site.financialmodelingprep.com/developer/docs/stable/ipos-prospectus)

Access comprehensive information on IPO prospectuses with the FMP IPO Prospectus API. Get key financial details, such as public offering prices, discounts, commissions, proceeds before expenses, and more. This API also provides links to official SEC prospectuses, helping investors stay informed on companies entering the public market.

**Endpoint:**

https://financialmodelingprep.com/stable/*ipos-prospectus*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response  
\[  
	{  
		"symbol": "ATAK",  
		"acceptedDate": "2025-02-03",  
		"filingDate": "2025-02-03",  
		"ipoDate": "2022-03-20",  
		"cik": "0001883788",  
		"pricePublicPerShare": 0.78,  
		"pricePublicTotal": 4649936.72,  
		"discountsAndCommissionsPerShare": 0.04,  
		"discountsAndCommissionsTotal": 254909.67,  
		"proceedsBeforeExpensesPerShare": 0.74,  
		"proceedsBeforeExpensesTotal": 4395207.05,  
		"form": "424B4",  
		"url": "https://www.sec.gov/Archives/edgar/data/1883788/000149315225004604/form424b4.htm"  
	}  
\]

[Stock Split Details API](https://site.financialmodelingprep.com/developer/docs/stable/splits-company)

Access detailed information on stock splits for a specific company using the FMP Stock Split Details API. This API provides essential data, including the split date and the split ratio, helping users understand changes in a company's share structure after a stock split.

**Endpoint:**

https://financialmodelingprep.com/stable/splits?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2020-08-31",  
		"numerator": 4,  
		"denominator": 1  
	}  
\]

[Stock Splits Calendar API](https://site.financialmodelingprep.com/developer/docs/stable/splits-calendar)

Stay informed about upcoming stock splits with the FMP Stock Splits Calendar API. This API provides essential data on upcoming stock splits across multiple companies, including the split date and ratio, helping you track changes in share structures before they occur.

**Endpoint:**

https://financialmodelingprep.com/stable/*splits-calendar*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-05-21 |
| to | date | 2025-08-21 |

Response

\[  
	{  
		"symbol": "EYEN",  
		"date": "2025-02-03",  
		"numerator": 1,  
		"denominator": 80  
	}  
\]

## **Chart**

[Stock Chart Light API](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-light)

Access simplified stock chart data using the FMP Basic Stock Chart API. This API provides essential charting information, including date, price, and trading volume, making it ideal for tracking stock performance with minimal data and creating basic price and volume charts.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/light?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"price": 232.8,  
		"volume": 44489128  
	}  
\]

[Stock Price and Volume Data API](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-full)

Access full price and volume data for any stock symbol using the FMP Comprehensive Stock Price and Volume Data API. Get detailed insights, including open, high, low, close prices, trading volume, price changes, percentage changes, and volume-weighted average price (VWAP).

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/full?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"open": 227.2,  
		"high": 233.13,  
		"low": 226.65,  
		"close": 232.8,  
		"volume": 44489128,  
		"change": 5.6,  
		"changePercent": 2.46479,  
		"vwap": 230.86  
	}  
\]

[Unadjusted Stock Price API](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-non-split-adjusted)

Access stock price and volume data without adjustments for stock splits with the FMP Unadjusted Stock Price Chart API. Get accurate insights into stock performance, including open, high, low, and close prices, along with trading volume, without split-related changes.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/non-split-adjusted?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"adjOpen": 227.2,  
		"adjHigh": 233.13,  
		"adjLow": 226.65,  
		"adjClose": 232.8,  
		"volume": 44489128  
	}  
\]

[Dividend Adjusted Price Chart API](https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-dividend-adjusted)

Analyze stock performance with dividend adjustments using the FMP Dividend-Adjusted Price Chart API. Access end-of-day price and volume data that accounts for dividend payouts, offering a more comprehensive view of stock trends over time.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/dividend-adjusted?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"adjOpen": 227.2,  
		"adjHigh": 233.13,  
		"adjLow": 226.65,  
		"adjClose": 232.8,  
		"volume": 44489128  
	}  
\]

[1 Min Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-1-min)

Access precise intraday stock price and volume data with the FMP 1-Minute Interval Stock Chart API. Retrieve real-time or historical stock data in 1-minute intervals, including key information such as open, high, low, and close prices, and trading volume for each minute.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1min?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response  
\[  
	{  
		"date": "2025-02-04 15:59:00",  
		"open": 233.01,  
		"low": 232.72,  
		"high": 233.13,  
		"close": 232.79,  
		"volume": 720121  
	}  
\]

[5 Min Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-5-min)

Access stock price and volume data with the FMP 5-Minute Interval Stock Chart API. Retrieve detailed stock data in 5-minute intervals, including open, high, low, and close prices, along with trading volume for each 5-minute period. This API is perfect for short-term trading analysis and building intraday charts.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/5min?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response  
\[  
	{  
		"date": "2025-02-04 15:55:00",  
		"open": 232.87,  
		"low": 232.72,  
		"high": 233.13,  
		"close": 232.79,  
		"volume": 1555040  
	}  
\]

[15 Min Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-15-min)

Access stock price and volume data with the FMP 15-Minute Interval Stock Chart API. Retrieve detailed stock data in 15-minute intervals, including open, high, low, close prices, and trading volume. This API is ideal for creating intraday charts and analyzing medium-term price trends during the trading day.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/15min?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response

\[  
	{  
		"date": "2025-02-04 15:45:00",  
		"open": 232.25,  
		"low": 232.18,  
		"high": 233.13,  
		"close": 232.79,  
		"volume": 2535629  
	}  
\]

[30 Min Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-30-min)

Access stock price and volume data with the FMP 30-Minute Interval Stock Chart API. Retrieve essential stock data in 30-minute intervals, including open, high, low, close prices, and trading volume. This API is perfect for creating intraday charts and tracking medium-term price movements for more strategic trading decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/30min?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response  
\[  
	{  
		"date": "2025-02-04 15:30:00",  
		"open": 232.29,  
		"low": 232.01,  
		"high": 233.13,  
		"close": 232.79,  
		"volume": 3476320  
	}  
\]

[1 Hour Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-1-hour)

Track stock price movements over hourly intervals with the FMP 1-Hour Interval Stock Chart API. Access essential stock price and volume data, including open, high, low, and close prices for each hour, to analyze broader intraday trends with precision.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1hour?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response  
\[  
	{  
		"date": "2025-02-04 15:30:00",  
		"open": 232.29,  
		"low": 232.01,  
		"high": 233.13,  
		"close": 232.37,  
		"volume": 15079381  
	}  
\]

[4 Hour Interval Stock Chart API](https://site.financialmodelingprep.com/developer/docs/stable/intraday-4-hour)

Analyze stock price movements over extended intraday periods with the FMP 4-Hour Interval Stock Chart API. Access key stock price and volume data in 4-hour intervals, perfect for tracking longer intraday trends and understanding broader market movements.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/4hour?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |
| nonadjusted | boolean | false |

Response  
\[  
	{  
		"date": "2025-02-04 12:30:00",  
		"open": 231.79,  
		"low": 231.37,  
		"high": 233.13,  
		"close": 232.37,  
		"volume": 23781913  
	}  
\]

## **Company**

[Company Profile Data API](https://site.financialmodelingprep.com/developer/docs/stable/profile-symbol)

Access detailed company profile data with the FMP Company Profile Data API. This API provides key financial and operational information for a specific stock symbol, including the company's market capitalization, stock price, industry, and much more.

**Endpoint:**

https://financialmodelingprep.com/stable/profile?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"price": 232.8,  
		"marketCap": 3500823120000,  
		"beta": 1.24,  
		"lastDividend": 0.99,  
		"range": "164.08-260.1",  
		"change": 4.79,  
		"changePercentage": 2.1008,  
		"volume": 0,  
		"averageVolume": 50542058,  
		"companyName": "Apple Inc.",  
		"currency": "USD",  
		"cik": "0000320193",  
		"isin": "US0378331005",  
		"cusip": "037833100",  
		"exchangeFullName": "NASDAQ Global Select",  
		"exchange": "NASDAQ",  
		"industry": "Consumer Electronics",  
		"website": "https://www.apple.com",  
		"description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discov...",  
		"ceo": "Mr. Timothy D. Cook",  
		"sector": "Technology",  
		"country": "US",  
		"fullTimeEmployees": "164000",  
		"phone": "(408) 996-1010",  
		"address": "One Apple Park Way",  
		"city": "Cupertino",  
		"state": "CA",  
		"zip": "95014",  
		"image": "https://images.financialmodelingprep.com/symbol/AAPL.png",  
		"ipoDate": "1980-12-12",  
		"defaultImage": false,  
		"isEtf": false,  
		"isActivelyTrading": true,  
		"isAdr": false,  
		"isFund": false  
	}  
\]

[Company Notes API](https://site.financialmodelingprep.com/developer/docs/stable/company-notes)

Retrieve detailed information about company-issued notes with the FMP Company Notes API. Access essential data such as CIK number, stock symbol, note title, and the exchange where the notes are listed.

**Endpoint:**

https://financialmodelingprep.com/stable/company-notes?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"cik": "0000320193",  
		"symbol": "AAPL",  
		"title": "1.000% Notes due 2022",  
		"exchange": "NASDAQ"  
	}  
\]

[Company Employee Count API](https://site.financialmodelingprep.com/developer/docs/stable/employee-count)

Retrieve detailed workforce information for companies, including employee count, reporting period, and filing date. The FMP Company Employee Count API also provides direct links to official SEC documents for further verification and in-depth research.

**Endpoint:**

https://financialmodelingprep.com/stable/employee-count?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"cik": "0000320193",  
		"acceptanceTime": "2024-11-01 06:01:36",  
		"periodOfReport": "2024-09-28",  
		"companyName": "Apple Inc.",  
		"formType": "10-K",  
		"filingDate": "2024-11-01",  
		"employeeCount": 164000,  
		"source": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/0000320193-24-000123-index.htm"  
	}  
\]  
[Company Historical Employee Count API](https://site.financialmodelingprep.com/developer/docs/stable/historical-employee-count)

Access historical employee count data for a company based on specific reporting periods. The FMP Company Historical Employee Count API provides insights into how a company’s workforce has evolved over time, allowing users to analyze growth trends and operational changes.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-employee-count?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"cik": "0000320193",  
		"acceptanceTime": "2024-11-01 06:01:36",  
		"periodOfReport": "2024-09-28",  
		"companyName": "Apple Inc.",  
		"formType": "10-K",  
		"filingDate": "2024-11-01",  
		"employeeCount": 164000,  
		"source": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/0000320193-24-000123-index.htm"  
	}  
\]

[Company Market Cap API](https://site.financialmodelingprep.com/developer/docs/stable/market-cap)

Retrieve the market capitalization for a specific company on any given date using the FMP Company Market Capitalization API. This API provides essential data to assess the size and value of a company in the stock market, helping users gauge its overall market standing.

**Endpoint:**

https://financialmodelingprep.com/stable/market-capitalization?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"marketCap": 3500823120000  
	}  
\]

[Batch Market Cap API](https://site.financialmodelingprep.com/developer/docs/stable/batch-market-cap)

Retrieve market capitalization data for multiple companies in a single request with the FMP Batch Market Capitalization API. This API allows users to compare the market size of various companies simultaneously, streamlining the analysis of company valuations.

**Endpoint:**

https://financialmodelingprep.com/stable/market-capitalization-batch?*symbols*\=AAPL,MSFT,GOOG

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbols\* | string | AAPL,MSFT,GOOG |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"marketCap": 3500823120000  
	}  
\]

[Historical Market Cap API](https://site.financialmodelingprep.com/developer/docs/stable/historical-market-cap)

Access historical market capitalization data for a company using the FMP Historical Market Capitalization API. This API helps track the changes in market value over time, enabling long-term assessments of a company's growth or decline.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-market-capitalization?*symbol*\=AAPL

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 100 |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-02-29",  
		"marketCap": 2784608472000  
	}  
\]

[Company Share Float & Liquidity API](https://site.financialmodelingprep.com/developer/docs/stable/shares-float)

Understand the liquidity and volatility of a stock with the FMP Company Share Float and Liquidity API. Access the total number of publicly traded shares for any company to make informed investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/shares-float?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04 17:01:35",  
		"freeFloat": 99.9095,  
		"floatShares": 15024290700,  
		"outstandingShares": 15037900000  
	}  
\]

[All Shares Float API](https://site.financialmodelingprep.com/developer/docs/stable/all-shares-float)

Access comprehensive shares float data for all available companies with the FMP All Shares Float API. Retrieve critical information such as free float, float shares, and outstanding shares to analyze liquidity across a wide range of companies.

**Endpoint:**

https://financialmodelingprep.com/stable/shares-float-all?*page*\=0&*limit*\=1000

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| limit | number | 1000 |
| page | number | 0 |

Response  
\[  
	{  
		"symbol": "6898.HK",  
		"date": "2025-02-04 17:27:01",  
		"freeFloat": 33.2536,  
		"floatShares": 318128880,  
		"outstandingShares": 956675009  
	}  
\]

[Latest Mergers & Acquisitions API](https://site.financialmodelingprep.com/developer/docs/stable/latest-mergers-acquisitions)

Access real-time data on the latest mergers and acquisitions with the FMP Latest Mergers and Acquisitions API. This API provides key information such as the transaction date, company names, and links to detailed filing information for further analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/mergers-acquisitions-latest?*page*\=0&*limit*\=100

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 100 |

Response

\[  
	{  
		"symbol": "NLOK",  
		"companyName": "NortonLifeLock Inc.",  
		"cik": "0000849399",  
		"targetedCompanyName": "MoneyLion Inc.",  
		"targetedCik": "0001807846",  
		"targetedSymbol": "ML",  
		"transactionDate": "2025-02-03",  
		"acceptedDate": "2025-02-03 06:01:10",  
		"link": "https://www.sec.gov/Archives/edgar/data/849399/000114036125002752/ny20039778x6\_s4.htm"  
	}  
\]

[Search Mergers & Acquisitions API](https://site.financialmodelingprep.com/developer/docs/stable/search-mergers-acquisitions)

Search for specific mergers and acquisitions data with the FMP Search Mergers and Acquisitions API. Retrieve detailed information on M\&A activity, including acquiring and targeted companies, transaction dates, and links to official SEC filings.

**Endpoint:**

https://financialmodelingprep.com/stable/mergers-acquisitions-search?*name*\=Apple

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| name\* | string | Apple |

Response  
\[  
	{  
		"symbol": "PEGY",  
		"companyName": "Pineapple Energy Inc.",  
		"cik": "0000022701",  
		"targetedCompanyName": "Communications Systems, Inc.",  
		"targetedCik": "0000022701",  
		"targetedSymbol": "JCS",  
		"transactionDate": "2021-11-12",  
		"acceptedDate": "2021-11-12 09:54:22",  
		"link": "https://www.sec.gov/Archives/edgar/data/22701/000089710121000932/a211292\_s-4.htm"  
	}  
\]

[Company Executives API](https://site.financialmodelingprep.com/developer/docs/stable/company-executives)

Retrieve detailed information on company executives with the FMP Company Executives API. This API provides essential data about key executives, including their name, title, compensation, and other demographic details such as gender and year of birth.

**Endpoint:**

https://financialmodelingprep.com/stable/key-executives?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| active | string | true |

Response

\[  
	{  
		"title": "Vice President of Worldwide Sales",  
		"name": "Mr. Michael  Fenger",  
		"pay": null,  
		"currencyPay": "USD",  
		"gender": "male",  
		"yearBorn": null,  
		"active": null  
	}  
\]

[Executive Compensation API](https://site.financialmodelingprep.com/developer/docs/stable/executive-compensation)

Retrieve comprehensive compensation data for company executives with the FMP Executive Compensation API. This API provides detailed information on salaries, stock awards, total compensation, and other relevant financial data, including filing details and links to official documents.

**Endpoint:**

https://financialmodelingprep.com/stable/governance-executive-compensation?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"cik": "0000320193",  
		"symbol": "AAPL",  
		"companyName": "Apple Inc.",  
		"filingDate": "2025-01-10",  
		"acceptedDate": "2025-01-10 16:31:18",  
		"nameAndPosition": "Kate Adams Senior Vice President, General Counsel and Secretary",  
		"year": 2023,  
		"salary": 1000000,  
		"bonus": 0,  
		"stockAward": 22323641,  
		"optionAward": 0,  
		"incentivePlanCompensation": 3571150,  
		"allOtherCompensation": 46914,  
		"total": 26941705,  
		"link": "https://www.sec.gov/Archives/edgar/data/320193/000130817925000008/0001308179-25-000008-index.htm"  
	}  
\]

[Executive Compensation Benchmark API](https://site.financialmodelingprep.com/developer/docs/stable/executive-compensation-benchmark)

Gain access to average executive compensation data across various industries with the FMP Executive Compensation Benchmark API. This API provides essential insights for comparing executive pay by industry, helping you understand compensation trends and benchmarks.

**Endpoint:**

https://financialmodelingprep.com/stable/*executive-compensation-benchmark*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| year | string | 2024 |

Response  
\[  
	{  
		"industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS",  
		"year": 2023,  
		"averageCompensation": 694313.1666666666  
	}  
\]

## **Commitment Of Traders**

[COT Report API](https://site.financialmodelingprep.com/developer/docs/stable/cot-report)

Access comprehensive Commitment of Traders (COT) reports with the FMP COT Report API. This API provides detailed information about long and short positions across various sectors, helping you assess market sentiment and track positions in commodities, indices, and financial instruments.

**Endpoint:**

https://financialmodelingprep.com/stable/*commitment-of-traders-report*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |

Response

\[  
	{  
		"symbol": "KC",  
		"date": "2024-02-27 00:00:00",  
		"name": "Coffee (KC)",  
		"sector": "SOFTS",  
		"marketAndExchangeNames": "COFFEE C \- ICE FUTURES U.S.",  
		"cftcContractMarketCode": "083731",  
		"cftcMarketCode": "ICUS",  
		"cftcRegionCode": "1",  
		"cftcCommodityCode": "83",  
		"openInterestAll": 209453,  
		"noncommPositionsLongAll": 75330,  
		"noncommPositionsShortAll": 23630,  
		"noncommPositionsSpreadAll": 47072,  
		"commPositionsLongAll": 79690,  
		"commPositionsShortAll": 132114,  
		"totReptPositionsLongAll": 202092,  
		"totReptPositionsShortAll": 202816,  
		"nonreptPositionsLongAll": 7361,  
		"nonreptPositionsShortAll": 6637,  
		"openInterestOld": 179986,  
		"noncommPositionsLongOld": 75483,  
		"noncommPositionsShortOld": 35395,  
		"noncommPositionsSpreadOld": 27067,  
		"commPositionsLongOld": 70693,  
		"commPositionsShortOld": 111666,  
		"totReptPositionsLongOld": 173243,  
		"totReptPositionsShortOld": 174128,  
		"nonreptPositionsLongOld": 6743,  
		"nonreptPositionsShortOld": 5858,  
		"openInterestOther": 29467,  
		"noncommPositionsLongOther": 18754,  
		"noncommPositionsShortOther": 7142,  
		"noncommPositionsSpreadOther": 1098,  
		"commPositionsLongOther": 8997,  
		"commPositionsShortOther": 20448,  
		"totReptPositionsLongOther": 28849,  
		"totReptPositionsShortOther": 28688,  
		"nonreptPositionsLongOther": 618,  
		"nonreptPositionsShortOther": 779,  
		"changeInOpenInterestAll": 2957,  
		"changeInNoncommLongAll": \-3545,  
		"changeInNoncommShortAll": 618,  
		"changeInNoncommSpeadAll": 1575,  
		"changeInCommLongAll": 4978,  
		"changeInCommShortAll": 802,  
		"changeInTotReptLongAll": 3008,  
		"changeInTotReptShortAll": 2995,  
		"changeInNonreptLongAll": \-51,  
		"changeInNonreptShortAll": \-38,  
		"pctOfOpenInterestAll": 100,  
		"pctOfOiNoncommLongAll": 36,  
		"pctOfOiNoncommShortAll": 11.3,  
		"pctOfOiNoncommSpreadAll": 22.5,  
		"pctOfOiCommLongAll": 38,  
		"pctOfOiCommShortAll": 63.1,  
		"pctOfOiTotReptLongAll": 96.5,  
		"pctOfOiTotReptShortAll": 96.8,  
		"pctOfOiNonreptLongAll": 3.5,  
		"pctOfOiNonreptShortAll": 3.2,  
		"pctOfOpenInterestOl": 100,  
		"pctOfOiNoncommLongOl": 41.9,  
		"pctOfOiNoncommShortOl": 19.7,  
		"pctOfOiNoncommSpreadOl": 15,  
		"pctOfOiCommLongOl": 39.3,  
		"pctOfOiCommShortOl": 62,  
		"pctOfOiTotReptLongOl": 96.3,  
		"pctOfOiTotReptShortOl": 96.7,  
		"pctOfOiNonreptLongOl": 3.7,  
		"pctOfOiNonreptShortOl": 3.3,  
		"pctOfOpenInterestOther": 100,  
		"pctOfOiNoncommLongOther": 63.6,  
		"pctOfOiNoncommShortOther": 24.2,  
		"pctOfOiNoncommSpreadOther": 3.7,  
		"pctOfOiCommLongOther": 30.5,  
		"pctOfOiCommShortOther": 69.4,  
		"pctOfOiTotReptLongOther": 97.9,  
		"pctOfOiTotReptShortOther": 97.4,  
		"pctOfOiNonreptLongOther": 2.1,  
		"pctOfOiNonreptShortOther": 2.6,  
		"tradersTotAll": 357,  
		"tradersNoncommLongAll": 132,  
		"tradersNoncommShortAll": 77,  
		"tradersNoncommSpreadAll": 94,  
		"tradersCommLongAll": 106,  
		"tradersCommShortAll": 119,  
		"tradersTotReptLongAll": 286,  
		"tradersTotReptShortAll": 250,  
		"tradersTotOl": 351,  
		"tradersNoncommLongOl": 136,  
		"tradersNoncommShortOl": 72,  
		"tradersNoncommSpeadOl": 88,  
		"tradersCommLongOl": 94,  
		"tradersCommShortOl": 114,  
		"tradersTotReptLongOl": 269,  
		"tradersTotReptShortOl": 239,  
		"tradersTotOther": 164,  
		"tradersNoncommLongOther": 31,  
		"tradersNoncommShortOther": 34,  
		"tradersNoncommSpreadOther": 16,  
		"tradersCommLongOther": 59,  
		"tradersCommShortOther": 68,  
		"tradersTotReptLongOther": 102,  
		"tradersTotReptShortOther": 106,  
		"concGrossLe4TdrLongAll": 16,  
		"concGrossLe4TdrShortAll": 23.7,  
		"concGrossLe8TdrLongAll": 25.8,  
		"concGrossLe8TdrShortAll": 38.9,  
		"concNetLe4TdrLongAll": 9.8,  
		"concNetLe4TdrShortAll": 16.2,  
		"concNetLe8TdrLongAll": 17.7,  
		"concNetLe8TdrShortAll": 25.4,  
		"concGrossLe4TdrLongOl": 13.6,  
		"concGrossLe4TdrShortOl": 24.7,  
		"concGrossLe8TdrLongOl": 23.2,  
		"concGrossLe8TdrShortOl": 40.3,  
		"concNetLe4TdrLongOl": 11.3,  
		"concNetLe4TdrShortOl": 18.2,  
		"concNetLe8TdrLongOl": 20.3,  
		"concNetLe8TdrShortOl": 31.9,  
		"concGrossLe4TdrLongOther": 68.2,  
		"concGrossLe4TdrShortOther": 29.1,  
		"concGrossLe8TdrLongOther": 77.8,  
		"concGrossLe8TdrShortOther": 47.3,  
		"concNetLe4TdrLongOther": 64.7,  
		"concNetLe4TdrShortOther": 26.7,  
		"concNetLe8TdrLongOther": 73.9,  
		"concNetLe8TdrShortOther": 44.2,  
		"contractUnits": "(CONTRACTS OF 37,500 POUNDS)"  
	}  
\]

[COT Analysis By Dates API](https://site.financialmodelingprep.com/developer/docs/stable/cot-report-analysis)

Gain in-depth insights into market sentiment with the FMP COT Report Analysis API. Analyze the Commitment of Traders (COT) reports for a specific date range to evaluate market dynamics, sentiment, and potential reversals across various sectors.

**Endpoint:**

https://financialmodelingprep.com/stable/*commitment-of-traders-analysis*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol | string | AAPL |
| from | date | 2024-01-01 |
| to | date | 2024-03-01 |

Response  
\[  
	{  
		"symbol": "B6",  
		"date": "2024-02-27 00:00:00",  
		"name": "British Pound (B6)",  
		"sector": "CURRENCIES",  
		"exchange": "BRITISH POUND \- CHICAGO MERCANTILE EXCHANGE",  
		"currentLongMarketSituation": 66.85,  
		"currentShortMarketSituation": 33.15,  
		"marketSituation": "Bullish",  
		"previousLongMarketSituation": 67.97,  
		"previousShortMarketSituation": 32.03,  
		"previousMarketSituation": "Bullish",  
		"netPostion": 46358,  
		"previousNetPosition": 46312,  
		"changeInNetPosition": 0.1,  
		"marketSentiment": "Increasing Bullish",  
		"reversalTrend": false  
	}  
\]

[COT Report List API](https://site.financialmodelingprep.com/developer/docs/stable/cot-report-list)

Access a comprehensive list of available Commitment of Traders (COT) reports by commodity or futures contract using the FMP COT Report List API. This API provides an overview of different market segments, allowing users to retrieve and explore COT reports for a wide variety of commodities and financial instruments.

**Endpoint:**

https://financialmodelingprep.com/stable/*commitment-of-traders-list*

Response  
\[  
	{  
		"symbol": "NG",  
		"name": "Natural Gas (NG)"  
	}  
\]

## **Discounted Cash Flow**

[DCF Valuation API](https://site.financialmodelingprep.com/developer/docs/stable/dcf-advanced)

Estimate the intrinsic value of a company with the FMP Discounted Cash Flow Valuation API. Calculate the DCF valuation based on expected future cash flows and discount rates.

**Endpoint:**

https://financialmodelingprep.com/stable/discounted-cash-flow?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"dcf": 147.2669883190846,  
		"Stock Price": 231.795  
	}  
\]

[Levered DCF API](https://site.financialmodelingprep.com/developer/docs/stable/dcf-levered)

Analyze a company’s value with the FMP Levered Discounted Cash Flow (DCF) API, which incorporates the impact of debt. This API provides post-debt company valuation, offering investors a more accurate measure of a company's true worth by accounting for its debt obligations.

**Endpoint:**

https://financialmodelingprep.com/stable/levered-discounted-cash-flow?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2025-02-04",  
		"dcf": 147.2669883190846,  
		"Stock Price": 231.795  
	}  
\]

[Custom DCF Advanced API](https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced)

Run a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.

**Endpoint:**

https://financialmodelingprep.com/stable/custom-discounted-cash-flow?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| revenueGrowthPct | number | 0.1094119804597946 |
| ebitdaPct | number | 0.31273548388 |
| depreciationAndAmortizationPct | number | 0.0345531631720999 |
| cashAndShortTermInvestmentsPct | number | 0.2344222126801843 |
| receivablesPct | number | 0.1533770531229388 |
| inventoriesPct | number | 0.0155245674227653 |
| payablePct | number | 0.1614868903169657 |
| ebitPct | number | 0.2781823207138459 |
| capitalExpenditurePct | number | 0.0306025847141713 |
| operatingCashFlowPct | number | 0.2886333485760204 |
| sellingGeneralAndAdministrativeExpensesPct | number | 0.0662854095187211 |
| taxRate | number | 0.14919579658453103 |
| longTermGrowthRate | number | 4 |
| costOfDebt | number | 3.64 |
| costOfEquity | number | 9.51168 |
| marketRiskPremium | number | 4.72 |
| beta | number | 1.244 |
| riskFreeRate | number | 3.64 |

Response  
\[  
	{  
		"year": "2029",  
		"symbol": "AAPL",  
		"revenue": 657173266965,  
		"revenuePercentage": 10.94,  
		"ebitda": 205521399637,  
		"ebitdaPercentage": 31.27,  
		"ebit": 182813984515,  
		"ebitPercentage": 27.82,  
		"depreciation": 22707415125,  
		"depreciationPercentage": 3.46,  
		"totalCash": 154056011356,  
		"totalCashPercentage": 23.44,  
		"receivables": 100795299078,  
		"receivablesPercentage": 15.34,  
		"inventories": 10202330691,  
		"inventoriesPercentage": 1.55,  
		"payable": 106124867281,  
		"payablePercentage": 16.15,  
		"capitalExpenditure": 20111200574,  
		"capitalExpenditurePercentage": 3.06,  
		"price": 232.8,  
		"beta": 1.244,  
		"dilutedSharesOutstanding": 15408095000,  
		"costofDebt": 3.64,  
		"taxRate": 24.09,  
		"afterTaxCostOfDebt": 2.76,  
		"riskFreeRate": 3.64,  
		"marketRiskPremium": 4.72,  
		"costOfEquity": 9.51,  
		"totalDebt": 106629000000,  
		"totalEquity": 3587004516000,  
		"totalCapital": 3693633516000,  
		"debtWeighting": 2.89,  
		"equityWeighting": 97.11,  
		"wacc": 9.33,  
		"taxRateCash": 14919580,  
		"ebiat": 155538906468,  
		"ufcf": 197876962552,  
		"sumPvUfcf": 616840860880,  
		"longTermGrowthRate": 4,  
		"terminalValue": 3863553224578,  
		"presentTerminalValue": 2473772391290,  
		"enterpriseValue": 3090613252170,  
		"netDebt": 76686000000,  
		"equityValue": 3013927252170,  
		"equityValuePerShare": 195.61,  
		"freeCashFlowT1": 205792041054  
	}  
\]

[Custom DCF Levered API](https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-levered)

Run a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.

**Endpoint:**

https://financialmodelingprep.com/stable/custom-levered-discounted-cash-flow?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| revenueGrowthPct | number | 0.1094119804597946 |
| ebitdaPct | number | 0.31273548388 |
| depreciationAndAmortizationPct | number | 0.0345531631720999 |
| cashAndShortTermInvestmentsPct | number | 0.2344222126801843 |
| receivablesPct | number | 0.1533770531229388 |
| inventoriesPct | number | 0.0155245674227653 |
| payablePct | number | 0.1614868903169657 |
| ebitPct | number | 0.2781823207138459 |
| capitalExpenditurePct | number | 0.0306025847141713 |
| operatingCashFlowPct | number | 0.2886333485760204 |
| sellingGeneralAndAdministrativeExpensesPct | number | 0.0662854095187211 |
| taxRate | number | 0.14919579658453103 |
| longTermGrowthRate | number | 4 |
| costOfDebt | number | 3.64 |
| costOfEquity | number | 9.51168 |
| marketRiskPremium | number | 4.72 |
| beta | number | 1.244 |
| riskFreeRate | number | 3.64 |

Response  
\[  
	{  
		"year": "2029",  
		"symbol": "AAPL",  
		"revenue": 657173266965,  
		"revenuePercentage": 10.94,  
		"capitalExpenditure": 20111200574,  
		"capitalExpenditurePercentage": 3.06,  
		"price": 232.8,  
		"beta": 1.244,  
		"dilutedSharesOutstanding": 15408095000,  
		"costofDebt": 3.64,  
		"taxRate": 24.09,  
		"afterTaxCostOfDebt": 2.76,  
		"riskFreeRate": 3.64,  
		"marketRiskPremium": 4.72,  
		"costOfEquity": 9.51,  
		"totalDebt": 106629000000,  
		"totalEquity": 3587004516000,  
		"totalCapital": 3693633516000,  
		"debtWeighting": 2.89,  
		"equityWeighting": 97.11,  
		"wacc": 9.33,  
		"operatingCashFlow": 189682120638,  
		"pvLfcf": 134327365439,  
		"sumPvLfcf": 652368547936,  
		"longTermGrowthRate": 4,  
		"freeCashFlow": 209793321212,  
		"terminalValue": 4096220460472,  
		"presentTerminalValue": 2622745564702,  
		"enterpriseValue": 3275114112638,  
		"netDebt": 76686000000,  
		"equityValue": 3198428112638,  
		"equityValuePerShare": 207.58,  
		"freeCashFlowT1": 218185054060,  
		"operatingCashFlowPercentage": 28.86  
	}  
\]

## **Economics**

[Treasury Rates API](https://site.financialmodelingprep.com/developer/docs/stable/treasury-rates)

Access real-time and historical Treasury rates for all maturities with the FMP Treasury Rates API. Track key benchmarks for interest rates across the economy.

**Endpoint:**

https://financialmodelingprep.com/stable/*treasury-rates*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"date": "2024-02-29",  
		"month1": 5.53,  
		"month2": 5.5,  
		"month3": 5.45,  
		"month6": 5.3,  
		"year1": 5.01,  
		"year2": 4.64,  
		"year3": 4.43,  
		"year5": 4.26,  
		"year7": 4.28,  
		"year10": 4.25,  
		"year20": 4.51,  
		"year30": 4.38  
	}  
\]

[Economics Indicators API](https://site.financialmodelingprep.com/developer/docs/stable/economics-indicators)

Access real-time and historical economic data for key indicators like GDP, unemployment, and inflation with the FMP Economic Indicators API. Use this data to measure economic performance and identify growth trends.

**Endpoint:**

https://financialmodelingprep.com/stable/economic-indicators?*name*\=GDP

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| name\* | string | GDP,realGDP,nominalPotentialGDP,realGDPPerCapita,federalFunds,CPI,inflationRate,inflation,retailSales,consumerSentiment,durableGoods,unemploymentRate,totalNonfarmPayroll,initialClaims,industrialProductionTotalIndex,newPrivatelyOwnedHousingUnitsStartedTotalUnits,totalVehicleSales,retailMoneyFunds,smoothedUSRecessionProbabilities,3MonthOr90DayRatesAndYieldsCertificatesOfDeposit,commercialBankInterestRateOnCreditCardPlansAllAccounts,30YearFixedRateMortgageAverage,15YearFixedRateMortgageAverage |
| from | date | 2024-07-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"name": "GDP",  
		"date": "2024-01-01",  
		"value": 28624.069  
	}  
\]

[Economic Data Releases Calendar API](https://site.financialmodelingprep.com/developer/docs/stable/economics-calendar)

Stay informed with the FMP Economic Data Releases Calendar API. Access a comprehensive calendar of upcoming economic data releases to prepare for market impacts and make informed investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/*economic-calendar*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response  
\[  
	{  
		"date": "2024-03-01 03:35:00",  
		"country": "JP",  
		"event": "3-Month Bill Auction",  
		"currency": "JPY",  
		"previous": \-0.112,  
		"estimate": null,  
		"actual": \-0.096,  
		"change": 0.016,  
		"impact": "Low",  
		"changePercentage": 14.286  
	}  
\]

[Market Risk Premium API](https://site.financialmodelingprep.com/developer/docs/stable/market-risk-premium)

Access the market risk premium for specific dates with the FMP Market Risk Premium API. Use this key financial metric to assess the additional return expected from investing in the stock market over a risk-free investment.

**Endpoint:**

https://financialmodelingprep.com/stable/*market-risk-premium*

Response  
\[  
	{  
		"country": "Zimbabwe",  
		"continent": "Africa",  
		"countryRiskPremium": 13.17,  
		"totalEquityRiskPremium": 17.77  
	}  
\]

## **Etf And Mutual Funds**

[ETF & Fund Holdings API](https://site.financialmodelingprep.com/developer/docs/stable/holdings)

Get a detailed breakdown of the assets held within ETFs and mutual funds using the FMP ETF & Fund Holdings API. Access real-time data on the specific securities and their weights in the portfolio, providing insights into asset composition and fund strategies.

**Endpoint:**

https://financialmodelingprep.com/stable/etf/holdings?*symbol*\=SPY

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

Response  
\[  
	{  
		"symbol": "SPY",  
		"asset": "AAPL",  
		"name": "APPLE INC",  
		"isin": "US0378331005",  
		"securityCusip": "037833100",  
		"sharesNumber": 188106081,  
		"weightPercentage": 7.137,  
		"marketValue": 44744793487.47,  
		"updatedAt": "2025-01-16 05:01:09",  
		"updated": "2025-02-04 19:02:31"  
	}  
\]

[ETF & Mutual Fund Information API](https://site.financialmodelingprep.com/developer/docs/stable/information)

Access comprehensive data on ETFs and mutual funds with the FMP ETF & Mutual Fund Information API. Retrieve essential details such as ticker symbol, fund name, expense ratio, assets under management, and more.

**Endpoint:**

https://financialmodelingprep.com/stable/etf/info?*symbol*\=SPY

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

Response  
\[  
	{  
		"symbol": "SPY",  
		"name": "SPDR S\&P 500 ETF Trust",  
		"description": "The Trust seeks to achieve its investment objective by holding a portfolio of the common stocks that are included in the index (the “Portfolio”), with the weight of each stock in the Portfolio substantially corresponding to the weight of such stock in the index.",  
		"isin": "US78462F1030",  
		"assetClass": "Equity",  
		"securityCusip": "78462F103",  
		"domicile": "US",  
		"website": "https://www.ssga.com/us/en/institutional/etfs/spdr-sp-500-etf-trust-spy",  
		"etfCompany": "SPDR",  
		"expenseRatio": 0.0945,  
		"assetsUnderManagement": 633120180000,  
		"avgVolume": 46396400,  
		"inceptionDate": "1993-01-22",  
		"nav": 603.64,  
		"navCurrency": "USD",  
		"holdingsCount": 503,  
		"updatedAt": "2024-12-03T20:32:48.873Z",  
		"sectorsList": \[  
			{  
				"industry": "Basic Materials",  
				"exposure": 1.97  
			},  
			{  
				"industry": "Communication Services",  
				"exposure": 8.87  
			},  
			{  
				"industry": "Consumer Cyclical",  
				"exposure": 9.84  
			}  
		\]  
	}  
\]

[ETF & Fund Country Allocation API](https://site.financialmodelingprep.com/developer/docs/stable/country-weighting)

Gain insight into how ETFs and mutual funds distribute assets across different countries with the FMP ETF & Fund Country Allocation API. This tool provides detailed information on the percentage of assets allocated to various regions, helping you make informed investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/etf/country-weightings?*symbol*\=SPY

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

Response  
\[  
	{  
		"country": "United States",  
		"weightPercentage": "97.29%"  
	}  
\]

[ETF Asset Exposure API](https://site.financialmodelingprep.com/developer/docs/stable/etf-asset-exposure)

Discover which ETFs hold specific stocks with the FMP ETF Asset Exposure API. Access detailed information on market value, share numbers, and weight percentages for assets within ETFs.

**Endpoint:**

https://financialmodelingprep.com/stable/etf/asset-exposure?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

Response  
\[  
	{  
		"symbol": "ZECP",  
		"asset": "AAPL",  
		"sharesNumber": 5482,  
		"weightPercentage": 5.86,  
		"marketValue": 0  
	}  
\]

[ETF Sector Weighting API](https://site.financialmodelingprep.com/developer/docs/stable/sector-weighting)

The FMP ETF Sector Weighting API provides a breakdown of the percentage of an ETF's assets that are invested in each sector. For example, an investor may want to invest in an ETF that has a high exposure to the technology sector if they believe that the technology sector is poised for growth.

**Endpoint:**

https://financialmodelingprep.com/stable/etf/sector-weightings?*symbol*\=SPY

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

\[  
	{  
		"symbol": "SPY",  
		"sector": "Basic Materials",  
		"weightPercentage": 1.97  
	}  
\]

[Mutual Fund & ETF Disclosure API](https://site.financialmodelingprep.com/developer/docs/stable/latest-disclosures)

Access the latest disclosures from mutual funds and ETFs with the FMP Mutual Fund & ETF Disclosure API. This API provides updates on filings, changes in holdings, and other critical disclosure data for mutual funds and ETFs.

**Endpoint:**

https://financialmodelingprep.com/stable/funds/disclosure-holders-latest?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | SPY |

Response  
\[  
	{  
		"cik": "0000106444",  
		"holder": "VANGUARD FIXED INCOME SECURITIES FUNDS",  
		"shares": 67030000,  
		"dateReported": "2024-07-31",  
		"change": 0,  
		"weightPercent": 0.03840197  
	}  
\]

[Mutual Fund Disclosures API](https://site.financialmodelingprep.com/developer/docs/stable/mutual-fund-disclosures)

Access comprehensive disclosure data for mutual funds with the FMP Mutual Fund Disclosures API. Analyze recent filings, balance sheets, and financial reports to gain insights into mutual fund portfolios.

**Endpoint:**

https://financialmodelingprep.com/stable/funds/disclosure?*symbol*\=VWO&*year*\=2023&*quarter*\=4

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | VWO |
| year\* | string | 2023 |
| quarter\* | string | 4 |
| cik | string | 0000857489 |

Response  
\[  
	{  
		"cik": "0000857489",  
		"date": "2023-10-31",  
		"acceptedDate": "2023-12-28 09:26:13",  
		"symbol": "000089.SZ",  
		"name": "Shenzhen Airport Co Ltd",  
		"lei": "3003009W045RIKRBZI44",  
		"title": "SHENZ AIRPORT-A",  
		"cusip": "N/A",  
		"isin": "CNE000000VK1",  
		"balance": 2438784,  
		"units": "NS",  
		"cur\_cd": "CNY",  
		"valUsd": 2255873.6,  
		"pctVal": 0.0023838966190458215,  
		"payoffProfile": "Long",  
		"assetCat": "EC",  
		"issuerCat": "CORP",  
		"invCountry": "CN",  
		"isRestrictedSec": "N",  
		"fairValLevel": "2",  
		"isCashCollateral": "N",  
		"isNonCashCollateral": "N",  
		"isLoanByFund": "N"  
	}  
\]

## **Commodity**

[Commodities List API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-list)

Access an extensive list of tracked commodities across various sectors, including energy, metals, and agricultural products. The FMP Commodities List API provides essential data on tradable commodities, giving investors the ability to explore market options in real-time.

**Endpoint:**

https://financialmodelingprep.com/stable/*commodities-list*

Response  
\[  
	{  
		"symbol": "HEUSX",  
		"name": "Lean Hogs Futures",  
		"exchange": null,  
		"tradeMonth": "Dec",  
		"currency": "USX"  
	}  
\]

[Commodities Quote API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-quote)

Access real-time price quotes for all commodities traded worldwide with the FMP Global Commodities Quotes API. Track market movements and identify investment opportunities with comprehensive price data.

**Endpoint:**

https://financialmodelingprep.com/stable/quote?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |

Response

\[  
	{  
		"symbol": "GCUSD",  
		"name": "Gold Futures",  
		"price": 3375.3,  
		"changePercentage": \-0.65635,  
		"change": \-22.3,  
		"volume": 170936,  
		"dayLow": 3355.2,  
		"dayHigh": 3401.1,  
		"yearHigh": 3509.9,  
		"yearLow": 2354.6,  
		"marketCap": null,  
		"priceAvg50": 3358.706,  
		"priceAvg200": 3054.501,  
		"exchange": "COMMODITY",  
		"open": 3398.6,  
		"previousClose": 3397.6,  
		"timestamp": 1753372205  
	}  
\]

[Commodities Quote Short API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-quote-short)

Get fast and accurate quotes for commodities with the FMP Commodities Quick Quote API. Instantly access the current price, recent changes, and trading volume for various commodities in real-time.

**Endpoint:**

https://financialmodelingprep.com/stable/quote-short?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |

Response  
\[  
	{  
		"symbol": "GCUSD",  
		"price": 3375.3,  
		"change": \-22.3,  
		"volume": 170936  
	}  
\]

[Light Chart API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-historical-price-eod-light)

Access historical end-of-day prices for various commodities with the FMP Historical Commodities Price API. Analyze past price movements, trading volume, and trends to support informed decision-making.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/light?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"symbol": "GCUSD",  
		"date": "2025-07-24",  
		"price": 3373.8,  
		"volume": 174758  
	}  
\]

[Full Chart API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-historical-price-eod-full)

Access full historical end-of-day price data for commodities with the FMP Comprehensive Commodities Price API. This API enables users to analyze long-term price trends, patterns, and market movements in great detail.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/full?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"symbol": "GCUSD",  
		"date": "2025-07-24",  
		"open": 3398.6,  
		"high": 3401.1,  
		"low": 3355.2,  
		"close": 3373.8,  
		"volume": 174758,  
		"change": \-24.8,  
		"changePercent": \-0.72971223,  
		"vwap": 3376.7  
	}  
\]

[1-Minute Interval Commodities Chart API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-intraday-1-min)

Track real-time, short-term price movements for commodities with the FMP 1-Minute Interval Commodities Chart API. This API provides detailed 1-minute interval data, enabling precise monitoring of intraday market changes.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1min?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:18:00",  
		"open": 3374.5,  
		"low": 3373.7,  
		"high": 3374.5,  
		"close": 3374,  
		"volume": 123  
	}  
\]

[5-Minute Interval Commodities Chart API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-intraday-5-min)

Monitor short-term price movements with the FMP 5-Minute Interval Commodities Chart API. This API provides detailed 5-minute interval data, enabling users to track near-term price trends for more strategic trading and investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/5min?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:15:00",  
		"open": 3374,  
		"low": 3374,  
		"high": 3374.8,  
		"close": 3374.4,  
		"volume": 193  
	}  
\]

[1-Hour Interval Commodities Chart API](https://site.financialmodelingprep.com/developer/docs/stable/commodities-intraday-1-hour)

Monitor hourly price movements and trends with the FMP 1-Hour Interval Commodities Chart API. This API provides hourly data, offering a detailed look at price fluctuations throughout the trading day to support mid-term trading strategies and market analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1hour?*symbol*\=GCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | GCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"date": "2025-07-24 11:30:00",  
		"open": 3378.4,  
		"low": 3373.1,  
		"high": 3378.8,  
		"close": 3374.4,  
		"volume": 7108  
	}  
\]

## **Crypto**

[Cryptocurrency List API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-list)

Access a comprehensive list of all cryptocurrencies traded on exchanges worldwide with the FMP Cryptocurrencies Overview API. Get detailed information on each cryptocurrency to inform your investment strategies.

**Endpoint:**

https://financialmodelingprep.com/stable/*cryptocurrency-list*

#### 

Response  
\[  
	{  
		"symbol": "ALIENUSD",  
		"name": "Alien Inu USD",  
		"exchange": "CCC",  
		"icoDate": "2021-11-22",  
		"circulatingSupply": 0,  
		"totalSupply": null  
	}  
\]

[Full Cryptocurrency Quote API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-quote)

Access real-time quotes for all cryptocurrencies with the FMP Full Cryptocurrency Quote API. Obtain comprehensive price data including current, high, low, and open prices.

**Endpoint:**

https://financialmodelingprep.com/stable/quote?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |

Response  
\[  
	{  
		"symbol": "BTCUSD",  
		"name": "Bitcoin USD",  
		"price": 118741.16,  
		"changePercentage": \-0.03193323,  
		"change": \-37.93,  
		"volume": 75302985728,  
		"dayLow": 117435.22,  
		"dayHigh": 119535.45,  
		"yearHigh": 123091.61,  
		"yearLow": 49121.24,  
		"marketCap": 2344693699320,  
		"priceAvg50": 109824.32,  
		"priceAvg200": 98161.086,  
		"exchange": "CRYPTO",  
		"open": 118779.09,  
		"previousClose": 118779.09,  
		"timestamp": 1753374602  
	}  
\]

[Cryptocurrency Quote Short API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-quote-short)

Access real-time cryptocurrency quotes with the FMP Cryptocurrency Quick Quote API. Get a concise overview of current crypto prices, changes, and trading volume for a wide range of digital assets.

**Endpoint:**

https://financialmodelingprep.com/stable/quote-short?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |

Response  
\[  
	{  
		"symbol": "BTCUSD",  
		"price": 118741.16,  
		"change": \-37.93,  
		"volume": 75302985728  
	}  
\]

[All Cryptocurrencies Quotes API](https://site.financialmodelingprep.com/developer/docs/stable/all-cryptocurrency-quotes)

Access live price data for a wide range of cryptocurrencies with the FMP Real-Time Cryptocurrency Batch Quotes API. Get real-time updates on prices, market changes, and trading volumes for digital assets in a single request.

**Endpoint:**

https://financialmodelingprep.com/stable/*batch-crypto-quotes*

Parameter

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| short | boolean | true |

Response  
\[  
	{  
		"symbol": "00USD",  
		"price": 0.01755108,  
		"change": 0.00035108,  
		"volume": 3719492.41  
	}  
\]

[Historical Cryptocurrency Light Chart API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-historical-price-eod-light)

Access historical end-of-day prices for a variety of cryptocurrencies with the Historical Cryptocurrency Price Snapshot API. Track trends in price and trading volume over time to better understand market behavior.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/light?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"symbol": "BTCUSD",  
		"date": "2025-07-24",  
		"price": 118741.16,  
		"volume": 75302985728  
	}  
\]

[Historical Cryptocurrency Full Chart API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-historical-price-eod-full)

Access comprehensive end-of-day (EOD) price data for cryptocurrencies with the Full Historical Cryptocurrency Data API. Analyze long-term price trends, market movements, and trading volumes to inform strategic decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/full?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"symbol": "BTCUSD",  
		"date": "2025-07-24",  
		"open": 118779.09,  
		"high": 119535.45,  
		"low": 117435.22,  
		"close": 118741.16,  
		"volume": 75302985728,  
		"change": \-37.93,  
		"changePercent": \-0.03193323,  
		"vwap": 118570.61  
	}  
\]

[1-Minute Interval Cryptocurrency Data API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-intraday-1-min)

Get real-time, 1-minute interval price data for cryptocurrencies with the 1-Minute Cryptocurrency Intraday Data API. Monitor short-term price fluctuations and trading volume to stay updated on market movements.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1min?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:29:00",  
		"open": 118797.96,  
		"low": 118760.42,  
		"high": 118818.11,  
		"close": 118784.04,  
		"volume": 52293740.08888889  
	}  
\]

[5-Minute Interval Cryptocurrency Data API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-intraday-5-min)

Analyze short-term price trends with the 5-Minute Interval Cryptocurrency Data API. Access real-time, intraday price data for cryptocurrencies to monitor rapid market movements and optimize trading strategies.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/5min?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"date": "2025-07-24 12:25:00",  
		"open": 118988.32,  
		"low": 118797.03,  
		"high": 118997.22,  
		"close": 118797.03,  
		"volume": 208601161.95555556  
	}  
\]

[1-Hour Interval Cryptocurrency Data API](https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-intraday-1-hour)

Access detailed 1-hour intraday price data for cryptocurrencies with the 1-Hour Interval Cryptocurrency Data API. Track hourly price movements to gain insights into market trends and make informed trading decisions throughout the day.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1hour?*symbol*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | BTCUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:00:00",  
		"open": 119189.36,  
		"low": 118768.68,  
		"high": 119272.88,  
		"close": 118797.03,  
		"volume": 1493617925.6888888  
	}  
\]

## **Forex**

[Forex Currency Pairs API](https://site.financialmodelingprep.com/developer/docs/stable/forex-list)

Access a comprehensive list of all currency pairs traded on the forex market with the FMP Forex Currency Pairs API. Analyze and track the performance of currency pairs to make informed investment decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/*forex-list*

Response

\[  
	{  
		"symbol": "ARSMXN",  
		"fromCurrency": "ARS",  
		"toCurrency": "MXN",  
		"fromName": "Argentine Peso",  
		"toName": "Mexican Peso"  
	}  
\]

[Forex Quote API](https://site.financialmodelingprep.com/developer/docs/stable/forex-quote)

Access real-time forex quotes for currency pairs with the Forex Quote API. Retrieve up-to-date information on exchange rates and price changes to help monitor market movements.

**Endpoint:**

https://financialmodelingprep.com/stable/quote?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |

Response  
\[  
	{  
		"symbol": "EURUSD",  
		"name": "EUR/USD",  
		"price": 1.17598,  
		"changePercentage": \-0.14754,  
		"change": \-0.0017376,  
		"volume": 184065,  
		"dayLow": 1.17371,  
		"dayHigh": 1.17911,  
		"yearHigh": 1.18303,  
		"yearLow": 1.01838,  
		"marketCap": null,  
		"priceAvg50": 1.15244,  
		"priceAvg200": 1.08866,  
		"exchange": "FOREX",  
		"open": 1.17744,  
		"previousClose": 1.17772,  
		"timestamp": 1753374603  
	}  
\]

[Forex Short Quote API](https://site.financialmodelingprep.com/developer/docs/stable/forex-quote-short)

Quickly access concise forex pair quotes with the Forex Quote Snapshot API. Get a fast look at live currency exchange rates, price changes, and volume in real time.

**Endpoint:**

https://financialmodelingprep.com/stable/quote-short?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |

Response  
\[  
	{  
		"symbol": "EURUSD",  
		"price": 1.17598,  
		"change": \-0.0017376,  
		"volume": 184065  
	}  
\]

[Batch Forex Quotes API](https://site.financialmodelingprep.com/developer/docs/stable/all-forex-quotes)

Easily access real-time quotes for multiple forex pairs simultaneously with the Batch Forex Quotes API. Stay updated on global currency exchange rates and monitor price changes across different markets.

**Endpoint:**

https://financialmodelingprep.com/stable/*batch-forex-quotes*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| short | boolean | true |

Response  
\[  
	{  
		"symbol": "AEDAUD",  
		"price": 0.41372,  
		"change": 0.00153892,  
		"volume": 0  
	}  
\]

[Historical Forex Light Chart API](https://site.financialmodelingprep.com/developer/docs/stable/forex-historical-price-eod-light)

Access historical end-of-day forex prices with the Historical Forex Light Chart API. Track long-term price trends across different currency pairs to enhance your trading and analysis strategies.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/light?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"symbol": "EURUSD",  
		"date": "2025-07-24",  
		"price": 1.17639,  
		"volume": 182290  
	}  
\]

[Historical Forex Full Chart API](https://site.financialmodelingprep.com/developer/docs/stable/forex-historical-price-eod-full)

Access comprehensive historical end-of-day forex price data with the Full Historical Forex Chart API. Gain detailed insights into currency pair movements, including open, high, low, close (OHLC) prices, volume, and percentage changes.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/full?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"symbol": "EURUSD",  
		"date": "2025-07-24",  
		"open": 1.17744,  
		"high": 1.17911,  
		"low": 1.17371,  
		"close": 1.17639,  
		"volume": 182290,  
		"change": \-0.00105,  
		"changePercent": \-0.08917652,  
		"vwap": 1.18  
	}  
\]

[1-Minute Interval Forex Chart API](https://site.financialmodelingprep.com/developer/docs/stable/forex-intraday-1-min)

Access real-time 1-minute intraday forex data with the 1-Minute Forex Interval Chart API. Track short-term price movements for precise, up-to-the-minute insights on currency pair fluctuations.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1min?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:29:00",  
		"open": 1.17582,  
		"low": 1.17582,  
		"high": 1.17599,  
		"close": 1.17598,  
		"volume": 184  
	}  
\]

[5-Minute Interval Forex Chart API](https://site.financialmodelingprep.com/developer/docs/stable/forex-intraday-5-min)

Track short-term forex trends with the 5-Minute Forex Interval Chart API. Access detailed 5-minute intraday data to monitor currency pair price movements and market conditions in near real-time.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/5min?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:25:00",  
		"open": 1.17612,  
		"low": 1.17571,  
		"high": 1.17613,  
		"close": 1.17578,  
		"volume": 873  
	}  
\]

[1-Hour Interval Forex Chart API](https://site.financialmodelingprep.com/developer/docs/stable/forex-intraday-1-hour)

Track forex price movements over the trading day with the 1-Hour Forex Interval Chart API. This tool provides hourly intraday data for currency pairs, giving a detailed view of trends and market shifts.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1hour?*symbol*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | EURUSD |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response  
\[  
	{  
		"date": "2025-07-24 12:00:00",  
		"open": 1.17639,  
		"low": 1.17571,  
		"high": 1.1773,  
		"close": 1.17578,  
		"volume": 4909  
	}  
\]

## **Statements**

[Income Statement API](https://site.financialmodelingprep.com/developer/docs/stable/income-statement)

Access real-time income statement data for public companies, private companies, and ETFs with the FMP Real-Time Income Statements API. Track profitability, compare competitors, and identify business trends with up-to-date financial data.

**Endpoint:**

https://financialmodelingprep.com/stable/income-statement?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"date": "2024-09-28",  
		"symbol": "AAPL",  
		"reportedCurrency": "USD",  
		"cik": "0000320193",  
		"filingDate": "2024-11-01",  
		"acceptedDate": "2024-11-01 06:01:36",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"revenue": 391035000000,  
		"costOfRevenue": 210352000000,  
		"grossProfit": 180683000000,  
		"researchAndDevelopmentExpenses": 31370000000,  
		"generalAndAdministrativeExpenses": 0,  
		"sellingAndMarketingExpenses": 0,  
		"sellingGeneralAndAdministrativeExpenses": 26097000000,  
		"otherExpenses": 0,  
		"operatingExpenses": 57467000000,  
		"costAndExpenses": 267819000000,  
		"netInterestIncome": 0,  
		"interestIncome": 0,  
		"interestExpense": 0,  
		"depreciationAndAmortization": 11445000000,  
		"ebitda": 134661000000,  
		"ebit": 123216000000,  
		"nonOperatingIncomeExcludingInterest": 0,  
		"operatingIncome": 123216000000,  
		"totalOtherIncomeExpensesNet": 269000000,  
		"incomeBeforeTax": 123485000000,  
		"incomeTaxExpense": 29749000000,  
		"netIncomeFromContinuingOperations": 93736000000,  
		"netIncomeFromDiscontinuedOperations": 0,  
		"otherAdjustmentsToNetIncome": 0,  
		"netIncome": 93736000000,  
		"netIncomeDeductions": 0,  
		"bottomLineNetIncome": 93736000000,  
		"eps": 6.11,  
		"epsDiluted": 6.08,  
		"weightedAverageShsOut": 15343783000,  
		"weightedAverageShsOutDil": 15408095000  
	}  
\]

[Balance Sheet Statement API](https://site.financialmodelingprep.com/developer/docs/stable/balance-sheet-statement)

Access detailed balance sheet statements for publicly traded companies with the Balance Sheet Data API. Analyze assets, liabilities, and shareholder equity to gain insights into a company's financial health.

**Endpoint:**

https://financialmodelingprep.com/stable/balance-sheet-statement?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response:  
\[  
	{  
		"date": "2024-09-28",  
		"symbol": "AAPL",  
		"reportedCurrency": "USD",  
		"cik": "0000320193",  
		"filingDate": "2024-11-01",  
		"acceptedDate": "2024-11-01 06:01:36",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"cashAndCashEquivalents": 29943000000,  
		"shortTermInvestments": 35228000000,  
		"cashAndShortTermInvestments": 65171000000,  
		"netReceivables": 66243000000,  
		"accountsReceivables": 33410000000,  
		"otherReceivables": 32833000000,  
		"inventory": 7286000000,  
		"prepaids": 0,  
		"otherCurrentAssets": 14287000000,  
		"totalCurrentAssets": 152987000000,  
		"propertyPlantEquipmentNet": 45680000000,  
		"goodwill": 0,  
		"intangibleAssets": 0,  
		"goodwillAndIntangibleAssets": 0,  
		"longTermInvestments": 91479000000,  
		"taxAssets": 19499000000,  
		"otherNonCurrentAssets": 55335000000,  
		"totalNonCurrentAssets": 211993000000,  
		"otherAssets": 0,  
		"totalAssets": 364980000000,  
		"totalPayables": 95561000000,  
		"accountPayables": 68960000000,  
		"otherPayables": 26601000000,  
		"accruedExpenses": 0,  
		"shortTermDebt": 20879000000,  
		"capitalLeaseObligationsCurrent": 1632000000,  
		"taxPayables": 26601000000,  
		"deferredRevenue": 8249000000,  
		"otherCurrentLiabilities": 50071000000,  
		"totalCurrentLiabilities": 176392000000,  
		"longTermDebt": 85750000000,  
		"deferredRevenueNonCurrent": 10798000000,  
		"deferredTaxLiabilitiesNonCurrent": 0,  
		"otherNonCurrentLiabilities": 35090000000,  
		"totalNonCurrentLiabilities": 131638000000,  
		"otherLiabilities": 0,  
		"capitalLeaseObligations": 12430000000,  
		"totalLiabilities": 308030000000,  
		"treasuryStock": 0,  
		"preferredStock": 0,  
		"commonStock": 83276000000,  
		"retainedEarnings": \-19154000000,  
		"additionalPaidInCapital": 0,  
		"accumulatedOtherComprehensiveIncomeLoss": \-7172000000,  
		"otherTotalStockholdersEquity": 0,  
		"totalStockholdersEquity": 56950000000,  
		"totalEquity": 56950000000,  
		"minorityInterest": 0,  
		"totalLiabilitiesAndTotalEquity": 364980000000,  
		"totalInvestments": 126707000000,  
		"totalDebt": 106629000000,  
		"netDebt": 76686000000  
	}  
\]

[Cash Flow Statement API](https://site.financialmodelingprep.com/developer/docs/stable/cashflow-statement)

Gain insights into a company's cash flow activities with the Cash Flow Statements API. Analyze cash generated and used from operations, investments, and financing activities to evaluate the financial health and sustainability of a business.

**Endpoint:**

https://financialmodelingprep.com/stable/cash-flow-statement?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"date": "2024-09-28",  
		"symbol": "AAPL",  
		"reportedCurrency": "USD",  
		"cik": "0000320193",  
		"filingDate": "2024-11-01",  
		"acceptedDate": "2024-11-01 06:01:36",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"netIncome": 93736000000,  
		"depreciationAndAmortization": 11445000000,  
		"deferredIncomeTax": 0,  
		"stockBasedCompensation": 11688000000,  
		"changeInWorkingCapital": 3651000000,  
		"accountsReceivables": \-5144000000,  
		"inventory": \-1046000000,  
		"accountsPayables": 6020000000,  
		"otherWorkingCapital": 3821000000,  
		"otherNonCashItems": \-2266000000,  
		"netCashProvidedByOperatingActivities": 118254000000,  
		"investmentsInPropertyPlantAndEquipment": \-9447000000,  
		"acquisitionsNet": 0,  
		"purchasesOfInvestments": \-48656000000,  
		"salesMaturitiesOfInvestments": 62346000000,  
		"otherInvestingActivities": \-1308000000,  
		"netCashProvidedByInvestingActivities": 2935000000,  
		"netDebtIssuance": \-5998000000,  
		"longTermNetDebtIssuance": \-9958000000,  
		"shortTermNetDebtIssuance": 3960000000,  
		"netStockIssuance": \-94949000000,  
		"netCommonStockIssuance": \-94949000000,  
		"commonStockIssuance": 0,  
		"commonStockRepurchased": \-94949000000,  
		"netPreferredStockIssuance": 0,  
		"netDividendsPaid": \-15234000000,  
		"commonDividendsPaid": \-15234000000,  
		"preferredDividendsPaid": 0,  
		"otherFinancingActivities": \-5802000000,  
		"netCashProvidedByFinancingActivities": \-121983000000,  
		"effectOfForexChangesOnCash": 0,  
		"netChangeInCash": \-794000000,  
		"cashAtEndOfPeriod": 29943000000,  
		"cashAtBeginningOfPeriod": 30737000000,  
		"operatingCashFlow": 118254000000,  
		"capitalExpenditure": \-9447000000,  
		"freeCashFlow": 108807000000,  
		"incomeTaxesPaid": 26102000000,  
		"interestPaid": 0  
	}  
\]

[Key Metrics API](https://site.financialmodelingprep.com/developer/docs/stable/key-metrics)

Access essential financial metrics for a company with the FMP Financial Key Metrics API. Evaluate revenue, net income, P/E ratio, and more to assess performance and compare it to competitors.

**Endpoint:**

https://financialmodelingprep.com/stable/key-metrics?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"marketCap": 3495160329570,  
		"enterpriseValue": 3571846329570,  
		"evToSales": 9.134339201273542,  
		"evToOperatingCashFlow": 30.204866893043786,  
		"evToFreeCashFlow": 32.82735788662494,  
		"evToEBITDA": 26.524727497716487,  
		"netDebtToEBITDA": 0.5694744580836323,  
		"currentRatio": 0.8673125765340832,  
		"incomeQuality": 1.2615643936161134,  
		"grahamNumber": 22.587017267616833,  
		"grahamNetNet": \-12.352478525015636,  
		"taxBurden": 0.7590881483581001,  
		"interestBurden": 1.0021831580314244,  
		"workingCapital": \-23405000000,  
		"investedCapital": 22275000000,  
		"returnOnAssets": 0.25682503150857583,  
		"operatingReturnOnAssets": 0.3434290787011036,  
		"returnOnTangibleAssets": 0.25682503150857583,  
		"returnOnEquity": 1.6459350307287095,  
		"returnOnInvestedCapital": 0.4430708117427921,  
		"returnOnCapitalEmployed": 0.6533607652660827,  
		"earningsYield": 0.026818798327209237,  
		"freeCashFlowYield": 0.03113076074921754,  
		"capexToOperatingCashFlow": 0.07988736110406414,  
		"capexToDepreciation": 0.8254259501965924,  
		"capexToRevenue": 0.02415896275269477,  
		"salesGeneralAndAdministrativeToRevenue": 0,  
		"researchAndDevelopementToRevenue": 0.08022299794136074,  
		"stockBasedCompensationToRevenue": 0.02988990755303234,  
		"intangiblesToTotalAssets": 0,  
		"averageReceivables": 63614000000,  
		"averagePayables": 65785500000,  
		"averageInventory": 6808500000,  
		"daysOfSalesOutstanding": 61.83255974529134,  
		"daysOfPayablesOutstanding": 119.65847721913745,  
		"daysOfInventoryOutstanding": 12.642570548414087,  
		"operatingCycle": 74.47513029370543,  
		"cashConversionCycle": \-45.18334692543202,  
		"freeCashFlowToEquity": 32121000000,  
		"freeCashFlowToFirm": 117192805288.09166,  
		"tangibleAssetValue": 56950000000,  
		"netCurrentAssetValue": \-155043000000  
	}  
\]

[Financial Ratios API](https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios)

Analyze a company's financial performance using the Financial Ratios API. This API provides detailed profitability, liquidity, and efficiency ratios, enabling users to assess a company's operational and financial health across various metrics.

**Endpoint:**

https://financialmodelingprep.com/stable/ratios?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response

\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"grossProfitMargin": 0.4620634981523393,  
		"ebitMargin": 0.31510222870075566,  
		"ebitdaMargin": 0.3443707085043538,  
		"operatingProfitMargin": 0.31510222870075566,  
		"pretaxProfitMargin": 0.3157901466620635,  
		"continuousOperationsProfitMargin": 0.23971255769943867,  
		"netProfitMargin": 0.23971255769943867,  
		"bottomLineProfitMargin": 0.23971255769943867,  
		"receivablesTurnover": 5.903038811648023,  
		"payablesTurnover": 3.0503480278422272,  
		"inventoryTurnover": 28.870710952511665,  
		"fixedAssetTurnover": 8.560310858143607,  
		"assetTurnover": 1.0713874732862074,  
		"currentRatio": 0.8673125765340832,  
		"quickRatio": 0.8260068483831466,  
		"solvencyRatio": 0.3414634938155374,  
		"cashRatio": 0.16975259648963673,  
		"priceToEarningsRatio": 37.287278415656736,  
		"priceToEarningsGrowthRatio": \-45.93792700808932,  
		"forwardPriceToEarningsGrowthRatio": \-45.93792700808932,  
		"priceToBookRatio": 61.37243774486391,  
		"priceToSalesRatio": 8.93822887866815,  
		"priceToFreeCashFlowRatio": 32.12256867269569,  
		"priceToOperatingCashFlowRatio": 29.55638142954995,  
		"debtToAssetsRatio": 0.29215025480848267,  
		"debtToEquityRatio": 1.872326602282704,  
		"debtToCapitalRatio": 0.6518501763673821,  
		"longTermDebtToCapitalRatio": 0.6009110021023125,  
		"financialLeverageRatio": 6.408779631255487,  
		"workingCapitalTurnoverRatio": \-31.099932397502684,  
		"operatingCashFlowRatio": 0.6704045534944896,  
		"operatingCashFlowSalesRatio": 0.3024128274962599,  
		"freeCashFlowOperatingCashFlowRatio": 0.9201126388959359,  
		"debtServiceCoverageRatio": 5.024761722304708,  
		"interestCoverageRatio": 0,  
		"shortTermOperatingCashFlowCoverageRatio": 5.663777000814215,  
		"operatingCashFlowCoverageRatio": 1.109022873702276,  
		"capitalExpenditureCoverageRatio": 12.517624642743728,  
		"dividendPaidAndCapexCoverageRatio": 4.7912969490701345,  
		"dividendPayoutRatio": 0.16252026969360758,  
		"dividendYield": 0.0043585983369965175,  
		"dividendYieldPercentage": 0.43585983369965176,  
		"revenuePerShare": 25.484914639368924,  
		"netIncomePerShare": 6.109054070954992,  
		"interestDebtPerShare": 6.949329249507765,  
		"cashPerShare": 4.247388013764271,  
		"bookValuePerShare": 3.711600978715614,  
		"tangibleBookValuePerShare": 3.711600978715614,  
		"shareholdersEquityPerShare": 3.711600978715614,  
		"operatingCashFlowPerShare": 7.706965094592383,  
		"capexPerShare": 0.6156891035281195,  
		"freeCashFlowPerShare": 7.091275991064264,  
		"netIncomePerEBT": 0.7590881483581001,  
		"ebtPerEbit": 1.0021831580314244,  
		"priceToFairValue": 61.37243774486391,  
		"debtToMarketCap": 0.03050761336980449,  
		"effectiveTaxRate": 0.24091185164189982,  
		"enterpriseValueMultiple": 26.524727497716487  
	}  
\]

[Financial Scores API](https://site.financialmodelingprep.com/developer/docs/stable/financial-scores)

Assess a company's financial strength using the Financial Health Scores API. This API provides key metrics such as the Altman Z-Score and Piotroski Score, giving users insights into a company’s overall financial health and stability.

**Endpoint:**

https://financialmodelingprep.com/stable/financial-scores?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"reportedCurrency": "USD",  
		"altmanZScore": 9.322985825443649,  
		"piotroskiScore": 8,  
		"workingCapital": \-11125000000,  
		"totalAssets": 344085000000,  
		"retainedEarnings": \-11221000000,  
		"ebit": 125675000000,  
		"marketCap": 3259495258000,  
		"totalLiabilities": 277327000000,  
		"revenue": 395760000000  
	}  
\]

[Owner Earnings API](https://site.financialmodelingprep.com/developer/docs/stable/owner-earnings)

Retrieve a company's owner earnings with the Owner Earnings API, which provides a more accurate representation of cash available to shareholders by adjusting net income. This metric is crucial for evaluating a company’s profitability from the perspective of investors.

**Endpoint:**

https://financialmodelingprep.com/stable/owner-earnings?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"reportedCurrency": "USD",  
		"fiscalYear": "2025",  
		"period": "Q1",  
		"date": "2024-12-28",  
		"averagePPE": 0.13969,  
		"maintenanceCapex": \-2279964750,  
		"ownersEarnings": 27655035250,  
		"growthCapex": \-660035250,  
		"ownersEarningsPerShare": 1.83  
	}  
\]

[Enterprise Values API](https://site.financialmodelingprep.com/developer/docs/stable/enterprise-values)

Access a company's enterprise value using the Enterprise Values API. This metric offers a comprehensive view of a company's total market value by combining both its equity (market capitalization) and debt, providing a better understanding of its worth.

**Endpoint:**

https://financialmodelingprep.com/stable/enterprise-values?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"stockPrice": 227.79,  
		"numberOfShares": 15343783000,  
		"marketCapitalization": 3495160329570,  
		"minusCashAndCashEquivalents": 29943000000,  
		"addTotalDebt": 106629000000,  
		"enterpriseValue": 3571846329570  
	}  
\]

[Income Statement Growth API](https://site.financialmodelingprep.com/developer/docs/stable/income-statement-growth)

Track key financial growth metrics with the Income Statement Growth API. Analyze how revenue, profits, and expenses have evolved over time, offering insights into a company’s financial health and operational efficiency.

**Endpoint:**

https://financialmodelingprep.com/stable/income-statement-growth?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"growthRevenue": 0.020219940775141214,  
		"growthCostOfRevenue": \-0.017675600199872046,  
		"growthGrossProfit": 0.06819471705252206,  
		"growthGrossProfitRatio": 0.04776303446712012,  
		"growthResearchAndDevelopmentExpenses": 0.04863780712017383,  
		"growthGeneralAndAdministrativeExpenses": 0,  
		"growthSellingAndMarketingExpenses": 0,  
		"growthOtherExpenses": \-1,  
		"growthOperatingExpenses": 0.04776924900176856,  
		"growthCostAndExpenses": \-0.004331112631234571,  
		"growthInterestIncome": \-1,  
		"growthInterestExpense": \-1,  
		"growthDepreciationAndAmortization": \-0.006424168764649709,  
		"growthEBITDA": 0.07026704816404387,  
		"growthOperatingIncome": 0.07799581805933456,  
		"growthIncomeBeforeTax": 0.08571604417246959,  
		"growthIncomeTaxExpense": 0.7770145152619318,  
		"growthNetIncome": \-0.033599670086086914,  
		"growthEPS": \-0.008116883116883088,  
		"growthEPSDiluted": \-0.008156606851549727,  
		"growthWeightedAverageShsOut": \-0.02543458616683152,  
		"growthWeightedAverageShsOutDil": \-0.02557791606880283,  
		"growthEBIT": 0.0471407082579099,  
		"growthNonOperatingIncomeExcludingInterest": 1,  
		"growthNetInterestIncome": 1,  
		"growthTotalOtherIncomeExpensesNet": 1.4761061946902654,  
		"growthNetIncomeFromContinuingOperations": \-0.033599670086086914,  
		"growthOtherAdjustmentsToNetIncome": 0,  
		"growthNetIncomeDeductions": 0  
	}  
\]

[Balance Sheet Statement Growth API](https://site.financialmodelingprep.com/developer/docs/stable/balance-sheet-statement-growth)

Analyze the growth of key balance sheet items over time with the Balance Sheet Statement Growth API. Track changes in assets, liabilities, and equity to understand the financial evolution of a company.

**Endpoint:**

https://financialmodelingprep.com/stable/balance-sheet-statement-growth?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"growthCashAndCashEquivalents": \-0.0007341898882029034,  
		"growthShortTermInvestments": 0.11516302627413738,  
		"growthCashAndShortTermInvestments": 0.058744212492892536,  
		"growthNetReceivables": 0.08621792243994425,  
		"growthInventory": 0.15084504817564365,  
		"growthOtherCurrentAssets": \-0.02776454576386526,  
		"growthTotalCurrentAssets": 0.06562138667929733,  
		"growthPropertyPlantEquipmentNet": \-0.15992349565984992,  
		"growthGoodwill": 0,  
		"growthIntangibleAssets": 0,  
		"growthGoodwillAndIntangibleAssets": 0,  
		"growthLongTermInvestments": \-0.09015953214513049,  
		"growthTaxAssets": 0.09225857046829487,  
		"growthOtherNonCurrentAssets": 0.5266933370120016,  
		"growthTotalNonCurrentAssets": 0.014238076328719674,  
		"growthOtherAssets": 0,  
		"growthTotalAssets": 0.035160515396374756,  
		"growthAccountPayables": 0.1014039066617687,  
		"growthShortTermDebt": 0.32087050041121024,  
		"growthTaxPayables": 2.01632838190271,  
		"growthDeferredRevenue": 0.023322168465450935,  
		"growthOtherCurrentLiabilities": \-0.1254584832500786,  
		"growthTotalCurrentLiabilities": 0.21391802240757563,  
		"growthLongTermDebt": \-0.10003043628845205,  
		"growthDeferredRevenueNonCurrent": 0,  
		"growthDeferredTaxLiabilitiesNonCurrent": 0,  
		"growthOtherNonCurrentLiabilities": \-0.09048495373370312,  
		"growthTotalNonCurrentLiabilities": \-0.09295867814151548,  
		"growthOtherLiabilities": 0,  
		"growthTotalLiabilities": 0.060574238130816666,  
		"growthPreferredStock": 0,  
		"growthCommonStock": 0.12821763398905328,  
		"growthRetainedEarnings": \-88.50467289719626,  
		"growthAccumulatedOtherComprehensiveIncomeLoss": 0.3737338456164862,  
		"growthOthertotalStockholdersEquity": 0,  
		"growthTotalStockholdersEquity": \-0.0836095645737457,  
		"growthMinorityInterest": 0,  
		"growthTotalEquity": \-0.0836095645737457,  
		"growthTotalLiabilitiesAndStockholdersEquity": 0.035160515396374756,  
		"growthTotalInvestments": \-0.04107194211936368,  
		"growthTotalDebt": \-0.0401393489845888,  
		"growthNetDebt": \-0.05469472282829777,  
		"growthAccountsReceivables": 0.13223532601328453,  
		"growthOtherReceivables": 0.04307907360930203,  
		"growthPrepaids": 0,  
		"growthTotalPayables": 0.5262653527335452,  
		"growthOtherPayables": 0,  
		"growthAccruedExpenses": 0,  
		"growthCapitalLeaseObligationsCurrent": 0.03619047619047619,  
		"growthAdditionalPaidInCapital": 0,  
		"growthTreasuryStock": 0  
	}  
\]

[Cashflow Statement Growth API](https://site.financialmodelingprep.com/developer/docs/stable/cashflow-statement-growth)

Measure the growth rate of a company’s cash flow with the FMP Cashflow Statement Growth API. Determine how quickly a company’s cash flow is increasing or decreasing over time.

**Endpoint:**

https://financialmodelingprep.com/stable/cash-flow-statement-growth?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"growthNetIncome": \-0.033599670086086914,  
		"growthDepreciationAndAmortization": \-0.006424168764649709,  
		"growthDeferredIncomeTax": 0,  
		"growthStockBasedCompensation": 0.07892550540016616,  
		"growthChangeInWorkingCapital": 1.555116314429071,  
		"growthAccountsReceivables": \-2.0473933649289098,  
		"growthInventory": 0.3535228677379481,  
		"growthAccountsPayables": 4.1868713605082055,  
		"growthOtherWorkingCapital": 2.4402563136072373,  
		"growthOtherNonCashItems": \-0.017512348450830714,  
		"growthNetCashProvidedByOperatingActivites": 0.06975566069312394,  
		"growthInvestmentsInPropertyPlantAndEquipment": 0.13796879277306323,  
		"growthAcquisitionsNet": 0,  
		"growthPurchasesOfInvestments": \-0.6486294175448107,  
		"growthSalesMaturitiesOfInvestments": 0.3698202750801951,  
		"growthOtherInvestingActivites": 0.02169035153328347,  
		"growthNetCashUsedForInvestingActivites": \-0.2078272604588394,  
		"growthDebtRepayment": \-0.012662502110417018,  
		"growthCommonStockIssued": 0,  
		"growthCommonStockRepurchased": \-0.2243584784010316,  
		"growthDividendsPaid": \-0.013910149750415973,  
		"growthOtherFinancingActivites": 0.03493013972055888,  
		"growthNetCashUsedProvidedByFinancingActivities": \-0.12439163778482412,  
		"growthEffectOfForexChangesOnCash": 0,  
		"growthNetChangeInCash": \-1.1378472222222222,  
		"growthCashAtEndOfPeriod": \-0.02583205908188828,  
		"growthCashAtBeginningOfPeriod": 0.23061216319013492,  
		"growthOperatingCashFlow": 0.06975566069312394,  
		"growthCapitalExpenditure": 0.13796879277306323,  
		"growthFreeCashFlow": 0.092615279562982,  
		"growthNetDebtIssuance": 0.3942026057973942,  
		"growthLongTermNetDebtIssuance": \-0.6812426135404356,  
		"growthShortTermNetDebtIssuance": 1.995475113122172,  
		"growthNetStockIssuance": \-0.2243584784010316,  
		"growthPreferredDividendsPaid": \-0.013910149750415973,  
		"growthIncomeTaxesPaid": 0.3973981476524439,  
		"growthInterestPaid": \-1  
	}  
\]

[Financial Statement Growth API](https://site.financialmodelingprep.com/developer/docs/stable/financial-statement-growth)

Analyze the growth of key financial statement items across income, balance sheet, and cash flow statements with the Financial Statement Growth API. Track changes over time to understand trends in financial performance.

**Endpoint:**

https://financialmodelingprep.com/stable/financial-growth?*symbol*\=AAPL

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 5 |
| period | string | Q1,Q2,Q3,Q4,FY,annual,quarter |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"date": "2024-09-28",  
		"fiscalYear": "2024",  
		"period": "FY",  
		"reportedCurrency": "USD",  
		"revenueGrowth": 0.020219940775141214,  
		"grossProfitGrowth": 0.06819471705252206,  
		"ebitgrowth": 0.07799581805933456,  
		"operatingIncomeGrowth": 0.07799581805933456,  
		"netIncomeGrowth": \-0.033599670086086914,  
		"epsgrowth": \-0.008116883116883088,  
		"epsdilutedGrowth": \-0.008156606851549727,  
		"weightedAverageSharesGrowth": \-0.02543458616683152,  
		"weightedAverageSharesDilutedGrowth": \-0.02557791606880283,  
		"dividendsPerShareGrowth": 0.040371570095532654,  
		"operatingCashFlowGrowth": 0.06975566069312394,  
		"receivablesGrowth": 0.08621792243994425,  
		"inventoryGrowth": 0.15084504817564365,  
		"assetGrowth": 0.035160515396374756,  
		"bookValueperShareGrowth": \-0.059693251557224776,  
		"debtGrowth": \-0.0401393489845888,  
		"rdexpenseGrowth": 0.04863780712017383,  
		"sgaexpensesGrowth": 0.04672709770575967,  
		"freeCashFlowGrowth": 0.092615279562982,  
		"tenYRevenueGrowthPerShare": 2.3937532854122625,  
		"fiveYRevenueGrowthPerShare": 0.8093292228858464,  
		"threeYRevenueGrowthPerShare": 0.163506592883552,  
		"tenYOperatingCFGrowthPerShare": 2.1417809176982403,  
		"fiveYOperatingCFGrowthPerShare": 1.051533221923415,  
		"threeYOperatingCFGrowthPerShare": 0.23720294833900227,  
		"tenYNetIncomeGrowthPerShare": 2.76381558093543,  
		"fiveYNetIncomeGrowthPerShare": 1.0421744314966246,  
		"threeYNetIncomeGrowthPerShare": 0.07761907162786884,  
		"tenYShareholdersEquityGrowthPerShare": \-0.19003774225234785,  
		"fiveYShareholdersEquityGrowthPerShare": \-0.24235004889283715,  
		"threeYShareholdersEquityGrowthPerShare": \-0.017459858915902907,  
		"tenYDividendperShareGrowthPerShare": 1.1722201809466772,  
		"fiveYDividendperShareGrowthPerShare": 0.29890046876764864,  
		"threeYDividendperShareGrowthPerShare": 0.14617932692103452,  
		"ebitdaGrowth": null,  
		"growthCapitalExpenditure": null,  
		"tenYBottomLineNetIncomeGrowthPerShare": null,  
		"fiveYBottomLineNetIncomeGrowthPerShare": null,  
		"threeYBottomLineNetIncomeGrowthPerShare": null  
	}  
\]

[Revenue Product Segmentation API](https://site.financialmodelingprep.com/developer/docs/stable/revenue-product-segmentation)

Access detailed revenue breakdowns by product line with the Revenue Product Segmentation API. Understand which products drive a company's earnings and get insights into the performance of individual product segments.

**Endpoint:**

https://financialmodelingprep.com/stable/revenue-product-segmentation?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| period | string | annual,quarter |
| structure | string | flat |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"fiscalYear": 2024,  
		"period": "FY",  
		"reportedCurrency": null,  
		"date": "2024-09-28",  
		"data": {  
			"Mac": 29984000000,  
			"Service": 96169000000,  
			"Wearables, Home and Accessories": 37005000000,  
			"iPad": 26694000000,  
			"iPhone": 201183000000  
		}  
	}  
\]

[Revenue Geographic Segments API](https://site.financialmodelingprep.com/developer/docs/stable/revenue-geographic-segments)

Access detailed revenue breakdowns by geographic region with the Revenue Geographic Segments API. Analyze how different regions contribute to a company’s total revenue and identify key markets for growth.

**Endpoint:**

https://financialmodelingprep.com/stable/revenue-geographic-segmentation?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| period | string | annual,quarter |
| structure | string | flat |

Response  
\[  
	{  
		"symbol": "AAPL",  
		"fiscalYear": 2024,  
		"period": "FY",  
		"reportedCurrency": null,  
		"date": "2024-09-28",  
		"data": {  
			"Americas Segment": 167045000000,  
			"Europe Segment": 101328000000,  
			"Greater China Segment": 66952000000,  
			"Japan Segment": 25052000000,  
			"Rest of Asia Pacific": 30658000000  
		}  
	}  
\]

## **Form 13F**

[Institutional Ownership Filings API](https://site.financialmodelingprep.com/developer/docs/stable/latest-filings)

Stay up to date with the most recent SEC filings related to institutional ownership using the Institutional Ownership Filings API. This tool allows you to track the latest reports and disclosures from institutional investors, giving you a real-time view of major holdings and regulatory submissions.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/latest?*page*\=0&*limit*\=100

Query Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 100 |

Response  
\[  
	{  
		"cik": "0001963967",  
		"name": "CPA ASSET MANAGEMENT LLC",  
		"date": "2024-12-31",  
		"filingDate": "2025-02-04 00:00:00",  
		"acceptedDate": "2025-02-04 17:28:36",  
		"formType": "13F-HR",  
		"link": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/0001963967-25-000001-index.htm",  
		"finalLink": "https://www.sec.gov/Archives/edgar/data/1963967/000196396725000001/boc2024q413f.xml"  
	}  
\]

[Filings Extract API](https://site.financialmodelingprep.com/developer/docs/stable/filings-extract)

The SEC Filings Extract API allows users to extract detailed data directly from official SEC filings. This API provides access to key information such as company shares, security details, and filing links, making it easier to analyze corporate disclosures.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/extract?*cik*\=0001388838&*year*\=2023&*quarter*\=3

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| cik\* | string | 0001388838 |
| year\* | string | 2023 |
| quarter\* | string | 3 |

Response  
\[  
	{  
		"date": "2023-09-30",  
		"filingDate": "2023-11-13",  
		"acceptedDate": "2023-11-13",  
		"cik": "0001388838",  
		"securityCusip": "674215207",  
		"symbol": "CHRD",  
		"nameOfIssuer": "CHORD ENERGY CORPORATION",  
		"shares": 13280,  
		"titleOfClass": "COM NEW",  
		"sharesType": "SH",  
		"putCallShare": "",  
		"value": 2152290,  
		"link": "https://www.sec.gov/Archives/edgar/data/1388838/000117266123003760/0001172661-23-003760-index.htm",  
		"finalLink": "https://www.sec.gov/Archives/edgar/data/1388838/000117266123003760/infotable.xml"  
	}  
\]  
[Form 13F Filings Dates API](https://site.financialmodelingprep.com/developer/docs/stable/form-13f-filings-dates)

The Form 13F Filings Dates API allows you to retrieve dates associated with Form 13F filings by institutional investors. This is crucial for tracking stock holdings of institutional investors at specific points in time, providing valuable insights into their investment strategies.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/dates?*cik*\=0001067983

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| cik\* | string | 0001067983 |

Response

\[  
	{  
		"date": "2024-09-30",  
		"year": 2024,  
		"quarter": 3  
	}  
\]

[Filings Extract With Analytics By Holder API](https://site.financialmodelingprep.com/developer/docs/stable/filings-extract-with-analytics-by-holder)

The Filings Extract With Analytics By Holder API provides an analytical breakdown of institutional filings. This API offers insight into stock movements, strategies, and portfolio changes by major institutional holders, helping you understand their investment behavior and track significant changes in stock ownership.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/extract-analytics/holder?*symbol*\=AAPL&*year*\=2023&*quarter*\=3&*page*\=0&*limit*\=10

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| year\* | string | 2023 |
| quarter\* | string | 3 |
| page | number | 0 |
| limit | number | 10 |

Response

\[  
	{  
		"date": "2023-09-30",  
		"cik": "0000102909",  
		"filingDate": "2023-12-18",  
		"investorName": "VANGUARD GROUP INC",  
		"symbol": "AAPL",  
		"securityName": "APPLE INC",  
		"typeOfSecurity": "COM",  
		"securityCusip": "037833100",  
		"sharesType": "SH",  
		"putCallShare": "Share",  
		"investmentDiscretion": "SOLE",  
		"industryTitle": "ELECTRONIC COMPUTERS",  
		"weight": 5.4673,  
		"lastWeight": 5.996,  
		"changeInWeight": \-0.5287,  
		"changeInWeightPercentage": \-8.8175,  
		"marketValue": 222572509140,  
		"lastMarketValue": 252876459509,  
		"changeInMarketValue": \-30303950369,  
		"changeInMarketValuePercentage": \-11.9837,  
		"sharesNumber": 1299997133,  
		"lastSharesNumber": 1303688506,  
		"changeInSharesNumber": \-3691373,  
		"changeInSharesNumberPercentage": \-0.2831,  
		"quarterEndPrice": 171.21,  
		"avgPricePaid": 95.86,  
		"isNew": false,  
		"isSoldOut": false,  
		"ownership": 8.3336,  
		"lastOwnership": 8.305,  
		"changeInOwnership": 0.0286,  
		"changeInOwnershipPercentage": 0.3445,  
		"holdingPeriod": 42,  
		"firstAdded": "2013-06-30",  
		"performance": \-29671950396,  
		"performancePercentage": \-11.7338,  
		"lastPerformance": 38078179274,  
		"changeInPerformance": \-67750129670,  
		"isCountedForPerformance": true  
	}  
\]

[Holder Performance Summary API](https://site.financialmodelingprep.com/developer/docs/stable/holder-performance-summary)

The Holder Performance Summary API provides insights into the performance of institutional investors based on their stock holdings. This data helps track how well institutional holders are performing, their portfolio changes, and how their performance compares to benchmarks like the S\&P 500\.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/holder-performance-summary?*cik*\=0001067983&*page*\=0

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| cik\* | string | 0001067983 |
| page | number | 0 |

Response

\[  
	{  
		"date": "2024-09-30",  
		"cik": "0001067983",  
		"investorName": "BERKSHIRE HATHAWAY INC",  
		"portfolioSize": 40,  
		"securitiesAdded": 3,  
		"securitiesRemoved": 4,  
		"marketValue": 266378900503,  
		"previousMarketValue": 279969062343,  
		"changeInMarketValue": \-13590161840,  
		"changeInMarketValuePercentage": \-4.8542,  
		"averageHoldingPeriod": 18,  
		"averageHoldingPeriodTop10": 31,  
		"averageHoldingPeriodTop20": 27,  
		"turnover": 0.175,  
		"turnoverAlternateSell": 13.9726,  
		"turnoverAlternateBuy": 1.1974,  
		"performance": 17707926874,  
		"performancePercentage": 6.325,  
		"lastPerformance": 38318168662,  
		"changeInPerformance": \-20610241788,  
		"performance1year": 89877376224,  
		"performancePercentage1year": 28.5368,  
		"performance3year": 91730847239,  
		"performancePercentage3year": 31.2597,  
		"performance5year": 157058602844,  
		"performancePercentage5year": 73.1617,  
		"performanceSinceInception": 182067479115,  
		"performanceSinceInceptionPercentage": 198.2138,  
		"performanceRelativeToSP500Percentage": 6.325,  
		"performance1yearRelativeToSP500Percentage": 28.5368,  
		"performance3yearRelativeToSP500Percentage": 36.5632,  
		"performance5yearRelativeToSP500Percentage": 36.1296,  
		"performanceSinceInceptionRelativeToSP500Percentage": 37.0968  
	}  
\]

[Holders Industry Breakdown API](https://site.financialmodelingprep.com/developer/docs/stable/holders-industry-breakdown)

The Holders Industry Breakdown API provides an overview of the sectors and industries that institutional holders are investing in. This API helps analyze how institutional investors distribute their holdings across different industries and track changes in their investment strategies over time.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/holder-industry-breakdown?*cik*\=0001067983&*year*\=2023&*quarter*\=3

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| cik\* | string | 0001067983 |
| year\* | string | 2023 |
| quarter\* | string | 3 |

Response  
\[  
	{  
		"date": "2023-09-30",  
		"cik": "0001067983",  
		"investorName": "BERKSHIRE HATHAWAY INC",  
		"industryTitle": "ELECTRONIC COMPUTERS",  
		"weight": 49.7704,  
		"lastWeight": 51.0035,  
		"changeInWeight": \-1.2332,  
		"changeInWeightPercentage": \-2.4178,  
		"performance": \-20838154294,  
		"performancePercentage": \-178.2938,  
		"lastPerformance": 26615340304,  
		"changeInPerformance": \-47453494598  
	}  
\]

[Positions Summary API](https://site.financialmodelingprep.com/developer/docs/stable/positions-summary)

The Positions Summary API provides a comprehensive snapshot of institutional holdings for a specific stock symbol. It tracks key metrics like the number of investors holding the stock, changes in the number of shares, total investment value, and ownership percentages over time.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/symbol-positions-summary?*symbol*\=AAPL&*year*\=2023&*quarter*\=3

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| year\* | string | 2023 |
| quarter\* | string | 3 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"cik": "0000320193",  
		"date": "2023-09-30",  
		"investorsHolding": 4805,  
		"lastInvestorsHolding": 4749,  
		"investorsHoldingChange": 56,  
		"numberOf13Fshares": 9247670386,  
		"lastNumberOf13Fshares": 9345671472,  
		"numberOf13FsharesChange": \-98001086,  
		"totalInvested": 1613733330618,  
		"lastTotalInvested": 1825154796061,  
		"totalInvestedChange": \-211421465443,  
		"ownershipPercent": 59.2821,  
		"lastOwnershipPercent": 59.5356,  
		"ownershipPercentChange": \-0.2535,  
		"newPositions": 158,  
		"lastNewPositions": 188,  
		"newPositionsChange": \-30,  
		"increasedPositions": 1921,  
		"lastIncreasedPositions": 1775,  
		"increasedPositionsChange": 146,  
		"closedPositions": 156,  
		"lastClosedPositions": 122,  
		"closedPositionsChange": 34,  
		"reducedPositions": 2375,  
		"lastReducedPositions": 2506,  
		"reducedPositionsChange": \-131,  
		"totalCalls": 173528138,  
		"lastTotalCalls": 198746782,  
		"totalCallsChange": \-25218644,  
		"totalPuts": 192878290,  
		"lastTotalPuts": 177007062,  
		"totalPutsChange": 15871228,  
		"putCallRatio": 1.1115,  
		"lastPutCallRatio": 0.8906,  
		"putCallRatioChange": 22.0894  
	}  
\]

[Industry Performance Summary API](https://site.financialmodelingprep.com/developer/docs/stable/industry-summary)

The Industry Performance Summary API provides an overview of how various industries are performing financially. By analyzing the value of industries over a specific period, this API helps investors and analysts understand the health of entire sectors and make informed decisions about sector-based investments.

**Endpoint:**

https://financialmodelingprep.com/stable/institutional-ownership/industry-summary?*year*\=2023&*quarter*\=3

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| year\* | string | 2023 |
| quarter\* | string | 3 |

Response

\[  
	{  
		"industryTitle": "ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS",  
		"industryValue": 10979226300,  
		"date": "2023-09-30"  
	}  
\]

## **Indexes**

[Stock Market Indexes List API](https://site.financialmodelingprep.com/developer/docs/stable/indexes-list)

Retrieve a comprehensive list of stock market indexes across global exchanges using the FMP Stock Market Indexes List API. This API provides essential information such as the symbol, name, exchange, and currency for each index, helping analysts and investors keep track of various market benchmarks.

**Endpoint:**

https://financialmodelingprep.com/stable/*index-list*

Response

\[  
	{  
		"symbol": "^TTIN",  
		"name": "S\&P/TSX Capped Industrials Index",  
		"exchange": "TSX",  
		"currency": "CAD"  
	}  
\]

[Index Quote API](https://site.financialmodelingprep.com/developer/docs/stable/index-quote)

Access real-time stock index quotes with the Stock Index Quote API. Stay updated with the latest price changes, daily highs and lows, volume, and other key metrics for major stock indices around the world.

**Endpoint:**

https://financialmodelingprep.com/stable/quote?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |

Response

\[  
	{  
		"symbol": "^GSPC",  
		"name": "S\&P 500",  
		"price": 6366.13,  
		"changePercentage": 0.11354,  
		"change": 7.22,  
		"volume": 1498664000,  
		"dayLow": 6360.57,  
		"dayHigh": 6379.54,  
		"yearHigh": 6379.54,  
		"yearLow": 4835.04,  
		"marketCap": 0,  
		"priceAvg50": 6068.663,  
		"priceAvg200": 5880.0864,  
		"exchange": "INDEX",  
		"open": 6368.6,  
		"previousClose": 6358.91,  
		"timestamp": 1753374601  
	}  
\]

[Index Short Quote API](https://site.financialmodelingprep.com/developer/docs/stable/index-quote-short)

Access concise stock index quotes with the Stock Index Short Quote API. This API provides a snapshot of the current price, change, and volume for stock indexes, making it ideal for users who need a quick overview of market movements.

**Endpoint:**

https://financialmodelingprep.com/stable/quote-short?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |

Response

\[  
	{  
		"symbol": "^GSPC",  
		"price": 6366.13,  
		"change": 7.22,  
		"volume": 1498664000  
	}  
\]

[All Index Quotes API](https://site.financialmodelingprep.com/developer/docs/stable/all-index-quotes)

The All Index Quotes API provides real-time quotes for a wide range of stock indexes, from major market benchmarks to niche indexes. This API allows users to track market performance across multiple indexes in a single request, giving them a broad view of the financial markets.

**Endpoint:**

https://financialmodelingprep.com/stable/*batch-index-quotes*

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| short | boolean | true |

Response

\[  
	{  
		"symbol": "^DJBGIE",  
		"price": 4155.76,  
		"change": 1.09,  
		"volume": 0  
	}  
\]

[Historical Index Light Chart API](https://site.financialmodelingprep.com/developer/docs/stable/index-historical-price-eod-light)

Retrieve end-of-day historical prices for stock indexes using the Historical Price Data API. This API provides essential data such as date, price, and volume, enabling detailed analysis of price movements over time.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/light?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"symbol": "^GSPC",  
		"date": "2025-07-24",  
		"price": 6365.77,  
		"volume": 1499302000  
	}  
\]

[Historical Index Full Chart API](https://site.financialmodelingprep.com/developer/docs/stable/index-historical-price-eod-full)

Access full historical end-of-day prices for stock indexes using the Detailed Historical Price Data API. This API provides comprehensive information, including open, high, low, close prices, volume, and additional metrics for detailed financial analysis.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-price-eod/full?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"symbol": "^GSPC",  
		"date": "2025-07-24",  
		"open": 6368.6,  
		"high": 6379.54,  
		"low": 6360.57,  
		"close": 6365.77,  
		"volume": 1499302000,  
		"change": \-2.83,  
		"changePercent": \-0.04443677,  
		"vwap": 6368.63  
	}  
\]

[1-Minute Interval Index Price API](https://site.financialmodelingprep.com/developer/docs/stable/index-intraday-1-min)

Retrieve 1-minute interval intraday data for stock indexes using the Intraday 1-Minute Price Data API. This API provides granular price information, helping users track short-term price movements and trading volume within each minute.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1min?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"date": "2025-07-24 12:29:00",  
		"open": 6365.34,  
		"low": 6365.34,  
		"high": 6366.09,  
		"close": 6366.09,  
		"volume": 4428000  
	}  
\]

[5-Minute Interval Index Price API](https://site.financialmodelingprep.com/developer/docs/stable/index-intraday-5-min)

Retrieve 5-minute interval intraday price data for stock indexes using the Intraday 5-Minute Price Data API. This API provides crucial insights into price movements and trading volume within 5-minute windows, ideal for traders who require short-term data.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/5min?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"date": "2025-07-24 12:30:00",  
		"open": 6366.18,  
		"low": 6365.57,  
		"high": 6366.18,  
		"close": 6365.69,  
		"volume": 1574690  
	}  
\]

[1-Hour Interval Index Price API](https://site.financialmodelingprep.com/developer/docs/stable/index-intraday-1-hour)

Access 1-hour interval intraday data for stock indexes using the Intraday 1-Hour Price Data API. This API provides detailed price movements and volume within hourly intervals, making it ideal for tracking medium-term market trends during the trading day.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-chart/1hour?*symbol*\=^GSPC

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | ^GSPC |
| from | date | 2025-04-25 |
| to | date | 2025-07-25 |

Response

\[  
	{  
		"date": "2025-07-24 12:30:00",  
		"open": 6366.18,  
		"low": 6365.57,  
		"high": 6366.18,  
		"close": 6365.69,  
		"volume": 1574690  
	}  
\]

## **Insider Trades**

[Latest Insider Trading API](https://site.financialmodelingprep.com/developer/docs/stable/latest-insider-trade)

Access the latest insider trading activity using the Latest Insider Trading API. Track which company insiders are buying or selling stocks and analyze their transactions.

**Endpoint:**

https://financialmodelingprep.com/stable/insider-trading/latest?*page*\=0&*limit*\=100

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| date | date | 2025-04-24 |
| page | number | 0 |
| limit | number | 100 |

Response

\[  
	{  
		"symbol": "APA",  
		"filingDate": "2025-02-04",  
		"transactionDate": "2025-02-01",  
		"reportingCik": "0001380034",  
		"companyCik": "0001841666",  
		"transactionType": "M-Exempt",  
		"securitiesOwned": 104398,  
		"reportingName": "Hoyt Rebecca A",  
		"typeOfOwner": "officer: Sr. VP, Chief Acct Officer",  
		"acquisitionOrDisposition": "A",  
		"directOrIndirect": "D",  
		"formType": "4",  
		"securitiesTransacted": 3450,  
		"price": 0,  
		"securityName": "Common Stock",  
		"url": "https://www.sec.gov/Archives/edgar/data/1841666/000194906025000035/0001949060-25-000035-index.htm"  
	}  
\]

[Search Insider Trades API](https://site.financialmodelingprep.com/developer/docs/stable/search-insider-trades)

Search insider trading activity by company or symbol using the Search Insider Trades API. Find specific trades made by corporate insiders, including executives and directors.

**Endpoint:**

https://financialmodelingprep.com/stable/insider-trading/search?*page*\=0&*limit*\=100

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol | string | AAPL |
| page | number | 0 |
| limit | number | 100 |
| reportingCik | string | 0001496686 |
| companyCik | string | 0000320193 |
| transactionType | string | S-Sale |

Response

\[  
	{  
		"symbol": "AAPL",  
		"filingDate": "2025-02-04",  
		"transactionDate": "2025-02-03",  
		"reportingCik": "0001214128",  
		"companyCik": "0000320193",  
		"transactionType": "S-Sale",  
		"securitiesOwned": 4159576,  
		"reportingName": "LEVINSON ARTHUR D",  
		"typeOfOwner": "director",  
		"acquisitionOrDisposition": "D",  
		"directOrIndirect": "D",  
		"formType": "4",  
		"securitiesTransacted": 1516,  
		"price": 226.3501,  
		"securityName": "Common Stock",  
		"url": "https://www.sec.gov/Archives/edgar/data/320193/000032019325000019/0000320193-25-000019-index.htm"  
	}  
\]

[Search Insider Trades by Reporting Name API](https://site.financialmodelingprep.com/developer/docs/stable/search-reporting-name)

Search for insider trading activity by reporting name using the Search Insider Trades by Reporting Name API. Track trading activities of specific individuals or groups involved in corporate insider transactions.

**Endpoint:**

https://financialmodelingprep.com/stable/insider-trading/reporting-name?*name*\=Zuckerberg

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| name\* | string | Zuckerberg |

Response

\[  
	{  
		"reportingCik": "0001548760",  
		"reportingName": "Zuckerberg Mark"  
	}  
\]

[All Insider Transaction Types API](https://site.financialmodelingprep.com/developer/docs/stable/all-transaction-types)

Access a comprehensive list of insider transaction types with the All Insider Transaction Types API. This API provides details on various transaction actions, including purchases, sales, and other corporate actions involving insider trading.

**Endpoint:**

https://financialmodelingprep.com/stable/*insider-trading-transaction-type*

Response

\[  
	{  
		"transactionType": "A-Award"  
	}  
\]

[Insider Trade Statistics API](https://site.financialmodelingprep.com/developer/docs/stable/insider-trade-statistics)

Analyze insider trading activity with the Insider Trade Statistics API. This API provides key statistics on insider transactions, including total purchases, sales, and trends for specific companies or stock symbols.

**Endpoint:**

https://financialmodelingprep.com/stable/insider-trading/statistics?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[  
	{  
		"symbol": "AAPL",  
		"cik": "0000320193",  
		"year": 2024,  
		"quarter": 4,  
		"acquiredTransactions": 6,  
		"disposedTransactions": 38,  
		"acquiredDisposedRatio": 0.1579,  
		"totalAcquired": 994544,  
		"totalDisposed": 2297088,  
		"averageAcquired": 165757.3333,  
		"averageDisposed": 60449.6842,  
		"totalPurchases": 0,  
		"totalSales": 22  
	}  
\]

[Acquisition Ownership API](https://site.financialmodelingprep.com/developer/docs/stable/acquisition-ownership)

Track changes in stock ownership during acquisitions using the Acquisition Ownership API. This API provides detailed information on how mergers, takeovers, or beneficial ownership changes impact the stock ownership structure of a company.

**Endpoint:**

https://financialmodelingprep.com/stable/acquisition-of-beneficial-ownership?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| limit | number | 2000 |

Response

\[  
	{  
		"cik": "0000320193",  
		"symbol": "AAPL",  
		"filingDate": "2024-02-14",  
		"acceptedDate": "2024-02-14",  
		"cusip": "037833100",  
		"nameOfReportingPerson": "National Indemnity Company",  
		"citizenshipOrPlaceOfOrganization": "State of Nebraska",  
		"soleVotingPower": "0",  
		"sharedVotingPower": "755059877",  
		"soleDispositivePower": "0",  
		"sharedDispositivePower": "755059877",  
		"amountBeneficiallyOwned": "755059877",  
		"percentOfClass": "4.8",  
		"typeOfReportingPerson": "IC, EP, IN, CO",  
		"url": "https://www.sec.gov/Archives/edgar/data/320193/000119312524036431/d751537dsc13ga.htm"  
	}  
\]

## **Market Performance**

[Market Sector Performance Snapshot API](https://site.financialmodelingprep.com/developer/docs/stable/sector-performance-snapshot)

Get a snapshot of sector performance using the Market Sector Performance Snapshot API. Analyze how different industries are performing in the market based on average changes across sectors.

**Endpoint:**

https://financialmodelingprep.com/stable/sector-performance-snapshot?*date*\=2024-02-01

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| date\* | string | 2024-02-01 |
| exchange | string | NASDAQ |
| sector | string | Energy |

Response

\[  
	{  
		"date": "2024-02-01",  
		"sector": "Basic Materials",  
		"exchange": "NASDAQ",  
		"averageChange": \-0.31481377464310634  
	}  
\]

[Industry Performance Snapshot API](https://site.financialmodelingprep.com/developer/docs/stable/industry-performance-snapshot)

Access detailed performance data by industry using the Industry Performance Snapshot API. Analyze trends, movements, and daily performance metrics for specific industries across various stock exchanges.

**Endpoint:**

https://financialmodelingprep.com/stable/industry-performance-snapshot?*date*\=2024-02-01

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| date\* | string | 2024-02-01 |
| exchange | string | NASDAQ |
| industry | string | Biotechnology |

Response

\[  
	{  
		"date": "2024-02-01",  
		"industry": "Advertising Agencies",  
		"exchange": "NASDAQ",  
		"averageChange": 3.8660194344955996  
	}  
\]

[Historical Market Sector Performance API](https://site.financialmodelingprep.com/developer/docs/stable/historical-sector-performance)

Access historical sector performance data using the Historical Market Sector Performance API. Review how different sectors have performed over time across various stock exchanges.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-sector-performance?*sector*\=Energy

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | string | 2024-02-01 |
| exchange | string | NASDAQ |
| sector\* | string | Energy |
| to | string | 2024-03-01 |

Response

\[  
	{  
		"date": "2024-02-01",  
		"sector": "Energy",  
		"exchange": "NASDAQ",  
		"averageChange": 0.6397534025664513  
	}  
\]

[Historical Industry Performance API](https://site.financialmodelingprep.com/developer/docs/stable/historical-industry-performance)

Access historical performance data for industries using the Historical Industry Performance API. Track long-term trends and analyze how different industries have evolved over time across various stock exchanges.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-industry-performance?*industry*\=Biotechnology

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| industry\* | string | Biotechnology |
| exchange | string | NASDAQ |
| from | string | 2024-02-01 |
| to | string | 2024-03-01 |

Response

\[  
	{  
		"date": "2024-02-01",  
		"industry": "Biotechnology",  
		"exchange": "NASDAQ",  
		"averageChange": 1.1479066960358322  
	}  
\]

[Sector PE Snapshot API](https://site.financialmodelingprep.com/developer/docs/stable/sector-pe-snapshot)

Retrieve the price-to-earnings (P/E) ratios for various sectors using the Sector P/E Snapshot API. Compare valuation levels across sectors to better understand market valuations.

**Endpoint:**

https://financialmodelingprep.com/stable/sector-pe-snapshot?*date*\=2024-02-01

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| date\* | string | 2024-02-01 |
| exchange | string | NASDAQ |
| sector | string | Energy |

Response

\[  
	{  
		"date": "2024-02-01",  
		"sector": "Basic Materials",  
		"exchange": "NASDAQ",  
		"pe": 15.687711758428254  
	}  
\]

[Industry PE Snapshot API](https://site.financialmodelingprep.com/developer/docs/stable/industry-pe-snapshot)

View price-to-earnings (P/E) ratios for different industries using the Industry P/E Snapshot API. Analyze valuation levels across various industries to understand how each is priced relative to its earnings.

**Endpoint:**

https://financialmodelingprep.com/stable/industry-pe-snapshot?*date*\=2024-02-01

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| date\* | string | 2024-02-01 |
| exchange | string | NASDAQ |
| industry | string | Biotechnology |

Response

\[  
	{  
		"date": "2024-02-01",  
		"industry": "Advertising Agencies",  
		"exchange": "NASDAQ",  
		"pe": 71.09601665201151  
	}  
\]

[Historical Sector PE API](https://site.financialmodelingprep.com/developer/docs/stable/historical-sector-pe)

Access historical price-to-earnings (P/E) ratios for various sectors using the Historical Sector P/E API. Analyze how sector valuations have evolved over time to understand long-term trends and market shifts.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-sector-pe?*sector*\=Energy

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | string | 2024-02-01 |
| exchange | string | NASDAQ |
| sector\* | string | Energy |
| to | string | 2024-03-01 |

Response

\[  
	{  
		"date": "2024-02-01",  
		"sector": "Energy",  
		"exchange": "NASDAQ",  
		"pe": 14.411400922841464  
	}  
\]

[Historical Industry PE API](https://site.financialmodelingprep.com/developer/docs/stable/historical-industry-pe)

Access historical price-to-earnings (P/E) ratios by industry using the Historical Industry P/E API. Track valuation trends across various industries to understand how market sentiment and valuations have evolved over time.

**Endpoint:**

https://financialmodelingprep.com/stable/historical-industry-pe?*industry*\=Biotechnology

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| industry\* | string | Biotechnology |
| exchange | string | NASDAQ |
| from | string | 2024-02-01 |
| to | string | 2024-03-01 |

Response  
\[  
	{  
		"date": "2024-02-01",  
		"industry": "Biotechnology",  
		"exchange": "NASDAQ",  
		"pe": 10.181600321811821  
	}  
\]

[Biggest Stock Gainers API](https://site.financialmodelingprep.com/developer/docs/stable/biggest-gainers)

Track the stocks with the largest price increases using the Top Stock Gainers API. Identify the companies that are leading the market with significant price surges, offering potential growth opportunities.

**Endpoint:**

https://financialmodelingprep.com/stable/*biggest-gainers*

Response

\[  
	{  
		"symbol": "LTRY",  
		"price": 0.5876,  
		"name": "Lottery.com Inc.",  
		"change": 0.2756,  
		"changesPercentage": 88.3333,  
		"exchange": "NASDAQ"  
	}  
\]

[Biggest Stock Losers API](https://site.financialmodelingprep.com/developer/docs/stable/biggest-losers)

Access data on the stocks with the largest price drops using the Biggest Stock Losers API. Identify companies experiencing significant declines and track the stocks that are falling the fastest in the market.

**Endpoint:**

https://financialmodelingprep.com/stable/*biggest-losers*

Response

\[  
	{  
		"symbol": "IDEX",  
		"price": 0.0021,  
		"name": "Ideanomics, Inc.",  
		"change": \-0.0029,  
		"changesPercentage": \-58,  
		"exchange": "NASDAQ"  
	}  
\]

[Top Traded Stocks API](https://site.financialmodelingprep.com/developer/docs/stable/most-active)

View the most actively traded stocks using the Top Traded Stocks API. Identify the companies experiencing the highest trading volumes in the market and track where the most trading activity is happening.

**Endpoint:**

https://financialmodelingprep.com/stable/*most-actives*

Response

\[  
	{  
		"symbol": "LUCY",  
		"price": 5.03,  
		"name": "Innovative Eyewear, Inc.",  
		"change": \-0.01,  
		"changesPercentage": \-0.1984,  
		"exchange": "NASDAQ"  
	}  
\]

## **News**

[FMP Articles API](https://site.financialmodelingprep.com/developer/docs/stable/fmp-articles)

Access the latest articles from Financial Modeling Prep with the FMP Articles API. Get comprehensive updates including headlines, snippets, and publication URLs.

**Endpoint:**

https://financialmodelingprep.com/stable/fmp-articles?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"title": "Merck Shares Plunge 8% as Weak Guidance Overshadows Strong Revenue Growth",  
		"date": "2025-02-04 09:33:00",  
		"content": "\<p\>\<a href='https://financialmodelingprep.com/financial-summary/MRK'\>Merck & Co (NYSE:MRK)\</a\> saw its stock sink over 8% in pre-market today after delivering mixed fourth-quarter results, with earnings missing expectations, revenue exceeding forecasts, and full-year guidance coming in below analyst estimates.\</p\>\\n\<p\>For Q4, the pharmaceutical giant reported adjusted earnings per share (EPS) of $1.72, falling short of the $1.81 consensus estimate. However, revenue climbed 7% year-over-year to $1...",  
		"tickers": "NYSE:MRK",  
		"image": "https://cdn.financialmodelingprep.com/images/fmp-1738679603793.jpg",  
		"link": "https://financialmodelingprep.com/market-news/fmp-merck-shares-plunge-8-as-weak-guidance-overshadows-strong-revenue-growth",  
		"author": "Davit Kirakosyan",  
		"site": "Financial Modeling Prep"  
	}  
\]

[General News API](https://site.financialmodelingprep.com/developer/docs/stable/general-news)

Access the latest general news articles from a variety of sources with the FMP General News API. Obtain headlines, snippets, and publication URLs for comprehensive news coverage.

**Endpoint:**

https://financialmodelingprep.com/stable/news/general-latest?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"symbol": null,  
		"publishedDate": "2025-02-03 23:51:37",  
		"publisher": "CNBC",  
		"title": "Asia tech stocks rise after Trump pauses tariffs on China and Mexico",  
		"image": "https://images.financialmodelingprep.com/news/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-20250203.jpg",  
		"site": "cnbc.com",  
		"text": "Gains in Asian tech companies were broad-based, with stocks in Japan, South Korea and Hong Kong advancing. Semiconductor players Advantest and Lasertec led gains among Japanese tech stocks.",  
		"url": "https://www.cnbc.com/2025/02/04/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-china-and-mexico.html"  
	}  
\]

[Press Releases API](https://site.financialmodelingprep.com/developer/docs/stable/press-releases)

Access official company press releases with the FMP Press Releases API. Get real-time updates on corporate announcements, earnings reports, mergers, and more.

**Endpoint:**

https://financialmodelingprep.com/stable/news/press-releases-latest?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"symbol": "LNW",  
		"publishedDate": "2025-02-03 23:32:00",  
		"publisher": "PRNewsWire",  
		"title": "Rosen Law Firm Encourages Light & Wonder, Inc. Investors to Inquire About Securities Class Action Investigation \- LNW",  
		"image": "https://images.financialmodelingprep.com/news/rosen-law-firm-encourages-light-wonder-inc-investors-to-20250203.jpg",  
		"site": "prnewswire.com",  
		"text": "NEW YORK , Feb. 3, 2025 /PRNewswire/ \-- Why: Rosen Law Firm, a global investor rights law firm, continues to investigate potential securities claims on behalf of shareholders of Light & Wonder, Inc. (NASDAQ: LNW) resulting from allegations that Light & Wonder may have issued materially misleading business information to the investing public. So What: If you purchased Light & Wonder securities you may be entitled to compensation without payment of any out of pocket fees or costs through a contingency fee arrangement.",  
		"url": "https://www.prnewswire.com/news-releases/rosen-law-firm-encourages-light--wonder-inc-investors-to-inquire-about-securities-class-action-investigation--lnw-302366877.html"  
	}  
\]

[Stock News API](https://site.financialmodelingprep.com/developer/docs/stable/stock-news)

Stay informed with the latest stock market news using the FMP Stock News Feed API. Access headlines, snippets, publication URLs, and ticker symbols for the most recent articles from a variety of sources.

**Endpoint:**

https://financialmodelingprep.com/stable/news/stock-latest?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"symbol": "INSG",  
		"publishedDate": "2025-02-03 23:53:40",  
		"publisher": "Seeking Alpha",  
		"title": "Q4 Earnings Release Looms For Inseego, But Don't Expect Miracles",  
		"image": "https://images.financialmodelingprep.com/news/q4-earnings-release-looms-for-inseego-but-dont-expect-20250203.jpg",  
		"site": "seekingalpha.com",  
		"text": "Inseego's Q3 beat was largely due to a one-time debt restructuring gain, not sustainable earnings growth, raising concerns about future performance. The sale of its telematics business for $52 million allows INSG to focus on North America, but it remains to be seen if this was wise. Despite improved margins and reduced debt, Inseego's revenue growth is insufficient, and its high stock price remains unjustifiable for new investors.",  
		"url": "https://seekingalpha.com/article/4754485-inseego-stock-q4-earnings-preview-monitor-growth-margins-closely"  
	}  
\]

[Crypto News API](https://site.financialmodelingprep.com/developer/docs/stable/crypto-news)

Stay informed with the latest cryptocurrency news using the FMP Crypto News API. Access a curated list of articles from various sources, including headlines, snippets, and publication URLs.

**Endpoint:**

https://financialmodelingprep.com/stable/news/crypto-latest?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"symbol": "BTCUSD",  
		"publishedDate": "2025-02-03 23:32:19",  
		"publisher": "Coingape",  
		"title": "Crypto Prices Today Feb 4: BTC & Altcoins Recover Amid Pause On Trump's Tariffs",  
		"image": "https://images.financialmodelingprep.com/news/crypto-prices-today-feb-4-btc-altcoins-recover-amid-20250203.webp",  
		"site": "coingape.com",  
		"text": "Crypto prices today have shown signs of recovery as U.S. President Donald Trump's newly announced import tariffs on Canada and Mexico were paused for 30 days. Bitcoin (BTC) price regained its value, hitting a $102K high amid broader market recovery.",  
		"url": "https://coingape.com/crypto-prices-today-feb-4-btc-altcoins-recover-amid-pause-on-trumps-tariffs/"  
	}  
\]

[Forex News API](https://site.financialmodelingprep.com/developer/docs/stable/forex-news)

Stay updated with the latest forex news articles from various sources using the FMP Forex News API. Access headlines, snippets, and publication URLs for comprehensive market insights.

**Endpoint:**

https://financialmodelingprep.com/stable/news/forex-latest?*page*\=0&*limit*\=20

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

\[  
	{  
		"symbol": "XAUUSD",  
		"publishedDate": "2025-02-03 23:55:44",  
		"publisher": "FX Street",  
		"title": "United Arab Emirates Gold price today: Gold steadies, according to FXStreet data",  
		"image": "https://images.financialmodelingprep.com/news/united-arab-emirates-gold-price-today-gold-steadies-according-20250203.jpg",  
		"site": "fxstreet.com",  
		"text": "Gold prices remained broadly unchanged in United Arab Emirates on Tuesday, according to data compiled by FXStreet.",  
		"url": "https://www.fxstreet.com/news/united-arab-emirates-gold-price-today-gold-steadies-according-to-fxstreet-data-202502040455"  
	}  
\]

[Search Press Releases API](https://site.financialmodelingprep.com/developer/docs/stable/search-press-releases)

Search for company press releases with the FMP Search Press Releases API. Find specific corporate announcements and updates by entering a stock symbol or company name.

**Endpoint:**

https://financialmodelingprep.com/stable/news/press-releases?*symbols*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbols\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[  
	{  
		"symbol": "AAPL",  
		"publishedDate": "2025-01-30 16:30:00",  
		"publisher": "Business Wire",  
		"title": "Apple reports first quarter results",  
		"image": "https://images.financialmodelingprep.com/news/apple-reports-first-quarter-results-20250130.jpg",  
		"site": "businesswire.com",  
		"text": "CUPERTINO, Calif.--(BUSINESS WIRE)--Apple® today announced financial results for its fiscal 2025 first quarter ended December 28, 2024\. The Company posted quarterly revenue of $124.3 billion, up 4 percent year over year, and quarterly diluted earnings per share of $2.40, up 10 percent year over year. “Today Apple is reporting our best quarter ever, with revenue of $124.3 billion, up 4 percent from a year ago,” said Tim Cook, Apple's CEO. “We were thrilled to bring customers our best-ever lineup.",  
		"url": "https://www.businesswire.com/news/home/20250130261281/en/Apple-reports-first-quarter-results/"  
	}  
\]

[Search Stock News API](https://site.financialmodelingprep.com/developer/docs/stable/search-stock-news)

Search for stock-related news using the FMP Search Stock News API. Find specific stock news by entering a ticker symbol or company name to track the latest developments.

**Endpoint:**

[https://financialmodelingprep.com/stable/news/stock?*symbols*\=AAPL](https://financialmodelingprep.com/stable/news/stock?symbols=AAPL)

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbols\* | string | AAPL |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[

	{

		"symbol": "AAPL",

		"publishedDate": "2025-02-03 21:05:14",

		"publisher": "Zacks Investment Research",

		"title": "Apple & China Tariffs: A Closer Look",

		"image": "https://images.financialmodelingprep.com/news/apple-china-tariffs-a-closer-look-20250203.jpg",

		"site": "zacks.com",

		"text": "Tariffs have been the talk of the town over recent weeks, regularly overshadowing other important developments and causing volatility spikes.",

		"url": "https://www.zacks.com/stock/news/2408814/apple-china-tariffs-a-closer-look?cid=CS-STOCKNEWSAPI-FT-stocks\_in\_the\_news-2408814"

	}

\]

[Search Crypto News API](https://site.financialmodelingprep.com/developer/docs/stable/search-crypto-news)

Search for cryptocurrency news using the FMP Search Crypto News API. Retrieve news related to specific coins or tokens by entering their name or symbol.

**Endpoint:**

https://financialmodelingprep.com/stable/news/crypto?*symbols*\=BTCUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbols\* | string | BTCUSD |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[

	{

		"symbol": "BTCUSD",

		"publishedDate": "2025-02-03 23:32:19",

		"publisher": "Coingape",

		"title": "Crypto Prices Today Feb 4: BTC & Altcoins Recover Amid Pause On Trump's Tariffs",

		"image": "https://images.financialmodelingprep.com/news/crypto-prices-today-feb-4-btc-altcoins-recover-amid-20250203.webp",

		"site": "coingape.com",

		"text": "Crypto prices today have shown signs of recovery as U.S. President Donald Trump's newly announced import tariffs on Canada and Mexico were paused for 30 days. Bitcoin (BTC) price regained its value, hitting a $102K high amid broader market recovery.",

		"url": "https://coingape.com/crypto-prices-today-feb-4-btc-altcoins-recover-amid-pause-on-trumps-tariffs/"

	}

\]

[Search Forex News API](https://site.financialmodelingprep.com/developer/docs/stable/search-forex-news)

Search for foreign exchange news using the FMP Search Forex News API. Find targeted news on specific currency pairs by entering their symbols for focused updates.

**Endpoint:**

https://financialmodelingprep.com/stable/news/forex?*symbols*\=EURUSD

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbols\* | string | EURUSD |
| from | date | 2025-04-24 |
| to | date | 2025-07-25 |
| page | number | 0 |
| limit | number | 20 |

Response

\[

	{

		"symbol": "EURUSD",

		"publishedDate": "2025-02-03 18:43:01",

		"publisher": "FX Street",

		"title": "EUR/USD trims losses but still sheds weight",

		"image": "https://images.financialmodelingprep.com/news/eurusd-trims-losses-but-still-sheds-weight-20250203.jpg",

		"site": "fxstreet.com",

		"text": "EUR/USD dropped sharply following fresh tariff threats from US President Donald Trump, impacting the markets. However, significant declines in global risk markets eased as the Trump administration offered 30-day concessions on impending tariffs for Canada and Mexico.",

		"url": "https://www.fxstreet.com/news/eur-usd-trims-losses-but-still-sheds-weight-202502032343"

	}

\]

## **Technical Indicators**

[Simple Moving Average API](https://site.financialmodelingprep.com/developer/docs/stable/simple-moving-average)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/sma?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"sma": 231.215

	}

\]

[Exponential Moving Average API](https://site.financialmodelingprep.com/developer/docs/stable/exponential-moving-average)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/ema?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"ema": 232.8406611792779

	}

\]

[Weighted Moving Average API](https://site.financialmodelingprep.com/developer/docs/stable/weighted-moving-average)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/wma?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"wma": 233.04745454545454

	}

\]

[Double Exponential Moving Average API](https://site.financialmodelingprep.com/developer/docs/stable/double-exponential-moving-average)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/dema?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"dema": 232.10592058582725

	}

\]

[Triple Exponential Moving Average API](https://site.financialmodelingprep.com/developer/docs/stable/triple-exponential-moving-average)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/tema?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"tema": 233.66383715917516

	}

\]

[Relative Strength Index API](https://site.financialmodelingprep.com/developer/docs/stable/relative-strength-index)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/rsi?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"rsi": 47.64507340768903

	}

\]

[Standard Deviation API](https://site.financialmodelingprep.com/developer/docs/stable/standard-deviation)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/standarddeviation?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"standardDeviation": 6.139182763202282

	}

\]

[Williams API](https://site.financialmodelingprep.com/developer/docs/stable/williams)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/williams?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"williams": \-52.51824817518242

	}

\]

[Average Directional Index API](https://site.financialmodelingprep.com/developer/docs/stable/average-directional-index)

**Endpoint:**

https://financialmodelingprep.com/stable/technical-indicators/adx?*symbol*\=AAPL&*periodLength*\=10&*timeframe*\=1day

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |
| periodLength\* | number | 10 |
| timeframe\* | string | 1min,5min,15min,30min,1hour,4hour,1day |
| from | date | 2025-04-24 |
| to | date | 2025-07-24 |

Response

\[

	{

		"date": "2025-02-04 00:00:00",

		"open": 227.2,

		"high": 233.13,

		"low": 226.65,

		"close": 232.8,

		"volume": 44489128,

		"adx": 26.414065772772613

	}

\]

## **Quote**

[Stock Quote API](https://site.financialmodelingprep.com/developer/docs/stable/quote)

Access real-time stock quotes with the FMP Stock Quote API. Get up-to-the-minute prices, changes, and volume data for individual stocks.

**Endpoint:**

https://financialmodelingprep.com/stable/quote?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"name": "Apple Inc.",

		"price": 232.8,

		"changePercentage": 2.1008,

		"change": 4.79,

		"volume": 44489128,

		"dayLow": 226.65,

		"dayHigh": 233.13,

		"yearHigh": 260.1,

		"yearLow": 164.08,

		"marketCap": 3500823120000,

		"priceAvg50": 240.2278,

		"priceAvg200": 219.98755,

		"exchange": "NASDAQ",

		"open": 227.2,

		"previousClose": 228.01,

		"timestamp": 1738702801

	}

\]

[Aftermarket Trade API](https://site.financialmodelingprep.com/developer/docs/stable/aftermarket-trade)

Track real-time trading activity occurring after regular market hours with the FMP Aftermarket Trade API. Access key details such as trade prices, sizes, and timestamps for trades executed during the post-market session.

**Endpoint:**

https://financialmodelingprep.com/stable/aftermarket-trade?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"price": 232.53,

		"tradeSize": 132,

		"timestamp": 1738715334311

	}

\]

[Aftermarket Quote API](https://site.financialmodelingprep.com/developer/docs/stable/aftermarket-quote)

Access real-time aftermarket quotes for stocks with the FMP Aftermarket Quote API. Track bid and ask prices, volume, and other relevant data outside of regular trading hours.

**Endpoint:**

https://financialmodelingprep.com/stable/aftermarket-quote?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"bidSize": 1,

		"bidPrice": 232.45,

		"askSize": 3,

		"askPrice": 232.64,

		"volume": 41647042,

		"timestamp": 1738715334311

	}

\]

[Stock Price Change API](https://site.financialmodelingprep.com/developer/docs/stable/quote-change)

Track stock price fluctuations in real-time with the FMP Stock Price Change API. Monitor percentage and value changes over various time periods, including daily, weekly, monthly, and long-term.

**Endpoint:**

https://financialmodelingprep.com/stable/stock-price-change?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"1D": 2.1008,

		"5D": \-2.45946,

		"1M": \-4.33925,

		"3M": 4.86014,

		"6M": 5.88556,

		"ytd": \-4.53147,

		"1Y": 24.04092,

		"3Y": 35.04264,

		"5Y": 192.05871,

		"10Y": 678.8558,

		"max": 181279.04168

	}

\]

## **Senate**

[Latest Senate Financial Disclosures API](https://site.financialmodelingprep.com/developer/docs/stable/senate-latest)

Access the latest financial disclosures from U.S. Senate members with the FMP Latest Senate Financial Disclosures API. Track recent trades, asset ownership, and transaction details for enhanced transparency in government financial activities.

**Endpoint:**

https://financialmodelingprep.com/stable/senate-latest?*page*\=0&*limit*\=100

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 100 |

Response

\[

	{

		"symbol": "LRN",

		"disclosureDate": "2025-01-31",

		"transactionDate": "2025-01-02",

		"firstName": "Markwayne",

		"lastName": "Mullin",

		"office": "Markwayne Mullin",

		"district": "OK",

		"owner": "Self",

		"assetDescription": "Stride Inc",

		"assetType": "Stock",

		"type": "Purchase",

		"amount": "$15,001 \- $50,000",

		"comment": "",

		"link": "https://efdsearch.senate.gov/search/view/ptr/446c7588-5f97-42c0-8983-3ca975b91793/"

	}

\]

[Latest House Financial Disclosures API](https://site.financialmodelingprep.com/developer/docs/stable/house-latest)

Access real-time financial disclosures from U.S. House members with the FMP Latest House Financial Disclosures API. Track recent trades, asset ownership, and financial holdings for enhanced visibility into political figures' financial activities.

**Endpoint:**

https://financialmodelingprep.com/stable/house-latest?*page*\=0&*limit*\=100

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| page | number | 0 |
| limit | number | 100 |

Response

\[

	{

		"symbol": "$VIRTUALUSD",

		"disclosureDate": "2025-02-03",

		"transactionDate": "2025-01-03",

		"firstName": "Michael",

		"lastName": "Collins",

		"office": "Michael Collins",

		"district": "GA10",

		"owner": "",

		"assetDescription": "VIRTUALS PROTOCOL",

		"assetType": "Cryptocurrency",

		"type": "Purchase",

		"amount": "$1,001 \- $15,000",

		"capitalGainsOver200USD": "False",

		"comment": "",

		"link": "https://disclosures-clerk.house.gov/public\_disc/ptr-pdfs/2025/20026696.pdf"

	}

\]

[Senate Trading Activity API](https://site.financialmodelingprep.com/developer/docs/stable/senate-trading)

Monitor the trading activity of US Senators with the FMP Senate Trading Activity API. Access detailed information on trades made by Senators, including trade dates, assets, amounts, and potential conflicts of interest.

**Endpoint:**

https://financialmodelingprep.com/stable/senate-trades?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"disclosureDate": "2025-01-08",

		"transactionDate": "2024-12-19",

		"firstName": "Sheldon",

		"lastName": "Whitehouse",

		"office": "Sheldon Whitehouse",

		"district": "RI",

		"owner": "Self",

		"assetDescription": "Apple Inc",

		"assetType": "Stock",

		"type": "Sale (Partial)",

		"amount": "$15,001 \- $50,000",

		"capitalGainsOver200USD": "False",

		"comment": "--",

		"link": "https://efdsearch.senate.gov/search/view/ptr/70c80513-d89a-4382-afa6-d80f6c1fcbf1/"

	}

\]

[Senate Trades By Name API](https://site.financialmodelingprep.com/developer/docs/stable/senate-trading-by-name)

**Endpoint:**

https://financialmodelingprep.com/stable/senate-trades-by-name?*name*\=Jerry

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| name\* | string | Jerry |

Response

\[

	{

		"symbol": "BRK/B",

		"disclosureDate": "2025-01-18",

		"transactionDate": "2024-12-16",

		"firstName": "Jerry",

		"lastName": "Moran",

		"office": "Jerry Moran",

		"district": "KS",

		"owner": "Self",

		"assetDescription": "Berkshire Hathaway Inc",

		"assetType": "Stock",

		"type": "Purchase",

		"amount": "$1,001 \- $15,000",

		"capitalGainsOver200USD": "False",

		"comment": "",

		"link": "https://efdsearch.senate.gov/search/view/ptr/e37322e3-0829-4e3c-9faf-7a4a1a957e09/"

	}

\]

[U.S. House Trades API](https://site.financialmodelingprep.com/developer/docs/stable/house-trading)

Track the financial trades made by U.S. House members and their families with the FMP U.S. House Trades API. Access real-time information on stock sales, purchases, and other investment activities to gain insight into their financial decisions.

**Endpoint:**

https://financialmodelingprep.com/stable/house-trades?*symbol*\=AAPL

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| symbol\* | string | AAPL |

Response

\[

	{

		"symbol": "AAPL",

		"disclosureDate": "2025-01-20",

		"transactionDate": "2024-12-31",

		"firstName": "Nancy",

		"lastName": "Pelosi",

		"office": "Nancy Pelosi",

		"district": "CA11",

		"owner": "Spouse",

		"assetDescription": "Apple Inc",

		"assetType": "Stock",

		"type": "Sale",

		"amount": "$10,000,001 \- $25,000,000",

		"capitalGainsOver200USD": "False",

		"comment": "",

		"link": "https://disclosures-clerk.house.gov/public\_disc/ptr-pdfs/2025/20026590.pdf"

	}

\]

[House Trades By Name API](https://site.financialmodelingprep.com/developer/docs/stable/house-trading-by-name)

**Endpoint:**

https://financialmodelingprep.com/stable/house-trades-by-name?*name*\=James

Parameters

| Query Parameter | Type | Example |
| :---- | :---- | :---- |
| name\* | string | James |

Response

\[

	{

		"symbol": "LUV",

		"disclosureDate": "2025-01-13",

		"transactionDate": "2024-12-31",

		"firstName": "James",

		"lastName": "Comer",

		"office": "James Comer",

		"district": "KY01",

		"owner": "",

		"assetDescription": "Southwest Airlines Co",

		"assetType": "Stock",

		"type": "Sale",

		"amount": "$1,001 \- $15,000",

		"capitalGainsOver200USD": "False",

		"comment": "",

		"link": "https://disclosures-clerk.house.gov/public\_disc/ptr-pdfs/2025/20018054.pdf"

	}

\]

