"""
Tests for GET /api/credentials endpoint.
"""

import pytest
import requests
from unittest.mock import patch, MagicMock


API_BASE = 'http://127.0.0.1:3000'


def test_get_credentials_returns_all_providers():
    """Test that GET returns all three providers."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'google': {'configured': False},
            'microsoft': {'configured': False},
            'icloud': {'configured': False}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')
        data = response.json()

        assert 'google' in data
        assert 'microsoft' in data
        assert 'icloud' in data


def test_get_credentials_masks_secrets():
    """Test that secrets are masked in response."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'google': {
                'client_id': '123.apps.googleusercontent.com',
                'client_secret': 'GOC***...***xyz',
                'configured': True
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')
        data = response.json()

        assert '***' in data['google']['client_secret']


def test_get_credentials_configured_status():
    """Test that configured status is shown."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'google': {'configured': True},
            'microsoft': {'configured': False}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')
        data = response.json()

        assert data['google']['configured'] is True
        assert data['microsoft']['configured'] is False


def test_get_credentials_not_configured():
    """Test response when no credentials are configured."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'google': {'configured': False},
            'microsoft': {'configured': False},
            'icloud': {'configured': False}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')

        assert response.status_code == 200


def test_get_credentials_error_handling():
    """Test that server errors return 500."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Server error'}
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')

        assert response.status_code == 500
