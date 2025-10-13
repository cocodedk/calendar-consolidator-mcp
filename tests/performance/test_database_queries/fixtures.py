"""Fixtures for database query performance tests."""

import pytest
import tempfile
from pathlib import Path
from python.state import Database


@pytest.fixture
def db_with_many_mappings():
    """Database with 1000 mapping entries."""
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

        # Insert 1000 mappings
        for i in range(1000):
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, last_hash)
                VALUES (?, ?, ?, ?)
            """, (1, f'event_{i}', f'target_{i}', f'hash_{i}'))

        db.conn.commit()
        yield db
        db.close()
