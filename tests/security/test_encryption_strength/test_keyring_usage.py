"""Tests for keyring usage in encryption."""

from unittest.mock import patch


def test_encryption_uses_keyring():
    """Encryption uses system keyring for key storage."""
    from python.state.encryption import store_credentials

    credentials = {'access_token': 'token123'}

    with patch('python.state.encryption.keyring') as mock_keyring:
        mock_keyring.get_password.return_value = None

        store_credentials('user_id', credentials)

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
