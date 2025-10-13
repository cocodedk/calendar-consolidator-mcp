"""Tests for credential isolation in error messages."""

from unittest.mock import Mock, patch
import requests
from datetime import datetime, timedelta, timezone


def test_credentials_not_in_error_messages():
    """Error messages don't expose credentials."""
    from python.connectors.graph_connector import GraphConnector

    credentials = {
        'access_token': 'secret_token_12345',
        'refresh_token': 'secret_refresh_67890',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.connector.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")
        mock_get.return_value = mock_response

        connector = GraphConnector(credentials)

        try:
            connector.list_calendars()
        except Exception as e:
            error_msg = str(e)
            # Credentials should not appear in error message
            assert 'secret_token_12345' not in error_msg
            assert 'secret_refresh_67890' not in error_msg
