"""Test GoogleConnector event fetching operations."""

import pytest
from unittest.mock import Mock, patch, MagicMock
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
def test_list_calendars_success(mock_build, valid_credentials):
    """List calendars returns calendar info."""
    mock_service = Mock()
    mock_calendar_list = Mock()
    mock_calendar_list.list().execute.return_value = {
        'items': [
            {'id': 'cal1', 'summary': 'Work', 'accessRole': 'owner'},
            {'id': 'cal2', 'summary': 'Personal', 'accessRole': 'reader'}
        ]
    }
    mock_service.calendarList.return_value = mock_calendar_list
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    calendars = connector.list_calendars()

    assert len(calendars) == 2
    assert calendars[0]['id'] == 'cal1'
    assert calendars[0]['name'] == 'Work'
    assert calendars[0]['canWrite'] is True
    assert calendars[1]['canWrite'] is False


@patch('python.connectors.google_connector.service.build')
def test_get_events_delta_initial_sync(mock_build, valid_credentials):
    """Get events delta for initial sync."""
    mock_service = Mock()
    mock_events = Mock()
    mock_events.list().execute.return_value = {
        'items': [
            {'id': 'event1', 'summary': 'Meeting 1'},
            {'id': 'event2', 'summary': 'Meeting 2'}
        ],
        'nextSyncToken': 'sync_token_abc123'
    }
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    result = connector.get_events_delta('cal1')

    assert len(result['events']) == 2
    assert result['nextSyncToken'] == 'sync_token_abc123'


@patch('python.connectors.google_connector.service.build')
def test_get_events_delta_with_token(mock_build, valid_credentials):
    """Get events delta with existing sync token."""
    sync_token = 'sync_token_abc123'
    mock_service = Mock()
    mock_events = Mock()
    mock_events.list().execute.return_value = {
        'items': [{'id': 'event3', 'summary': 'New Event'}],
        'nextSyncToken': 'sync_token_xyz789'
    }
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    result = connector.get_events_delta('cal1', sync_token)

    assert len(result['events']) == 1
    mock_events.list.assert_called_with(calendarId='cal1', syncToken=sync_token)

