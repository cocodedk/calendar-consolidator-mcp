"""Test TargetStore.get methods."""

import pytest
from unittest.mock import patch, MagicMock
from python.state.target_store import TargetStore


@patch('python.state.target_store.blob_to_credentials')
def test_target_get_success(mock_blob_to_creds, mock_database):
    """Test getting target calendar."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: {
        'id': 1, 'type': 'graph', 'calendar_id': 'target-123',
        'name': 'Consolidated', 'cred_blob': b'blob'
    }[key]
    mock_row.keys.return_value = ['id', 'type', 'calendar_id', 'name', 'cred_blob']

    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    mock_blob_to_creds.return_value = {'token': 'abc'}

    store = TargetStore(mock_database)
    result = store.get()

    assert result is not None
    assert result['credentials'] == {'token': 'abc'}
    assert result['type'] == 'graph'


@patch('python.state.target_store.blob_to_credentials')
def test_target_get_not_set(mock_blob_to_creds, mock_database):
    """Test getting target when none is set."""
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = None

    store = TargetStore(mock_database)
    result = store.get()

    assert result is None


def test_target_exists_true(mock_database):
    """Test exists when target is configured."""
    mock_row = {'count': 1}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row

    store = TargetStore(mock_database)
    result = store.exists()

    assert result is True


def test_target_exists_false(mock_database):
    """Test exists when target is not configured."""
    mock_row = {'count': 0}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row

    store = TargetStore(mock_database)
    result = store.exists()

    assert result is False
