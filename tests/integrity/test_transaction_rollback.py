"""Test database transaction rollback on errors."""

import pytest
import tempfile
from pathlib import Path
from python.state import Database


def test_rollback_on_constraint_violation():
    """Transaction rolls back on constraint violation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Insert initial data
        cursor.execute("""
            INSERT INTO mappings
            (source_id, source_event_uid, target_event_id, content_hash)
            VALUES (?, ?, ?, ?)
        """, (1, 'evt1', 'target1', 'hash1'))
        db.conn.commit()

        try:
            # Try to insert duplicate (should fail on unique constraint)
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, content_hash)
                VALUES (?, ?, ?, ?)
            """, (1, 'evt1', 'target1', 'hash1'))
            db.conn.commit()
        except Exception:
            db.conn.rollback()

        # Verify only one record exists
        cursor.execute("SELECT COUNT(*) FROM mappings")
        count = cursor.fetchone()[0]
        assert count == 1

        db.close()


def test_rollback_preserves_previous_state():
    """Rollback restores database to pre-transaction state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Initial state
        cursor.execute("""
            INSERT INTO settings (key, value) VALUES ('test', 'initial')
        """)
        db.conn.commit()

        # Start transaction
        try:
            cursor.execute("BEGIN")
            cursor.execute("UPDATE settings SET value = 'modified' WHERE key = 'test'")

            # Simulate error
            raise Exception("Transaction failed")

            db.conn.commit()
        except Exception:
            db.conn.rollback()

        # Verify value wasn't changed
        cursor.execute("SELECT value FROM settings WHERE key = 'test'")
        value = cursor.fetchone()[0]
        assert value == 'initial'

        db.close()


def test_nested_transaction_rollback():
    """Nested transaction rollback works correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        try:
            # Outer transaction
            cursor.execute("BEGIN")

            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, content_hash)
                VALUES (?, ?, ?, ?)
            """, (1, 'evt1', 'target1', 'hash1'))

            # Inner operation
            try:
                cursor.execute("""
                    INSERT INTO mappings
                    (source_id, source_event_uid, target_event_id, content_hash)
                    VALUES (?, ?, ?, ?)
                """, (1, 'evt2', 'target2', 'hash2'))

                raise Exception("Inner failure")
            except Exception:
                # Inner failure - rollback everything
                db.conn.rollback()
                raise

            db.conn.commit()
        except Exception:
            pass

        # Nothing should be committed
        cursor.execute("SELECT COUNT(*) FROM mappings")
        count = cursor.fetchone()[0]
        assert count == 0

        db.close()


def test_explicit_savepoint_rollback():
    """Explicit savepoint allows partial rollback."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        # Start transaction
        cursor.execute("BEGIN")

        # Insert first record
        cursor.execute("""
            INSERT INTO mappings
            (source_id, source_event_uid, target_event_id, content_hash)
            VALUES (?, ?, ?, ?)
        """, (1, 'evt1', 'target1', 'hash1'))

        # Create savepoint
        cursor.execute("SAVEPOINT sp1")

        # Insert second record
        cursor.execute("""
            INSERT INTO mappings
            (source_id, source_event_uid, target_event_id, content_hash)
            VALUES (?, ?, ?, ?)
        """, (1, 'evt2', 'target2', 'hash2'))

        # Rollback to savepoint (removes evt2)
        cursor.execute("ROLLBACK TO sp1")

        # Commit transaction
        db.conn.commit()

        # Only first record should exist
        cursor.execute("SELECT COUNT(*) FROM mappings")
        count = cursor.fetchone()[0]
        assert count == 1

        db.close()
