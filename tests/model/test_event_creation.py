"""Test Event creation and initialization."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event


def test_event_basic_creation():
    """Test creating a basic Event instance."""
    start = datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
    end = datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)

    event = Event(
        uid='test-123',
        subject='Test Event',
        start=start,
        end=end
    )

    assert event.uid == 'test-123'
    assert event.subject == 'Test Event'
    assert event.start == start
    assert event.end == end
    assert event.is_all_day is False
    assert event.is_cancelled is False


def test_event_from_graph(sample_graph_event):
    """Test creating Event from Microsoft Graph format."""
    event = Event.from_graph(sample_graph_event)

    assert event.uid == 'graph-event-456'
    assert event.subject == 'Project Review'
    assert event.location == 'Room B'
    assert event.description == 'Quarterly project review'
    assert event.organizer == 'organizer@example.com'
    assert len(event.attendees) == 2


def test_event_from_graph_minimal():
    """Test from_graph with minimal required fields."""
    minimal_event = {
        'id': 'min-123',
        'start': {'dateTime': '2025-01-15T10:00:00Z'},
        'end': {'dateTime': '2025-01-15T11:00:00Z'}
    }

    event = Event.from_graph(minimal_event)

    assert event.uid == 'min-123'
    assert event.subject == '(No title)'
    assert event.location is None
    assert event.is_all_day is False
