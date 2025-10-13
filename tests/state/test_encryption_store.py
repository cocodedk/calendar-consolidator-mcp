"""Test credential storage with keyring."""

import pytest
from unittest.mock import patch, Mock
from python.state.encryption import store_credentials


@patch('python.state.encryption.keyring')
def test_store_credentials_basic(mock_keyring):
    """Test storing credentials in keyring."""
    credentials = {
        'access_token': 'token-abc',
        'refresh_token': 'refresh-xyz'
    }

    store_credentials('source-1', credentials)

    mock_keyring.set_password.assert_called_once()
    args = mock_keyring.set_password.call_args[0]
    assert args[0] == 'calendar-consolidator-mcp'
    assert args[1] == 'source-1'
    assert 'token-abc' in args[2]


@patch('python.state.encryption.keyring')
def test_store_credentials_different_identifiers(mock_keyring):
    """Test storing credentials with different identifiers."""
    creds1 = {'token': 'value1'}
    creds2 = {'token': 'value2'}

    store_credentials('source-1', creds1)
    store_credentials('target-1', creds2)

    assert mock_keyring.set_password.call_count == 2
    call_ids = [call[0][1] for call in mock_keyring.set_password.call_args_list]
    assert 'source-1' in call_ids
    assert 'target-1' in call_ids


@patch('python.state.encryption.keyring')
def test_store_credentials_overwrites(mock_keyring):
    """Test storing credentials overwrites existing."""
    creds = {'token': 'new-value'}

    store_credentials('source-1', creds)
    store_credentials('source-1', creds)

    assert mock_keyring.set_password.call_count == 2
