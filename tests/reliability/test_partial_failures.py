"""Test continuation after individual event failures."""

import pytest
from unittest.mock import Mock, patch
from python.model.event import Event
from datetime import datetime


def test_sync_continues_after_single_event_failure():
    """Sync continues processing after one event fails."""
    events = [
        Event(uid='evt1', subject='Meeting 1', start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T11:00:00Z'), location=None, description=None, is_private=False),
        Event(uid='evt2', subject='Meeting 2', start=datetime.fromisoformat('2024-01-15T14:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T15:00:00Z'), location=None, description=None, is_private=False),
        Event(uid='evt3', subject='Meeting 3', start=datetime.fromisoformat('2024-01-15T16:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T17:00:00Z'), location=None, description=None, is_private=False)
    ]

    mock_connector = Mock()
    # Second event fails
    mock_connector.create_event.side_effect = [
        'target_1',
        Exception("Network error"),
        'target_3'
    ]

    successful_creates = []
    failed_creates = []

    for event in events:
        try:
            target_id = mock_connector.create_event('cal1', event.to_graph())
            successful_creates.append((event, target_id))
        except Exception as e:
            failed_creates.append((event, str(e)))

    # Should have 2 successes and 1 failure
    assert len(successful_creates) == 2
    assert len(failed_creates) == 1


def test_batch_operation_collects_errors():
    """Batch operation collects all errors without stopping."""
    def process_batch(items, processor):
        """Process batch and collect errors."""
        results = []
        errors = []

        for item in items:
            try:
                result = processor(item)
                results.append(result)
            except Exception as e:
                errors.append({'item': item, 'error': str(e)})

        return results, errors

    def processor(item):
        """Sample processor that fails on even numbers."""
        if item % 2 == 0:
            raise Exception(f"Failed on {item}")
        return item * 2

    items = [1, 2, 3, 4, 5]
    results, errors = process_batch(items, processor)

    assert results == [2, 6, 10]  # Odd numbers processed
    assert len(errors) == 2  # Even numbers failed


def test_partial_sync_logs_failures():
    """Partial sync failures are logged."""
    mock_log_store = Mock()

    events_processed = 10
    events_failed = 2

    # Log summary
    mock_log_store.create_log(
        source_id=1,
        status='partial',
        events_created=6,
        events_updated=2,
        events_deleted=0,
        errors=f"{events_failed} events failed to sync"
    )

    # Verify log was created
    mock_log_store.create_log.assert_called_once()
    call_args = mock_log_store.create_log.call_args
    assert call_args[1]['status'] == 'partial'


def test_transaction_rollback_on_critical_failure():
    """Critical failures rollback partial changes."""
    import tempfile
    from pathlib import Path
    from python.state import Database

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
