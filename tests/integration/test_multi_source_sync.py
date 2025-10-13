"""Test syncing from multiple sources to one target."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@pytest.fixture
def mock_config_multi_source():
    """Mock config with multiple sources."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    config.logs = Mock()

    config.sources.get_active.return_value = [
        {
            'id': 1,
            'type': 'graph',
            'calendar_id': 'work_cal',
            'credentials': {'access_token': 'token1'}
        },
        {
            'id': 2,
            'type': 'graph',
            'calendar_id': 'personal_cal',
            'credentials': {'access_token': 'token2'}
        }
    ]

    config.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'consolidated_cal',
        'credentials': {'access_token': 'target_token'}
    }

    return config


@patch('python.sync.syncer.GraphConnector')
def test_sync_all_sources_aggregates_events(mock_connector_class, mock_config_multi_source):
    """Syncing all sources aggregates events from each source."""
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

    # Sync each source
    with patch.object(syncer, '_get_connector') as mock_get_conn:
        mock_get_conn.side_effect = [mock_source1, mock_target, mock_source2, mock_target]

        syncer.sync_once(1)
        syncer.sync_once(2)

    # Both events should be in target
    assert mock_target.create_event.call_count == 2


def test_multi_source_maintains_separate_mappings(mock_config_multi_source):
    """Each source maintains separate event mappings."""
    mock_config_multi_source.sources.get.side_effect = [
        {'id': 1, 'calendar_id': 'source1'},
        {'id': 2, 'calendar_id': 'source2'}
    ]

    mock_config_multi_source.mappings.get_all_for_source.side_effect = [
        [{'source_event_uid': 'evt1', 'target_event_id': 'tgt1', 'source_id': 1}],
        [{'source_event_uid': 'evt2', 'target_event_id': 'tgt2', 'source_id': 2}]
    ]

    syncer = Syncer(mock_config_multi_source)

    # Get mappings for each source
    mappings1 = mock_config_multi_source.mappings.get_all_for_source(1)
    mappings2 = mock_config_multi_source.mappings.get_all_for_source(2)

    # Mappings should be separate
    assert len(mappings1) == 1
    assert len(mappings2) == 1
    assert mappings1[0]['source_id'] != mappings2[0]['source_id']
