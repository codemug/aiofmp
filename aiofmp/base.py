"""
Base client for Financial Modeling Prep API

This module provides the core functionality for making HTTP requests to the FMP API,
including session management, rate limiting, and error handling.
"""

import asyncio
import contextvars
import logging
import time
from collections.abc import Callable
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


class FMPBudgetError(FMPError):
    """Raised when the harvester's monthly hard bandwidth cap is exceeded."""

    pass


class FMPServerError(FMPError):
    """Raised when the API returns a 5xx server error response."""

    pass


class FMPPaywallError(FMPError):
    """Raised when the API returns HTTP 402 Payment Required.

    Signals that the endpoint or specific resource (symbol, period, region) is
    not included in the caller's plan. Permanent for the life of the plan —
    callers should NOT retry and should treat it as "this endpoint is unavailable
    until the plan is upgraded".
    """

    pass


current_harvest_category: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_harvest_category", default=None
)


class _SlidingWindowRateLimiter:
    """Paces requests so no more than ``max_per_minute`` go out per rolling minute.

    Uses a deterministic interval (``60 / max_per_minute``) rather than a token
    bucket: each ``acquire()`` returns at or after the next slot. This avoids
    bursts and makes the per-minute cap a hard ceiling regardless of concurrency.
    """

    def __init__(self, max_per_minute: int) -> None:
        if max_per_minute <= 0:
            raise ValueError(f"max_per_minute must be positive, got {max_per_minute}")
        self._interval = 60.0 / max_per_minute
        self._next_slot = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_slot - now)
            # Schedule the next slot relative to whichever is later: the previous
            # slot we reserved or right now. Prevents the queue from "owing time"
            # if there have been long idle periods.
            self._next_slot = max(now, self._next_slot) + self._interval
        if wait > 0:
            await asyncio.sleep(wait)


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
        requests_per_minute: int | None = None,
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
            requests_per_minute: Optional plan-level cap on requests per rolling
                minute. When set, requests are paced via a sliding-window limiter
                so the per-minute rate stays below the cap regardless of
                concurrency. Default ``None`` disables pacing (server-side 429s
                are the only ceiling).
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
        self._rate_limiter: _SlidingWindowRateLimiter | None = (
            _SlidingWindowRateLimiter(requests_per_minute)
            if requests_per_minute is not None
            else None
        )

        # Bandwidth callback
        self.on_response_size: Callable[[str | None, int], None] | None = None

        # Logging
        logger.info(f"FMP client initialized with base URL: {self.base_url}")
        if self._rate_limiter is not None:
            logger.info(
                "Rate limiter active: %d requests/minute (%.0fms between requests)",
                requests_per_minute,
                60_000 / requests_per_minute,
            )

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
                # Plan-level rate pacing happens INSIDE the retry loop so that
                # a retried request also waits for its slot.
                if self._rate_limiter is not None:
                    await self._rate_limiter.acquire()
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

                # Wait before retry (except on last attempt).
                # Only TimeoutError and aiohttp.ClientError reach here;
                # FMP* exceptions (auth, paywall, not-found, response/parse,
                # rate-limit, server-error, budget) propagate immediately so
                # callers (including the harvester's _run_cycle_with_retry)
                # can apply the right per-exception policy.
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
                raw = await response.read()
                byte_count = len(raw)
                cb = self.on_response_size
                if cb is not None:
                    try:
                        cb(current_harvest_category.get(), byte_count)
                    except Exception:
                        logger.exception("on_response_size callback raised; ignoring")

                import json  # local import keeps top of file unchanged

                # Some FMP endpoints return status 200 with an empty or
                # whitespace-only body when the resource isn't included in
                # the caller's plan (instead of a clean 402). Treat those as
                # "no data" silently so per-item loops don't trip on a JSON
                # decode error.
                data = json.loads(raw) if raw.strip() else None

                if isinstance(data, dict) and "Error Message" in data:
                    raise FMPResponseError(f"API Error: {data['Error Message']}")
                return data
            except FMPError:
                raise
            except Exception as e:
                raise FMPError(f"Failed to parse response: {e}") from e

        elif response.status == 401:
            raise FMPAuthenticationError("Invalid API key or authentication failed")
        elif response.status == 402:
            raise FMPPaywallError(
                f"HTTP 402: endpoint or resource not included in current plan"
            )
        elif response.status == 429:
            raise FMPRateLimitError("Rate limit exceeded")
        elif response.status >= 500:
            raise FMPServerError(f"Server error: {response.status}")
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
