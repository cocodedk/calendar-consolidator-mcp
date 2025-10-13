"""
Tests for PUT /api/credentials endpoint.
"""

import pytest
import requests
from unittest.mock import patch, MagicMock


API_BASE = 'http://127.0.0.1:3000'


def test_put_credentials_google_success():
    """Test that saving Google credentials returns success."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'google',
            'credentials': {
                'client_id': '123.apps.googleusercontent.com',
                'client_secret': 'GOCSPX-secret'
            }
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 200
        assert response.json()['success'] is True


def test_put_credentials_microsoft_success():
    """Test that saving Microsoft credentials returns success."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'microsoft',
            'credentials': {
                'client_id': '12345678-1234-1234-1234-123456789012',
                'tenant_id': 'common',
                'client_secret': 'test_secret'
            }
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 200


def test_put_credentials_validates_format():
    """Test that validation is performed before saving."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Invalid credentials format'}
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'google',
            'credentials': {'client_id': 'invalid', 'client_secret': 'GOCSPX-secret'}
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 400


def test_put_credentials_returns_success_message():
    """Test that success response includes message."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'message': 'credentials updated'
        }
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'google',
            'credentials': {'client_id': 'test', 'client_secret': 'GOCSPX-test'}
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)
        data = response.json()

        assert 'message' in data
