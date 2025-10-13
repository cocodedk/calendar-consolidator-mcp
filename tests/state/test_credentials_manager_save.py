"""
Tests for saving credentials to database.
"""

import pytest
from unittest.mock import patch, MagicMock
from python.state.credentials_manager import save_credentials


@pytest.fixture
def mock_db():
    """Mock database connection and cursor."""
    with patch('python.state.credentials_manager.get_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection
        yield mock_connection, mock_cursor


def test_save_credentials_success(mock_db):
    """Test that save_credentials saves encrypted data."""
    mock_connection, mock_cursor = mock_db
    credentials = {'client_id': 'test_id', 'client_secret': 'test_secret'}

    with patch('python.state.credentials_manager.encrypt_credentials') as mock_encrypt:
        mock_encrypt.return_value = 'encrypted_data'
        result = save_credentials('google', credentials)

        assert result is True
        mock_encrypt.assert_called_once_with(credentials)
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()


def test_save_credentials_upsert(mock_db):
    """Test that save_credentials updates existing credentials."""
    mock_connection, mock_cursor = mock_db
    credentials = {'client_id': 'new_id'}

    with patch('python.state.credentials_manager.encrypt_credentials', return_value='encrypted'):
        save_credentials('microsoft', credentials)

        # Check that UPSERT SQL is used
        call_args = mock_cursor.execute.call_args[0][0]
        assert 'INSERT INTO settings' in call_args
        assert 'ON CONFLICT' in call_args
        assert 'DO UPDATE SET' in call_args


def test_save_credentials_encryption_called(mock_db):
    """Test that encryption is called before saving."""
    mock_connection, mock_cursor = mock_db
    credentials = {'key': 'value'}

    with patch('python.state.credentials_manager.encrypt_credentials') as mock_encrypt:
        mock_encrypt.return_value = 'encrypted_result'
        save_credentials('google', credentials)

        mock_encrypt.assert_called_once_with(credentials)


def test_save_credentials_database_error(mock_db):
    """Test that database errors are handled."""
    mock_connection, mock_cursor = mock_db
    mock_cursor.execute.side_effect = Exception('DB Error')

    result = save_credentials('google', {'key': 'value'})

    assert result is False


def test_save_credentials_provider_in_key(mock_db):
    """Test that provider name is used in settings key."""
    mock_connection, mock_cursor = mock_db

    with patch('python.state.credentials_manager.encrypt_credentials', return_value='enc'):
        save_credentials('icloud', {'key': 'value'})

        call_args = mock_cursor.execute.call_args[0][1]
        assert call_args[0] == 'icloud_credentials'
