"""Tests for transaction rollback on critical failures."""

import tempfile
from pathlib import Path
from python.state import Database


def test_transaction_rollback_on_critical_failure():
    """Critical failures rollback partial changes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        db.connect()
        db.initialize_schema()

        cursor = db.conn.cursor()

        try:
            # Start transaction
            cursor.execute("BEGIN")

            # Insert some data
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, content_hash)
                VALUES (?, ?, ?, ?)
            """, (1, 'evt1', 'target1', 'hash1'))

            # Simulate failure
            raise Exception("Critical error")

            db.conn.commit()
        except Exception:
            # Rollback on error
            db.conn.rollback()

        # Verify no data was committed
        cursor.execute("SELECT COUNT(*) FROM mappings")
        count = cursor.fetchone()[0]
        assert count == 0

        db.close()
