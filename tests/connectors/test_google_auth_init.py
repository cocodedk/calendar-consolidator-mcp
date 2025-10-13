"""Test GoogleAuthenticator initialization and device flow."""

import pytest
from unittest.mock import Mock, patch
from python.connectors.google_auth import GoogleAuthenticator, CLIENT_ID


def test_google_authenticator_init_default():
    """GoogleAuthenticator initializes with default client_id."""
    auth = GoogleAuthenticator()
    assert auth.client_id == CLIENT_ID
    assert "calendar.readonly" in auth.scopes[0]
    assert "calendar.events" in auth.scopes[1]


def test_google_authenticator_init_custom_client():
    """GoogleAuthenticator accepts custom client_id and secret."""
    custom_id = "custom-client-123"
    custom_secret = "custom-secret-456"
    auth = GoogleAuthenticator(
        client_id=custom_id,
        client_secret=custom_secret
    )
    assert auth.client_id == custom_id
    assert auth.client_secret == custom_secret


@patch('python.connectors.google_auth.InstalledAppFlow')
def test_get_device_code_flow_success(mock_flow_class):
    """Device code flow returns verification_url."""
    mock_flow = Mock()
    mock_flow.authorization_url.return_value = (
        'https://accounts.google.com/o/oauth2/auth?code=ABC123',
        'state123'
    )
    mock_flow_class.from_client_config.return_value = mock_flow

    auth = GoogleAuthenticator()
    flow = auth.get_device_code_flow()

    assert 'verification_url' in flow
    assert 'flow_state' in flow
    assert 'accounts.google.com' in flow['verification_url']


@patch('python.connectors.google_auth.InstalledAppFlow')
def test_acquire_token_by_code_success(mock_flow_class):
    """Acquire token with authorization code returns tokens."""
    mock_creds = Mock()
    mock_creds.token = 'access_token_123'
    mock_creds.refresh_token = 'refresh_token_456'
    mock_creds.expiry = None

    mock_flow = Mock()
    mock_flow.credentials = mock_creds
    mock_flow_class.from_client_config.return_value = mock_flow

    auth = GoogleAuthenticator()
    result = auth.acquire_token_by_code('auth_code_123')

    assert result['access_token'] == 'access_token_123'
    assert result['refresh_token'] == 'refresh_token_456'
    mock_flow.fetch_token.assert_called_once_with(code='auth_code_123')
