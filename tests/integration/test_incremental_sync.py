"""Test incremental sync with delta tokens."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@pytest.fixture
def mock_config_with_token():
    """Mock config with existing sync token."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    config.logs = Mock()
    return config


@patch('python.sync.syncer.GraphConnector')
def test_initial_sync_stores_token(mock_connector_class, mock_config_with_token):
    """Initial sync stores delta token for next sync."""
    mock_source = Mock()
    mock_source.get_events_delta.return_value = {
        'events': [{
            'id': 'evt1',
            'subject': 'Meeting',
            'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
        }],
        'nextSyncToken': 'https://graph.microsoft.com/delta?token=abc123'
    }

    mock_target = Mock()
    mock_target.create_event.return_value = 'target_id1'

    mock_connector_class.side_effect = [mock_source, mock_target]

    mock_config_with_token.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token'},
        'sync_token': None  # No previous token
    }
    mock_config_with_token.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'target',
        'credentials': {'access_token': 'token'}
    }
    mock_config_with_token.mappings.get_all_for_source.return_value = []
    mock_config_with_token.settings.get_bool.return_value = False

    syncer = Syncer(mock_config_with_token)
    syncer.sync_once(1)

    # Verify token was stored
    mock_config_with_token.sources.update_token.assert_called_once()


@patch('python.sync.syncer.GraphConnector')
def test_incremental_sync_uses_token(mock_connector_class, mock_config_with_token):
    """Incremental sync uses stored delta token."""
    existing_token = 'https://graph.microsoft.com/delta?token=previous'

    mock_source = Mock()
    mock_source.get_events_delta.return_value = {
        'events': [],  # No new events
        'nextSyncToken': 'https://graph.microsoft.com/delta?token=new123'
    }

    mock_target = Mock()
    mock_connector_class.side_effect = [mock_source, mock_target]

    mock_config_with_token.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token'},
        'sync_token': existing_token  # Has previous token
    }
    mock_config_with_token.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'target',
        'credentials': {'access_token': 'token'}
    }
    mock_config_with_token.mappings.get_all_for_source.return_value = []
    mock_config_with_token.settings.get_bool.return_value = False

    syncer = Syncer(mock_config_with_token)
    syncer.sync_once(1)

    # Verify token was passed to API
    mock_source.get_events_delta.assert_called_with('cal1', existing_token)


@patch('python.sync.syncer.GraphConnector')
def test_incremental_sync_only_processes_changes(mock_connector_class, mock_config_with_token):
    """Incremental sync only processes changed events."""
    mock_source = Mock()
    mock_source.get_events_delta.return_value = {
        'events': [{
            'id': 'new_evt',
            'subject': 'New Meeting',
            'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
        }],
        'nextSyncToken': 'token_new'
    }

    mock_target = Mock()
    mock_target.create_event.return_value = 'target_new'

    mock_connector_class.side_effect = [mock_source, mock_target]

    mock_config_with_token.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token'},
        'sync_token': 'token_old'
    }
    mock_config_with_token.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'target',
        'credentials': {'access_token': 'token'}
    }
    mock_config_with_token.mappings.get_all_for_source.return_value = []
    mock_config_with_token.settings.get_bool.return_value = False

    syncer = Syncer(mock_config_with_token)
    syncer.sync_once(1)

    # Only one new event should be created
    assert mock_target.create_event.call_count == 1
