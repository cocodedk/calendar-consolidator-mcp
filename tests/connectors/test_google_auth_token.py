"""Test GoogleAuthenticator token refresh operations."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from python.connectors.google_auth import GoogleAuthenticator


@patch('python.connectors.google_auth.Request')
@patch('python.connectors.google_auth.Credentials')
def test_refresh_token_success(mock_creds_class, mock_request):
    """Refresh token returns new access token."""
    mock_creds = Mock()
    mock_creds.token = 'new_access_token'
    mock_creds.refresh_token = 'refresh_token_456'
    mock_creds.expiry = datetime.utcnow() + timedelta(hours=1)
    mock_creds_class.return_value = mock_creds

    auth = GoogleAuthenticator()
    result = auth.refresh_token('refresh_token_456')

    assert result['access_token'] == 'new_access_token'
    assert result['refresh_token'] == 'refresh_token_456'
    assert 'expires_at' in result
    mock_creds.refresh.assert_called_once()


@patch('python.connectors.google_auth.Request')
@patch('python.connectors.google_auth.Credentials')
def test_refresh_token_preserves_refresh_token(mock_creds_class, mock_request):
    """Refresh token preserves original refresh token if not returned."""
    mock_creds = Mock()
    mock_creds.token = 'new_access_token'
    mock_creds.refresh_token = None  # Some providers don't return new one
    mock_creds.expiry = None
    mock_creds_class.return_value = mock_creds

    auth = GoogleAuthenticator()
    result = auth.refresh_token('original_refresh_token')

    assert result['refresh_token'] == 'original_refresh_token'


@patch('python.connectors.google_auth.Request')
@patch('python.connectors.google_auth.Credentials')
def test_refresh_token_failure(mock_creds_class, mock_request):
    """Refresh token raises exception on failure."""
    mock_creds = Mock()
    mock_creds.refresh.side_effect = Exception("Token expired")
    mock_creds_class.return_value = mock_creds

    auth = GoogleAuthenticator()
    with pytest.raises(Exception):
        auth.refresh_token('invalid_token')

