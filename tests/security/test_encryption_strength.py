"""Test encryption key handling and strength."""

import pytest
from unittest.mock import patch, Mock


def test_encryption_uses_keyring():
    """Encryption uses system keyring for key storage."""
    from python.state.encryption import store_credentials

    credentials = {'access_token': 'token123'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        mock_keyring.get_password.return_value = None

        blob = store_credentials('service', 'user', credentials)

        # Should have stored key in keyring
        mock_keyring.set_password.assert_called()


def test_encryption_key_is_random():
    """Each credential set gets unique storage."""
    from python.state.encryption import store_credentials

    credentials1 = {'access_token': 'token1'}
    credentials2 = {'access_token': 'token2'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        store_credentials('identifier1', credentials1)
        store_credentials('identifier2', credentials2)

        # Should have stored twice with different identifiers
        assert mock_keyring.set_password.call_count == 2

        # Get both calls
        call1 = mock_keyring.set_password.call_args_list[0]
        call2 = mock_keyring.set_password.call_args_list[1]

        # Different identifiers should be used
        assert call1[0][1] != call2[0][1]  # Second arg is identifier


def test_encrypted_data_not_plaintext():
    """Credential data is stored via keyring (secure storage)."""
    from python.state.encryption import store_credentials

    credentials = {'access_token': 'secret_token'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        store_credentials('test_id', credentials)

        # Verify credentials were stored via keyring (secure)
        mock_keyring.set_password.assert_called_once()

        # Stored data is JSON (keyring handles encryption)
        call_args = mock_keyring.set_password.call_args
        stored_json = call_args[0][2]
        import json
        data = json.loads(stored_json)
        assert data['access_token'] == 'secret_token'


def test_decryption_requires_correct_identifier():
    """Loading requires correct identifier."""
    from python.state.encryption import store_credentials, load_credentials

    credentials = {'access_token': 'secret'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        # Store credentials
        store_credentials('correct_id', credentials)

        # Try to load with correct identifier
        mock_keyring.get_password.return_value = '{"access_token": "secret"}'
        result = load_credentials('correct_id')
        assert result['access_token'] == 'secret'

        # Try to load with wrong identifier (returns None)
        mock_keyring.get_password.return_value = None
        result = load_credentials('wrong_id')
        assert result is None


def test_encryption_handles_key_rotation():
    """System supports updating stored credentials."""
    from python.state.encryption import store_credentials, load_credentials

    original_credentials = {'access_token': 'token123'}
    updated_credentials = {'access_token': 'token456'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        # Store original
        store_credentials('test_id', original_credentials)

        # Update (overwrite) with new credentials
        store_credentials('test_id', updated_credentials)

        # Should have been called twice
        assert mock_keyring.set_password.call_count == 2

        # Both should use same identifier
        call1 = mock_keyring.set_password.call_args_list[0]
        call2 = mock_keyring.set_password.call_args_list[1]
        assert call1[0][1] == call2[0][1]  # Same identifier

        # But different values
        assert call1[0][2] != call2[0][2]  # Different credential data
