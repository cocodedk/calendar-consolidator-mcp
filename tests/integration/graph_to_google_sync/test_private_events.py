"""Test syncing private events from Graph to Google."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer
from python.connectors import GraphConnector, GoogleConnector


@patch('python.connectors.GoogleConnector')
@patch('python.connectors.GraphConnector')
def test_sync_graph_to_google_private_event(mock_graph_class, mock_google_class):
    """Test syncing private event from Graph to Google."""
    # Setup mock source with private event
    mock_source_connector = Mock(spec=GraphConnector)
    mock_source_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'graph-private-123',
            'subject': 'Personal Appointment',
            'start': {'dateTime': '2025-01-15T14:00:00Z'},
            'end': {'dateTime': '2025-01-15T15:00:00Z'},
            'sensitivity': 'private',
            'isAllDay': False,
            'isCancelled': False
        }],
        'nextSyncToken': 'token-xyz'
    }

    # Setup mock target
    mock_target_connector = Mock(spec=GoogleConnector)
    mock_target_connector.create_event.return_value = 'google-private-789'

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

    # Verify private event format for Google
    mock_target_connector.create_event.assert_called_once()
    event_data = mock_target_connector.create_event.call_args[0][1]

    # Google uses 'visibility' field for privacy
    assert event_data['visibility'] == 'private'
