"""A trail ViewStore backed by the snapshot database.

trail keeps its view-persistence machinery; what changes is where the frames
land. Instead of parquet files on a local disk, tracked views become rows in the
snapshot store — so a view sits alongside the facts it was computed from rather
than in a parallel artifact beside them.

Frames are stored as parquet bytes rather than shredded into columns. trail
reads and writes whole frames, so a column-per-export schema would buy nothing
and would need a migration every time a model's exports changed — and this
project has already had exports change twice.

Registered as ``views_pg`` under the ``trail.providers`` entry-point group. Note
that trail resolves the store from ``config.providers["views"]`` — a hardcoded
key — so the trail.yaml stanza must be named ``views`` whatever the driver is.
"""
from __future__ import annotations

import io
import json
import os

import polars as pl
import psycopg
from psycopg.rows import dict_row
from trail.store import Manifest, ViewStore

_DDL = """
CREATE TABLE IF NOT EXISTS {schema}.views (
  name       text PRIMARY KEY,
  frame      bytea NOT NULL,
  manifest   jsonb NOT NULL,
  written_at timestamptz NOT NULL DEFAULT now()
)
"""


class PgViewStore(ViewStore):
    """Implements trail's five-method ViewStore ABC against Postgres."""

    def __init__(self, options: dict | None = None) -> None:
        options = options or {}
        # Option first, environment second — the same precedence trail-fmp uses
        # for its API key. trail.yaml is a ConfigMap, so the DSN carrying a
        # password must come from the environment (secret-backed) rather than be
        # written into config that ends up in version control.
        self._dsn = options.get("dsn") or os.environ.get("SNAPSHOT_DSN")
        if not self._dsn:
            raise ValueError(
                "E-SNAPSHOT-DSN views_pg requires a connection string; "
                "set options.dsn or the SNAPSHOT_DSN environment variable"
            )
        self._schema = options.get("schema", "snapshot")
        with self._connect() as c:
            c.execute(f"CREATE SCHEMA IF NOT EXISTS {self._schema}")
            c.execute(_DDL.format(schema=self._schema))

    def _connect(self):
        return psycopg.connect(self._dsn, autocommit=True, row_factory=dict_row)

    def read(self, name: str) -> pl.DataFrame | None:
        with self._connect() as c:
            row = c.execute(
                f"SELECT frame FROM {self._schema}.views WHERE name = %s", (name,)
            ).fetchone()
        return pl.read_parquet(io.BytesIO(row["frame"])) if row else None

    def manifest(self, name: str) -> Manifest | None:
        with self._connect() as c:
            row = c.execute(
                f"SELECT manifest FROM {self._schema}.views WHERE name = %s", (name,)
            ).fetchone()
        return Manifest.from_dict(row["manifest"]) if row else None

    def write(self, name: str, frame: pl.DataFrame, manifest: Manifest) -> None:
        buf = io.BytesIO()
        frame.write_parquet(buf)
        # UPSERT, not INSERT. A rebuild REPLACES a view; appending would silently
        # double every tracked frame on the second build, and a doubled row count
        # still looks plausible enough to go unnoticed.
        with self._connect() as c:
            c.execute(
                f"""
                INSERT INTO {self._schema}.views (name, frame, manifest)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                   SET frame      = EXCLUDED.frame,
                       manifest   = EXCLUDED.manifest,
                       written_at = now()
                """,
                (name, buf.getvalue(), json.dumps(manifest.to_dict())),
            )

    def delete(self, name: str) -> bool:
        with self._connect() as c:
            return (
                c.execute(
                    f"DELETE FROM {self._schema}.views WHERE name = %s", (name,)
                ).rowcount
                > 0
            )

    def list(self) -> list[str]:
        with self._connect() as c:
            rows = c.execute(
                f"SELECT name FROM {self._schema}.views ORDER BY name"
            ).fetchall()
        return [r["name"] for r in rows]
