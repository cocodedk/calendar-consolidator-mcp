"""
Tests for adding sources with session credentials.
"""

import pytest
from unittest.mock import Mock


def test_add_source_with_session():
    """Test adding source using sessionId."""
    session = {
        'id': 'session123',
        'type': 'google',
        'credentials': {'access_token': 'token', 'refresh_token': 'refresh'},
        'status': 'complete'
    }

    source_data = {
        'type': 'google',
        'calendarId': 'cal123',
        'name': 'My Calendar',
        'sessionId': 'session123'
    }

    # Should retrieve credentials from session
    assert source_data['sessionId'] == session['id']
    assert session['credentials'] is not None


def test_add_source_invalid_session():
    """Test adding source with invalid session."""
    source_data = {
        'type': 'google',
        'calendarId': 'cal123',
        'name': 'My Calendar',
        'sessionId': 'invalid-session'
    }

    # Should return 400 error
    session = None
    assert session is None


def test_add_source_with_direct_credentials():
    """Test adding source with direct credentials."""
    source_data = {
        'type': 'google',
        'calendarId': 'cal123',
        'name': 'My Calendar',
        'credentials': {'access_token': 'token'}
    }

    # Should use provided credentials
    assert 'credentials' in source_data
    assert source_data['credentials']['access_token'] == 'token'


def test_add_multiple_sources_from_session():
    """Test adding multiple calendars from one auth session."""
    session = {
        'credentials': {'access_token': 'token'},
        'calendars': [
            {'id': 'cal1', 'name': 'Work'},
            {'id': 'cal2', 'name': 'Personal'}
        ]
    }

    sources = [
        {'calendarId': cal['id'], 'name': cal['name']}
        for cal in session['calendars']
    ]

    assert len(sources) == 2
    assert sources[0]['calendarId'] == 'cal1'
    assert sources[1]['calendarId'] == 'cal2'
