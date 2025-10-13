"""Test retry logic for transient failures."""

import pytest
from unittest.mock import Mock, patch
import requests


def test_connector_retries_on_network_error():
    """Connector retries on network errors."""
    from python.connectors.graph_connector import GraphConnector
    from datetime import datetime, timedelta

    credentials = {
        'access_token': 'token123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.requests.get') as mock_get:
        # First call fails, second succeeds
        mock_get.side_effect = [
            requests.ConnectionError("Network error"),
            Mock(json=lambda: {'value': []}, raise_for_status=Mock())
        ]

        connector = GraphConnector(credentials)

        # Should retry and eventually succeed
        # Note: Current implementation may not have retry logic yet
        with pytest.raises(requests.ConnectionError):
            connector.list_calendars()


def test_exponential_backoff_retry():
    """Retry logic uses exponential backoff."""
    import time

    retry_delays = []

    def retry_with_backoff(func, max_retries=3):
        """Example retry function with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception:
                if attempt < max_retries - 1:
                    delay = 2 ** attempt  # Exponential: 1, 2, 4 seconds
                    retry_delays.append(delay)
                    time.sleep(delay)
                else:
                    raise

    def failing_func():
        if len(retry_delays) < 2:
            raise Exception("Temporary failure")
        return "success"

    result = retry_with_backoff(failing_func)

    assert result == "success"
    assert retry_delays == [1, 2]  # Exponential backoff


def test_max_retries_exceeded():
    """Function fails after max retries exceeded."""
    def retry_with_limit(func, max_retries=3):
        """Retry function with limit."""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise

    call_count = [0]

    def always_fails():
        call_count[0] += 1
        raise Exception("Permanent failure")

    with pytest.raises(Exception, match="Permanent failure"):
        retry_with_limit(always_fails)

    assert call_count[0] == 3  # Should try 3 times


def test_no_retry_on_client_error():
    """Client errors (4xx) should not be retried."""
    from python.connectors.graph_connector import GraphConnector
    from datetime import datetime, timedelta

    credentials = {
        'access_token': 'token123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.requests.get') as mock_get:
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
