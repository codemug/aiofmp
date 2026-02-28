"""
FMP Client Management

This module provides the FMP client instance management for MCP tools.

When the ``AIOFMP_CACHED`` environment variable is set to ``true``, the
returned client is a :class:`~aiofmp.cachedclient.CachedClient` that
transparently caches time-series data in local Parquet files.
"""

import os

from . import FmpClient
from .base import FMPAuthenticationError

# Global client instance (FmpClient or CachedClient)
_fmp_client: FmpClient | None = None


def reset_fmp_client():
    """Reset the global FMP client instance (for testing)."""
    global _fmp_client
    _fmp_client = None


def get_fmp_client() -> FmpClient:
    """Get or create the FMP client instance.

    If ``AIOFMP_CACHED=true`` the returned object is a
    :class:`~aiofmp.cachedclient.CachedClient` wrapping a real ``FmpClient``.
    The ``CachedClient`` is API-compatible (same category attributes and
    context-manager protocol) so all MCP tools work without modification.
    """
    global _fmp_client
    if _fmp_client is None:
        api_key = os.getenv("FMP_API_KEY")
        if not api_key:
            raise FMPAuthenticationError("FMP_API_KEY environment variable is required")

        fmp = FmpClient(api_key=api_key)

        if os.getenv("AIOFMP_CACHED", "").lower() == "true":
            from .cachedclient import CachedClient

            _fmp_client = CachedClient(fmp)
        else:
            _fmp_client = fmp
    return _fmp_client
