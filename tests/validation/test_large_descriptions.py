"""Test handling of long text fields (descriptions, subjects)."""

import pytest
from python.model.event import Event
from datetime import datetime


def test_event_with_large_description():
    """Event handles large description text."""
    large_description = "A" * 10000  # 10KB description

    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=large_description,
        is_private=False
    )

    assert len(event.description) == 10000
    assert event.compute_hash() is not None


def test_event_with_multiline_description():
    """Event handles multiline description."""
    multiline_desc = """
    This is a meeting about project planning.

    Agenda:
    1. Review Q1 goals
    2. Discuss resource allocation
    3. Set timeline

    Please prepare your status updates.
    """

    event = Event(
        uid='evt1',
        subject='Planning Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=multiline_desc,
        is_private=False
    )

    assert '\n' in event.description


def test_event_with_html_description():
    """Event handles HTML content in description."""
    html_desc = """
    <html><body>
    <h1>Meeting Notes</h1>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    </body></html>
    """

    event = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=html_desc,
        is_private=False
    )

    assert '<html>' in event.description


def test_event_with_long_subject():
    """Event handles very long subject line."""
    long_subject = "Q1 Planning Meeting for Engineering Team Including " + "Discussion Topics " * 20

    event = Event(
        uid='evt1',
        subject=long_subject,
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    assert len(event.subject) > 100
