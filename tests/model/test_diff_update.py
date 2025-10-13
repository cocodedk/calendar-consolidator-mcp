"""Test diff computation for updated events."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event
from python.model.diff import compute_diff


def test_diff_updated_event():
    """Test diff detects changed events."""
    event = Event(
        uid='existing-123',
        subject='Updated Title',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    mappings = {
        'existing-123': {
            'target_event_id': 'target-456',
            'last_hash': 'old-hash-value'
        }
    }

    result = compute_diff([event], mappings)

    assert len(result.to_update) == 1
    assert result.to_update[0][0].uid == 'existing-123'
    assert result.to_update[0][1] == 'target-456'


def test_diff_unchanged_event():
    """Test diff skips unchanged events."""
    event = Event(
        uid='existing-123',
        subject='Same Title',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    current_hash = event.compute_hash()
    mappings = {
        'existing-123': {
            'target_event_id': 'target-456',
            'last_hash': current_hash
        }
    }

    result = compute_diff([event], mappings)

    assert len(result.to_update) == 0
    assert len(result.to_create) == 0
