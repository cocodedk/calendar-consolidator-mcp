"""Test handling of conflicting updates from multiple sources."""

import pytest
from unittest.mock import Mock, patch
from python.model.event import Event
from datetime import datetime
from python.model.diff import compute_diff


def test_same_event_from_different_sources_creates_separate_entries():
    """Same event UID from different sources creates separate target events."""
    # Two sources with events having same subject/time but different source IDs
    event1 = Event(
        uid='recurring-meeting-1',
        subject='Weekly Standup',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T10:30:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    event2 = Event(
        uid='recurring-meeting-1',
        subject='Weekly Standup',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T10:30:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    # Different source mappings
    mappings_source1 = {}
    mappings_source2 = {}

    diff1 = compute_diff([event1], mappings_source1, ignore_private=False)
    diff2 = compute_diff([event2], mappings_source2, ignore_private=False)

    # Both should create new events (no conflict)
    assert len(diff1.to_create) == 1
    assert len(diff2.to_create) == 1


def test_event_hash_change_triggers_update():
    """Content change in source event triggers update."""
    original_event = Event(
        uid='event1',
        subject='Original Title',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    updated_event = Event(
        uid='event1',
        subject='Updated Title',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    # Create mapping with original hash
    mappings = {
        'event1': {
            'source_event_uid': 'event1',
            'target_event_id': 'target1',
            'content_hash': original_event.compute_hash()
        }
    }

    # Compute diff with updated event
    diff = compute_diff([updated_event], mappings, ignore_private=False)

    # Should trigger update
    assert len(diff.to_update) == 1
    assert diff.to_update[0][0].subject == 'Updated Title'


def test_deleted_source_event_triggers_target_deletion():
    """Deleted event in source triggers deletion in target."""
    # No source events, but mapping exists
    mappings = {
        'deleted_event': {
            'source_event_uid': 'deleted_event',
            'target_event_id': 'target123',
            'content_hash': 'hash123'
        }
    }

    diff = compute_diff([], mappings, ignore_private=False)

    # Should mark for deletion
    assert len(diff.to_delete) == 1
    assert diff.to_delete[0] == 'target123'
