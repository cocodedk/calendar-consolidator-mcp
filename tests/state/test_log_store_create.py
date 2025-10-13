"""Test LogStore.log_sync functionality."""

import pytest
from python.state.log_store import LogStore


def test_log_sync_success(mock_database):
    """Test logging successful sync."""
    store = LogStore(mock_database)
    
    log_id = store.log_sync(1, 'success', 5, 3, 1, duration_ms=2340)
    
    assert log_id == 1
    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()


def test_log_sync_error(mock_database):
    """Test logging failed sync."""
    store = LogStore(mock_database)
    
    log_id = store.log_sync(
        1, 'error', 0, 0, 0,
        error_message='API Error', duration_ms=500
    )
    
    assert log_id == 1
    conn = mock_database.connect()
    args = conn.execute.call_args[0]
    assert 'API Error' in args[1]


def test_log_sync_partial(mock_database):
    """Test logging partial sync."""
    store = LogStore(mock_database)
    
    log_id = store.log_sync(
        2, 'partial', 3, 2, 0,
        error_message='Some events failed'
    )
    
    assert log_id == 1


def test_log_sync_no_source(mock_database):
    """Test logging sync without source ID."""
    store = LogStore(mock_database)
    
    log_id = store.log_sync(None, 'success', 10, 0, 0)
    
    assert log_id == 1
    conn = mock_database.connect()
    args = conn.execute.call_args[0]
    assert args[1][0] is None

