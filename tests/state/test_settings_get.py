"""Test SettingsStore.get methods."""

import pytest
from unittest.mock import MagicMock
from python.state.settings_store import SettingsStore


def test_settings_get_existing(mock_database):
    """Test getting existing setting."""
    mock_row = {'value': '5'}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    
    store = SettingsStore(mock_database)
    result = store.get('sync_interval_minutes')
    
    assert result == '5'


def test_settings_get_not_found(mock_database):
    """Test getting non-existent setting."""
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = None
    
    store = SettingsStore(mock_database)
    result = store.get('nonexistent')
    
    assert result is None


def test_settings_get_with_default(mock_database):
    """Test getting setting with default value."""
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = None
    
    store = SettingsStore(mock_database)
    result = store.get('nonexistent', default='10')
    
    assert result == '10'


def test_settings_get_bool_true(mock_database):
    """Test getting boolean setting (true)."""
    mock_row = {'value': 'true'}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    
    store = SettingsStore(mock_database)
    result = store.get_bool('continuous_sync')
    
    assert result is True


def test_settings_get_bool_false(mock_database):
    """Test getting boolean setting (false)."""
    mock_row = {'value': 'false'}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    
    store = SettingsStore(mock_database)
    result = store.get_bool('continuous_sync')
    
    assert result is False


def test_settings_get_int(mock_database):
    """Test getting integer setting."""
    mock_row = {'value': '42'}
    conn = mock_database.connect()
    conn.execute().fetchone.return_value = mock_row
    
    store = SettingsStore(mock_database)
    result = store.get_int('max_retries')
    
    assert result == 42

