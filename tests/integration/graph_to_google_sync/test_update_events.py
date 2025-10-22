"""Test updating existing events when syncing Graph to Google."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer
from python.connectors import GraphConnector, GoogleConnector


@patch('python.connectors.GoogleConnector')
@patch('python.connectors.GraphConnector')
def test_sync_graph_to_google_update_existing(mock_graph_class, mock_google_class):
    """Test updating existing event when syncing Graph to Google."""
    # Setup mock source with updated event
    mock_source_connector = Mock(spec=GraphConnector)
    mock_source_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'graph-existing-123',
            'subject': 'Updated Meeting Title',
            'start': {'dateTime': '2025-01-15T10:00:00Z'},
            'end': {'dateTime': '2025-01-15T11:00:00Z'},
            'location': {'displayName': 'New Location'},
            'isAllDay': False,
            'isCancelled': False
        }],
        'nextSyncToken': 'token-update'
    }

    # Setup mock target
    mock_target_connector = Mock(spec=GoogleConnector)

    # Configure mock classes
    mock_graph_class.return_value = mock_source_connector
    mock_google_class.return_value = mock_target_connector

    # Setup config with existing mapping
    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {},
        'sync_token': 'old-token'
    }
    mock_config.target.get.return_value = {
        'type': 'google',
        'calendar_id': 'cal2',
        'credentials': {}
    }

    # Existing mapping with old hash
    mock_config.mappings.get_all_for_source.return_value = [{
        'source_event_uid': 'graph-existing-123',
        'target_event_id': 'google-mapped-456',
        'last_hash': 'old-hash-value'
    }]
    mock_config.settings.get_bool.return_value = False

    # Run sync
    syncer = Syncer(mock_config)
    result = syncer.sync_once(1)

    # Verify update was called
    assert result['created'] == 0
    assert result['updated'] == 1
    assert result['deleted'] == 0

    mock_target_connector.update_event.assert_called_once()
    call_args = mock_target_connector.update_event.call_args

    # Verify correct IDs and Google format
    assert call_args[0][0] == 'cal2'
    assert call_args[0][1] == 'google-mapped-456'

    event_data = call_args[0][2]
    assert event_data['summary'] == 'Updated Meeting Title'
    assert event_data['location'] == 'New Location'
