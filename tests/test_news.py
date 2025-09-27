"""
Unit tests for FMP News category
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.news import NewsCategory


class TestNewsCategory:
    """Test cases for NewsCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def news_category(self, mock_client):
        """News category instance with mocked client"""
        return NewsCategory(mock_client)

    @pytest.mark.asyncio
    async def test_fmp_articles_basic(self, news_category, mock_client):
        """Test FMP articles with no parameters"""
        mock_response = [
            {
                "title": "Merck Shares Plunge 8% as Weak Guidance Overshadows Strong Revenue Growth",
                "date": "2025-02-04 09:33:00",
                "content": "<p><a href='https://financialmodelingprep.com/financial-summary/MRK'>Merck & Co (NYSE:MRK)</a> saw its stock sink over 8% in pre-market today after delivering mixed fourth-quarter results, with earnings missing expectations, revenue exceeding forecasts, and full-year guidance coming in below analyst estimates.</p>\\n<p>For Q4, the pharmaceutical giant reported adjusted earnings per share (EPS) of $1.72, falling short of the $1.81 consensus estimate. However, revenue climbed 7% year-over-year to $1...",
                "tickers": "NYSE:MRK",
                "image": "https://cdn.financialmodelingprep.com/images/fmp-1738679603793.jpg",
                "link": "https://financialmodelingprep.com/market-news/fmp-merck-shares-plunge-8-as-weak-guidance-overshadows-strong-revenue-growth",
                "author": "Davit Kirakosyan",
                "site": "Financial Modeling Prep",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.fmp_articles()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("fmp-articles", {})

    @pytest.mark.asyncio
    async def test_fmp_articles_with_params(self, news_category, mock_client):
        """Test FMP articles with pagination parameters"""
        mock_response = [{"title": "Test Article", "date": "2025-02-04 09:33:00"}]
        mock_client._make_request.return_value = mock_response

        result = await news_category.fmp_articles(page=1, limit=10)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "fmp-articles", {"page": 1, "limit": 10}
        )

    @pytest.mark.asyncio
    async def test_general_news_basic(self, news_category, mock_client):
        """Test general news with no parameters"""
        mock_response = [
            {
                "symbol": None,
                "publishedDate": "2025-02-03 23:51:37",
                "publisher": "CNBC",
                "title": "Asia tech stocks rise after Trump pauses tariffs on China and Mexico",
                "image": "https://images.financialmodelingprep.com/news/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-20250203.jpg",
                "site": "cnbc.com",
                "text": "Gains in Asian tech companies were broad-based, with stocks in Japan, South Korea and Hong Kong advancing. Semiconductor players Advantest and Lasertec led gains among Japanese tech stocks.",
                "url": "https://www.cnbc.com/2025/02/04/asia-tech-stocks-rise-after-trump-pauses-tariffs-on-china-and-mexico.html",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.general_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("news/general-latest", {})

    @pytest.mark.asyncio
    async def test_general_news_with_dates(self, news_category, mock_client):
        """Test general news with date parameters"""
        mock_response = [{"title": "Test News", "publishedDate": "2025-02-03 23:51:37"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.general_news(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/general-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_press_releases_basic(self, news_category, mock_client):
        """Test press releases with no parameters"""
        mock_response = [
            {
                "symbol": "LNW",
                "publishedDate": "2025-02-03 23:32:00",
                "publisher": "PRNewsWire",
                "title": "Rosen Law Firm Encourages Light & Wonder, Inc. Investors to Inquire About Securities Class Action Investigation - LNW",
                "image": "https://images.financialmodelingprep.com/news/rosen-law-firm-encourages-light-wonder-inc-investors-to-20250203.jpg",
                "site": "prnewswire.com",
                "text": "NEW YORK , Feb. 3, 2025 /PRNewswire/ -- Why: Rosen Law Firm, a global investor rights law firm, continues to investigate potential securities claims on behalf of shareholders of Light & Wonder, Inc. (NASDAQ: LNW) resulting from allegations that Light & Wonder may have issued materially misleading business information to the investing public. So What: If you purchased Light & Wonder securities you may be entitled to compensation without payment of any out of pocket fees or costs through a contingency fee arrangement.",
                "url": "https://www.prnewswire.com/news-releases/rosen-law-firm-encourages-light--wonder-inc-investors-to-inquire-about-securities-class-action-investigation--lnw-302366877.html",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.press_releases()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/press-releases-latest", {}
        )

    @pytest.mark.asyncio
    async def test_press_releases_with_dates(self, news_category, mock_client):
        """Test press releases with date parameters"""
        mock_response = [{"symbol": "LNW", "title": "Test Press Release"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.press_releases(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/press-releases-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_stock_news_basic(self, news_category, mock_client):
        """Test stock news with no parameters"""
        mock_response = [
            {
                "symbol": "INSG",
                "publishedDate": "2025-02-03 23:53:40",
                "publisher": "Seeking Alpha",
                "title": "Q4 Earnings Release Looms For Inseego, But Don't Expect Miracles",
                "image": "https://images.financialmodelingprep.com/news/q4-earnings-release-looms-for-inseego-but-dont-expect-20250203.jpg",
                "site": "seekingalpha.com",
                "text": "Inseego's Q3 beat was largely due to a one-time debt restructuring gain, not sustainable earnings growth, raising concerns about future performance. The sale of its telematics business for $52 million allows INSG to focus on North America, but it remains to be seen if this was wise. Despite improved margins and reduced debt, Inseego's revenue growth is insufficient, and its high stock price remains unjustifiable for new investors.",
                "url": "https://seekingalpha.com/article/4754485-inseego-stock-q4-earnings-preview-monitor-growth-margins-closely",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.stock_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("news/stock-latest", {})

    @pytest.mark.asyncio
    async def test_stock_news_with_dates(self, news_category, mock_client):
        """Test stock news with date parameters"""
        mock_response = [{"symbol": "INSG", "title": "Test Stock News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.stock_news(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/stock-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_crypto_news_basic(self, news_category, mock_client):
        """Test crypto news with no parameters"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "publishedDate": "2025-02-03 23:32:19",
                "publisher": "Coingape",
                "title": "Crypto Prices Today Feb 4: BTC & Altcoins Recover Amid Pause On Trump's Tariffs",
                "image": "https://images.financialmodelingprep.com/news/crypto-prices-today-feb-4-btc-altcoins-recover-amid-20250203.webp",
                "site": "coingape.com",
                "text": "Crypto prices today have shown signs of recovery as U.S. President Donald Trump's newly announced import tariffs on Canada and Mexico were paused for 30 days. Bitcoin (BTC) price regained its value, hitting a $102K high amid broader market recovery.",
                "url": "https://coingape.com/crypto-prices-today-feb-4-btc-altcoins-recover-amid-pause-on-trumps-tariffs/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.crypto_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("news/crypto-latest", {})

    @pytest.mark.asyncio
    async def test_crypto_news_with_dates(self, news_category, mock_client):
        """Test crypto news with date parameters"""
        mock_response = [{"symbol": "BTCUSD", "title": "Test Crypto News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.crypto_news(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/crypto-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_forex_news_basic(self, news_category, mock_client):
        """Test forex news with no parameters"""
        mock_response = [
            {
                "symbol": "XAUUSD",
                "publishedDate": "2025-02-03 23:55:44",
                "publisher": "FX Street",
                "title": "United Arab Emirates Gold price today: Gold steadies, according to FXStreet data",
                "image": "https://images.financialmodelingprep.com/news/united-arab-emirates-gold-price-today-gold-steadies-according-20250203.jpg",
                "site": "fxstreet.com",
                "text": "Gold prices remained broadly unchanged in United Arab Emirates on Tuesday, according to data compiled by FXStreet.",
                "url": "https://www.fxstreet.com/news/united-arab-emirates-gold-price-today-gold-steadies-according-to-fxstreet-data-202502040455",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.forex_news()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("news/forex-latest", {})

    @pytest.mark.asyncio
    async def test_forex_news_with_dates(self, news_category, mock_client):
        """Test forex news with date parameters"""
        mock_response = [{"symbol": "XAUUSD", "title": "Test Forex News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.forex_news(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/forex-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_search_press_releases_basic(self, news_category, mock_client):
        """Test search press releases with required parameter only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "publishedDate": "2025-01-30 16:30:00",
                "publisher": "Business Wire",
                "title": "Apple reports first quarter results",
                "image": "https://images.financialmodelingprep.com/news/apple-reports-first-quarter-results-20250130.jpg",
                "site": "businesswire.com",
                "text": 'CUPERTINO, Calif.--(BUSINESS WIRE)--Apple® today announced financial results for its fiscal 2025 first quarter ended December 28, 2024. The Company posted quarterly revenue of $124.3 billion, up 4 percent year over year, and quarterly diluted earnings per share of $2.40, up 10 percent year over year. "Today Apple is reporting our best quarter ever, with revenue of $124.3 billion, up 4 percent from a year ago," said Tim Cook, Apple\'s CEO. "We were thrilled to bring customers our best-ever lineup.',
                "url": "https://www.businesswire.com/news/home/20250130261281/en/Apple-reports-first-quarter-results/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.search_press_releases("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/press-releases", {"symbols": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_search_press_releases_with_params(self, news_category, mock_client):
        """Test search press releases with all parameters"""
        mock_response = [{"symbol": "AAPL", "title": "Test Press Release"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.search_press_releases(
            "AAPL", page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/press-releases",
            {
                "symbols": "AAPL",
                "page": 0,
                "limit": 20,
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_search_stock_news_basic(self, news_category, mock_client):
        """Test search stock news with required parameter only"""
        mock_response = [
            {
                "symbol": "AAPL",
                "publishedDate": "2025-02-03 21:05:14",
                "publisher": "Zacks Investment Research",
                "title": "Apple & China Tariffs: A Closer Look",
                "image": "https://images.financialmodelingprep.com/news/apple-china-tariffs-a-closer-look-20250203.jpg",
                "site": "zacks.com",
                "text": "Tariffs have been the talk of the town over recent weeks, regularly overshadowing other important developments and causing volatility spikes.",
                "url": "https://www.zacks.com/stock/news/2408814/apple-china-tariffs-a-closer-look?cid=CS-STOCKNEWSAPI-FT-stocks_in_the_news-2408814",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.search_stock_news("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/stock", {"symbols": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_search_stock_news_with_params(self, news_category, mock_client):
        """Test search stock news with all parameters"""
        mock_response = [{"symbol": "AAPL", "title": "Test Stock News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.search_stock_news(
            "AAPL", page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/stock",
            {
                "symbols": "AAPL",
                "page": 0,
                "limit": 20,
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_search_crypto_news_basic(self, news_category, mock_client):
        """Test search crypto news with required parameter only"""
        mock_response = [
            {
                "symbol": "BTCUSD",
                "publishedDate": "2025-02-03 23:32:19",
                "publisher": "Coingape",
                "title": "Crypto Prices Today Feb 4: BTC & Altcoins Recover Amid Pause On Trump's Tariffs",
                "image": "https://images.financialmodelingprep.com/news/crypto-prices-today-feb-4-btc-altcoins-recover-amid-20250203.webp",
                "site": "coingape.com",
                "text": "Crypto prices today have shown signs of recovery as U.S. President Donald Trump's newly announced import tariffs on Canada and Mexico were paused for 30 days. Bitcoin (BTC) price regained its value, hitting a $102K high amid broader market recovery.",
                "url": "https://coingape.com/crypto-prices-today-feb-4-btc-altcoins-recover-amid-pause-on-trumps-tariffs/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.search_crypto_news("BTCUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/crypto", {"symbols": "BTCUSD"}
        )

    @pytest.mark.asyncio
    async def test_search_crypto_news_with_params(self, news_category, mock_client):
        """Test search crypto news with all parameters"""
        mock_response = [{"symbol": "BTCUSD", "title": "Test Crypto News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.search_crypto_news(
            "BTCUSD", page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/crypto",
            {
                "symbols": "BTCUSD",
                "page": 0,
                "limit": 20,
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_search_forex_news_basic(self, news_category, mock_client):
        """Test search forex news with required parameter only"""
        mock_response = [
            {
                "symbol": "EURUSD",
                "publishedDate": "2025-02-03 18:43:01",
                "publisher": "FX Street",
                "title": "EUR/USD trims losses but still sheds weight",
                "image": "https://images.financialmodelingprep.com/news/eurusd-trims-losses-but-still-sheds-weight-20250203.jpg",
                "site": "fxstreet.com",
                "text": "EUR/USD dropped sharply following fresh tariff threats from US President Donald Trump, impacting the markets. However, significant declines in global risk markets eased as the Trump administration offered 30-day concessions on impending tariffs for Canada and Mexico.",
                "url": "https://www.fxstreet.com/news/eur-usd-trims-losses-but-still-sheds-weight-202502032343",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.search_forex_news("EURUSD")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/forex", {"symbols": "EURUSD"}
        )

    @pytest.mark.asyncio
    async def test_search_forex_news_with_params(self, news_category, mock_client):
        """Test search forex news with all parameters"""
        mock_response = [{"symbol": "EURUSD", "title": "Test Forex News"}]
        mock_client._make_request.return_value = mock_response

        from_date = date(2025, 2, 1)
        to_date = date(2025, 2, 28)

        result = await news_category.search_forex_news(
            "EURUSD", page=0, limit=20, from_date=from_date, to_date=to_date
        )

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "news/forex",
            {
                "symbols": "EURUSD",
                "page": 0,
                "limit": 20,
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )

    @pytest.mark.asyncio
    async def test_empty_response_handling(self, news_category, mock_client):
        """Test handling of empty responses"""
        mock_client._make_request.return_value = []

        result = await news_category.fmp_articles()

        assert result == []
        mock_client._make_request.assert_called_once_with("fmp-articles", {})

    @pytest.mark.asyncio
    async def test_large_response_handling(self, news_category, mock_client):
        """Test handling of large responses"""
        # Create a large mock response with multiple articles
        large_response = [
            {
                "title": f"Article {i:03d}",
                "date": "2025-02-04 09:33:00",
                "content": f"Content for article {i}",
                "tickers": "NYSE:TEST",
                "author": "Test Author",
                "site": "Financial Modeling Prep",
            }
            for i in range(1, 101)  # 100 articles
        ]
        mock_client._make_request.return_value = large_response

        result = await news_category.fmp_articles(page=0, limit=100)

        assert len(result) == 100
        assert result[0]["title"] == "Article 001"
        assert result[99]["title"] == "Article 100"
        mock_client._make_request.assert_called_once_with(
            "fmp-articles", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, news_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
            {
                "title": "Test Article",
                "date": "2025-02-04 09:33:00",
                "content": "Test content",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await news_category.fmp_articles()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("fmp-articles", {})

    @pytest.mark.asyncio
    async def test_different_symbols(self, news_category, mock_client):
        """Test news functionality with different symbols"""
        mock_response = [{"symbol": "AAPL", "title": "Test News"}]
        mock_client._make_request.return_value = mock_response

        # Test with AAPL
        result = await news_category.search_stock_news("AAPL")
        assert result == mock_response
        mock_client._make_request.assert_called_with("news/stock", {"symbols": "AAPL"})

        # Test with MSFT
        result = await news_category.search_stock_news("MSFT")
        assert result == mock_response
        mock_client._make_request.assert_called_with("news/stock", {"symbols": "MSFT"})

        # Test with GOOGL
        result = await news_category.search_stock_news("GOOGL")
        assert result == mock_response
        mock_client._make_request.assert_called_with("news/stock", {"symbols": "GOOGL"})

    @pytest.mark.asyncio
    async def test_different_crypto_symbols(self, news_category, mock_client):
        """Test crypto news functionality with different symbols"""
        mock_response = [{"symbol": "BTCUSD", "title": "Test Crypto News"}]
        mock_client._make_request.return_value = mock_response

        # Test with BTCUSD
        result = await news_category.search_crypto_news("BTCUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/crypto", {"symbols": "BTCUSD"}
        )

        # Test with ETHUSD
        result = await news_category.search_crypto_news("ETHUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/crypto", {"symbols": "ETHUSD"}
        )

        # Test with ADAUSD
        result = await news_category.search_crypto_news("ADAUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/crypto", {"symbols": "ADAUSD"}
        )

    @pytest.mark.asyncio
    async def test_different_forex_symbols(self, news_category, mock_client):
        """Test forex news functionality with different symbols"""
        mock_response = [{"symbol": "EURUSD", "title": "Test Forex News"}]
        mock_client._make_request.return_value = mock_response

        # Test with EURUSD
        result = await news_category.search_forex_news("EURUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/forex", {"symbols": "EURUSD"}
        )

        # Test with GBPUSD
        result = await news_category.search_forex_news("GBPUSD")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/forex", {"symbols": "GBPUSD"}
        )

        # Test with USDJPY
        result = await news_category.search_forex_news("USDJPY")
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/forex", {"symbols": "USDJPY"}
        )

    @pytest.mark.asyncio
    async def test_date_edge_cases(self, news_category, mock_client):
        """Test date handling edge cases"""
        mock_response = [{"title": "Test News", "publishedDate": "2025-02-03 23:51:37"}]
        mock_client._make_request.return_value = mock_response

        # Test with leap year date
        leap_date = date(2024, 2, 29)
        result = await news_category.general_news(from_date=leap_date)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest", {"from": "2024-02-29"}
        )

        # Test with year boundary
        year_boundary = date(2024, 12, 31)
        result = await news_category.general_news(to_date=year_boundary)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest", {"to": "2024-12-31"}
        )

        # Test with beginning of year
        year_beginning = date(2024, 1, 1)
        result = await news_category.general_news(from_date=year_beginning)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest", {"from": "2024-01-01"}
        )

    @pytest.mark.asyncio
    async def test_parameter_combinations(self, news_category, mock_client):
        """Test various parameter combinations"""
        mock_response = [{"title": "Test News", "publishedDate": "2025-02-03 23:51:37"}]
        mock_client._make_request.return_value = mock_response

        # Test with only page
        result = await news_category.general_news(page=0)
        assert result == mock_response
        mock_client._make_request.assert_called_with("news/general-latest", {"page": 0})

        # Test with page and limit
        result = await news_category.general_news(page=0, limit=20)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest", {"page": 0, "limit": 20}
        )

        # Test with page, limit, and from_date
        from_date = date(2025, 2, 1)
        result = await news_category.general_news(page=0, limit=20, from_date=from_date)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest", {"page": 0, "limit": 20, "from": "2025-02-01"}
        )

        # Test with all parameters
        to_date = date(2025, 2, 28)
        result = await news_category.general_news(
            page=0, limit=20, from_date=from_date, to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/general-latest",
            {"page": 0, "limit": 20, "from": "2025-02-01", "to": "2025-02-28"},
        )

    @pytest.mark.asyncio
    async def test_search_parameter_combinations(self, news_category, mock_client):
        """Test search methods with different parameter combinations"""
        mock_response = [{"symbol": "AAPL", "title": "Test News"}]
        mock_client._make_request.return_value = mock_response

        # Test with only symbols
        result = await news_category.search_stock_news("AAPL")
        assert result == mock_response
        mock_client._make_request.assert_called_with("news/stock", {"symbols": "AAPL"})

        # Test with symbols and page
        result = await news_category.search_stock_news("AAPL", page=0)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/stock", {"symbols": "AAPL", "page": 0}
        )

        # Test with symbols, page, and limit
        result = await news_category.search_stock_news("AAPL", page=0, limit=20)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/stock", {"symbols": "AAPL", "page": 0, "limit": 20}
        )

        # Test with symbols, page, limit, and from_date
        from_date = date(2025, 2, 1)
        result = await news_category.search_stock_news(
            "AAPL", page=0, limit=20, from_date=from_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/stock",
            {"symbols": "AAPL", "page": 0, "limit": 20, "from": "2025-02-01"},
        )

        # Test with all parameters
        to_date = date(2025, 2, 28)
        result = await news_category.search_stock_news(
            "AAPL", page=0, limit=20, from_date=from_date, to_date=to_date
        )
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "news/stock",
            {
                "symbols": "AAPL",
                "page": 0,
                "limit": 20,
                "from": "2025-02-01",
                "to": "2025-02-28",
            },
        )
