"""Test full Syncer integration flow (mocked)."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from python.sync.syncer import Syncer
from python.model.event import Event


@patch('python.connectors.GraphConnector')
def test_syncer_full_sync_flow(mock_graph_connector):
    """Test complete sync_once flow with mocked components."""
    # Setup mock connector
    mock_source_connector = Mock()
    mock_target_connector = Mock()
    mock_graph_connector.side_effect = [mock_source_connector, mock_target_connector]

    # Mock source events
    mock_source_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'graph-123',
            'subject': 'Test Event',
            'start': {'dateTime': '2025-01-15T10:00:00Z'},
            'end': {'dateTime': '2025-01-15T11:00:00Z'}
        }],
        'nextSyncToken': 'new-token'
    }

    mock_target_connector.create_event.return_value = 'target-456'

    # Setup config
    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph', 'calendar_id': 'source-cal',
        'credentials': {}, 'sync_token': None
    }
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target-cal',
        'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    syncer = Syncer(mock_config)
    result = syncer.sync_once(1)

    assert result['success'] is True
    assert result['created'] == 1
    mock_config.sources.update_token.assert_called_with(1, 'new-token')
    mock_config.logs.log_sync.assert_called_once()


@patch('python.connectors.GraphConnector')
def test_syncer_sync_with_no_changes(mock_graph_connector):
    """Test sync when no changes detected."""
    mock_connector = Mock()
    mock_graph_connector.return_value = mock_connector

    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token'
    }

    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph', 'calendar_id': 'cal',
        'credentials': {}
    }
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target',
        'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    syncer = Syncer(mock_config)
    result = syncer.sync_once(1)

    assert result['created'] == 0
    assert result['updated'] == 0
    assert result['deleted'] == 0
