"""Test sync token storage."""

from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@patch('python.connectors.GraphConnector')
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
