"""Test diff computation for deleted events."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event
from python.model.diff import compute_diff


def test_diff_cancelled_event():
    """Test diff detects cancelled events as deletions."""
    event = Event(
        uid='cancelled-123',
        subject='Cancelled Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc),
        is_cancelled=True
    )

    mappings = {
        'cancelled-123': {
            'target_event_id': 'target-789',
            'last_hash': 'some-hash'
        }
    }

    result = compute_diff([event], mappings)

    assert len(result.to_delete) == 1
    assert result.to_delete[0] == 'target-789'


def test_diff_missing_source_event():
    """Test diff detects events removed from source."""
    mappings = {
        'old-event-123': {
            'target_event_id': 'target-456',
            'last_hash': 'hash-value'
        }
    }

    result = compute_diff([], mappings)

    assert len(result.to_delete) == 1
    assert result.to_delete[0] == 'target-456'


def test_diff_multiple_deletions():
    """Test diff handles multiple deletions."""
    mappings = {
        f'old-{i}': {'target_event_id': f'target-{i}', 'last_hash': 'hash'}
        for i in range(3)
    }

    result = compute_diff([], mappings)

    assert len(result.to_delete) == 3
