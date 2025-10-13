"""Test MappingStore.create functionality."""

import pytest
from python.state.mapping_store import MappingStore


def test_mapping_create_basic(mock_database):
    """Test creating a new event mapping."""
    store = MappingStore(mock_database)

    store.create(1, 'source-uid-123', 'target-id-456', 'hash-abc')

    conn = mock_database.connect()
    conn.execute.assert_called()
    args = conn.execute.call_args[0]
    assert 'INSERT INTO mappings' in args[0]
    assert args[1] == (1, 'source-uid-123', 'target-id-456', 'hash-abc')
    conn.commit.assert_called_once()


def test_mapping_create_multiple(mock_database):
    """Test creating multiple mappings."""
    store = MappingStore(mock_database)

    store.create(1, 'uid-1', 'target-1', 'hash-1')
    store.create(1, 'uid-2', 'target-2', 'hash-2')

    conn = mock_database.connect()
    assert conn.execute.call_count == 2
    assert conn.commit.call_count == 2


def test_mapping_create_different_sources(mock_database):
    """Test creating mappings for different sources."""
    store = MappingStore(mock_database)

    store.create(1, 'uid-a', 'target-a', 'hash-a')
    store.create(2, 'uid-b', 'target-b', 'hash-b')

    conn = mock_database.connect()
    calls = conn.execute.call_args_list
    assert calls[0][0][1][0] == 1
    assert calls[1][0][1][0] == 2
