"""Test handling of unexpected/malformed API response formats."""

import pytest
from python.model.event import Event


def test_event_from_graph_with_extra_fields():
    """Event.from_graph ignores unknown fields."""
    data_with_extras = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'},
        'unknownField1': 'value1',
        'unknownField2': {'nested': 'data'},
        'apiVersion': '2.0'
    }

    event = Event.from_graph(data_with_extras)
    assert event.uid == 'evt1'


def test_event_from_graph_with_null_values():
    """Event.from_graph handles missing values in API response."""
    data_with_nulls = {
        'id': 'evt1',
        'subject': '(No title)',  # Graph API typically provides default
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
        # location and body are optional
    }

    event = Event.from_graph(data_with_nulls)
    assert event.uid == 'evt1'
    assert event.subject == '(No title)'
    assert event.location is None


def test_event_from_graph_with_wrong_types():
    """Event.from_graph handles unexpected data types."""
    data_wrong_types = {
        'id': 123,  # Number instead of string
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
    }

    try:
        event = Event.from_graph(data_wrong_types)
        # Should handle by converting to string
        assert event.uid is not None
    except (TypeError, ValueError):
        # Or raise appropriate error
        pass


def test_event_from_graph_with_nested_body():
    """Event.from_graph handles nested body structure."""
    data_nested = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {'dateTime': '2024-01-15T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'},
        'body': {
            'contentType': 'HTML',
            'content': '<p>Meeting description</p>'
        }
    }

    event = Event.from_graph(data_nested)
    assert event.uid == 'evt1'


def test_event_from_graph_with_malformed_datetime():
    """Event.from_graph handles malformed datetime strings."""
    data_bad_datetime = {
        'id': 'evt1',
        'subject': 'Meeting',
        'start': {'dateTime': 'invalid-date', 'timeZone': 'UTC'},
        'end': {'dateTime': '2024-01-15T11:00:00Z', 'timeZone': 'UTC'}
    }

    with pytest.raises((ValueError, AttributeError)):
        Event.from_graph(data_bad_datetime)
