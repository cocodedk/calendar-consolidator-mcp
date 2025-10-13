"""Test hash-based mapping detection."""

from python.model.event import Event
from python.model.diff import compute_diff
from datetime import datetime


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
            'last_hash': original.compute_hash()
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

