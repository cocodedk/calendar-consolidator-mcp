"""Test performance with bulk operations (100+ events)."""

import pytest
from unittest.mock import Mock, patch
from python.model.event import Event
from datetime import datetime
from python.model.diff import compute_diff
from faker import Faker


@pytest.fixture
def bulk_events():
    """Generate 100 test events."""
    fake = Faker()
    events = []

    for i in range(100):
        event = Event(
            uid=f'event_{i}',
            subject=fake.sentence(nb_words=4),
            start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
            end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
            location=fake.city(),
            description=fake.paragraph(),
            is_private=False
        )
        events.append(event)

    return events


def test_compute_diff_with_100_events(bulk_events):
    """compute_diff handles 100 events efficiently."""
    import time

    start = time.time()
    diff = compute_diff(bulk_events, {}, ignore_private=False)
    elapsed = time.time() - start

    assert len(diff.to_create) == 100
    assert elapsed < 5.0  # Should complete in under 5 seconds


def test_hash_computation_bulk_events(bulk_events):
    """Hash computation for 100 events is performant."""
    import time

    start = time.time()
    hashes = [event.compute_hash() for event in bulk_events]
    elapsed = time.time() - start

    assert len(hashes) == 100
    assert elapsed < 2.0  # Should complete in under 2 seconds


def test_event_conversion_bulk(bulk_events):
    """Converting 100 events to Graph format is performant."""
    import time

    start = time.time()
    graph_events = [event.to_graph() for event in bulk_events]
    elapsed = time.time() - start

    assert len(graph_events) == 100
    assert elapsed < 3.0


@pytest.mark.parametrize("event_count", [50, 100, 200])
def test_scalability_with_varying_counts(event_count):
    """Test performance scales linearly with event count."""
    fake = Faker()
    events = []

    for i in range(event_count):
        event = Event(
            uid=f'event_{i}',
            subject=f'Meeting {i}',
            start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
            end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
            location=None,
            description=None,
            is_private=False
        )
        events.append(event)

    import time
    start = time.time()
    diff = compute_diff(events, {}, ignore_private=False)
    elapsed = time.time() - start

    # Linear scalability: O(n)
    assert elapsed < event_count * 0.05  # Max 50ms per event
