"""Test MappingStore.get methods."""

import pytest
from unittest.mock import MagicMock
from python.state.mapping_store import MappingStore


def test_mapping_get_success(mock_database):
    """Test getting mapping by source ID and UID."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: {
        'source_id': 1, 'source_event_uid': 'uid-123',
        'target_event_id': 'target-456', 'last_hash': 'hash-abc'
    }[key]
    mock_row.keys.return_value = ['source_id', 'source_event_uid', 'target_event_id', 'last_hash']

    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row

    store = MappingStore(mock_database)
    result = store.get(1, 'uid-123')

    assert result is not None
    assert result['target_event_id'] == 'target-456'


def test_mapping_get_not_found(mock_database):
    """Test getting non-existent mapping."""
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = None

    store = MappingStore(mock_database)
    result = store.get(1, 'nonexistent-uid')

    assert result is None


def test_mapping_get_all_for_source(mock_database):
    """Test getting all mappings for a source."""
    mock_rows = []
    for i in range(3):
        row = MagicMock()
        row.__getitem__ = lambda self, key, idx=i: f'value-{idx}'
        row.keys.return_value = ['source_event_uid']
        mock_rows.append(row)

    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows

    store = MappingStore(mock_database)
    results = store.get_all_for_source(1)

    assert len(results) == 3


def test_mapping_count_for_source(mock_database):
    """Test counting mappings for a source."""
    mock_row = {'count': 42}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row

    store = MappingStore(mock_database)
    count = store.count_for_source(1)

    assert count == 42
