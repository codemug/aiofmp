"""Facts as trail panel columns, plus the changefeed that drives incremental recompute."""

import os

import pytest
from trail_snapshot_source import SnapshotSource


@pytest.fixture
def src(conn):
    return SnapshotSource({"dsn": os.environ["SNAPSHOT_TEST_DSN"]})


def _fact(conn, subj, pred, val, valid_from, published_at):
    conn.execute(
        """INSERT INTO snapshot.facts
             (subject, predicate, value, kind, valid_from, published_at, fidelity, source_id)
           VALUES (%s, %s, %s, 'observation', %s, %s, 'vintage', 1)""",
        (subj, pred, val, valid_from, published_at),
    )


def test_freshness_token_is_none_when_empty(conn, src):
    assert src.freshness_token() is None


def test_freshness_token_moves_when_a_fact_arrives(conn, src):
    before = src.freshness_token()
    _fact(conn, "AAPL", "revenue", 1.0, "2025-12-31", "2026-02-01Z")
    assert src.freshness_token() != before


def test_changed_since_returns_only_newer_cells(conn, src):
    _fact(conn, "AAPL", "revenue", 1.0, "2024-12-31", "2025-02-01Z")
    _fact(conn, "MSFT", "revenue", 2.0, "2025-12-31", "2026-02-01Z")
    changed = src.changed_since("2025-06-01T00:00:00+00:00")
    assert {e for e, _ in changed} == {"MSFT"}


def test_changed_since_none_cursor_returns_everything(conn, src):
    _fact(conn, "AAPL", "revenue", 1.0, "2024-12-31", "2025-02-01Z")
    assert len(src.changed_since(None)) == 1


def test_restatement_dirties_the_cell_again(conn, src):
    """A restatement arrives as a NEW row with a later published_at, so the same
    (entity, period) cell must reappear in the changefeed - otherwise the view
    would never pick the correction up."""
    _fact(conn, "AAPL", "revenue", 1.0, "2024-12-31", "2025-02-01Z")
    _fact(conn, "AAPL", "revenue", 0.9, "2024-12-31", "2026-03-01Z")
    changed = src.changed_since("2025-06-01T00:00:00+00:00")
    assert ("AAPL", __import__("datetime").date(2024, 12, 31)) in changed


def test_load_pivots_predicates_into_columns(conn, src):
    _fact(conn, "AAPL", "revenue", 100.0, "2025-12-31", "2026-02-01Z")
    _fact(conn, "AAPL", "net_income", 20.0, "2025-12-31", "2026-02-01Z")
    df = src.load()
    assert set(df.columns) >= {"entity", "time", "revenue", "net_income"}
    assert df.height == 1


def test_load_takes_the_latest_published_value(conn, src):
    _fact(conn, "AAPL", "revenue", 100.0, "2025-12-31", "2026-02-01Z")
    _fact(conn, "AAPL", "revenue", 90.0, "2025-12-31", "2026-05-01Z")
    assert src.load()["revenue"].to_list() == [90.0]
