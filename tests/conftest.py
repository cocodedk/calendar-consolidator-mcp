"""Shared pytest fixtures for Calendar Consolidator MCP tests."""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock
import sqlite3


@pytest.fixture
def sample_datetime():
    """Sample datetime for testing."""
    return datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_event_data(sample_datetime):
    """Sample event data dictionary."""
    return {
        'uid': 'event-123',
        'subject': 'Team Meeting',
        'start': sample_datetime,
        'end': datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc),
        'location': 'Conference Room A',
        'description': 'Weekly team sync',
        'is_all_day': False,
        'is_cancelled': False,
        'is_private': False
    }


@pytest.fixture
def sample_graph_event():
    """Sample Microsoft Graph API event format."""
    return {
        'id': 'graph-event-456',
        'subject': 'Project Review',
        'start': {'dateTime': '2025-01-20T14:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2025-01-20T15:30:00Z', 'timeZone': 'UTC'},
        'location': {'displayName': 'Room B'},
        'bodyPreview': 'Quarterly project review',
        'isAllDay': False,
        'isCancelled': False,
        'sensitivity': 'normal',
        'organizer': {'emailAddress': {'address': 'organizer@example.com'}},
        'attendees': [
            {'emailAddress': {'address': 'attendee1@example.com'}},
            {'emailAddress': {'address': 'attendee2@example.com'}}
        ]
    }


@pytest.fixture
def sample_credentials():
    """Sample credentials dictionary."""
    return {
        'access_token': 'mock-token-xyz',
        'refresh_token': 'mock-refresh-abc',
        'expires_at': 1705334400
    }


@pytest.fixture
def mock_db_connection():
    """Mock SQLite database connection."""
    conn = MagicMock(spec=sqlite3.Connection)
    conn.row_factory = sqlite3.Row
    cursor = MagicMock()
    cursor.lastrowid = 1
    cursor.fetchone.return_value = None
    cursor.fetchall.return_value = []
    conn.execute.return_value = cursor
    conn.cursor.return_value = cursor
    return conn


@pytest.fixture
def mock_database(mock_db_connection):
    """Mock Database instance."""
    from python.state.database import Database
    db = Mock(spec=Database)
    db.connect.return_value = mock_db_connection
    db.db_path = ':memory:'
    return db
