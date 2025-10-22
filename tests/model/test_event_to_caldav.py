"""Test Event to_caldav conversion."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event


def test_event_to_caldav_basic():
    """Test converting basic Event to CalDAV format."""
    event = Event(
        uid='test-123',
        subject='Meeting',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    caldav_data = event.to_caldav()

    assert caldav_data['subject'] == 'Meeting'
    assert 'start' in caldav_data
    assert isinstance(caldav_data['start'], str)
    assert 'end' in caldav_data
    assert isinstance(caldav_data['end'], str)
    # isAllDay is only included when True (via to_icloud)
    assert caldav_data.get('isAllDay') != True


def test_event_to_caldav_with_location():
    """Test to_caldav includes location when present."""
    event = Event(
        uid='test-456',
        subject='On-site Meeting',
        start=datetime(2025, 1, 15, 14, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 15, 0, 0, tzinfo=timezone.utc),
        location='Building A'
    )

    caldav_data = event.to_caldav()

    assert 'location' in caldav_data
    assert caldav_data['location'] == 'Building A'


def test_event_to_caldav_with_description():
    """Test to_caldav includes body field for description."""
    event = Event(
        uid='test-789',
        subject='Team Meeting',
        start=datetime(2025, 1, 15, 16, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 17, 0, 0, tzinfo=timezone.utc),
        description='Discuss project status'
    )

    caldav_data = event.to_caldav()

    assert 'body' in caldav_data
    assert caldav_data['body'] == 'Discuss project status'


def test_event_to_caldav_all_day():
    """Test to_caldav correctly handles all-day events."""
    event = Event(
        uid='test-all-day',
        subject='Conference',
        start=datetime(2025, 1, 15, 0, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 16, 0, 0, 0, tzinfo=timezone.utc),
        is_all_day=True
    )

    caldav_data = event.to_caldav()

    assert caldav_data.get('isAllDay') is True


def test_event_to_caldav_format_compatibility():
    """Test that to_caldav format is compatible with ical_builder."""
    event = Event(
        uid='test-compat',
        subject='Test Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc),
        location='Room 101',
        description='Meeting notes'
    )

    caldav_data = event.to_caldav()

    # Verify format matches what ical_builder expects
    # start/end should be simple ISO strings, not nested objects
    assert isinstance(caldav_data['start'], str)
    assert isinstance(caldav_data['end'], str)
    assert '+' in caldav_data['start'] or 'Z' in caldav_data['start']

    # description should be 'body', not nested
    assert 'body' in caldav_data
    assert isinstance(caldav_data['body'], str)

    # location should be simple string, not nested
    assert isinstance(caldav_data['location'], str)
