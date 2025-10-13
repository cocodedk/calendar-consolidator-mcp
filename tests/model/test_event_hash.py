"""Test Event hash computation."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event


def test_compute_hash_consistency():
    """Test hash is consistent for same event data."""
    event = Event(
        uid='test-123',
        subject='Meeting',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    hash1 = event.compute_hash()
    hash2 = event.compute_hash()

    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex digest


def test_compute_hash_different_for_changes():
    """Test hash changes when event content changes."""
    base_event = Event(
        uid='test-123',
        subject='Original',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    modified_event = Event(
        uid='test-123',
        subject='Modified',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    assert base_event.compute_hash() != modified_event.compute_hash()


def test_compute_hash_ignores_uid():
    """Test hash doesn't include UID (for content comparison)."""
    event1 = Event(
        uid='different-uid-1',
        subject='Same Content',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    event2 = Event(
        uid='different-uid-2',
        subject='Same Content',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    assert event1.compute_hash() == event2.compute_hash()
