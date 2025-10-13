"""Tests for encryption key rotation support."""

from unittest.mock import patch


def test_encryption_handles_key_rotation():
    """System supports updating stored credentials."""
    from python.state.encryption import store_credentials

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
