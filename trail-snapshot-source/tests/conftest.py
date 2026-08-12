import os
import pathlib
import psycopg
import pytest
from psycopg.rows import dict_row

# Reuse the harness migrations: this source reads the same schema.
MIGRATIONS = pathlib.Path(
    "/home/usmanshahid/Documents/claude/workspaces/harness/snapshot/migrations")


@pytest.fixture
def conn():
    c = psycopg.connect(os.environ["SNAPSHOT_TEST_DSN"], autocommit=True,
                        row_factory=dict_row)
    c.execute("DROP SCHEMA IF EXISTS snapshot CASCADE")
    c.execute("LOAD 'age'")
    c.execute('SET search_path = ag_catalog, "$user", public')
    if c.execute("SELECT 1 FROM ag_catalog.ag_graph WHERE name='snapshot_graph'").fetchone():
        c.execute("SELECT ag_catalog.drop_graph('snapshot_graph', true)")
    for f in sorted(MIGRATIONS.glob("*.sql")):
        c.execute(f.read_text())
    c.execute("INSERT INTO snapshot.sources (source_id, name) VALUES (1,'test') "
              "ON CONFLICT DO NOTHING")
    yield c
    c.close()
