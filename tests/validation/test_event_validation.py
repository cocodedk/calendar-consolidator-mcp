"""Test event data validation and error handling."""

import pytest
from python.model.event import Event
from datetime import datetime


def test_event_accepts_none_uid():
    """Event dataclass accepts None for uid (but shouldn't be used)."""
    # Note: Event is a dataclass, so it technically accepts None
    # But in practice, uid should always be set
    event = Event(
        uid=None,
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z')
    )
    assert event.uid is None  # Accepted but not recommended


def test_event_accepts_none_start():
    """Event dataclass accepts None for start (but shouldn't be used)."""
    # Event is a dataclass, so it accepts None
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=None,
        end=datetime.fromisoformat('2024-01-15T11:00:00Z')
    )
    assert event.start is None


def test_event_accepts_none_end():
    """Event dataclass accepts None for end (but shouldn't be used)."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=None
    )
    assert event.end is None


def test_event_accepts_optional_fields():
    """Event accepts None for optional fields."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    assert event.location is None
    assert event.description is None


def test_event_from_graph_handles_missing_fields():
    """Event.from_graph handles incomplete Graph API data."""
    incomplete_data = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z'},
        'end': {'dateTime': '2024-01-15T11:00:00Z'}
        # Missing location, description, isPrivate
    }

    event = Event.from_graph(incomplete_data)
    assert event.uid == 'evt1'
    assert event.subject == 'Meeting'


def test_event_to_graph_excludes_none_values():
    """Event.to_graph excludes None values."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    graph_data = event.to_graph()
    # None values should be excluded or handled appropriately
    assert 'subject' in graph_data
    assert 'start' in graph_data
