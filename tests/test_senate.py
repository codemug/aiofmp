"""
Unit tests for FMP Senate category
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.base import FMPBaseClient
from aiofmp.senate import SenateCategory


class TestSenateCategory:
    """Test cases for SenateCategory"""

    @pytest.fixture
    def mock_client(self):
        """Mock FMP base client"""
        client = MagicMock(spec=FMPBaseClient)
        client._make_request = AsyncMock()
        return client

    @pytest.fixture
    def senate_category(self, mock_client):
        """Senate category instance with mocked client"""
        return SenateCategory(mock_client)

    @pytest.mark.asyncio
    async def test_latest_senate_disclosures_basic(self, senate_category, mock_client):
        """Test latest Senate disclosures with no parameters"""
        mock_response = [
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
                "amount": "$15,001 - $50,000",
                "comment": "",
                "link": "https://efdsearch.senate.gov/search/view/ptr/446c7588-5f97-42c0-8983-3ca975b91793/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("senate-latest", {})

    @pytest.mark.asyncio
    async def test_latest_senate_disclosures_with_pagination(
        self, senate_category, mock_client
    ):
        """Test latest Senate disclosures with pagination parameters"""
        mock_response = [
            {"symbol": "LRN", "firstName": "Markwayne", "lastName": "Mullin"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures(page=1, limit=50)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-latest", {"page": 1, "limit": 50}
        )

    @pytest.mark.asyncio
    async def test_latest_senate_disclosures_page_only(
        self, senate_category, mock_client
    ):
        """Test latest Senate disclosures with page parameter only"""
        mock_response = [
            {"symbol": "LRN", "firstName": "Markwayne", "lastName": "Mullin"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures(page=2)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("senate-latest", {"page": 2})

    @pytest.mark.asyncio
    async def test_latest_senate_disclosures_limit_only(
        self, senate_category, mock_client
    ):
        """Test latest Senate disclosures with limit parameter only"""
        mock_response = [
            {"symbol": "LRN", "firstName": "Markwayne", "lastName": "Mullin"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures(limit=25)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-latest", {"limit": 25}
        )

    @pytest.mark.asyncio
    async def test_latest_house_disclosures_basic(self, senate_category, mock_client):
        """Test latest House disclosures with no parameters"""
        mock_response = [
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
                "amount": "$1,001 - $15,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20026696.pdf",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_house_disclosures()

        assert result == mock_response
        mock_client._make_request.assert_called_once_with("house-latest", {})

    @pytest.mark.asyncio
    async def test_latest_house_disclosures_with_pagination(
        self, senate_category, mock_client
    ):
        """Test latest House disclosures with pagination parameters"""
        mock_response = [
            {"symbol": "$VIRTUALUSD", "firstName": "Michael", "lastName": "Collins"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_house_disclosures(page=0, limit=75)

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "house-latest", {"page": 0, "limit": 75}
        )

    @pytest.mark.asyncio
    async def test_senate_trading_activity_basic(self, senate_category, mock_client):
        """Test Senate trading activity with required symbol parameter"""
        mock_response = [
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
                "amount": "$15,001 - $50,000",
                "capitalGainsOver200USD": "False",
                "comment": "--",
                "link": "https://efdsearch.senate.gov/search/view/ptr/70c80513-d89a-4382-afa6-d80f6c1fcbf1/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.senate_trading_activity("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-trades", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_senate_trading_activity_different_symbol(
        self, senate_category, mock_client
    ):
        """Test Senate trading activity with different symbol"""
        mock_response = [{"symbol": "MSFT", "firstName": "John", "lastName": "Doe"}]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.senate_trading_activity("MSFT")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-trades", {"symbol": "MSFT"}
        )

    @pytest.mark.asyncio
    async def test_senate_trading_activity_empty(self, senate_category, mock_client):
        """Test Senate trading activity with empty response"""
        mock_client._make_request.return_value = []

        result = await senate_category.senate_trading_activity("UNKNOWN")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "senate-trades", {"symbol": "UNKNOWN"}
        )

    @pytest.mark.asyncio
    async def test_senate_trades_by_name_basic(self, senate_category, mock_client):
        """Test Senate trades by name with required name parameter"""
        mock_response = [
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
                "amount": "$1,001 - $15,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": "https://efdsearch.senate.gov/search/view/ptr/e37322e3-0829-4e3c-9faf-7a4a1a957e09/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.senate_trades_by_name("Jerry")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-trades-by-name", {"name": "Jerry"}
        )

    @pytest.mark.asyncio
    async def test_senate_trades_by_name_different_name(
        self, senate_category, mock_client
    ):
        """Test Senate trades by name with different name"""
        mock_response = [{"symbol": "TSLA", "firstName": "Jane", "lastName": "Smith"}]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.senate_trades_by_name("Jane")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "senate-trades-by-name", {"name": "Jane"}
        )

    @pytest.mark.asyncio
    async def test_senate_trades_by_name_empty(self, senate_category, mock_client):
        """Test Senate trades by name with empty response"""
        mock_client._make_request.return_value = []

        result = await senate_category.senate_trades_by_name("Unknown")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "senate-trades-by-name", {"name": "Unknown"}
        )

    @pytest.mark.asyncio
    async def test_house_trading_activity_basic(self, senate_category, mock_client):
        """Test House trading activity with required symbol parameter"""
        mock_response = [
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
                "amount": "$10,000,001 - $25,000,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20026590.pdf",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.house_trading_activity("AAPL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "house-trades", {"symbol": "AAPL"}
        )

    @pytest.mark.asyncio
    async def test_house_trading_activity_different_symbol(
        self, senate_category, mock_client
    ):
        """Test House trading activity with different symbol"""
        mock_response = [{"symbol": "GOOGL", "firstName": "John", "lastName": "Doe"}]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.house_trading_activity("GOOGL")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "house-trades", {"symbol": "GOOGL"}
        )

    @pytest.mark.asyncio
    async def test_house_trading_activity_empty(self, senate_category, mock_client):
        """Test House trading activity with empty response"""
        mock_client._make_request.return_value = []

        result = await senate_category.house_trading_activity("UNKNOWN")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "house-trades", {"symbol": "UNKNOWN"}
        )

    @pytest.mark.asyncio
    async def test_house_trades_by_name_basic(self, senate_category, mock_client):
        """Test House trades by name with required name parameter"""
        mock_response = [
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
                "amount": "$1,001 - $15,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20018054.pdf",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.house_trades_by_name("James")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "house-trades-by-name", {"name": "James"}
        )

    @pytest.mark.asyncio
    async def test_house_trades_by_name_different_name(
        self, senate_category, mock_client
    ):
        """Test House trades by name with different name"""
        mock_response = [
            {"symbol": "NVDA", "firstName": "Sarah", "lastName": "Johnson"}
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.house_trades_by_name("Sarah")

        assert result == mock_response
        mock_client._make_request.assert_called_once_with(
            "house-trades-by-name", {"name": "Sarah"}
        )

    @pytest.mark.asyncio
    async def test_house_trades_by_name_empty(self, senate_category, mock_client):
        """Test House trades by name with empty response"""
        mock_client._make_request.return_value = []

        result = await senate_category.house_trades_by_name("Unknown")

        assert result == []
        mock_client._make_request.assert_called_once_with(
            "house-trades-by-name", {"name": "Unknown"}
        )

    @pytest.mark.asyncio
    async def test_large_senate_disclosures_response(
        self, senate_category, mock_client
    ):
        """Test handling of large Senate disclosures responses"""
        # Create a large mock response with multiple disclosures
        large_response = [
            {
                "symbol": f"SYMBOL{i}",
                "disclosureDate": "2025-01-31",
                "transactionDate": "2025-01-02",
                "firstName": f"FirstName{i}",
                "lastName": f"LastName{i}",
                "office": f"Office{i}",
                "district": f"District{i}",
                "owner": "Self",
                "assetDescription": f"Asset{i}",
                "assetType": "Stock",
                "type": "Purchase",
                "amount": "$15,001 - $50,000",
                "comment": "",
                "link": f"https://example.com/link{i}",
            }
            for i in range(100)  # 100 disclosures
        ]
        mock_client._make_request.return_value = large_response

        result = await senate_category.latest_senate_disclosures(page=0, limit=100)

        assert len(result) == 100
        assert result[0]["symbol"] == "SYMBOL0"
        assert result[99]["symbol"] == "SYMBOL99"
        assert result[0]["firstName"] == "FirstName0"
        assert result[99]["firstName"] == "FirstName99"
        mock_client._make_request.assert_called_once_with(
            "senate-latest", {"page": 0, "limit": 100}
        )

    @pytest.mark.asyncio
    async def test_large_house_disclosures_response(self, senate_category, mock_client):
        """Test handling of large House disclosures responses"""
        # Create a large mock response with multiple disclosures
        large_response = [
            {
                "symbol": f"SYMBOL{i}",
                "disclosureDate": "2025-02-03",
                "transactionDate": "2025-01-03",
                "firstName": f"FirstName{i}",
                "lastName": f"LastName{i}",
                "office": f"Office{i}",
                "district": f"District{i}",
                "owner": "Self",
                "assetDescription": f"Asset{i}",
                "assetType": "Stock",
                "type": "Purchase",
                "amount": "$1,001 - $15,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": f"https://example.com/link{i}",
            }
            for i in range(75)  # 75 disclosures
        ]
        mock_client._make_request.return_value = large_response

        result = await senate_category.latest_house_disclosures(page=1, limit=75)

        assert len(result) == 75
        assert result[0]["symbol"] == "SYMBOL0"
        assert result[74]["symbol"] == "SYMBOL74"
        assert result[0]["firstName"] == "FirstName0"
        assert result[74]["firstName"] == "FirstName74"
        mock_client._make_request.assert_called_once_with(
            "house-latest", {"page": 1, "limit": 75}
        )

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, senate_category, mock_client):
        """Test that response structure is preserved"""
        mock_response = [
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
                "amount": "$15,001 - $50,000",
                "comment": "",
                "link": "https://efdsearch.senate.gov/search/view/ptr/446c7588-5f97-42c0-8983-3ca975b91793/",
                "extraField": "should be preserved",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures()

        assert result == mock_response
        assert result[0]["extraField"] == "should be preserved"
        mock_client._make_request.assert_called_once_with("senate-latest", {})

    @pytest.mark.asyncio
    async def test_different_symbols_consistency(self, senate_category, mock_client):
        """Test that trading activity methods work consistently with different symbols"""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "BRK.A", "BRK.B"]

        for symbol in symbols:
            # Test Senate trading activity
            mock_senate = [{"symbol": symbol, "firstName": "John", "lastName": "Doe"}]
            mock_client._make_request.return_value = mock_senate
            result = await senate_category.senate_trading_activity(symbol)
            assert result[0]["symbol"] == symbol
            mock_client._make_request.assert_called_with(
                "senate-trades", {"symbol": symbol}
            )

            # Test House trading activity
            mock_house = [{"symbol": symbol, "firstName": "Jane", "lastName": "Smith"}]
            mock_client._make_request.return_value = mock_house
            result = await senate_category.house_trading_activity(symbol)
            assert result[0]["symbol"] == symbol
            mock_client._make_request.assert_called_with(
                "house-trades", {"symbol": symbol}
            )

    @pytest.mark.asyncio
    async def test_different_names_consistency(self, senate_category, mock_client):
        """Test that name-based search methods work consistently with different names"""
        names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert"]

        for name in names:
            # Test Senate trades by name
            mock_senate = [{"symbol": "AAPL", "firstName": name, "lastName": "Doe"}]
            mock_client._make_request.return_value = mock_senate
            result = await senate_category.senate_trades_by_name(name)
            assert result[0]["firstName"] == name
            mock_client._make_request.assert_called_with(
                "senate-trades-by-name", {"name": name}
            )

            # Test House trades by name
            mock_house = [{"symbol": "MSFT", "firstName": name, "lastName": "Smith"}]
            mock_client._make_request.return_value = mock_house
            result = await senate_category.house_trades_by_name(name)
            assert result[0]["firstName"] == name
            mock_client._make_request.assert_called_with(
                "house-trades-by-name", {"name": name}
            )

    @pytest.mark.asyncio
    async def test_pagination_edge_cases(self, senate_category, mock_client):
        """Test pagination edge cases"""
        mock_response = [
            {"symbol": "LRN", "firstName": "Markwayne", "lastName": "Mullin"}
        ]
        mock_client._make_request.return_value = mock_response

        # Test with page 0
        result = await senate_category.latest_senate_disclosures(page=0, limit=100)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "senate-latest", {"page": 0, "limit": 100}
        )

        # Test with large page number
        result = await senate_category.latest_senate_disclosures(page=999, limit=50)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "senate-latest", {"page": 999, "limit": 50}
        )

        # Test with large limit
        result = await senate_category.latest_senate_disclosures(page=1, limit=1000)
        assert result == mock_response
        mock_client._make_request.assert_called_with(
            "senate-latest", {"page": 1, "limit": 1000}
        )

    @pytest.mark.asyncio
    async def test_method_consistency(self, senate_category, mock_client):
        """Test that all methods follow the same parameter pattern"""
        methods = [
            ("latest_senate_disclosures", "senate-latest"),
            ("latest_house_disclosures", "house-latest"),
            ("senate_trading_activity", "senate-trades"),
            ("senate_trades_by_name", "senate-trades-by-name"),
            ("house_trading_activity", "house-trades"),
            ("house_trades_by_name", "house-trades-by-name"),
        ]

        for method_name, endpoint in methods:
            method = getattr(senate_category, method_name)
            mock_response = [{"test": "data"}]
            mock_client._make_request.return_value = mock_response

            if "disclosures" in method_name:
                # Methods with optional pagination parameters
                result = await method(page=0, limit=100)
                assert result == mock_response
                mock_client._make_request.assert_called_with(
                    endpoint, {"page": 0, "limit": 100}
                )
            elif "activity" in method_name or "trades" in method_name:
                # Methods with required symbol/name parameters
                if "senate" in method_name and "name" in method_name:
                    result = await method("Jerry")
                    assert result == mock_response
                    mock_client._make_request.assert_called_with(
                        endpoint, {"name": "Jerry"}
                    )
                elif "house" in method_name and "name" in method_name:
                    result = await method("James")
                    assert result == mock_response
                    mock_client._make_request.assert_called_with(
                        endpoint, {"name": "James"}
                    )
                else:
                    result = await method("AAPL")
                    assert result == mock_response
                    mock_client._make_request.assert_called_with(
                        endpoint, {"symbol": "AAPL"}
                    )

    @pytest.mark.asyncio
    async def test_senate_disclosures_response_validation(
        self, senate_category, mock_client
    ):
        """Test Senate disclosures response validation"""
        mock_response = [
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
                "amount": "$15,001 - $50,000",
                "comment": "",
                "link": "https://efdsearch.senate.gov/search/view/ptr/446c7588-5f97-42c0-8983-3ca975b91793/",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_senate_disclosures()

        assert len(result) == 1
        assert result[0]["symbol"] == "LRN"
        assert result[0]["disclosureDate"] == "2025-01-31"
        assert result[0]["transactionDate"] == "2025-01-02"
        assert result[0]["firstName"] == "Markwayne"
        assert result[0]["lastName"] == "Mullin"
        assert result[0]["office"] == "Markwayne Mullin"
        assert result[0]["district"] == "OK"
        assert result[0]["owner"] == "Self"
        assert result[0]["assetDescription"] == "Stride Inc"
        assert result[0]["assetType"] == "Stock"
        assert result[0]["type"] == "Purchase"
        assert result[0]["amount"] == "$15,001 - $50,000"
        assert result[0]["comment"] == ""
        assert (
            result[0]["link"]
            == "https://efdsearch.senate.gov/search/view/ptr/446c7588-5f97-42c0-8983-3ca975b91793/"
        )
        mock_client._make_request.assert_called_once_with("senate-latest", {})

    @pytest.mark.asyncio
    async def test_house_disclosures_response_validation(
        self, senate_category, mock_client
    ):
        """Test House disclosures response validation"""
        mock_response = [
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
                "amount": "$1,001 - $15,000",
                "capitalGainsOver200USD": "False",
                "comment": "",
                "link": "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20026696.pdf",
            }
        ]
        mock_client._make_request.return_value = mock_response

        result = await senate_category.latest_house_disclosures()

        assert len(result) == 1
        assert result[0]["symbol"] == "$VIRTUALUSD"
        assert result[0]["disclosureDate"] == "2025-02-03"
        assert result[0]["transactionDate"] == "2025-01-03"
        assert result[0]["firstName"] == "Michael"
        assert result[0]["lastName"] == "Collins"
        assert result[0]["office"] == "Michael Collins"
        assert result[0]["district"] == "GA10"
        assert result[0]["owner"] == ""
        assert result[0]["assetDescription"] == "VIRTUALS PROTOCOL"
        assert result[0]["assetType"] == "Cryptocurrency"
        assert result[0]["type"] == "Purchase"
        assert result[0]["amount"] == "$1,001 - $15,000"
        assert result[0]["capitalGainsOver200USD"] == "False"
        assert result[0]["comment"] == ""
        assert (
            result[0]["link"]
            == "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2025/20026696.pdf"
        )
        mock_client._make_request.assert_called_once_with("house-latest", {})
