"""Test SourceStore.get methods."""

import pytest
from unittest.mock import patch, MagicMock
from python.state.source_store import SourceStore


@patch('python.state.source_store.blob_to_credentials')
def test_source_get_success(mock_blob_to_creds, mock_database):
    """Test getting source by ID."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: {
        'id': 1, 'type': 'graph', 'calendar_id': 'cal-123',
        'name': 'Work', 'cred_blob': b'blob', 'active': 1
    }[key]
    mock_row.keys.return_value = ['id', 'type', 'calendar_id', 'name', 'cred_blob', 'active']

    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    mock_blob_to_creds.return_value = {'token': 'abc'}

    store = SourceStore(mock_database)
    result = store.get(1)

    assert result is not None
    assert result['credentials'] == {'token': 'abc'}


@patch('python.state.source_store.blob_to_credentials')
def test_source_get_not_found(mock_blob_to_creds, mock_database):
    """Test getting non-existent source."""
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = None

    store = SourceStore(mock_database)
    result = store.get(999)

    assert result is None


@patch('python.state.source_store.blob_to_credentials')
def test_source_get_active(mock_blob_to_creds, mock_database):
    """Test getting all active sources."""
    mock_rows = [MagicMock() for _ in range(2)]
    for i, row in enumerate(mock_rows):
        row.__getitem__ = lambda self, key, idx=i: {
            'id': idx+1, 'type': 'graph', 'cred_blob': b'blob'
        }.get(key, f'value-{idx}')
        row.keys.return_value = ['id', 'type', 'cred_blob']

    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows
    mock_blob_to_creds.return_value = {'token': 'test'}

    store = SourceStore(mock_database)
    results = store.get_active()

    assert len(results) == 2
