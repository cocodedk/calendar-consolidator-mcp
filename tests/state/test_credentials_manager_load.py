"""
Tests for loading credentials from database.
"""

import pytest
from unittest.mock import patch, MagicMock
from python.state.credentials_manager import load_credentials


@pytest.fixture
def mock_db():
    """Mock database connection and cursor."""
    with patch('python.state.credentials_manager.get_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection
        yield mock_connection, mock_cursor


def test_load_credentials_success(mock_db):
    """Test that load_credentials returns decrypted dict."""
    mock_connection, mock_cursor = mock_db
    mock_row = {'value': 'encrypted_data'}
    mock_cursor.fetchone.return_value = mock_row

    expected_creds = {'client_id': 'test', 'client_secret': 'secret'}
    with patch('python.state.credentials_manager.decrypt_credentials') as mock_decrypt:
        mock_decrypt.return_value = expected_creds
        result = load_credentials('google')

        assert result == expected_creds
        mock_decrypt.assert_called_once_with('encrypted_data')


def test_load_credentials_not_found(mock_db):
    """Test that load_credentials returns None if missing."""
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None

    result = load_credentials('google')

    assert result is None


def test_load_credentials_decryption_called(mock_db):
    """Test that decryption is called when loading."""
    mock_connection, mock_cursor = mock_db
    mock_row = {'value': 'encrypted_string'}
    mock_cursor.fetchone.return_value = mock_row

    with patch('python.state.credentials_manager.decrypt_credentials') as mock_decrypt:
        mock_decrypt.return_value = {'key': 'value'}
        load_credentials('microsoft')

        mock_decrypt.assert_called_once_with('encrypted_string')


def test_load_credentials_database_error(mock_db):
    """Test that database errors are handled."""
    mock_connection, mock_cursor = mock_db
    mock_cursor.execute.side_effect = Exception('DB Error')

    result = load_credentials('google')

    assert result is None


def test_load_credentials_query_correct_key(mock_db):
    """Test that query uses correct settings key."""
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None

    load_credentials('icloud')

    call_args = mock_cursor.execute.call_args[0][1]
    assert call_args[0] == 'icloud_credentials'
