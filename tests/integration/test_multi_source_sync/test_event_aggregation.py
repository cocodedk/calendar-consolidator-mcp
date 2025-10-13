"""Tests for event aggregation from multiple sources."""

import pytest
from unittest.mock import Mock, patch


@pytest.mark.skip(reason="Test needs implementation - mocking setup requires adjustment")
@patch('python.connectors.GraphConnector')
def test_sync_all_sources_aggregates_events(mock_connector_class, mock_config_multi_source):
    """Syncing all sources aggregates events from each source."""
    from python.sync.syncer import Syncer

    # Mock connectors for each source
    mock_source1 = Mock()
    mock_source1.get_events_delta.return_value = {
        'events': [{
            'id': 'work1',
            'subject': 'Work Meeting',
            'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
        }],
        'nextSyncToken': 'token1'
    }

    mock_source2 = Mock()
    mock_source2.get_events_delta.return_value = {
        'events': [{
            'id': 'personal1',
            'subject': 'Dentist Appointment',
            'start': {'dateTime': '2024-01-15T14:00:00Z', 'timeZone': 'UTC'},
            'end': {'dateTime': '2024-01-15T15:00:00Z', 'timeZone': 'UTC'}
        }],
        'nextSyncToken': 'token2'
    }

    mock_target = Mock()
    mock_target.create_event.side_effect = ['target_work1', 'target_personal1']

    mock_config_multi_source.sources.get.side_effect = [
        mock_config_multi_source.sources.get_active()[0],
        mock_config_multi_source.sources.get_active()[1]
    ]
    mock_config_multi_source.mappings.get_all_for_source.return_value = []
    mock_config_multi_source.settings.get_bool.return_value = False

    syncer = Syncer(mock_config_multi_source)

    # Sync each source - patch the connector factory used by SyncExecutor
    with patch('python.sync.syncer.connector_factory.get_connector') as mock_get_conn:
        mock_get_conn.side_effect = [mock_source1, mock_target, mock_source2, mock_target]

        syncer.sync_once(1)
        syncer.sync_once(2)

    # Both events should be in target
    assert mock_target.create_event.call_count == 2
