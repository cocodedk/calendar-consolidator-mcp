"""Test basic hash consistency."""

from python.model.event import Event
from datetime import datetime


def test_event_hash_consistency(sample_event):
    """Same event data produces same hash."""
    event1 = sample_event
    event2 = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Room 101',
        description='Team meeting',
        is_private=False
    )

    assert event1.compute_hash() == event2.compute_hash()


def test_event_hash_changes_with_content():
    """Different event content produces different hash."""
    event1 = Event(
        uid='evt1',
        subject='Original Title',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    event2 = Event(
        uid='evt1',
        subject='Modified Title',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    assert event1.compute_hash() != event2.compute_hash()

