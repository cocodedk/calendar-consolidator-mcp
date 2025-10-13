"""Test GoogleConnector event deletion operations."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from python.connectors.google_connector import GoogleConnector


@pytest.fixture
def valid_credentials():
    """Valid credentials fixture."""
    return {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }


@patch('python.connectors.google_connector.service.build')
def test_delete_event_success(mock_build, valid_credentials):
    """Delete event removes event from calendar."""
    mock_service = Mock()
    mock_events = Mock()
    mock_delete = Mock()
    mock_delete.execute.return_value = {}
    mock_events.delete.return_value = mock_delete
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    connector.delete_event('cal1', 'event_123')

    mock_events.delete.assert_called_with(
        calendarId='cal1',
        eventId='event_123'
    )


@patch('python.connectors.google_connector.service.build')
def test_get_event_success(mock_build, valid_credentials):
    """Get event returns event data."""
    mock_service = Mock()
    mock_events = Mock()
    mock_events.get().execute.return_value = {
        'id': 'event_123',
        'summary': 'Test Meeting'
    }
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    event = connector.get_event('cal1', 'event_123')

    assert event['id'] == 'event_123'
    assert event['summary'] == 'Test Meeting'


@patch('python.connectors.google_connector.service.build')
def test_get_event_not_found(mock_build, valid_credentials):
    """Get event returns None for non-existent event."""
    mock_service = Mock()
    mock_events = Mock()
    mock_events.get().execute.side_effect = Exception("Event not found")
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    event = connector.get_event('cal1', 'nonexistent')

    assert event is None

