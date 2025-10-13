"""Shared fixtures for data consistency tests."""

import pytest
from python.model.event import Event
from datetime import datetime


@pytest.fixture
def sample_event():
    """Standard test event."""
    return Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Room 101',
        description='Team meeting',
        is_private=False
    )
