"""Test GraphConnector event deletion."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from python.connectors.graph_connector import GraphConnector


@pytest.fixture
def valid_credentials():
    """Valid credentials fixture."""
    return {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }


@patch('python.connectors.graph_connector.connector.requests.delete')
def test_delete_event_success(mock_delete, valid_credentials):
    """Delete event removes event from calendar."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_delete.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    connector.delete_event('cal1', 'event123')

    mock_delete.assert_called_once()
    call_args = mock_delete.call_args
    assert 'event123' in call_args[0][0]


@patch('python.connectors.graph_connector.connector.requests.delete')
def test_delete_event_with_auth(mock_delete, valid_credentials):
    """Delete event includes authorization header."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_delete.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    connector.delete_event('cal1', 'event456')

    call_args = mock_delete.call_args
    headers = call_args[1]['headers']
    assert 'Bearer access123' in headers['Authorization']


@patch('python.connectors.graph_connector.connector.requests.delete')
def test_delete_event_raises_on_error(mock_delete, valid_credentials):
    """Delete event raises exception on API error."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_delete.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    with pytest.raises(Exception, match="API Error"):
        connector.delete_event('cal1', 'event789')
