"""Test DryRunSyncer comparison with regular syncer."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer


@pytest.fixture
def mock_config():
    """Mock config store."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    return config


def test_dry_run_uses_same_diff_logic(mock_config):
    """DryRunSyncer uses same diff logic as regular Syncer."""
    mock_config.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token123'}
    }
    mock_config.target.get.return_value = {'calendar_id': 'target'}
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token123'
    }

    syncer = DryRunSyncer(mock_config)

    with patch('python.sync.dry_run_syncer.compute_diff') as mock_diff:
        mock_diff.return_value.to_summary.return_value = {
            'wouldCreate': 1, 'wouldUpdate': 0, 'wouldDelete': 0, 'sampleEvents': []
        }

        with patch.object(syncer, '_get_connector', return_value=mock_connector):
            syncer.preview_sync(1)

        # Verify compute_diff was called
        mock_diff.assert_called_once()


def test_dry_run_raises_on_missing_source(mock_config):
    """DryRunSyncer raises exception for missing source."""
    mock_config.sources.get.return_value = None
    mock_config.target.get.return_value = {'calendar_id': 'target'}

    syncer = DryRunSyncer(mock_config)

    with pytest.raises(Exception, match="Source or target not configured"):
        syncer.preview_sync(999)


def test_dry_run_raises_on_missing_target(mock_config):
    """DryRunSyncer raises exception for missing target."""
    mock_config.sources.get.return_value = {'id': 1}
    mock_config.target.get.return_value = None

    syncer = DryRunSyncer(mock_config)

    with pytest.raises(Exception, match="Source or target not configured"):
        syncer.preview_sync(1)
