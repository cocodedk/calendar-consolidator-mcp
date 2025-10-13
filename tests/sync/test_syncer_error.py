"""Test Syncer error handling."""

import pytest
from unittest.mock import Mock, patch
from python.sync.syncer import Syncer


@patch('python.sync.syncer.GraphConnector')
def test_syncer_handles_missing_source(mock_graph_connector):
    """Test Syncer handles missing source configuration."""
    mock_config = Mock()
    mock_config.sources.get.return_value = None
    mock_config.target.get.return_value = {'type': 'graph'}

    syncer = Syncer(mock_config)

    with pytest.raises(Exception, match="Source or target not configured"):
        syncer.sync_once(999)


@patch('python.sync.syncer.GraphConnector')
def test_syncer_handles_missing_target(mock_graph_connector):
    """Test Syncer handles missing target configuration."""
    mock_config = Mock()
    mock_config.sources.get.return_value = {'type': 'graph'}
    mock_config.target.get.return_value = None

    syncer = Syncer(mock_config)

    with pytest.raises(Exception, match="Source or target not configured"):
        syncer.sync_once(1)


@patch('python.sync.syncer.GraphConnector')
def test_syncer_logs_error_on_exception(mock_graph_connector):
    """Test Syncer logs errors when sync fails."""
    mock_connector = Mock()
    mock_connector.get_events_delta.side_effect = Exception("API Error")
    mock_graph_connector.return_value = mock_connector

    mock_config = Mock()
    mock_config.sources.get.return_value = {
        'type': 'graph', 'calendar_id': 'cal-1',
        'credentials': {}
    }
    mock_config.target.get.return_value = {
        'type': 'graph', 'calendar_id': 'target-cal',
        'credentials': {}
    }

    syncer = Syncer(mock_config)

    with pytest.raises(Exception, match="API Error"):
        syncer.sync_once(1)

    mock_config.logs.log_sync.assert_called_once()
    call_args = mock_config.logs.log_sync.call_args[0]
    assert call_args[1] == 'error'
