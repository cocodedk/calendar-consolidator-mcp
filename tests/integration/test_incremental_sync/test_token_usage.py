"""Test incremental sync token usage."""

from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@patch('python.connectors.GraphConnector')
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
        'sync_token': existing_token  # Has token
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

    # Verify connector was called with existing token
    mock_source.get_events_delta.assert_called_once_with('cal1', existing_token)

