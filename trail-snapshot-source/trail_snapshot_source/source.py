"""Expose snapshot facts to trail as panel columns, with a changefeed.

This is the load-bearing half of the trail integration. trail already has the
incremental update engine the snapshot design needs — per ``trail/views.py``,
staleness is a declaration hash plus a panel-config fingerprint plus per-source
freshness, and a source exposing ``changed_since`` gets footprint-scoped
recompute instead of a whole-view rebuild. We are not building an update engine;
we are feeding one that works.

``changed_since`` keys on ``published_at`` — the point-in-time clock — so a
restatement, which arrives as a NEW row with a later ``published_at``, dirties
exactly the cells it should. ``trail-fmp`` does the same thing keyed on filing
date (``trail_fmp/source.py:172``), noting that an amendment carries a newer
acceptedDate; this is the same idea for a different backend.
"""
from __future__ import annotations

import datetime as dt
import os

import polars as pl
import psycopg
from psycopg.rows import dict_row

# One row per (entity, period), latest publication winning. The DISTINCT ON
# ordering mirrors snapshot.facts.as_of: published_at DESC picks the newest
# vintage, and source_id breaks ties deterministically so two sources publishing
# at the same instant cannot make the panel non-reproducible.
_LOAD = """
SELECT DISTINCT ON (subject, predicate, valid_from)
       subject AS entity, valid_from AS time, predicate, value
  FROM {schema}.facts
 WHERE value IS NOT NULL
 ORDER BY subject, predicate, valid_from, published_at DESC, source_id
"""


class SnapshotSource:
    """A trail source over ``snapshot.facts``."""

    name = "snapshot"

    def __init__(self, options: dict | None = None) -> None:
        options = options or {}
        # Option first, environment second - the precedence trail-fmp uses for
        # its API key. trail.yaml is a ConfigMap, so a password-bearing DSN has
        # to arrive through the environment from a secret.
        self._dsn = options.get("dsn") or os.environ.get("SNAPSHOT_DSN")
        if not self._dsn:
            raise ValueError(
                "E-SNAPSHOT-DSN snapshot source requires a connection string; "
                "set options.dsn or the SNAPSHOT_DSN environment variable"
            )
        self._schema = options.get("schema", "snapshot")

    def _connect(self):
        return psycopg.connect(self._dsn, autocommit=True, row_factory=dict_row)

    def load(self, *args, **kwargs) -> pl.DataFrame:
        """The panel: entity x time, one column per predicate."""
        with self._connect() as c:
            rows = c.execute(_LOAD.format(schema=self._schema)).fetchall()
        if not rows:
            return pl.DataFrame({"entity": [], "time": []})
        return (
            pl.DataFrame(rows)
            .pivot(values="value", index=["entity", "time"], on="predicate")
            .sort(["entity", "time"])
        )

    def freshness_token(self) -> str | None:
        """Max published_at — cheap, and moves whenever anything new lands.

        None means "no freshness signal", which tells trail to serve the stored
        view until the program changes. That is the correct answer for an empty
        store: there is nothing to be stale about yet.
        """
        with self._connect() as c:
            row = c.execute(
                f"SELECT max(published_at) AS m FROM {self._schema}.facts"
            ).fetchone()
        return row["m"].isoformat() if row and row["m"] else None

    def changed_since(self, cursor: str | None):
        """The ``(entity, period-end)`` cells published after ``cursor``.

        ``cursor`` is a token previously returned by :meth:`freshness_token`.
        None means "everything", which is what a first build wants.
        """
        sql = f"SELECT DISTINCT subject, valid_from FROM {self._schema}.facts"
        params: tuple = ()
        if cursor is not None:
            sql += " WHERE published_at > %s"
            params = (dt.datetime.fromisoformat(cursor),)
        with self._connect() as c:
            rows = c.execute(sql, params).fetchall()
        return {(r["subject"], r["valid_from"]) for r in rows}
