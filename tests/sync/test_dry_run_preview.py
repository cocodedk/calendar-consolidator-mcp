"""Test DryRunSyncer.preview_sync functionality."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer


@patch('python.sync.dry_run_syncer.GraphConnector')
def test_dry_run_preview_basic(mock_graph_connector):
    """Test basic preview sync."""
    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token-123'
    }
    mock_graph_connector.return_value = mock_connector
    
    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph', 'calendar_id': 'cal-1',
        'credentials': {}, 'sync_token': None
    }
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target-cal',
        'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False
    
    syncer = DryRunSyncer(mock_config)
    result = syncer.preview_sync(1)
    
    assert 'wouldCreate' in result
    assert 'wouldUpdate' in result
    assert 'wouldDelete' in result


@patch('python.sync.dry_run_syncer.GraphConnector')
def test_dry_run_preview_with_changes(mock_graph_connector):
    """Test preview with pending changes."""
    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [{
            'id': 'event-1',
            'subject': 'New Event',
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
    
    assert result['wouldCreate'] == 1

