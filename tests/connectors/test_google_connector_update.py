"""Test GoogleConnector event update operations."""

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


@patch('python.connectors.google_connector.build')
def test_update_event_success(mock_build, valid_credentials):
    """Update event modifies existing event."""
    updated_data = {
        'summary': 'Updated Meeting',
        'start': {'dateTime': '2025-01-15T11:00:00Z'},
        'end': {'dateTime': '2025-01-15T12:00:00Z'}
    }

    mock_service = Mock()
    mock_events = Mock()
    mock_update = Mock()
    mock_update.execute.return_value = {}
    mock_events.update.return_value = mock_update
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    connector.update_event('cal1', 'event_123', updated_data)

    mock_events.update.assert_called_with(
        calendarId='cal1',
        eventId='event_123',
        body=updated_data
    )


@patch('python.connectors.google_connector.build')
def test_update_event_partial_fields(mock_build, valid_credentials):
    """Update event with partial data."""
    partial_data = {'summary': 'New Title Only'}

    mock_service = Mock()
    mock_events = Mock()
    mock_events.update().execute.return_value = {}
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    connector.update_event('cal1', 'event_456', partial_data)

    call_args = mock_events.update.call_args
    assert call_args[1]['body']['summary'] == 'New Title Only'

