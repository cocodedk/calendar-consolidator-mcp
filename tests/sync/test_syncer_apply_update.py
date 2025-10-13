"""Test Syncer apply update operations."""

import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from python.sync.syncer import Syncer
from python.model.event import Event
from python.model.diff import DiffResult


def test_syncer_apply_updates_single_event():
    """Test applying update operation for single event."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    event = Event(
        uid='existing-123',
        subject='Updated Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    diff = DiffResult()
    diff.to_update = [(event, 'target-456')]

    mock_connector = Mock()

    created, updated, deleted = syncer._apply_changes(
        diff, mock_connector, 'cal-1', 1
    )

    assert created == 0
    assert updated == 1
    assert deleted == 0
    mock_connector.update_event.assert_called_once()


def test_syncer_apply_updates_multiple_events():
    """Test applying update operations for multiple events."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    events = [
        (Event(uid=f'upd-{i}', subject=f'Event {i}',
               start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
               end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)),
         f'target-{i}')
        for i in range(2)
    ]

    diff = DiffResult()
    diff.to_update = events

    mock_connector = Mock()

    _, updated, _ = syncer._apply_changes(diff, mock_connector, 'cal-1', 1)

    assert updated == 2
    assert mock_connector.update_event.call_count == 2
