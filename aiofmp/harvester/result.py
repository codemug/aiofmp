"""Harvest result types."""

from dataclasses import dataclass


@dataclass
class HarvestResult:
    """Result of harvesting a single endpoint + entity."""
    endpoint_name: str          # e.g. "chart.historical_price_full"
    entity: str | None = None   # e.g. "AAPL" or None for global endpoints
    records_fetched: int = 0
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None
