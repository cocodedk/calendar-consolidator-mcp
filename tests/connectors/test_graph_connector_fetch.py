"""Test GraphConnector event fetching operations."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta, timezone
from python.connectors.graph_connector import GraphConnector


@pytest.fixture
def valid_credentials():
    """Valid credentials fixture."""
    return {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }


@patch('python.connectors.graph_connector.connector.requests.get')
def test_list_calendars_success(mock_get, valid_credentials):
    """List calendars returns calendar info."""
    mock_response = Mock()
    mock_response.json.return_value = {
        'value': [
            {'id': 'cal1', 'name': 'Work', 'canEdit': True},
            {'id': 'cal2', 'name': 'Personal', 'canEdit': False}
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    calendars = connector.list_calendars()

    assert len(calendars) == 2
    assert calendars[0]['id'] == 'cal1'
    assert calendars[0]['name'] == 'Work'
    assert calendars[0]['canWrite'] is True


@patch('python.connectors.graph_connector.connector.requests.get')
def test_get_events_delta_initial_sync(mock_get, valid_credentials):
    """Get events delta for initial sync."""
    mock_response = Mock()
    mock_response.json.return_value = {
        'value': [
            {'id': 'event1', 'subject': 'Meeting 1'},
            {'id': 'event2', 'subject': 'Meeting 2'}
        ],
        '@odata.deltaLink': 'https://graph.microsoft.com/delta?token=abc123'
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    result = connector.get_events_delta('cal1')

    assert len(result['events']) == 2
    assert result['nextSyncToken'] is not None


@patch('python.connectors.graph_connector.connector.requests.get')
def test_get_events_delta_with_token(mock_get, valid_credentials):
    """Get events delta with existing sync token."""
    sync_token = 'https://graph.microsoft.com/delta?token=abc123'
    mock_response = Mock()
    mock_response.json.return_value = {
        'value': [{'id': 'event3', 'subject': 'New Event'}],
        '@odata.deltaLink': 'https://graph.microsoft.com/delta?token=xyz789'
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    connector = GraphConnector(valid_credentials)
    result = connector.get_events_delta('cal1', sync_token)

    # Verify get was called with the sync token
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[0][0] == sync_token
    assert 'headers' in call_args[1]
    assert len(result['events']) == 1
