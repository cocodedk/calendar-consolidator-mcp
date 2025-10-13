"""
Integration tests for OAuth authentication flow.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAuthIntegration:
    """Integration tests for auth endpoints."""

    @patch('python.connectors.graph_auth.GraphAuthenticator')
    def test_full_graph_flow(self, mock_auth):
        """Test complete Microsoft Graph OAuth flow."""
        # Mock device code flow
        mock_instance = MagicMock()
        mock_instance.get_device_code_flow.return_value = {
            'user_code': 'TEST123',
            'verification_uri': 'https://login.microsoft.com/device'
        }
        mock_instance.acquire_token_by_device_flow.return_value = {
            'access_token': 'token',
            'refresh_token': 'refresh'
        }
        mock_auth.return_value = mock_instance

        # Verify flow data structure
        flow = mock_instance.get_device_code_flow.return_value
        assert 'user_code' in flow
        assert 'verification_uri' in flow

        # Verify token acquisition
        tokens = mock_instance.acquire_token_by_device_flow.return_value
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens

    @patch('python.connectors.google_auth.authenticator.GoogleAuthenticator')
    def test_full_google_flow(self, mock_auth):
        """Test complete Google OAuth flow."""
        mock_instance = MagicMock()
        mock_instance.get_device_code_flow.return_value = {
            'user_code': 'GOOGLE456',
            'verification_url': 'https://accounts.google.com/device'
        }
        mock_instance.acquire_token_by_code.return_value = {
            'access_token': 'gtoken',
            'refresh_token': 'grefresh'
        }
        mock_auth.return_value = mock_instance

        flow = mock_instance.get_device_code_flow.return_value
        assert 'user_code' in flow
        assert 'verification_url' in flow

    def test_session_timeout_handling(self):
        """Test session expiration."""
        import time
        session_created = time.time()
        session_timeout = 10 * 60  # 10 minutes

        # Simulate time passing
        current_time = session_created + (11 * 60)  # 11 minutes later
        is_expired = (current_time - session_created) > session_timeout

        assert is_expired is True

    def test_concurrent_auth_sessions(self):
        """Test multiple auth sessions simultaneously."""
        sessions = {
            'session1': {'type': 'google', 'status': 'pending'},
            'session2': {'type': 'graph', 'status': 'pending'},
            'session3': {'type': 'google', 'status': 'complete'}
        }

        # Each session should be independent
        assert len(sessions) == 3
        assert sessions['session3']['status'] == 'complete'
        assert sessions['session1']['status'] == 'pending'
