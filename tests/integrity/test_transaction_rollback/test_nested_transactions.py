"""Test nested transaction rollback behavior."""


def test_nested_transaction_rollback(test_db):
    """Nested transaction rollback works correctly."""
    cursor = test_db.conn.cursor()

    try:
        # Outer transaction
        cursor.execute("BEGIN")

        cursor.execute("""
            INSERT INTO mappings
            (source_id, source_event_uid, target_event_id, last_hash)
            VALUES (?, ?, ?, ?)
        """, (1, 'evt1', 'target1', 'hash1'))

        # Inner operation
        try:
            cursor.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id, last_hash)
                VALUES (?, ?, ?, ?)
            """, (1, 'evt2', 'target2', 'hash2'))

            raise Exception("Inner failure")
        except Exception:
            # Inner failure - rollback everything
            test_db.conn.rollback()
            raise

        test_db.conn.commit()
    except Exception:
        pass

    # Nothing should be committed
    cursor.execute("SELECT COUNT(*) FROM mappings")
    count = cursor.fetchone()[0]
    assert count == 0
