"""Test Syncer apply delete operations."""

import pytest
from unittest.mock import Mock
from python.sync.syncer import Syncer
from python.model.diff import DiffResult


def test_syncer_apply_deletes_single_event():
    """Test applying delete operation for single event."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    diff = DiffResult()
    diff.to_delete = ['target-789']

    mock_connector = Mock()

    created, updated, deleted = syncer._apply_changes(
        diff, mock_connector, 'cal-1', 1
    )

    assert created == 0
    assert updated == 0
    assert deleted == 1
    mock_connector.delete_event.assert_called_once_with('cal-1', 'target-789')


def test_syncer_apply_deletes_multiple_events():
    """Test applying delete operations for multiple events."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    diff = DiffResult()
    diff.to_delete = ['target-1', 'target-2', 'target-3']

    mock_connector = Mock()

    _, _, deleted = syncer._apply_changes(diff, mock_connector, 'cal-1', 1)

    assert deleted == 3
    assert mock_connector.delete_event.call_count == 3


def test_syncer_apply_delete_handles_errors():
    """Test delete operations continue on errors."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    diff = DiffResult()
    diff.to_delete = ['target-1', 'target-2']

    mock_connector = Mock()
    mock_connector.delete_event.side_effect = [Exception("Error"), None]

    _, _, deleted = syncer._apply_changes(diff, mock_connector, 'cal-1', 1)

    # First delete fails but continues to second
    assert mock_connector.delete_event.call_count == 2
