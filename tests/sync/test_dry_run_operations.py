"""Test DryRunSyncer operations verify no actual changes made."""

import pytest
from unittest.mock import Mock, patch
from python.sync.dry_run_syncer import DryRunSyncer
from python.model.event import Event


@pytest.fixture
def mock_config():
    """Mock config store."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    return config


def test_preview_sync_no_writes_to_database(mock_config):
    """Preview sync does not write to database."""
    mock_config.sources.get.return_value = {
        'id': 1,
        'type': 'graph',
        'calendar_id': 'cal1',
        'credentials': {'access_token': 'token123'},
        'sync_token': None
    }
    mock_config.target.get.return_value = {
        'calendar_id': 'target_cal'
    }
    mock_config.mappings.get_all_for_source.return_value = []
    mock_config.settings.get_bool.return_value = False

    mock_connector = Mock()
    mock_connector.get_events_delta.return_value = {
        'events': [],
        'nextSyncToken': 'token123'
    }

    syncer = DryRunSyncer(mock_config)

    with patch.object(syncer, '_get_connector', return_value=mock_connector):
        result = syncer.preview_sync(1)

    # Verify no create/update/delete methods called on mappings
    mock_config.mappings.create.assert_not_called()
    mock_config.mappings.update_hash.assert_not_called()
    mock_config.mappings.delete.assert_not_called()

    assert isinstance(result, dict)


def test_preview_sync_no_api_writes(mock_config):
    """Preview sync does not call API write operations."""
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
        'nextSyncToken': 'token456'
    }

    syncer = DryRunSyncer(mock_config)

    with patch.object(syncer, '_get_connector', return_value=mock_connector):
        syncer.preview_sync(1)

    # Verify no create/update/delete API calls
    mock_connector.create_event.assert_not_called()
    mock_connector.update_event.assert_not_called()
    mock_connector.delete_event.assert_not_called()
