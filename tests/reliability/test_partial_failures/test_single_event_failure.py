"""Tests for continuing after single event failures."""

from unittest.mock import Mock
from python.model.event import Event
from datetime import datetime


def test_sync_continues_after_single_event_failure():
    """Sync continues processing after one event fails."""
    events = [
        Event(uid='evt1', subject='Meeting 1', start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T11:00:00Z'), location=None, description=None, is_private=False),
        Event(uid='evt2', subject='Meeting 2', start=datetime.fromisoformat('2024-01-15T14:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T15:00:00Z'), location=None, description=None, is_private=False),
        Event(uid='evt3', subject='Meeting 3', start=datetime.fromisoformat('2024-01-15T16:00:00Z'),
              end=datetime.fromisoformat('2024-01-15T17:00:00Z'), location=None, description=None, is_private=False)
    ]

    mock_connector = Mock()
    # Second event fails
    mock_connector.create_event.side_effect = [
        'target_1',
        Exception("Network error"),
        'target_3'
    ]

    successful_creates = []
    failed_creates = []

    for event in events:
        try:
            target_id = mock_connector.create_event('cal1', event.to_graph())
            successful_creates.append((event, target_id))
        except Exception as e:
            failed_creates.append((event, str(e)))

    # Should have 2 successes and 1 failure
    assert len(successful_creates) == 2
    assert len(failed_creates) == 1
