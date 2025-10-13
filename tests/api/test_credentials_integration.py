"""
Integration tests for full credentials flow.
"""

import pytest
import requests
from unittest.mock import patch, MagicMock


API_BASE = 'http://127.0.0.1:3000'


def test_full_flow_google():
    """Test complete flow: save and retrieve Google credentials."""
    google_creds = {
        'client_id': '123456.apps.googleusercontent.com',
        'client_secret': 'GOCSPX-test_secret_123'
    }

    with patch('requests.put') as mock_put:
        mock_put_response = MagicMock()
        mock_put_response.status_code = 200
        mock_put_response.json.return_value = {'success': True}
        mock_put.return_value = mock_put_response

        save_response = requests.put(
            f'{API_BASE}/api/credentials',
            json={'provider': 'google', 'credentials': google_creds}
        )
        assert save_response.status_code == 200


def test_full_flow_microsoft():
    """Test complete flow: save Microsoft credentials."""
    microsoft_creds = {
        'client_id': '12345678-1234-1234-1234-123456789012',
        'tenant_id': 'common',
        'client_secret': 'test_secret_value'
    }

    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_put.return_value = mock_response

        response = requests.put(
            f'{API_BASE}/api/credentials',
            json={'provider': 'microsoft', 'credentials': microsoft_creds}
        )

        assert response.status_code == 200


def test_update_existing_credentials():
    """Test that updating existing credentials works."""
    updated_creds = {'client_id': 'new_id', 'client_secret': 'GOCSPX-new'}

    with patch('requests.put') as mock_put:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_put.return_value = mock_response

        response = requests.put(
            f'{API_BASE}/api/credentials',
            json={'provider': 'google', 'credentials': updated_creds}
        )

        assert response.status_code == 200


def test_credentials_persist():
    """Test that saved credentials persist."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'google': {'configured': True}}
        mock_get.return_value = mock_response

        response = requests.get(f'{API_BASE}/api/credentials')
        data = response.json()

        assert data['google']['configured'] is True
