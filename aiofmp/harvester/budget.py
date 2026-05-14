"""Bandwidth budget tracker for the harvester.

Reads/writes the ``bandwidth_ledger`` table in the StateStore. Provides:
  - ``record_bytes(category, byte_count)``: attribute bytes to a category
    (or the synthetic ``"user"`` category when called from user code).
  - ``is_paused(category)``: True if the monthly soft cap is reached and the
    configured behavior is ``pause_until_next_month``.
  - ``check_hard_cap(category)``: raise ``FMPBudgetError`` when the monthly
    hard cap is reached, for harvester-initiated requests only.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from aiofmp.base import FMPBudgetError
from aiofmp.harvester.config import BudgetConfig
from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)

GB = 1024 ** 3


class BudgetTracker:
    def __init__(self, store: StateStore, config: BudgetConfig) -> None:
        self._store = store
        self._config = config

    def current_month_key(self) -> str:
        return datetime.now(UTC).strftime("%Y-%m")

    def record_bytes(self, category: str | None, byte_count: int) -> None:
        attribution = category if category else "user"
        self._store.add_bytes(self.current_month_key(), attribution, byte_count)

    def is_paused(self, category: str) -> bool:
        if self._config.soft_cap_behavior != "pause_until_next_month":
            return False
        total = self._store.get_month_bytes(self.current_month_key())
        return total >= self._config.monthly_soft_cap_gb * GB

    def check_hard_cap(self, category: str | None) -> None:
        if category is None or category == "user":
            return
        total = self._store.get_month_bytes(self.current_month_key())
        if total >= self._config.monthly_hard_cap_gb * GB:
            raise FMPBudgetError(
                f"monthly hard cap ({self._config.monthly_hard_cap_gb} GB) reached for "
                f"category {category!r}; total this month: {total / GB:.2f} GB"
            )
