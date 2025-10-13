"""Test Syncer apply create operations."""

import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from python.sync.syncer import Syncer
from python.model.event import Event
from python.model.diff import DiffResult


def test_syncer_apply_creates_single_event():
    """Test applying create operation for single event."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    event = Event(
        uid='new-123',
        subject='New Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    diff = DiffResult()
    diff.to_create = [event]

    mock_connector = Mock()
    mock_connector.create_event.return_value = 'target-456'

    created, updated, deleted = syncer._apply_changes(
        diff, mock_connector, 'cal-1', 1
    )

    assert created == 1
    assert updated == 0
    assert deleted == 0
    mock_connector.create_event.assert_called_once()


def test_syncer_apply_creates_multiple_events():
    """Test applying create operations for multiple events."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    events = [
        Event(uid=f'new-{i}', subject=f'Event {i}',
              start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
              end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc))
        for i in range(3)
    ]

    diff = DiffResult()
    diff.to_create = events

    mock_connector = Mock()
    mock_connector.create_event.return_value = 'target-id'

    created, _, _ = syncer._apply_changes(diff, mock_connector, 'cal-1', 1)

    assert created == 3
    assert mock_connector.create_event.call_count == 3
