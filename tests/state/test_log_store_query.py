"""Test LogStore query methods."""

import pytest
from unittest.mock import MagicMock
from python.state.log_store import LogStore


def test_get_recent_logs(mock_database):
    """Test getting recent logs."""
    mock_rows = [MagicMock() for _ in range(3)]
    for i, row in enumerate(mock_rows):
        row.__getitem__ = lambda self, key, idx=i: f'value-{idx}'
        row.keys.return_value = ['id', 'timestamp']

    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows

    store = LogStore(mock_database)
    results = store.get_recent(limit=50)

    assert len(results) == 3


def test_get_logs_for_source(mock_database):
    """Test getting logs for specific source."""
    mock_rows = [MagicMock()]
    mock_rows[0].__getitem__ = lambda self, key: 'value'
    mock_rows[0].keys.return_value = ['id']

    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows

    store = LogStore(mock_database)
    results = store.get_for_source(1, limit=10)

    assert len(results) == 1
    conn.execute.assert_called()


def test_get_recent_errors(mock_database):
    """Test getting recent error logs."""
    mock_rows = []
    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows

    store = LogStore(mock_database)
    results = store.get_recent_errors(limit=10)

    assert len(results) == 0


def test_get_statistics(mock_database):
    """Test getting sync statistics."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: {
        'total_syncs': 10, 'success_count': 8,
        'total_created': 50, 'total_updated': 20, 'total_deleted': 5
    }[key]
    mock_row.keys.return_value = ['total_syncs', 'success_count', 'total_created', 'total_updated', 'total_deleted']

    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row

    store = LogStore(mock_database)
    stats = store.get_statistics(days=7)

    assert stats['total_syncs'] == 10
    assert stats['success_count'] == 8
