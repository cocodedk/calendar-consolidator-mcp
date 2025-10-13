"""Tests for bulk database operations performance."""

import tempfile
import time
from pathlib import Path
from python.state import Database
from python.state.mapping_store import MappingStore


def test_bulk_insert_mappings():
    """Bulk inserting mappings is efficient."""
    from python.state.source_store import SourceStore

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        # Create a source first (required by foreign key constraint)
        source_store = SourceStore(db)
        source_store.add('graph', 'test-calendar', 'Test', {'access_token': 'test'})

        store = MappingStore(db)

        start = time.time()

        for i in range(100):
            store.create(1, f'event_{i}', f'target_{i}', f'hash_{i}')

        elapsed = time.time() - start

        assert elapsed < 5.0  # 100 inserts in under 5 seconds
        db.close()
