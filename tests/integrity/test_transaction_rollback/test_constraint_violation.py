"""Test rollback on constraint violations."""


def test_rollback_on_constraint_violation(test_db_with_source):
    """Transaction rolls back on constraint violation."""
    cursor = test_db_with_source.conn.cursor()

    # Insert initial data
    cursor.execute("""
        INSERT INTO mappings
        (source_id, source_event_uid, target_event_id, last_hash)
        VALUES (?, ?, ?, ?)
    """, (1, 'evt1', 'target1', 'hash1'))
    test_db_with_source.conn.commit()

    try:
        # Try to insert duplicate (should fail on unique constraint)
        cursor.execute("""
            INSERT INTO mappings
            (source_id, source_event_uid, target_event_id, last_hash)
            VALUES (?, ?, ?, ?)
        """, (1, 'evt1', 'target1', 'hash1'))
        test_db_with_source.conn.commit()
    except Exception:
        test_db_with_source.conn.rollback()

    # Verify only one record exists
    cursor.execute("SELECT COUNT(*) FROM mappings")
    count = cursor.fetchone()[0]
    assert count == 1
