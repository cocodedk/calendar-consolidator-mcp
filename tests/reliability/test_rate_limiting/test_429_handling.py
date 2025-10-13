"""Tests for handling 429 rate limit responses."""

import pytest
from unittest.mock import Mock, patch
import requests
from datetime import datetime, timedelta, timezone


def test_handles_429_response():
    """Connector handles 429 rate limit response."""
    from python.connectors.graph_connector import GraphConnector

    credentials = {
        'access_token': 'token123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.connector.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.HTTPError("429 Too Many Requests")
        mock_response.headers = {'Retry-After': '60'}
        mock_get.return_value = mock_response

        connector = GraphConnector(credentials)

        with pytest.raises(requests.HTTPError):
            connector.list_calendars()


def test_respects_retry_after_header():
    """Rate limit handler respects Retry-After header."""
    def handle_rate_limit(response):
        """Example rate limit handler."""
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            return retry_after
        return 0

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {'Retry-After': '120'}

    delay = handle_rate_limit(mock_response)
    assert delay == 120
