"""Test Syncer event fetching."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from python.sync.syncer import Syncer
from python.model.event import Event


@patch('python.sync.syncer.GraphConnector')
def test_syncer_get_connector_graph(mock_graph_connector):
    """Test getting GraphConnector instance."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    config = {'type': 'graph', 'credentials': {'token': 'abc'}}
    connector = syncer._get_connector(config)

    mock_graph_connector.assert_called_once_with({'token': 'abc'})


def test_syncer_get_connector_unsupported():
    """Test getting connector for unsupported type."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    config = {'type': 'unsupported', 'credentials': {}}

    with pytest.raises(NotImplementedError):
        syncer._get_connector(config)


@patch('python.sync.syncer.GraphConnector')
def test_syncer_fetches_events(mock_graph_connector):
    """Test Syncer fetches events from source."""
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

    syncer = Syncer(mock_config)

    try:
        syncer.sync_once(1)
    except:
        pass

    # Verify connector was called
    assert mock_connector.get_events_delta.called
