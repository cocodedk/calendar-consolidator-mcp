"""Test DryRunSyncer.preview_all_sources functionality."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer


@patch('python.sync.dry_run_syncer.GraphConnector')
def test_dry_run_all_sources_empty(mock_graph_connector):
    """Test preview all sources with no active sources."""
    mock_config = Mock()
    mock_config.sources.get_active.return_value = []

    syncer = DryRunSyncer(mock_config)
    result = syncer.preview_all_sources()

    assert result['wouldCreate'] == 0
    assert result['wouldUpdate'] == 0
    assert result['wouldDelete'] == 0


@patch('python.sync.dry_run_syncer.GraphConnector')
def test_dry_run_all_sources_multiple(mock_graph_connector):
    """Test preview all sources aggregates results."""
    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token'
    }
    mock_graph_connector.return_value = mock_connector

    mock_config = Mock()
    source1 = {'id': 1, 'type': 'graph', 'calendar_id': 'cal-1', 'credentials': {}}
    source2 = {'id': 2, 'type': 'graph', 'calendar_id': 'cal-2', 'credentials': {}}
    mock_config.sources.get_active.return_value = [source1, source2]
    mock_config.sources.get.side_effect = lambda id: source1 if id == 1 else source2
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target', 'credentials': {}
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    syncer = DryRunSyncer(mock_config)
    result = syncer.preview_all_sources()

    assert 'wouldCreate' in result
    assert 'sampleEvents' in result
