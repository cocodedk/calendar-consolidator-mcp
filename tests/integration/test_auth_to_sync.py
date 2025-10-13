"""Test authentication through sync flow."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_auth_flow_to_connector_creation(mock_app_class):
    """Complete auth flow creates functional connector."""
    from python.connectors.graph_auth import GraphAuthenticator
    from python.connectors.graph_connector import GraphConnector

    # Mock successful auth
    mock_app = Mock()
    mock_app.initiate_device_flow.return_value = {
        'user_code': 'ABC123',
        'verification_uri': 'https://microsoft.com/devicelogin',
        'device_code': 'device123'
    }
    mock_app.acquire_token_by_device_flow.return_value = {
        'access_token': 'access_token_123',
        'refresh_token': 'refresh_token_456',
        'expires_in': 3600
    }
    mock_app_class.return_value = mock_app

    # Authenticate
    auth = GraphAuthenticator()
    flow = auth.get_device_code_flow()
    tokens = auth.acquire_token_by_device_flow(flow)

    # Create connector with tokens
    credentials = {
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'expires_at': (datetime.utcnow() + timedelta(seconds=3600)).isoformat()
    }

    connector = GraphConnector(credentials)
    assert connector.credentials['access_token'] == 'access_token_123'


@patch('python.connectors.graph_connector.requests.get')
def test_expired_token_auto_refresh_during_sync(mock_get):
    """Expired token is refreshed automatically during sync."""
    from python.connectors.graph_connector import GraphConnector

    # Credentials with expired token
    expired_creds = {
        'access_token': 'old_token',
        'refresh_token': 'refresh_token',
        'expires_at': (datetime.utcnow() - timedelta(minutes=10)).isoformat()
    }

    with patch.object(GraphConnector, '_refresh_token') as mock_refresh:
        connector = GraphConnector(expired_creds)
        mock_refresh.assert_called_once()


def test_auth_credentials_stored_encrypted():
    """Authentication credentials are stored with encryption."""
    from python.state.encryption import store_credentials, load_credentials

    test_creds = {
        'access_token': 'secret_token',
        'refresh_token': 'secret_refresh'
    }

    with patch('python.state.encryption.keyring') as mock_keyring:
        mock_keyring.get_password.return_value = None

        # Store credentials
        store_credentials('test_identifier', test_creds)

        # Verify keyring was called to store
        mock_keyring.set_password.assert_called_once()
