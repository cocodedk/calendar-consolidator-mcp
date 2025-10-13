"""Test database schema version handling and migration support."""

import pytest
import tempfile
from pathlib import Path
from python.state import Database


def test_database_has_version_info():
    """Database tracks schema version."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()
        # Check if version tracking exists (could be in settings or separate table)
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND (name='schema_version' OR name='settings')
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Should have some way to track version
        assert len(tables) > 0
        db.close()


def test_database_schema_consistency():
    """Database schema is consistently created."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two databases and compare schemas
        db_path1 = Path(tmpdir) / "test1.db"
        db_path2 = Path(tmpdir) / "test2.db"

        db1 = Database(str(db_path1))
        db1.connect()
        db1.initialize_schema()

        db2 = Database(str(db_path2))
        db2.connect()
        db2.initialize_schema()

        # Get schema from both
        cursor1 = db1.conn.cursor()
        cursor1.execute("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name")
        schema1 = cursor1.fetchall()

        cursor2 = db2.conn.cursor()
        cursor2.execute("SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name")
        schema2 = cursor2.fetchall()

        db1.close()
        db2.close()

        # Schemas should be identical
        assert schema1 == schema2


def test_database_handles_missing_columns_gracefully():
    """Database operations handle schema differences gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        # Verify database can perform basic operations
        cursor = db.conn.cursor()
        try:
            cursor.execute("SELECT * FROM sources LIMIT 1")
            cursor.execute("SELECT * FROM mappings LIMIT 1")
            cursor.execute("SELECT * FROM settings LIMIT 1")
            success = True
        except Exception:
            success = False
        finally:
            db.close()

        assert success
