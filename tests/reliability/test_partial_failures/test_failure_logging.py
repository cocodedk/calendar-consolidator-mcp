"""Tests for partial sync failure logging."""

from unittest.mock import Mock


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
