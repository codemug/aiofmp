"""The Postgres ViewStore: trail's 5-method ViewStore ABC, backed by the snapshot DB."""
import os
import polars as pl
import pytest
from trail.store import Manifest
from trail_snapshot_store import PgViewStore


@pytest.fixture
def store():
    s = PgViewStore({"dsn": os.environ["SNAPSHOT_TEST_DSN"], "schema": "snapshot"})
    for n in s.list():
        s.delete(n)
    return s


def _mf(name="rating", expr_hash="h1"):
    return Manifest(
        name=name, kind="model", exports=("score",), expr_hash=expr_hash,
        sources=("fmp",), freshness={"fmp": "t1"},
        built_at="2026-01-01T00:00:00Z", columns=("views.rating.score",),
    )


def test_write_then_read_roundtrips(store):
    df = pl.DataFrame({"entity": ["AAPL", "MSFT"], "time": ["2025-12-31"] * 2,
                       "views.rating.score": [0.8, 0.6]})
    store.write("rating", df, _mf())
    got = store.read("rating")
    assert got.shape == df.shape
    assert got["views.rating.score"].to_list() == [0.8, 0.6]


def test_manifest_roundtrips(store):
    store.write("rating", pl.DataFrame({"entity": ["A"]}), _mf())
    mf = store.manifest("rating")
    assert mf.expr_hash == "h1" and mf.sources == ("fmp",)


def test_rewrite_replaces_rather_than_appends(store):
    """A rebuild REPLACES a view. Accumulating would silently double every
    tracked frame on the second build - and the row count would still look
    plausible."""
    store.write("rating", pl.DataFrame({"entity": ["A", "B"]}), _mf())
    store.write("rating", pl.DataFrame({"entity": ["C"]}), _mf(expr_hash="h2"))
    assert store.read("rating").height == 1
    assert store.manifest("rating").expr_hash == "h2"


def test_missing_view_reads_none(store):
    assert store.read("nope") is None
    assert store.manifest("nope") is None


def test_delete_and_list(store):
    store.write("rating", pl.DataFrame({"entity": ["A"]}), _mf())
    assert "rating" in store.list()
    assert store.delete("rating") is True
    assert store.delete("rating") is False
    assert store.list() == []


def test_schema_and_dtypes_survive_the_roundtrip(store):
    """Parquet round-trip must not silently coerce types - a float score coming
    back as a string would break every downstream comparison."""
    df = pl.DataFrame({
        "entity": ["AAPL"], "time": ["2025-12-31"],
        "views.rating.score": [0.8],
        "views.rating.grade": ["A"],
        "views.rating.gate_ok": [True],
    })
    store.write("rating", df, _mf())
    got = store.read("rating")
    assert got.dtypes == df.dtypes
    assert got.columns == df.columns
