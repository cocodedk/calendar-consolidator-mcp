"""Test TargetStore.set functionality."""

import pytest
from unittest.mock import patch, Mock
from python.state.target_store import TargetStore


@patch('python.state.target_store.store_credentials')
@patch('python.state.target_store.credentials_to_blob')
def test_target_set_basic(mock_to_blob, mock_store_creds, mock_database):
    """Test setting target calendar."""
    mock_to_blob.return_value = b'mock-blob'
    store = TargetStore(mock_database)

    store.set('graph', 'target-123', 'Consolidated', {'token': 'abc'})

    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()
    mock_store_creds.assert_called_once_with('target-1', {'token': 'abc'})


@patch('python.state.target_store.store_credentials')
@patch('python.state.target_store.credentials_to_blob')
def test_target_set_replaces_existing(mock_to_blob, mock_store_creds, mock_database):
    """Test setting target replaces existing one."""
    mock_to_blob.return_value = b'mock-blob'
    store = TargetStore(mock_database)

    store.set('graph', 'target-1', 'First', {'token': '1'})
    store.set('graph', 'target-2', 'Second', {'token': '2'})

    conn = mock_database.connect()
    # Should use INSERT OR REPLACE
    assert 'INSERT OR REPLACE' in str(conn.execute.call_args_list[0])
