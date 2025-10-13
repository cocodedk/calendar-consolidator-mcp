"""Test MappingStore update operations."""

import pytest
from python.state.mapping_store import MappingStore


def test_mapping_update_hash(mock_database):
    """Test updating mapping hash."""
    store = MappingStore(mock_database)

    store.update_hash(1, 'uid-123', 'new-hash-xyz')

    conn = mock_database.connect()
    conn.execute.assert_called()
    args = conn.execute.call_args[0]
    assert 'UPDATE mappings' in args[0]
    assert 'new-hash-xyz' in args[1]
    conn.commit.assert_called_once()


def test_mapping_delete(mock_database):
    """Test deleting mapping."""
    store = MappingStore(mock_database)

    store.delete(1, 'uid-to-delete')

    conn = mock_database.connect()
    conn.execute.assert_called()
    args = conn.execute.call_args[0]
    assert 'DELETE FROM mappings' in args[0]
    assert args[1] == (1, 'uid-to-delete')
    conn.commit.assert_called_once()


def test_mapping_delete_multiple(mock_database):
    """Test deleting multiple mappings."""
    store = MappingStore(mock_database)

    store.delete(1, 'uid-1')
    store.delete(1, 'uid-2')

    conn = mock_database.connect()
    assert conn.execute.call_count == 2
    assert conn.commit.call_count == 2
