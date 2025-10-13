"""Test end-to-end sync flow with mocked Graph API."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from python.sync.syncer import Syncer
from python.model.event import Event


@pytest.fixture
def mock_config_store():
    """Mock config store for integration test."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    config.logs = Mock()
    return config


@pytest.fixture
def sample_graph_events():
    """Sample Graph API events."""
    return [
        {
            'id': 'event1',
            'subject': 'Team Meeting',
            'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'},
            'isPrivate': False
        },
        {
            'id': 'event2',
            'subject': 'Project Review',
            'start': {'dateTime': '2024-01-16T14:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-16T15:00:00Z', 'timeZone': 'UTC'},
            'isPrivate': False
        }
    ]


@patch('python.connectors.GraphConnector')
def test_end_to_end_initial_sync(mock_connector_class, mock_config_store, sample_graph_events):
    """Complete initial sync flow: fetch, diff, create events."""
    # Setup mocks
    mock_source_connector = Mock()
    mock_source_connector.get_events_delta.return_value = {
        'events': sample_graph_events,
        'nextSyncToken': 'token123'
    }

    mock_target_connector = Mock()
    mock_target_connector.create_event.side_effect = ['target_id1', 'target_id2']

    mock_connector_class.side_effect = [mock_source_connector, mock_target_connector]

    mock_config_store.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'source_cal',
        'credentials': {'access_token': 'token'},
        'sync_token': None
    }
    mock_config_store.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'target_cal',
        'credentials': {'access_token': 'token'}
    }
    mock_config_store.mappings.get_all_for_source.return_value = []
    mock_config_store.settings.get_bool.return_value = False

    # Run sync
    syncer = Syncer(mock_config_store)
    syncer.sync_once(1)

    # Verify events were created in target
    assert mock_target_connector.create_event.call_count == 2

    # Verify mappings were stored
    assert mock_config_store.mappings.create.call_count == 2

    # Verify sync log was created
    mock_config_store.logs.log_sync.assert_called_once()
