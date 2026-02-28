"""CachedClient — caching wrapper around FmpClient."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from aiofmp import FmpClient

from .proxy import CachedCategoryProxy
from .registry import EndpointRegistry, build_default_registry
from .storage.base import StorageBackend
from .storage.parquet import ParquetStorage

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = str(Path.home() / ".aiofmp" / "cache")


@dataclass
class CachedClientConfig:
    """Configuration for the cached client."""

    staleness_days: int = 1
    """How many days old stored data can be before a Pattern B refetch is triggered."""


class CachedClient:
    """Drop-in replacement for FmpClient with local caching of time-series data.

    Wraps all 22 category attributes of FmpClient with a proxy that intercepts
    cacheable method calls, checks local storage, fetches only missing data
    from the upstream API, and returns the merged result.

    Non-cacheable methods pass through to the real FmpClient unchanged.

    By default, data is cached in Parquet files under ``~/.aiofmp/cache``.
    Override the location with the ``AIOFMP_CACHE_FILE_PATH`` environment
    variable or by passing a custom ``storage`` backend.

    Usage::

        from aiofmp import FmpClient
        from aiofmp.cachedclient import CachedClient

        fmp = FmpClient(api_key="YOUR_KEY")
        cached = CachedClient(fmp)  # caches to ~/.aiofmp/cache

        async with cached:
            # First call: fetches from API, stores in Parquet
            data = await cached.chart.historical_price_full("AAPL", "2020-01-01", "2023-12-31")

            # Second call: only fetches the gap (2024 onward)
            data = await cached.chart.historical_price_full("AAPL", "2020-01-01", "2025-01-01")

            # Non-cacheable: passes through directly
            profile = await cached.company.profile("AAPL")
    """

    def __init__(
        self,
        fmp_client: FmpClient,
        storage: StorageBackend | None = None,
        registry: EndpointRegistry | None = None,
        config: CachedClientConfig | None = None,
    ) -> None:
        self._fmp = fmp_client
        if storage is None:
            base_dir = os.environ.get("AIOFMP_CACHE_FILE_PATH", DEFAULT_CACHE_DIR)
            storage = ParquetStorage(base_dir=base_dir)
        self._storage = storage
        self._registry = registry or build_default_registry()
        self._config = config or CachedClientConfig()

        # All 22 category names from FmpClient.__init__
        category_names = [
            "search",
            "directory",
            "analyst",
            "calendar",
            "chart",
            "company",
            "cot",
            "dcf",
            "economics",
            "etf",
            "commodity",
            "crypto",
            "forex",
            "statements",
            "form13f",
            "indexes",
            "insider_trades",
            "market_performance",
            "news",
            "technical_indicators",
            "quote",
            "senate",
        ]

        for cat_name in category_names:
            real_category = getattr(fmp_client, cat_name)
            proxy = CachedCategoryProxy(
                real_category, cat_name, self._storage, self._registry
            )
            setattr(self, cat_name, proxy)

    async def __aenter__(self) -> "CachedClient":
        await self._fmp.start()
        await self._storage.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        await self._fmp.close()
        await self._storage.close()

    @property
    def storage(self) -> StorageBackend:
        """Access the underlying storage backend."""
        return self._storage

    @property
    def fmp_client(self) -> FmpClient:
        """Access the underlying FmpClient."""
        return self._fmp

    @property
    def registry(self) -> EndpointRegistry:
        """Access the endpoint registry."""
        return self._registry
