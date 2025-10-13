"""Test GraphConnector event update operations."""

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


@patch('python.connectors.graph_connector.requests.patch')
def test_update_event_success(mock_patch, valid_credentials):
    """Update event modifies existing event."""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_patch.return_value = mock_response
    
    connector = GraphConnector(valid_credentials)
    event_data = {'subject': 'Updated Meeting Title'}
    connector.update_event('cal1', 'event123', event_data)
    
    mock_patch.assert_called_once()
    call_args = mock_patch.call_args
    assert 'event123' in call_args[0][0]


@patch('python.connectors.graph_connector.requests.get')
def test_get_event_success(mock_get, valid_credentials):
    """Get event returns event data."""
    mock_response = Mock()
    mock_response.json.return_value = {
        'id': 'event123',
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00'}
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    connector = GraphConnector(valid_credentials)
    event = connector.get_event('cal1', 'event123')
    
    assert event is not None
    assert event['id'] == 'event123'
    assert event['subject'] == 'Meeting'


@patch('python.connectors.graph_connector.requests.get')
def test_get_event_not_found(mock_get, valid_credentials):
    """Get event returns None for missing event."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    connector = GraphConnector(valid_credentials)
    event = connector.get_event('cal1', 'missing_event')
    
    assert event is None

