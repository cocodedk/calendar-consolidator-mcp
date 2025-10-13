"""
Tests for masked credential retrieval and deletion.
"""

import pytest
from unittest.mock import patch, MagicMock
from python.state.credentials_manager import (
    get_masked_credentials,
    delete_credentials
)


def test_get_masked_credentials_masks_secrets():
    """Test that sensitive fields are masked."""
    creds = {
        'client_id': '12345',
        'client_secret': 'GOCSPX-secret123456'
    }

    with patch('python.state.credentials_manager.load_credentials', return_value=creds):
        with patch('python.state.credentials_manager.mask_secret', return_value='GOC***...***456'):
            result = get_masked_credentials('google')

            assert result['client_id'] == '12345'
            assert result['client_secret'] == 'GOC***...***456'


def test_get_masked_credentials_preserves_ids():
    """Test that IDs are not masked."""
    creds = {
        'client_id': 'test_client_id',
        'tenant_id': 'test_tenant_id',
        'client_secret': 'secret_value'
    }

    with patch('python.state.credentials_manager.load_credentials', return_value=creds):
        with patch('python.state.credentials_manager.mask_secret', return_value='***'):
            result = get_masked_credentials('microsoft')

            assert result['client_id'] == 'test_client_id'
            assert result['tenant_id'] == 'test_tenant_id'
            assert result['client_secret'] == '***'


def test_get_masked_credentials_not_found():
    """Test that None is returned if credentials don't exist."""
    with patch('python.state.credentials_manager.load_credentials', return_value=None):
        result = get_masked_credentials('google')

        assert result is None


@pytest.fixture
def mock_db():
    """Mock database connection."""
    with patch('python.state.credentials_manager.get_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_conn.return_value = mock_connection
        yield mock_connection, mock_cursor


def test_delete_credentials_success(mock_db):
    """Test that credentials are deleted from database."""
    mock_connection, mock_cursor = mock_db

    result = delete_credentials('google')

    assert result is True
    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_called_once()


def test_delete_credentials_database_error(mock_db):
    """Test that database errors are handled."""
    mock_connection, mock_cursor = mock_db
    mock_cursor.execute.side_effect = Exception('DB Error')

    result = delete_credentials('google')

    assert result is False
