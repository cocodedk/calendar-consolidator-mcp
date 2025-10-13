"""
Tests for Google credentials validation logic.
"""

import pytest


def validate_google_credentials(creds):
    """
    Validate Google credentials format.
    Mirrors logic from node/server/admin_api/credentials/validate.js
    """
    if not creds.get('client_id') or not creds.get('client_secret'):
        return {'valid': False, 'error': 'Missing client_id or client_secret'}

    if not creds['client_id'].endswith('.apps.googleusercontent.com'):
        return {'valid': False, 'error': 'Invalid Google client_id format'}

    if not creds['client_secret'].startswith('GOCSPX-'):
        return {'valid': False, 'error': 'Invalid Google client_secret format'}

    return {'valid': True}


def test_validate_google_valid_credentials():
    """Test that valid Google credentials are accepted."""
    creds = {
        'client_id': '123456.apps.googleusercontent.com',
        'client_secret': 'GOCSPX-test_secret_123'
    }

    result = validate_google_credentials(creds)

    assert result['valid'] is True


def test_validate_google_invalid_client_id():
    """Test that invalid client_id format is rejected."""
    creds = {
        'client_id': 'invalid_client_id',
        'client_secret': 'GOCSPX-test_secret'
    }

    result = validate_google_credentials(creds)

    assert result['valid'] is False
    assert 'client_id' in result['error']


def test_validate_google_invalid_client_secret():
    """Test that invalid client_secret format is rejected."""
    creds = {
        'client_id': '123.apps.googleusercontent.com',
        'client_secret': 'invalid_secret'
    }

    result = validate_google_credentials(creds)

    assert result['valid'] is False
    assert 'client_secret' in result['error']


def test_validate_google_missing_fields():
    """Test that incomplete credentials are rejected."""
    creds = {'client_id': '123.apps.googleusercontent.com'}

    result = validate_google_credentials(creds)

    assert result['valid'] is False
    assert 'Missing' in result['error']


def test_validate_google_error_messages():
    """Test that validation errors have descriptive messages."""
    test_cases = [
        ({'client_id': 'bad', 'client_secret': 'GOCSPX-test'}, 'client_id'),
        ({'client_id': 'test.apps.googleusercontent.com', 'client_secret': 'bad'}, 'client_secret')
    ]

    for creds, expected_term in test_cases:
        result = validate_google_credentials(creds)
        assert result['valid'] is False
        assert expected_term.lower() in result['error'].lower()
