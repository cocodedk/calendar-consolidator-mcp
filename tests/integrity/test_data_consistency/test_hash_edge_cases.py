"""Test hash edge cases and special values."""

from python.model.event import Event
from datetime import datetime


def test_null_value_hash_consistency():
    """Hash handles None values consistently."""
    event_with_none = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    event_with_empty = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='',
        description='',
        is_private=False
    )

    # None and empty string should produce different hashes
    assert event_with_none.compute_hash() != event_with_empty.compute_hash()


def test_whitespace_in_hash():
    """Hash considers whitespace differences."""
    event1 = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description='Line 1\nLine 2',
        is_private=False
    )

    event2 = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description='Line 1\n\nLine 2',  # Extra newline
        is_private=False
    )

    # Different whitespace should produce different hashes
    assert event1.compute_hash() != event2.compute_hash()
