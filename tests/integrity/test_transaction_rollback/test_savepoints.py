"""Test explicit savepoint functionality."""


def test_explicit_savepoint_rollback(test_db_with_source):
    """Explicit savepoint allows partial rollback."""
    cursor = test_db_with_source.conn.cursor()

    # Start transaction
    cursor.execute("BEGIN")

    # Insert first record
    cursor.execute("""
        INSERT INTO mappings
        (source_id, source_event_uid, target_event_id, last_hash)
        VALUES (?, ?, ?, ?)
    """, (1, 'evt1', 'target1', 'hash1'))

    # Create savepoint
    cursor.execute("SAVEPOINT sp1")

    # Insert second record
    cursor.execute("""
        INSERT INTO mappings
        (source_id, source_event_uid, target_event_id, last_hash)
        VALUES (?, ?, ?, ?)
    """, (1, 'evt2', 'target2', 'hash2'))

    # Rollback to savepoint (removes evt2)
    cursor.execute("ROLLBACK TO sp1")

    # Commit transaction
    test_db_with_source.conn.commit()

    # Only first record should exist
    cursor.execute("SELECT COUNT(*) FROM mappings")
    count = cursor.fetchone()[0]
    assert count == 1

