"""
Base client for Financial Modeling Prep API

This module provides the core functionality for making HTTP requests to the FMP API,
including session management, rate limiting, and error handling.
"""

import asyncio
import logging
from typing import Any
from urllib.parse import urlencode

import aiohttp

logger = logging.getLogger(__name__)


class FMPError(Exception):
    """Base exception for FMP API errors"""

    pass


class FMPAuthenticationError(FMPError):
    """Raised when authentication fails (invalid API key)"""

    pass


class FMPRateLimitError(FMPError):
    """Raised when rate limit is exceeded"""

    pass


class FMPResponseError(FMPError):
    """Raised when the API returns an error response"""

    pass


class FMPBaseClient:
    """Base client for FMP API with common functionality"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://financialmodelingprep.com/stable",
        timeout: int = 60,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_concurrent_requests: int = 10,
    ):
        """
        Initialize the FMP base client

        Args:
            api_key: FMP API key
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Base delay between retries (exponential backoff)
            max_concurrent_requests: Maximum concurrent requests allowed
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_concurrent_requests = max_concurrent_requests

        # Session management
        self._session: aiohttp.ClientSession | None = None
        self._session_owner = True

        # Rate limiting
        self._request_semaphore = asyncio.Semaphore(max_concurrent_requests)

        # Logging
        logger.info(f"FMP client initialized with base URL: {self.base_url}")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def start(self):
        """Start the client session if not already started"""
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
            self._session_owner = True
            logger.debug("FMP client session started")

    async def close(self):
        """Close the client session"""
        if self._session_owner and self._session:
            await self._session.close()
            self._session = None
            logger.debug("FMP client session closed")

    async def _make_request(
        self, endpoint: str, params: dict[str, Any] | None = None, method: str = "GET"
    ) -> Any:
        """
        Make an HTTP request to the FMP API

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            method: HTTP method (default: GET)

        Returns:
            API response data

        Raises:
            FMPError: For various API errors
        """
        if self._session is None:
            raise RuntimeError(
                "Client session not initialized. Use async context manager or call start()"
            )

        # Prepare parameters
        if params is None:
            params = {}

        # Always include API key
        params["apikey"] = self.api_key

        # Build full URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Prepare headers
        headers = {
            "User-Agent": "aiofmp-Client/1.0.0",
            "Accept": "application/json",
        }

        async with self._request_semaphore:
            for attempt in range(self.max_retries + 1):
                try:
                    if method.upper() == "GET":
                        async with self._session.get(
                            url, params=params, headers=headers
                        ) as response:
                            return await self._handle_response(response)
                    elif method.upper() == "POST":
                        async with self._session.post(
                            url, json=params, headers=headers
                        ) as response:
                            return await self._handle_response(response)
                    else:
                        raise ValueError(f"Unsupported HTTP method: {method}")

                except asyncio.TimeoutError as e:
                    if attempt == self.max_retries:
                        raise FMPError(
                            f"Request timeout after {self.max_retries + 1} attempts"
                        ) from e
                    logger.warning(
                        f"Request timeout, attempt {attempt + 1}/{self.max_retries + 1}"
                    )

                except aiohttp.ClientError as e:
                    if attempt == self.max_retries:
                        raise FMPError(f"HTTP client error: {e}") from e
                    logger.warning(
                        f"HTTP client error, attempt {attempt + 1}/{self.max_retries + 1}: {e}"
                    )

                except Exception as e:
                    if attempt == self.max_retries:
                        raise e
                    logger.warning(
                        f"Request failed, attempt {attempt + 1}/{self.max_retries + 1}: {e}"
                    )

                # Wait before retry (except on last attempt)
                if attempt < self.max_retries:
                    await asyncio.sleep(
                        self.retry_delay * (2**attempt)
                    )  # Exponential backoff

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Any:
        """
        Handle the HTTP response from the API

        Args:
            response: aiohttp response object

        Returns:
            Parsed response data

        Raises:
            FMPError: For various response errors
        """
        if response.status == 200:
            try:
                data = await response.json()

                # Check if response contains error information
                if isinstance(data, dict) and "Error Message" in data:
                    raise FMPResponseError(f"API Error: {data['Error Message']}")

                return data

            except Exception as e:
                raise FMPError(f"Failed to parse response: {e}") from e

        elif response.status == 401:
            raise FMPAuthenticationError("Invalid API key or authentication failed")
        elif response.status == 429:
            raise FMPRateLimitError("Rate limit exceeded")
        elif response.status >= 500:
            raise FMPError(f"Server error: {response.status}")
        else:
            raise FMPError(f"HTTP {response.status}: {response.reason}")

    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """
        Build a complete URL with query parameters

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Complete URL with parameters
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            # Filter out None values
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                url += "?" + urlencode(filtered_params)
        return url
