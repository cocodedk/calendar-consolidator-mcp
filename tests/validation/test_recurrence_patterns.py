"""Test recurring event handling."""

import pytest
from python.model.event import Event


def test_event_with_recurrence_pattern():
    """Event handles recurrence information."""
    graph_data = {
        'id': 'recurring-evt',
        'subject': 'Weekly Standup',
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T10:30:00Z', 'timeZone': 'UTC'},
        'recurrence': {
            'pattern': {
                'type': 'weekly',
                'interval': 1,
                'daysOfWeek': ['monday']
            },
            'range': {
                'type': 'noEnd',
                'startDate': '2024-01-15'
            }
        }
    }

    event = Event.from_graph(graph_data)
    assert event.uid == 'recurring-evt'


def test_recurring_event_series_master():
    """Event identifies series master vs occurrence."""
    series_master = {
        'id': 'series-master',
        'subject': 'Recurring Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'},
        'type': 'seriesMaster'
    }

    event = Event.from_graph(series_master)
    assert event.subject == 'Recurring Meeting'


def test_recurring_event_single_occurrence():
    """Event handles single occurrence of recurring event."""
    occurrence = {
        'id': 'occurrence-1',
        'subject': 'Recurring Meeting',
        'start': {'dateTime': '2024-01-22T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-22T11:00:00Z', 'timeZone': 'UTC'},
        'type': 'occurrence',
        'seriesMasterId': 'series-master'
    }

    event = Event.from_graph(occurrence)
    assert event.uid == 'occurrence-1'


def test_recurring_event_exception():
    """Event handles modified occurrence (exception)."""
    exception = {
        'id': 'exception-1',
        'subject': 'Recurring Meeting (Rescheduled)',
        'start': {'dateTime': '2024-01-22T14:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-22T15:00:00Z', 'timeZone': 'UTC'},
        'type': 'exception',
        'seriesMasterId': 'series-master'
    }

    event = Event.from_graph(exception)
    assert 'Rescheduled' in event.subject
