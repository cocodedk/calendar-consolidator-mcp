"""Test incremental change detection."""

from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@patch('python.connectors.GraphConnector')
def test_incremental_sync_only_processes_changes(mock_connector_class, mock_config_with_token):
    """Incremental sync processes only changed events."""
    # Existing mappings
    existing_mappings = [
        {
            'source_event_uid': 'evt1',
            'target_event_id': 'target_evt1',
            'last_hash': 'oldhash1'
        }
    ]

    mock_source = Mock()
    mock_source.get_events_delta.return_value = {
        'events': [
            # Updated event
            {
                'id': 'evt1',
                'subject': 'Updated Meeting',
                'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
                'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
            },
            # New event
            {
                'id': 'evt2',
                'subject': 'New Meeting',
                'start': {'dateTime': '2024-01-16T10:00:00Z', 'timeZone': 'UTC'},
                'end': {'dateTime': '2024-01-16T11:00:00Z', 'timeZone': 'UTC'}
            }
        ],
        'nextSyncToken': 'https://graph.microsoft.com/delta?token=new'
    }

    mock_target = Mock()
    mock_target.update_event.return_value = None
    mock_target.create_event.return_value = 'target_evt2'

    mock_connector_class.side_effect = [mock_source, mock_target]

    mock_config_with_token.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token'},
        'sync_token': 'https://graph.microsoft.com/delta?token=old'
    }
    mock_config_with_token.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'target',
        'credentials': {'access_token': 'token'}
    }
    mock_config_with_token.mappings.get_all_for_source.return_value = existing_mappings
    mock_config_with_token.settings.get_bool.return_value = False

    syncer = Syncer(mock_config_with_token)
    result = syncer.sync_once(1)

    # Should process both update and create
    assert result['updated'] == 1
    assert result['created'] == 1
