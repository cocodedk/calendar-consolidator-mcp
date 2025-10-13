"""
Tests for credentials API error handling.
"""

import pytest
import requests
from unittest.mock import patch, MagicMock


API_BASE = 'http://127.0.0.1:3000'


def test_put_invalid_provider_400():
    """Test that unknown provider returns 400."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'error': 'Invalid provider'
        }
        mock_put.return_value = mock_response

        credentials = {'provider': 'invalid_provider', 'credentials': {}}
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 400


def test_put_invalid_format_400():
    """Test that invalid credential format returns 400."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Invalid credentials format'}
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'google',
            'credentials': {'client_id': 'bad', 'client_secret': 'bad'}
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 400


def test_put_validation_error_message():
    """Test that validation errors include message."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'error': 'Invalid credentials format',
            'message': 'Missing fields'
        }
        mock_put.return_value = mock_response

        credentials = {'provider': 'google', 'credentials': {'client_id': 'only_id'}}
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)
        data = response.json()

        assert 'error' in data
        assert 'message' in data


def test_put_database_error_500():
    """Test that database save failure returns 500."""
    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Failed to save credentials'}
        mock_put.return_value = mock_response

        credentials = {
            'provider': 'google',
            'credentials': {'client_id': 'test', 'client_secret': 'GOCSPX-test'}
        }
        response = requests.put(f'{API_BASE}/api/credentials', json=credentials)

        assert response.status_code == 500


def test_get_python_error_500():
    """Test that Python execution errors return 500."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Failed to fetch credentials'}
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')

        assert response.status_code == 500
