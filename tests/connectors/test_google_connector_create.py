"""Test GoogleConnector event creation operations."""

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


@pytest.fixture
def sample_event():
    """Sample event data."""
    return {
        'summary': 'Test Meeting',
        'start': {'dateTime': '2025-01-15T10:00:00Z'},
        'end': {'dateTime': '2025-01-15T11:00:00Z'}
    }


@patch('python.connectors.google_connector.build')
def test_create_event_success(mock_build, valid_credentials, sample_event):
    """Create event returns event ID."""
    mock_service = Mock()
    mock_events = Mock()
    mock_insert = Mock()
    mock_insert.execute.return_value = {'id': 'event_123'}
    mock_events.insert.return_value = mock_insert
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    event_id = connector.create_event('cal1', sample_event)

    assert event_id == 'event_123'
    mock_events.insert.assert_called_with(
        calendarId='cal1',
        body=sample_event
    )


@patch('python.connectors.google_connector.build')
def test_create_event_with_attendees(mock_build, valid_credentials):
    """Create event with attendees."""
    event_data = {
        'summary': 'Team Meeting',
        'start': {'dateTime': '2025-01-15T14:00:00Z'},
        'end': {'dateTime': '2025-01-15T15:00:00Z'},
        'attendees': [
            {'email': 'user1@example.com'},
            {'email': 'user2@example.com'}
        ]
    }

    mock_service = Mock()
    mock_events = Mock()
    mock_events.insert().execute.return_value = {'id': 'event_456'}
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    event_id = connector.create_event('cal1', event_data)

    assert event_id == 'event_456'
    call_args = mock_events.insert.call_args
    assert call_args[1]['body']['attendees'] is not None

