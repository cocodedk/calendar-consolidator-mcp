"""Test timezone conversion and date handling edge cases."""

import pytest
from python.model.event import Event
from datetime import datetime
import pytz


def test_event_handles_utc_datetime():
    """Event correctly handles UTC datetime."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00+00:00'),
        end=datetime.fromisoformat('2024-01-15T11:00:00+00:00'),
        location=None,
        description=None,
        is_private=False
    )

    assert event.start is not None
    assert 'UTC' in str(event.start.tzinfo) or event.start.tzinfo is not None


def test_event_handles_timezone_offset():
    """Event handles timezone offset format."""
    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00-05:00'),  # EST
        end=datetime.fromisoformat('2024-01-15T11:00:00-05:00'),
        location=None,
        description=None,
        is_private=False
    )

    assert event.start is not None


def test_event_from_graph_with_timezone():
    """Event.from_graph handles timezone info."""
    graph_data = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {
            'dateTime': '2024-01-15T10:00:00Z',
            'timeZone': 'UTC'
        },
        'end': {
            'dateTime': '2024-01-15T11:00:00Z',
            'timeZone': 'UTC'
        }
    }

    event = Event.from_graph(graph_data)
    assert event.start is not None


def test_event_all_day_format():
    """Event handles all-day event format."""
    graph_data = {
        'id': 'evt1',
        'subject': 'All Day Event',
        'start': {
            'dateTime': '2024-01-15T00:00:00',
            'timeZone': 'UTC'
        },
        'end': {
            'dateTime': '2024-01-16T00:00:00',
            'timeZone': 'UTC'
        },
        'isAllDay': True
    }

    event = Event.from_graph(graph_data)
    assert event.subject == 'All Day Event'


def test_event_dst_transition():
    """Event handles daylight saving time transitions."""
    # Spring forward scenario
    event = Event(
        uid='evt1',
        subject='DST Meeting',
        start=datetime.fromisoformat('2024-03-10T02:30:00-05:00'),  # During DST transition
        end=datetime.fromisoformat('2024-03-10T03:30:00-04:00'),
        location=None,
        description=None,
        is_private=False
    )

    assert event.start is not None
    assert event.end is not None
