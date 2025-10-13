"""Test diff computation with private event filtering."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event
from python.model.diff import compute_diff


def test_diff_ignores_private_events():
    """Test diff skips private events when flag is set."""
    private_event = Event(
        uid='private-123',
        subject='Private Meeting',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc),
        is_private=True
    )

    public_event = Event(
        uid='public-456',
        subject='Public Meeting',
        start=datetime(2025, 1, 15, 14, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 15, 0, 0, tzinfo=timezone.utc),
        is_private=False
    )

    result = compute_diff([private_event, public_event], {}, ignore_private=True)

    assert len(result.to_create) == 1
    assert result.to_create[0].uid == 'public-456'


def test_diff_includes_private_when_not_ignored():
    """Test diff includes private events when not filtering."""
    private_event = Event(
        uid='private-789',
        subject='Private Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc),
        is_private=True
    )

    result = compute_diff([private_event], {}, ignore_private=False)

    assert len(result.to_create) == 1
    assert result.to_create[0].is_private is True
