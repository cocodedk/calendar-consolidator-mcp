"""Test data consistency and hash verification."""

import pytest
from python.model.event import Event
from datetime import datetime
from python.model.diff import compute_diff


def test_event_hash_consistency():
    """Same event data produces same hash."""
    event1 = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Room 101',
        description='Team meeting',
        is_private=False
    )

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


def test_mapping_hash_detects_content_changes():
    """Mapping hash correctly detects when event content changed."""
    original = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    # Create mapping with original hash
    mappings = {
        'evt1': {
            'source_event_uid': 'evt1',
            'target_event_id': 'target1',
            'content_hash': original.compute_hash()
        }
    }

    # Event with same UID but different content
    modified = Event(
        uid='evt1',
        subject='Updated Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    diff = compute_diff([modified], mappings, ignore_private=False)

    # Should detect as update
    assert len(diff.to_update) == 1


def test_hash_stable_across_serialization():
    """Event hash remains stable after to_graph/from_graph round-trip."""
    original = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Office',
        description='Discussion',
        is_private=False
    )

    original_hash = original.compute_hash()

    # Convert to Graph format and back
    graph_data = original.to_graph()
    graph_data['id'] = original.uid  # Add ID for round-trip
    # Add bodyPreview since from_graph reads from that, not body
    if 'body' in graph_data:
        graph_data['bodyPreview'] = graph_data['body']['content']
    restored = Event.from_graph(graph_data)
    restored_hash = restored.compute_hash()

    # Hashes should match
    assert original_hash == restored_hash


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
