"""Test Event to_graph conversion."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event


def test_event_to_graph_basic():
    """Test converting basic Event to Graph format."""
    event = Event(
        uid='test-123',
        subject='Meeting',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    graph_data = event.to_graph()

    assert graph_data['subject'] == 'Meeting'
    assert 'start' in graph_data
    assert graph_data['start']['timeZone'] == 'UTC'
    assert graph_data['isAllDay'] is False


def test_event_to_graph_with_location():
    """Test to_graph includes location when present."""
    event = Event(
        uid='test-456',
        subject='On-site Meeting',
        start=datetime(2025, 1, 15, 14, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 15, 0, 0, tzinfo=timezone.utc),
        location='Building A'
    )

    graph_data = event.to_graph()

    assert 'location' in graph_data
    assert graph_data['location']['displayName'] == 'Building A'


def test_event_to_graph_private():
    """Test to_graph includes sensitivity for private events."""
    event = Event(
        uid='test-789',
        subject='Private Event',
        start=datetime(2025, 1, 15, 16, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 17, 0, 0, tzinfo=timezone.utc),
        is_private=True
    )

    graph_data = event.to_graph()

    assert graph_data['sensitivity'] == 'private'
