"""Test database initialization is idempotent (safe to run multiple times)."""

import pytest
import tempfile
from pathlib import Path
from python.state import Database


def test_init_db_multiple_times():
    """Running init_db multiple times doesn't cause errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"

        # Initialize first time
        db1 = Database(str(db_path))
        db1.connect()
        db1.initialize_schema()
        db1.close()

        # Initialize second time (should not error)
        db2 = Database(str(db_path))
        try:
            db2.connect()
            db2.initialize_schema()
            success = True
        except Exception:
            success = False
        finally:
            db2.close()

        assert success


def test_init_db_preserves_data():
    """Re-initialization preserves existing data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"

        # Initialize and add data
        db1 = Database(str(db_path))
        db1.connect()
        db1.initialize_schema()
        cursor = db1.conn.cursor()
        cursor.execute("""
            INSERT INTO settings (key, value)
            VALUES ('test_key', 'test_value')
        """)
        db1.conn.commit()
        db1.close()

        # Re-initialize
        db2 = Database(str(db_path))
        db2.connect()
        db2.initialize_schema()
        cursor = db2.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='test_key'")
        row = cursor.fetchone()
        db2.close()

        assert row is not None
        assert row[0] == 'test_value'


def test_init_db_does_not_duplicate_settings():
    """Re-initialization doesn't duplicate default settings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"

        # Initialize twice
        db1 = Database(str(db_path))
        db1.connect()
        db1.initialize_schema()
        db1.close()

        db2 = Database(str(db_path))
        db2.connect()
        db2.initialize_schema()

        cursor = db2.conn.cursor()
        cursor.execute("SELECT key, COUNT(*) as cnt FROM settings GROUP BY key")
        duplicates = [row for row in cursor.fetchall() if row[1] > 1]
        db2.close()

        # No keys should have duplicates
        assert len(duplicates) == 0
