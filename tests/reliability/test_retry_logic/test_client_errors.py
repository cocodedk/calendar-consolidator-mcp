"""Tests for handling client errors (no retry)."""

import pytest
from unittest.mock import Mock, patch
import requests
from datetime import datetime, timedelta, timezone


def test_no_retry_on_client_error():
    """Client errors (4xx) should not be retried."""
    from python.connectors.graph_connector import GraphConnector

    credentials = {
        'access_token': 'token123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.connector.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.HTTPError("400 Bad Request")
        mock_get.return_value = mock_response

        connector = GraphConnector(credentials)

        # Should not retry on 400 error
        with pytest.raises(requests.HTTPError):
            connector.list_calendars()

        # Should only be called once (no retries)
        assert mock_get.call_count == 1
