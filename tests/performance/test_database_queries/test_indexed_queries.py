"""Tests for indexed query performance."""

import tempfile
import time
from pathlib import Path
from python.state import Database


def test_query_with_index_performance():
    """Indexed queries are fast."""
    from python.state.source_store import SourceStore

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        # Create a source first (required by foreign key constraint)
        source_store = SourceStore(db)
        source_store.add('graph', 'test-calendar', 'Test', {'access_token': 'test'})

        cursor = db.conn.cursor()

        # Insert many records
        for i in range(1000):
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, last_hash)
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
