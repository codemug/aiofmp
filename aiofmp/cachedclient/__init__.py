"""CachedClient — caching wrapper for the aiofmp SDK.

The cached client intercepts time-series API calls, caches results in a pluggable
storage backend, and only fetches missing date ranges from the upstream API.

By default, data is cached in Parquet files under ``~/.aiofmp/cache``.
Override with the ``AIOFMP_CACHE_FILE_PATH`` environment variable or by
passing a custom ``storage`` backend.

Usage::

    from aiofmp import FmpClient
    from aiofmp.cachedclient import CachedClient

    fmp = FmpClient(api_key="YOUR_KEY")
    cached = CachedClient(fmp)  # caches to ~/.aiofmp/cache

    async with cached:
        data = await cached.chart.historical_price_full("AAPL", "2020-01-01", "2025-01-01")
"""

from .client import CachedClient, CachedClientConfig
from .storage.base import StorageBackend, StoredRangeMetadata
from .storage.parquet import ParquetStorage

__all__ = [
    "CachedClient",
    "CachedClientConfig",
    "StorageBackend",
    "StoredRangeMetadata",
    "ParquetStorage",
]
