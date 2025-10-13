"""Test GraphConnector error handling (429, 401, 500)."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import requests
from python.connectors.graph_connector import GraphConnector


@pytest.fixture
def valid_credentials():
    """Valid credentials fixture."""
    return {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }


@patch('python.connectors.graph_connector.requests.get')
def test_api_error_401_unauthorized(mock_get, valid_credentials):
    """API raises exception on 401 unauthorized."""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
    mock_get.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    with pytest.raises(requests.HTTPError):
        connector.list_calendars()


@patch('python.connectors.graph_connector.requests.get')
def test_api_error_429_rate_limit(mock_get, valid_credentials):
    """API raises exception on 429 rate limit."""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = requests.HTTPError("429 Too Many Requests")
    mock_get.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    with pytest.raises(requests.HTTPError):
        connector.get_events_delta('cal1')


@patch('python.connectors.graph_connector.requests.post')
def test_api_error_500_server_error(mock_post, valid_credentials):
    """API raises exception on 500 server error."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Internal Server Error")
    mock_post.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    with pytest.raises(requests.HTTPError):
        connector.create_event('cal1', {'subject': 'Test'})


@patch('python.connectors.graph_connector.requests.get')
def test_expired_token_refreshes_automatically(mock_get, valid_credentials):
    """Expired token triggers automatic refresh before API call."""
    expired_creds = {
        'access_token': 'old_token',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() - timedelta(minutes=10)).isoformat()
    }

    with patch.object(GraphConnector, '_refresh_token') as mock_refresh:
        connector = GraphConnector(expired_creds)
        mock_refresh.assert_called_once()
