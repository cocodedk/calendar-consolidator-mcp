"""Test database query performance with large datasets."""

import pytest
import tempfile
from pathlib import Path
from python.state import Database
from python.state.mapping_store import MappingStore
import time


@pytest.fixture
def db_with_many_mappings():
    """Database with 1000 mapping entries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Insert 1000 mappings
        for i in range(1000):
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, content_hash)
                VALUES (?, ?, ?, ?)
            """, (1, f'event_{i}', f'target_{i}', f'hash_{i}'))

        db.conn.commit()
        yield db
        db.close()


def test_get_all_mappings_performance(db_with_many_mappings):
    """Fetching all mappings is performant."""
    store = MappingStore(db_with_many_mappings)

    start = time.time()
    mappings = store.get_all_for_source(1)
    elapsed = time.time() - start

    assert len(mappings) == 1000
    assert elapsed < 1.0  # Should complete in under 1 second


def test_get_single_mapping_performance(db_with_many_mappings):
    """Single mapping lookup is fast."""
    store = MappingStore(db_with_many_mappings)

    start = time.time()
    mapping = store.get_by_source_event(1, 'event_500')
    elapsed = time.time() - start

    assert mapping is not None
    assert elapsed < 0.1  # Should be instant with proper indexing


def test_bulk_insert_mappings():
    """Bulk inserting mappings is efficient."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        store = MappingStore(db)

        start = time.time()

        for i in range(100):
            store.create(1, f'event_{i}', f'target_{i}', f'hash_{i}')

        elapsed = time.time() - start

        assert elapsed < 5.0  # 100 inserts in under 5 seconds
        db.close()


def test_query_with_index_performance():
    """Indexed queries are fast."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Insert many records
        for i in range(1000):
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, content_hash)
                VALUES (?, ?, ?, ?)
            """, (1, f'event_{i}', f'target_{i}', f'hash_{i}'))

        db.conn.commit()

        # Query with indexed column
        start = time.time()
        cursor.execute("""
            SELECT * FROM mappings WHERE source_id = ? AND source_event_uid = ?
        """, (1, 'event_999'))
        result = cursor.fetchone()
        elapsed = time.time() - start

        assert result is not None
        assert elapsed < 0.1  # Indexed query should be instant

        db.close()
