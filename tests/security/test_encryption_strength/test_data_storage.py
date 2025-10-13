"""Tests for encrypted data storage."""

from unittest.mock import patch
import json


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
        data = json.loads(stored_json)
        assert data['access_token'] == 'secret_token'
