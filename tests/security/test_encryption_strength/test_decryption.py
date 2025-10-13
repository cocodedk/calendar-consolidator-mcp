"""Tests for decryption and credential retrieval."""

from unittest.mock import patch


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
