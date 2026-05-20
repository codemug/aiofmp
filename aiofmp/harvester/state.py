"""SQLite-backed state store for the harvester.

Holds:
  - category_runs:   per-cycle bookkeeping
  - checkpoints:     last-seen-date per (category, scope)
  - symbol_catalog:  cached symbol universes
  - catalog_refresh: when each universe was last refreshed
  - bandwidth_ledger: bytes consumed per (month, category)

Schema migrations are linear and idempotent; tracked via PRAGMA user_version.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


class RunStatus(str, Enum):
    RUNNING = "running"
    OK = "ok"
    PARTIAL = "partial"
    ERROR = "error"
    PAUSED_FOR_BUDGET = "paused_for_budget"


@dataclass(frozen=True)
class CategoryRun:
    category: str
    started_at: str
    finished_at: str | None
    status: RunStatus
    items_attempted: int
    items_succeeded: int
    bytes_estimate: int
    error: str | None


class StateStore:
    """Thin synchronous wrapper around a single SQLite file.

    All methods are synchronous. Callers running inside asyncio loops should
    wrap hot paths with ``asyncio.to_thread`` if blocking becomes a concern.
    In practice the harvester's state writes are sub-millisecond.
    """

    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    def initialize(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA user_version")
            current_version = cur.fetchone()[0]
            if current_version < 1:
                self._apply_v1(conn)
                conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _apply_v1(self, conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS category_runs (
              category TEXT NOT NULL,
              started_at TEXT NOT NULL,
              finished_at TEXT,
              status TEXT NOT NULL,
              items_attempted INTEGER NOT NULL DEFAULT 0,
              items_succeeded INTEGER NOT NULL DEFAULT 0,
              bytes_estimate INTEGER NOT NULL DEFAULT 0,
              error TEXT,
              PRIMARY KEY (category, started_at)
            );
            CREATE INDEX IF NOT EXISTS idx_category_runs_started
              ON category_runs(category, started_at DESC);

            CREATE TABLE IF NOT EXISTS checkpoints (
              category TEXT NOT NULL,
              scope TEXT NOT NULL,
              checkpoint TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              PRIMARY KEY (category, scope)
            );

            CREATE TABLE IF NOT EXISTS symbol_catalog (
              universe TEXT NOT NULL,
              symbol TEXT NOT NULL,
              payload_json TEXT,
              discovered_at TEXT NOT NULL,
              PRIMARY KEY (universe, symbol)
            );

            CREATE TABLE IF NOT EXISTS catalog_refresh (
              universe TEXT PRIMARY KEY,
              last_refreshed_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS bandwidth_ledger (
              month TEXT NOT NULL,
              category TEXT NOT NULL,
              bytes INTEGER NOT NULL DEFAULT 0,
              PRIMARY KEY (month, category)
            );
            """
        )

    # ----- category_runs -----

    def record_run_start(self, category: str, started_at: datetime) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO category_runs (category, started_at, status) VALUES (?, ?, ?)",
                (category, started_at.isoformat(), RunStatus.RUNNING.value),
            )
            conn.commit()

    def record_run_finish(
        self,
        category: str,
        started_at: datetime,
        *,
        status: RunStatus,
        items_attempted: int = 0,
        items_succeeded: int = 0,
        bytes_estimate: int = 0,
        error: str | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE category_runs
                   SET finished_at = ?,
                       status = ?,
                       items_attempted = ?,
                       items_succeeded = ?,
                       bytes_estimate = ?,
                       error = ?
                 WHERE category = ? AND started_at = ?
                """,
                (
                    datetime.now(UTC).isoformat(),
                    status.value,
                    items_attempted,
                    items_succeeded,
                    bytes_estimate,
                    error,
                    category,
                    started_at.isoformat(),
                ),
            )
            conn.commit()

    def get_latest_run(self, category: str) -> CategoryRun | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM category_runs WHERE category = ? ORDER BY started_at DESC LIMIT 1",
                (category,),
            ).fetchone()
            if row is None:
                return None
            return CategoryRun(
                category=row["category"],
                started_at=row["started_at"],
                finished_at=row["finished_at"],
                status=RunStatus(row["status"]),
                items_attempted=row["items_attempted"],
                items_succeeded=row["items_succeeded"],
                bytes_estimate=row["bytes_estimate"],
                error=row["error"],
            )

    # ----- checkpoints -----

    def set_checkpoint(self, category: str, scope: str, checkpoint: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO checkpoints (category, scope, checkpoint, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(category, scope) DO UPDATE SET
                  checkpoint = excluded.checkpoint,
                  updated_at = excluded.updated_at
                """,
                (category, scope, checkpoint, datetime.now(UTC).isoformat()),
            )
            conn.commit()

    def get_checkpoint(self, category: str, scope: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT checkpoint FROM checkpoints WHERE category = ? AND scope = ?",
                (category, scope),
            ).fetchone()
            return row["checkpoint"] if row else None

    # ----- symbol_catalog -----

    def upsert_symbol(
        self, universe: str, symbol: str, payload: dict[str, Any]
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO symbol_catalog (universe, symbol, payload_json, discovered_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(universe, symbol) DO UPDATE SET
                  payload_json = excluded.payload_json
                """,
                (universe, symbol, json.dumps(payload), datetime.now(UTC).isoformat()),
            )
            conn.commit()

    def replace_universe(
        self, universe: str, symbols: list[tuple[str, dict[str, Any]]]
    ) -> None:
        """Atomically replace all symbols for a universe."""
        with self._connect() as conn:
            conn.execute("DELETE FROM symbol_catalog WHERE universe = ?", (universe,))
            now_iso = datetime.now(UTC).isoformat()
            conn.executemany(
                """
                INSERT INTO symbol_catalog (universe, symbol, payload_json, discovered_at)
                VALUES (?, ?, ?, ?)
                """,
                [(universe, sym, json.dumps(p), now_iso) for sym, p in symbols],
            )
            conn.commit()

    def list_symbols(self, universe: str) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT symbol FROM symbol_catalog WHERE universe = ? ORDER BY symbol",
                (universe,),
            ).fetchall()
            return [r["symbol"] for r in rows]

    def list_symbol_records(
        self, universe: str
    ) -> list[tuple[str, dict[str, Any]]]:
        """Like :meth:`list_symbols` but also returns the cached FMP payload
        (parsed from ``payload_json``). Used by SymbolCatalog when the
        read-time filter needs payload fields (e.g. ``currency``)."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT symbol, payload_json FROM symbol_catalog "
                "WHERE universe = ? ORDER BY symbol",
                (universe,),
            ).fetchall()
            out: list[tuple[str, dict[str, Any]]] = []
            for r in rows:
                try:
                    payload = json.loads(r["payload_json"]) if r["payload_json"] else {}
                except (json.JSONDecodeError, TypeError):
                    payload = {}
                if not isinstance(payload, dict):
                    payload = {}
                out.append((r["symbol"], payload))
            return out

    def set_last_refresh(self, universe: str, when: datetime) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO catalog_refresh (universe, last_refreshed_at)
                VALUES (?, ?)
                ON CONFLICT(universe) DO UPDATE SET last_refreshed_at = excluded.last_refreshed_at
                """,
                (universe, when.isoformat()),
            )
            conn.commit()

    def get_last_refresh(self, universe: str) -> datetime | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT last_refreshed_at FROM catalog_refresh WHERE universe = ?",
                (universe,),
            ).fetchone()
            if row is None:
                return None
            return datetime.fromisoformat(row["last_refreshed_at"])

    # ----- bandwidth ledger -----

    def add_bytes(self, month: str, category: str, n_bytes: int) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO bandwidth_ledger (month, category, bytes)
                VALUES (?, ?, ?)
                ON CONFLICT(month, category) DO UPDATE SET bytes = bytes + excluded.bytes
                """,
                (month, category, n_bytes),
            )
            conn.commit()

    def get_month_bytes(self, month: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(bytes), 0) AS total FROM bandwidth_ledger WHERE month = ?",
                (month,),
            ).fetchone()
            return int(row["total"])

    def get_category_month_bytes(self, month: str, category: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT bytes FROM bandwidth_ledger WHERE month = ? AND category = ?",
                (month, category),
            ).fetchone()
            return int(row["bytes"]) if row else 0
