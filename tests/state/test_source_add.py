"""Test SourceStore.add functionality."""

import pytest
from unittest.mock import patch, Mock, MagicMock
from python.state.source_store import SourceStore


@patch('python.state.source_store.store_credentials')
@patch('python.state.source_store.credentials_to_blob')
def test_source_add_basic(mock_to_blob, mock_store_creds, mock_database):
    """Test adding a new source calendar."""
    mock_to_blob.return_value = b'mock-blob'
    store = SourceStore(mock_database)

    source_id = store.add(
        'graph', 'calendar-123', 'Work Calendar',
        {'token': 'abc'}, active=True
    )

    assert source_id == 1
    mock_store_creds.assert_called_once_with('source-1', {'token': 'abc'})


@patch('python.state.source_store.store_credentials')
@patch('python.state.source_store.credentials_to_blob')
def test_source_add_default_active(mock_to_blob, mock_store_creds, mock_database):
    """Test adding source with default active=True."""
    mock_to_blob.return_value = b'mock-blob'
    store = SourceStore(mock_database)

    source_id = store.add('graph', 'cal-456', 'Calendar', {'token': 'xyz'})

    assert source_id == 1
    conn = mock_database.connect()
    conn.execute.assert_called()


@patch('python.state.source_store.store_credentials')
@patch('python.state.source_store.credentials_to_blob')
def test_source_add_inactive(mock_to_blob, mock_store_creds, mock_database):
    """Test adding inactive source."""
    mock_to_blob.return_value = b'mock-blob'
    store = SourceStore(mock_database)

    source_id = store.add(
        'graph', 'cal-789', 'Inactive Cal',
        {'token': 'def'}, active=False
    )

    assert source_id == 1
