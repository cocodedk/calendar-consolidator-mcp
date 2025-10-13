"""Test DryRunSyncer preview generation."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer
from python.model.event import Event


@pytest.fixture
def mock_config_with_data():
    """Mock config with sample data."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()

    config.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token123'},
        'sync_token': None
    }
    config.target.get.return_value = {'calendar_id': 'target_cal'}
    config.mappings.get_all_for_source.return_value = []
    config.settings.get_bool.return_value = False

    return config


@patch('python.sync.dry_run_syncer.compute_diff')
def test_preview_sync_returns_summary(mock_compute_diff, mock_config_with_data):
    """Preview sync returns diff summary."""
    mock_diff = Mock()
    mock_diff.to_summary.return_value = {
        'wouldCreate': 5,
        'wouldUpdate': 2,
        'wouldDelete': 1,
        'sampleEvents': []
    }
    mock_compute_diff.return_value = mock_diff

    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token123'
    }

    syncer = DryRunSyncer(mock_config_with_data)

    with patch.object(syncer, '_get_connector', return_value=mock_connector):
        result = syncer.preview_sync(1)

    assert result['wouldCreate'] == 5
    assert result['wouldUpdate'] == 2
    assert result['wouldDelete'] == 1


def test_preview_all_sources_aggregates(mock_config_with_data):
    """Preview all sources aggregates counts."""
    mock_config_with_data.sources.get_active.return_value = [
        {'id': 1}, {'id': 2}
    ]

    syncer = DryRunSyncer(mock_config_with_data)

    with patch.object(syncer, 'preview_sync') as mock_preview:
        mock_preview.side_effect = [
            {'wouldCreate': 3, 'wouldUpdate': 1, 'wouldDelete': 0, 'sampleEvents': []},
            {'wouldCreate': 2, 'wouldUpdate': 1, 'wouldDelete': 1, 'sampleEvents': []}
        ]

        result = syncer.preview_all_sources()

    assert result['wouldCreate'] == 5
    assert result['wouldUpdate'] == 2
    assert result['wouldDelete'] == 1
