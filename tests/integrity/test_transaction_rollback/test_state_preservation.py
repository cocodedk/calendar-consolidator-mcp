"""Test transaction state preservation."""


def test_rollback_preserves_previous_state(test_db):
    """Rollback restores database to pre-transaction state."""
    cursor = test_db.conn.cursor()

    # Initial state
    cursor.execute("""
        INSERT INTO settings (key, value) VALUES ('test', 'initial')
    """)
    test_db.conn.commit()

    # Start transaction
    try:
        cursor.execute("BEGIN")
        cursor.execute("UPDATE settings SET value = 'modified' WHERE key = 'test'")

        # Simulate error
        raise Exception("Transaction failed")

        test_db.conn.commit()
    except Exception:
        test_db.conn.rollback()

    # Verify value wasn't changed
    cursor.execute("SELECT value FROM settings WHERE key = 'test'")
    value = cursor.fetchone()[0]
    assert value == 'initial'
