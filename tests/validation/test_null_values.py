"""Test handling of missing/optional field values."""

import pytest
from python.model.event import Event
from datetime import datetime
from python.model.diff import compute_diff


def test_event_with_no_location():
    """Event handles missing location."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description='Meeting description',
        is_private=False
    )

    assert event.location is None
    assert event.compute_hash() is not None


def test_event_with_no_description():
    """Event handles missing description."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Room 101',
        description=None,
        is_private=False
    )

    assert event.description is None


def test_event_with_empty_strings():
    """Event handles empty string values."""
    event = Event(
        uid='evt1',
        subject='',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='',
        description='',
        is_private=False
    )

    assert event.subject == ''
    assert event.location == ''


def test_diff_with_empty_mappings():
    """compute_diff handles empty mappings dictionary."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    diff = compute_diff([event], {}, ignore_private=False)
    assert len(diff.to_create) == 1


def test_diff_with_no_events():
    """compute_diff handles empty event list."""
    diff = compute_diff([], {}, ignore_private=False)
    assert len(diff.to_create) == 0
    assert len(diff.to_update) == 0


def test_event_from_graph_missing_optional_fields():
    """Event.from_graph handles Graph API response with minimal fields."""
    minimal_data = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z'},
        'end': {'dateTime': '2024-01-15T11:00:00Z'}
    }

    event = Event.from_graph(minimal_data)
    assert event.uid == 'evt1'
    assert event.subject == 'Meeting'
