"""Test SettingsStore.get_all functionality."""

import pytest
from unittest.mock import MagicMock
from python.state.settings_store import SettingsStore


def test_settings_get_all_empty(mock_database):
    """Test getting all settings when none exist."""
    conn = mock_database.connect()
    conn.execute().fetchall.return_value = []
    
    store = SettingsStore(mock_database)
    result = store.get_all()
    
    assert result == {}


def test_settings_get_all_multiple(mock_database):
    """Test getting all settings."""
    mock_rows = []
    for key, val in [('setting1', 'value1'), ('setting2', 'value2')]:
        row = MagicMock()
        row.__getitem__ = lambda self, k, key=key, val=val: {'key': key, 'value': val}[k]
        row.keys.return_value = ['key', 'value']
        mock_rows.append(row)
    
    conn = mock_database.connect()
    conn.execute().fetchall.return_value = mock_rows
    
    store = SettingsStore(mock_database)
    result = store.get_all()
    
    assert len(result) == 2
    assert 'setting1' in result
    assert 'setting2' in result

