"""Test SourceStore update operations."""

import pytest
from unittest.mock import patch
from python.state.source_store import SourceStore


def test_source_update_token(mock_database):
    """Test updating sync token for source."""
    store = SourceStore(mock_database)

    store.update_token(1, 'new-sync-token-abc')

    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()


def test_source_set_active(mock_database):
    """Test setting source active status."""
    store = SourceStore(mock_database)

    store.set_active(1, False)

    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()


@patch('python.state.source_store.delete_credentials')
def test_source_remove(mock_delete_creds, mock_database):
    """Test removing source and credentials."""
    store = SourceStore(mock_database)

    store.remove(1)

    mock_delete_creds.assert_called_once_with('source-1')
    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()
