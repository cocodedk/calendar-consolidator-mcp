"""Shared fixtures for transaction rollback tests."""

import tempfile
from pathlib import Path
import pytest
from python.state import Database


@pytest.fixture
def test_db():
    """Create a test database with schema."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()
        yield db
        db.close()


@pytest.fixture
def test_db_with_source(test_db):
    """Test database with a source record."""
    cursor = test_db.conn.cursor()
    cursor.execute("""
        INSERT INTO sources (type, calendar_id, name, cred_blob)
        VALUES (?, ?, ?, ?)
    """, ('graph', 'test-cal', 'Test', b'creds'))
    test_db.conn.commit()
    return test_db
