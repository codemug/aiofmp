"""Abstract storage backend for the cached client."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class StoredRangeMetadata:
    """Metadata about what date range is stored for a given key."""

    min_date: date
    max_date: date
    record_count: int
    last_updated: date


class StorageBackend(ABC):
    """Abstract base class for cached client storage backends.

    Storage keys are tuples of strings that identify a dataset, e.g.:
      ("historical-price-eod/full", "AAPL")
      ("income-statement", "AAPL", "annual")
    """

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the storage backend (create directories, connections, etc.)."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Clean up resources."""
        ...

    @abstractmethod
    async def get_stored_range(
        self, key: tuple[str, ...]
    ) -> StoredRangeMetadata | None:
        """Get metadata about what date range is stored for the given key.

        Returns None if no data is stored for this key.
        """
        ...

    @abstractmethod
    async def read(
        self,
        key: tuple[str, ...],
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """Read stored records for the given key, optionally filtered to a date range.

        Returns an empty list if no data exists.
        """
        ...

    @abstractmethod
    async def write(
        self,
        key: tuple[str, ...],
        records: list[dict[str, Any]],
        date_field: str = "date",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        """Write records to storage for the given key.

        This REPLACES all stored data for this key. The caller is responsible
        for merging old + new data before calling write.
        """
        ...

    @abstractmethod
    async def append(
        self,
        key: tuple[str, ...],
        records: list[dict[str, Any]],
        date_field: str = "date",
        date_format: str = "%Y-%m-%d",
    ) -> None:
        """Append records to existing storage for the given key.

        Deduplicates by the date field to avoid overlapping records.
        """
        ...

    @abstractmethod
    async def delete(self, key: tuple[str, ...]) -> None:
        """Delete all stored data for the given key."""
        ...

    @abstractmethod
    async def list_keys(
        self, prefix: tuple[str, ...] | None = None
    ) -> list[tuple[str, ...]]:
        """List all stored keys, optionally filtered by prefix."""
        ...
