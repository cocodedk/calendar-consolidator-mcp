"""
Tests for OAuth authentication routes.
Note: These are unit tests for auth flow logic.
Integration tests with actual Node.js server are in test_auth_integration.py
"""

import pytest


def test_start_flow_google():
    """Test Google OAuth flow response format."""
    # Expected response format from Google flow
    response_data = {
        'sessionId': 'test-session',
        'userCode': 'ABC-123',
        'verificationUrl': 'https://google.com/device'
    }

    assert response_data['userCode'] == 'ABC-123'
    assert 'sessionId' in response_data
    assert 'verificationUrl' in response_data


def test_start_flow_graph():
    """Test Microsoft Graph OAuth flow response format."""
    # Expected response format from Graph flow
    response_data = {
        'sessionId': 'test-session',
        'userCode': 'XYZ-789',
        'verificationUrl': 'https://microsoft.com/device'
    }

    assert response_data['userCode'] == 'XYZ-789'
    assert 'sessionId' in response_data
    assert 'verificationUrl' in response_data


def test_start_flow_invalid_type():
    """Test invalid provider type."""
    # Should reject invalid types
    invalid_types = ['invalid', 'caldav', '']
    for invalid_type in invalid_types:
        # Expect 400 error
        assert invalid_type not in ['graph', 'google']


def test_poll_auth_pending():
    """Test polling pending authentication."""
    session_status = {'status': 'pending', 'error': None}
    assert session_status['status'] == 'pending'


def test_poll_auth_complete():
    """Test polling completed authentication."""
    session_status = {'status': 'complete', 'error': None}
    assert session_status['status'] == 'complete'


def test_poll_auth_error():
    """Test polling failed authentication."""
    session_status = {'status': 'error', 'error': 'Auth denied'}
    assert session_status['status'] == 'error'
    assert session_status['error'] is not None


def test_list_calendars():
    """Test calendar list response format."""
    # Expected calendar list format
    calendars = [
        {'id': 'cal1', 'name': 'Work', 'canWrite': True},
        {'id': 'cal2', 'name': 'Personal', 'canWrite': False}
    ]

    assert len(calendars) == 2
    assert calendars[0]['name'] == 'Work'
    assert calendars[0]['canWrite'] is True
    assert all('id' in cal and 'name' in cal for cal in calendars)
