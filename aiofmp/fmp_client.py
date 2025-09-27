"""
FMP Client Management

This module provides the FMP client instance management for MCP tools.
"""

import os

from . import FmpClient
from .base import FMPAuthenticationError

# Global FMP client instance
_fmp_client: FmpClient | None = None


def reset_fmp_client():
    """Reset the global FMP client instance (for testing)."""
    global _fmp_client
    _fmp_client = None


def get_fmp_client() -> FmpClient:
    """Get or create the FMP client instance."""
    global _fmp_client
    if _fmp_client is None:
        api_key = os.getenv("FMP_API_KEY")
        if not api_key:
            raise FMPAuthenticationError("FMP_API_KEY environment variable is required")
        _fmp_client = FmpClient(api_key=api_key)
    return _fmp_client
