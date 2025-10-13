"""Test GraphConnector event creation."""

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


@pytest.fixture
def sample_event_data():
    """Sample event data."""
    return {
        'subject': 'Team Meeting',
        'start': {
            'dateTime': '2024-01-15T10:00:00',
            'timeZone': 'UTC'
        },
        'end': {
            'dateTime': '2024-01-15T11:00:00',
            'timeZone': 'UTC'
        }
    }


@patch('python.connectors.graph_connector.requests.post')
def test_create_event_success(mock_post, valid_credentials, sample_event_data):
    """Create event returns event ID."""
    mock_response = Mock()
    mock_response.json.return_value = {'id': 'new_event_123'}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response
    
    connector = GraphConnector(valid_credentials)
    event_id = connector.create_event('cal1', sample_event_data)
    
    assert event_id == 'new_event_123'
    mock_post.assert_called_once()


@patch('python.connectors.graph_connector.requests.post')
def test_create_event_with_headers(mock_post, valid_credentials, sample_event_data):
    """Create event includes proper headers."""
    mock_response = Mock()
    mock_response.json.return_value = {'id': 'event456'}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response
    
    connector = GraphConnector(valid_credentials)
    connector.create_event('cal1', sample_event_data)
    
    call_args = mock_post.call_args
    headers = call_args[1]['headers']
    assert 'Bearer access123' in headers['Authorization']
    assert headers['Content-Type'] == 'application/json'

