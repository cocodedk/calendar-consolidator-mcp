"""Test SettingsStore.set methods."""

import pytest
from python.state.settings_store import SettingsStore


def test_settings_set_basic(mock_database):
    """Test setting a value."""
    store = SettingsStore(mock_database)
    
    store.set('sync_interval', '10')
    
    conn = mock_database.connect()
    conn.execute.assert_called()
    conn.commit.assert_called_once()


def test_settings_set_bool_true(mock_database):
    """Test setting boolean (true)."""
    store = SettingsStore(mock_database)
    
    store.set_bool('continuous_sync', True)
    
    conn = mock_database.connect()
    args = conn.execute.call_args[0]
    assert 'true' in args[1]


def test_settings_set_bool_false(mock_database):
    """Test setting boolean (false)."""
    store = SettingsStore(mock_database)
    
    store.set_bool('continuous_sync', False)
    
    conn = mock_database.connect()
    args = conn.execute.call_args[0]
    assert 'false' in args[1]


def test_settings_set_int(mock_database):
    """Test setting integer value."""
    store = SettingsStore(mock_database)
    
    store.set_int('max_retries', 5)
    
    conn = mock_database.connect()
    args = conn.execute.call_args[0]
    assert '5' in args[1]

