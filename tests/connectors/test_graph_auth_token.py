"""Test GraphAuthenticator token acquisition and refresh."""

import pytest
from unittest.mock import Mock, patch
from python.connectors.graph_auth import GraphAuthenticator


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_acquire_token_by_device_flow_success(mock_app_class):
    """Token acquisition returns access and refresh tokens."""
    mock_app = Mock()
    mock_app.acquire_token_by_device_flow.return_value = {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_in': 3600
    }
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    flow = {'device_code': 'device123'}
    result = auth.acquire_token_by_device_flow(flow)

    assert result['access_token'] == 'access123'
    assert result['refresh_token'] == 'refresh456'


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_acquire_token_by_device_flow_failure(mock_app_class):
    """Token acquisition raises exception on auth failure."""
    mock_app = Mock()
    mock_app.acquire_token_by_device_flow.return_value = {
        'error': 'authorization_pending',
        'error_description': 'User has not completed authentication'
    }
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    flow = {'device_code': 'device123'}
    with pytest.raises(Exception, match="Authentication failed"):
        auth.acquire_token_by_device_flow(flow)


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_refresh_token_success(mock_app_class):
    """Refresh token returns new access token."""
    mock_app = Mock()
    mock_app.get_accounts.return_value = []
    mock_app.acquire_token_by_refresh_token.return_value = {
        'access_token': 'new_access789',
        'expires_in': 3600
    }
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    result = auth.refresh_token('refresh456')

    assert result['access_token'] == 'new_access789'


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_refresh_token_failure(mock_app_class):
    """Refresh token raises exception when refresh fails."""
    mock_app = Mock()
    mock_app.get_accounts.return_value = []
    mock_app.acquire_token_by_refresh_token.return_value = {
        'error': 'invalid_grant'
    }
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    with pytest.raises(Exception, match="Token refresh failed"):
        auth.refresh_token('invalid_refresh')
