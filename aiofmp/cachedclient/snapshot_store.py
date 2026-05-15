"""SnapshotStore — single-row-per-entity storage on top of a StorageBackend.

Used by the P4 snapshot-overwrite pattern (e.g. analyst ratings, DCF).
Storage keys take the shape ``("snapshot/<endpoint>", entity)``.
Each write replaces the previous row; reads return the latest dict or None.
"""

from __future__ import annotations

from typing import Any

from aiofmp.cachedclient.storage.base import StorageBackend


class SnapshotStore:
    """Thin wrapper that stores a single dict-row per (endpoint, entity) key."""

    def __init__(self, storage: StorageBackend) -> None:
        self._storage = storage

    def _key(self, endpoint: str, entity: str) -> tuple[str, ...]:
        return (f"snapshot/{endpoint}", entity)

    async def write(self, endpoint: str, entity: str, payload: dict[str, Any]) -> None:
        if not payload:
            return
        await self._storage.write(
            self._key(endpoint, entity), [payload], date_field="date"
        )

    async def read(self, endpoint: str, entity: str) -> dict[str, Any] | None:
        records = await self._storage.read(self._key(endpoint, entity))
        if not records:
            return None
        return records[0]

    async def list_entities(self, endpoint: str) -> list[str]:
        """List all entities stored under ``snapshot/<endpoint>``."""
        prefix = (f"snapshot/{endpoint}",)
        keys = await self._storage.list_keys(prefix=prefix)
        entities: list[str] = []
        for k in keys:
            # key shape is (f"snapshot/{endpoint}", entity)
            if len(k) >= 2:
                entities.append(k[1])
        return entities
