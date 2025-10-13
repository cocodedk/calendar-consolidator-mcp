"""Test diff computation for new events."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event
from python.model.diff import compute_diff


def test_diff_new_event():
    """Test diff detects new events to create."""
    event = Event(
        uid='new-123',
        subject='New Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    source_events = [event]
    mappings = {}

    result = compute_diff(source_events, mappings)

    assert len(result.to_create) == 1
    assert result.to_create[0].uid == 'new-123'
    assert len(result.to_update) == 0
    assert len(result.to_delete) == 0


def test_diff_multiple_new_events():
    """Test diff handles multiple new events."""
    events = [
        Event(uid=f'new-{i}', subject=f'Event {i}',
              start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
              end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc))
        for i in range(3)
    ]

    result = compute_diff(events, {})

    assert len(result.to_create) == 3
    assert result.count_total() == 3


def test_diff_empty_sources():
    """Test diff with no source events."""
    result = compute_diff([], {})

    assert len(result.to_create) == 0
    assert result.count_total() == 0
