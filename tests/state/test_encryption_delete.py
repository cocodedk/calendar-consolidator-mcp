"""Test credential deletion from keyring."""

import pytest
from unittest.mock import patch, Mock
from python.state.encryption import delete_credentials


@patch('python.state.encryption.keyring')
def test_delete_credentials_success(mock_keyring):
    """Test deleting credentials from keyring."""
    delete_credentials('source-1')

    mock_keyring.delete_password.assert_called_once_with(
        'calendar-consolidator-mcp', 'source-1'
    )


@patch('python.state.encryption.keyring')
def test_delete_credentials_not_found(mock_keyring):
    """Test deleting non-existent credentials doesn't raise error."""
    # Create a custom exception class
    class PasswordDeleteError(Exception):
        pass

    mock_keyring.delete_password.side_effect = PasswordDeleteError()
    mock_keyring.errors = Mock()
    mock_keyring.errors.PasswordDeleteError = PasswordDeleteError

    # Should not raise exception
    delete_credentials('nonexistent')


@patch('python.state.encryption.keyring')
def test_delete_credentials_multiple(mock_keyring):
    """Test deleting multiple credentials."""
    delete_credentials('source-1')
    delete_credentials('source-2')
    delete_credentials('target-1')

    assert mock_keyring.delete_password.call_count == 3
