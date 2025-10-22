"""Test syncing all-day events from Graph to Google."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer
from python.connectors import GraphConnector, GoogleConnector


@patch('python.connectors.GoogleConnector')
@patch('python.connectors.GraphConnector')
def test_sync_graph_to_google_all_day_event(mock_graph_class, mock_google_class):
    """Test syncing all-day event from Graph to Google."""
    # Setup mock source with all-day event
    mock_source_connector = Mock(spec=GraphConnector)
    mock_source_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'graph-allday-123',
            'subject': 'Conference Day',
            'start': {'dateTime': '2025-01-20T00:00:00Z'},
            'end': {'dateTime': '2025-01-21T00:00:00Z'},
            'isAllDay': True,
            'isCancelled': False
        }],
        'nextSyncToken': 'token-abc'
    }

    # Setup mock target
    mock_target_connector = Mock(spec=GoogleConnector)
    mock_target_connector.create_event.return_value = 'google-allday-456'

    # Configure mock classes
    mock_graph_class.return_value = mock_source_connector
    mock_google_class.return_value = mock_target_connector

    # Setup config
    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {},
        'sync_token': None
    }
    mock_config.target.get.return_value = {
        'type': 'google',
        'calendar_id': 'cal2',
        'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    # Run sync
    syncer = Syncer(mock_config)
    result = syncer.sync_once(1)

    # Verify all-day event format for Google
    mock_target_connector.create_event.assert_called_once()
    event_data = mock_target_connector.create_event.call_args[0][1]

    # Google all-day events use 'date' instead of 'dateTime'
    assert 'date' in event_data['start']
    assert 'date' in event_data['end']
    assert event_data['start']['date'] == '2025-01-20'
    assert event_data['end']['date'] == '2025-01-21'
