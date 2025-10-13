"""Test credential loading from keyring."""

import pytest
import json
from unittest.mock import patch
from python.state.encryption import load_credentials


@patch('python.state.encryption.keyring')
def test_load_credentials_success(mock_keyring):
    """Test loading credentials from keyring."""
    stored_data = {'access_token': 'token-123', 'refresh_token': 'refresh-456'}
    mock_keyring.get_password.return_value = json.dumps(stored_data)

    result = load_credentials('source-1')

    assert result == stored_data
    mock_keyring.get_password.assert_called_once_with(
        'calendar-consolidator-mcp', 'source-1'
    )


@patch('python.state.encryption.keyring')
def test_load_credentials_not_found(mock_keyring):
    """Test loading non-existent credentials returns None."""
    mock_keyring.get_password.return_value = None

    result = load_credentials('nonexistent')

    assert result is None


@patch('python.state.encryption.keyring')
def test_load_credentials_complex_data(mock_keyring):
    """Test loading complex credential structures."""
    complex_creds = {
        'tokens': {'access': 'a', 'refresh': 'r'},
        'expires': 12345,
        'scopes': ['calendar.read', 'calendar.write']
    }
    mock_keyring.get_password.return_value = json.dumps(complex_creds)

    result = load_credentials('source-2')

    assert result['tokens']['access'] == 'a'
    assert len(result['scopes']) == 2
