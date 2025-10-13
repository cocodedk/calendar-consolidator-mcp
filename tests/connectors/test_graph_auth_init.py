"""Test GraphAuthenticator initialization and device flow."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from python.connectors.graph_auth import GraphAuthenticator, CLIENT_ID


def test_graph_authenticator_init_default():
    """GraphAuthenticator initializes with default client_id."""
    auth = GraphAuthenticator()
    assert auth.client_id == CLIENT_ID
    assert auth.authority == "https://login.microsoftonline.com/common"
    assert "Calendars.ReadWrite" in auth.scopes


def test_graph_authenticator_init_custom_client():
    """GraphAuthenticator accepts custom client_id."""
    custom_id = "custom-client-123"
    auth = GraphAuthenticator(client_id=custom_id)
    assert auth.client_id == custom_id


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_get_device_code_flow_success(mock_app_class):
    """Device code flow returns user_code and verification_uri."""
    mock_app = Mock()
    mock_app.initiate_device_flow.return_value = {
        'user_code': 'ABC123',
        'verification_uri': 'https://microsoft.com/devicelogin',
        'device_code': 'device123',
        'expires_in': 900
    }
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    flow = auth.get_device_code_flow()

    assert flow['user_code'] == 'ABC123'
    assert 'verification_uri' in flow
    mock_app.initiate_device_flow.assert_called_once()


@patch('python.connectors.graph_auth.msal.PublicClientApplication')
def test_get_device_code_flow_failure(mock_app_class):
    """Device code flow raises exception on failure."""
    mock_app = Mock()
    mock_app.initiate_device_flow.return_value = {'error': 'failed'}
    mock_app_class.return_value = mock_app

    auth = GraphAuthenticator()
    with pytest.raises(Exception, match="Failed to create device flow"):
        auth.get_device_code_flow()
