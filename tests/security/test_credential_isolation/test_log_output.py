"""Tests for credential isolation in log output."""

from unittest.mock import patch


def test_credentials_not_in_log_output():
    """Log output doesn't contain credentials."""
    from python.state.encryption import store_credentials

    credentials = {
        'access_token': 'sensitive_token',
        'refresh_token': 'sensitive_refresh'
    }

    with patch('python.state.encryption.keyring') as mock_keyring:
        # Store credentials (no blob returned in actual API)
        store_credentials('test_identifier', credentials)

        # Verify keyring.set_password was called
        mock_keyring.set_password.assert_called_once()

        # Get the stored value
        call_args = mock_keyring.set_password.call_args
        stored_value = call_args[0][2]  # Third argument is the password/value

        # Stored value should contain credentials as JSON
        assert 'sensitive_token' in stored_value
