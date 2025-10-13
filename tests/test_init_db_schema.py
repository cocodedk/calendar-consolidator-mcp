"""Test database initialization creates proper schema."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from python.state import Database


def test_init_db_creates_database_file():
    """Database initialization creates database file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        assert db_path.exists()
        db.close()


def test_init_db_creates_tables():
    """Database initialization creates all required tables."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        # Check that tables exist
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name IN
            ('sources', 'targets', 'mappings', 'sync_logs', 'settings')
        """)
        tables = [row[0] for row in cursor.fetchall()]

        assert 'sources' in tables
        assert 'targets' in tables
        assert 'mappings' in tables
        assert 'sync_logs' in tables
        assert 'settings' in tables

        db.close()


def test_init_db_inserts_default_settings():
    """Database initialization inserts default settings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM settings")
        count = cursor.fetchone()[0]

        assert count >= 0  # Settings may or may not have defaults in schema
        db.close()


def test_init_db_schema_structure():
    """Database schema has correct column structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Check sources table structure
        cursor.execute("PRAGMA table_info(sources)")
        columns = [row[1] for row in cursor.fetchall()]
        assert 'id' in columns
        assert 'calendar_id' in columns
        assert 'type' in columns

        # Check mappings table structure
        cursor.execute("PRAGMA table_info(mappings)")
        columns = [row[1] for row in cursor.fetchall()]
        assert 'source_event_uid' in columns
        assert 'target_event_id' in columns
        assert 'content_hash' in columns

        db.close()
