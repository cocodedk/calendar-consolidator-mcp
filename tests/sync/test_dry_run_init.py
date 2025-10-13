"""Test DryRunSyncer initialization."""

import pytest
from unittest.mock import Mock
from python.sync.dry_run_syncer import DryRunSyncer


def test_dry_run_syncer_init():
    """DryRunSyncer initializes with config store."""
    mock_config = Mock()
    syncer = DryRunSyncer(mock_config)
    
    assert syncer.config is mock_config


def test_dry_run_syncer_get_connector_graph():
    """DryRunSyncer creates GraphConnector for graph type."""
    mock_config = Mock()
    syncer = DryRunSyncer(mock_config)
    
    source_config = {
        'type': 'graph',
        'credentials': {'access_token': 'token123'}
    }
    
    connector = syncer._get_connector(source_config)
    assert connector is not None


def test_dry_run_syncer_get_connector_unsupported():
    """DryRunSyncer raises error for unsupported connector type."""
    mock_config = Mock()
    syncer = DryRunSyncer(mock_config)
    
    source_config = {
        'type': 'caldav',
        'credentials': {}
    }
    
    with pytest.raises(NotImplementedError, match="caldav"):
        syncer._get_connector(source_config)

