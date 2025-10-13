"""Test DryRunSyncer makes no actual changes."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer


@patch('python.sync.dry_run_syncer.GraphConnector')
def test_dry_run_no_database_writes(mock_graph_connector):
    """Test dry run does not write to database."""
    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'event-1',
            'subject': 'Event',
            'start': {'dateTime': '2025-01-15T10:00:00Z'},
            'end': {'dateTime': '2025-01-15T11:00:00Z'}
        }],
        'nextSyncToken': 'token'
    }
    mock_graph_connector.return_value = mock_connector

    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph', 'calendar_id': 'cal-1',
        'credentials': {}
    }
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target',
        'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    syncer = DryRunSyncer(mock_config)
    result = syncer.preview_sync(1)

    # Verify no create/update/delete calls to connector
    assert not mock_connector.create_event.called
    assert not mock_connector.update_event.called
    assert not mock_connector.delete_event.called

    # Verify no mapping writes
    assert not mock_config.mappings.create.called
    assert not mock_config.mappings.update_hash.called

    # Verify no token updates
    assert not mock_config.sources.update_token.called
