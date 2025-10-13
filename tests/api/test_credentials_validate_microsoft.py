"""
Tests for Microsoft credentials validation logic.
"""

import pytest
import re


def validate_microsoft_credentials(creds):
    """
    Validate Microsoft credentials format.
    Mirrors logic from node/server/admin_api/credentials/validate.js
    """
    if not creds.get('client_id') or not creds.get('client_secret') or not creds.get('tenant_id'):
        return {'valid': False, 'error': 'Missing client_id, client_secret, or tenant_id'}

    # GUID validation regex
    guid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

    if not re.match(guid_regex, creds['client_id'], re.IGNORECASE) and creds['client_id'] != 'common':
        return {'valid': False, 'error': 'Invalid Microsoft client_id format'}

    if not re.match(guid_regex, creds['tenant_id'], re.IGNORECASE) and creds['tenant_id'] != 'common':
        return {'valid': False, 'error': 'Invalid Microsoft tenant_id format'}

    if len(creds['client_secret']) < 8:
        return {'valid': False, 'error': 'Invalid Microsoft client_secret format'}

    return {'valid': True}


def test_validate_microsoft_valid_credentials():
    """Test that valid Microsoft credentials with GUIDs are accepted."""
    creds = {
        'client_id': '12345678-1234-1234-1234-123456789012',
        'tenant_id': '87654321-4321-4321-4321-210987654321',
        'client_secret': 'test_secret_value_123'
    }
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is True


def test_validate_microsoft_common_tenant():
    """Test that 'common' tenant_id is accepted."""
    creds = {
        'client_id': '12345678-1234-1234-1234-123456789012',
        'tenant_id': 'common',
        'client_secret': 'test_secret_value'
    }
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is True


def test_validate_microsoft_invalid_client_id():
    """Test that invalid client_id GUID is rejected."""
    creds = {
        'client_id': 'not-a-valid-guid',
        'tenant_id': 'common',
        'client_secret': 'test_secret'
    }
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is False
    assert 'client_id' in result['error']


def test_validate_microsoft_invalid_tenant_id():
    """Test that invalid tenant_id is rejected."""
    creds = {
        'client_id': '12345678-1234-1234-1234-123456789012',
        'tenant_id': 'invalid_tenant',
        'client_secret': 'test_secret'
    }
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is False
    assert 'tenant_id' in result['error']


def test_validate_microsoft_short_secret():
    """Test that client_secret too short is rejected."""
    creds = {
        'client_id': '12345678-1234-1234-1234-123456789012',
        'tenant_id': 'common',
        'client_secret': 'short'
    }
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is False
    assert 'client_secret' in result['error']


def test_validate_microsoft_missing_fields():
    """Test that incomplete credentials are rejected."""
    creds = {'client_id': '12345678-1234-1234-1234-123456789012'}
    result = validate_microsoft_credentials(creds)
    assert result['valid'] is False
    assert 'Missing' in result['error']
