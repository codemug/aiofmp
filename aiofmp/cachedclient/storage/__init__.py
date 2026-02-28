"""Storage backends for the cached client."""

from .base import StorageBackend, StoredRangeMetadata
from .parquet import ParquetStorage

__all__ = [
    "StorageBackend",
    "StoredRangeMetadata",
    "ParquetStorage",
]
