"""Test basic syncing from Microsoft Graph to Google Calendar."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from python.sync.syncer import Syncer
from python.connectors import GraphConnector, GoogleConnector


@patch('python.connectors.GoogleConnector')
@patch('python.connectors.GraphConnector')
def test_sync_graph_source_to_google_target(mock_graph_class, mock_google_class):
    """Test syncing events from Microsoft Graph to Google Calendar."""
    # Setup mock source connector (Graph API)
    mock_source_connector = Mock(spec=GraphConnector)
    mock_source_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'graph-event-123',
            'subject': 'Team Meeting',
            'start': {'dateTime': '2025-01-15T10:00:00Z'},
            'end': {'dateTime': '2025-01-15T11:00:00Z'},
            'location': {'displayName': 'Conference Room A'},
            'bodyPreview': 'Discuss Q1 objectives',
            'isAllDay': False,
            'isCancelled': False
        }],
        'nextSyncToken': 'graph-token-456'
    }

    # Setup mock target connector (Google Calendar)
    mock_target_connector = Mock(spec=GoogleConnector)
    mock_target_connector.create_event.return_value = 'google-event-789'

    # Configure mock classes to return our mocks
    mock_graph_class.return_value = mock_source_connector
    mock_google_class.return_value = mock_target_connector

    # Setup config store
    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'source-graph-cal',
        'credentials': {'access_token': 'graph-token'},
        'sync_token': None
    }
    mock_config.target.get.return_value = {
        'type': 'google',
        'calendar_id': 'target-google-cal',
        'credentials': {'access_token': 'google-token', 'refresh_token': 'refresh'}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    # Run sync
    syncer = Syncer(mock_config)
    result = syncer.sync_once(1)

    # Verify sync was successful
    assert result['success'] is True
    assert result['created'] == 1
    assert result['updated'] == 0
    assert result['deleted'] == 0

    # Verify source connector was called
    mock_source_connector.get_events_delta.assert_called_once_with(
        'source-graph-cal', None
    )

    # Verify target connector received event in Google format
    mock_target_connector.create_event.assert_called_once()
    call_args = mock_target_connector.create_event.call_args

    assert call_args[0][0] == 'target-google-cal'
    event_data = call_args[0][1]

    # Verify Google Calendar format
    assert event_data['summary'] == 'Team Meeting'
    assert 'start' in event_data
    assert 'dateTime' in event_data['start']
    assert 'timeZone' in event_data['start']
    assert event_data['start']['timeZone'] == 'UTC'
    assert 'end' in event_data
    assert 'dateTime' in event_data['end']
    assert event_data['location'] == 'Conference Room A'
    assert event_data['description'] == 'Discuss Q1 objectives'

    # Verify mapping was created
    mock_config.mappings.create.assert_called_once()

    # Verify sync token was updated
    mock_config.sources.update_token.assert_called_once_with(1, 'graph-token-456')
