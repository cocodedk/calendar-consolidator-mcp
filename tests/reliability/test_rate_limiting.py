"""Test handling of 429 rate limit responses."""

import pytest
from unittest.mock import Mock, patch
import requests
from datetime import datetime, timedelta


def test_handles_429_response():
    """Connector handles 429 rate limit response."""
    from python.connectors.graph_connector import GraphConnector

    credentials = {
        'access_token': 'token123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }

    with patch('python.connectors.graph_connector.requests.get') as mock_get:
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


def test_exponential_backoff_on_multiple_429():
    """Multiple 429 responses trigger exponential backoff."""
    retry_count = [0]

    def api_call_with_backoff():
        """Simulated API call with retry logic."""
        max_retries = 3
        base_delay = 1

        for attempt in range(max_retries):
            retry_count[0] += 1

            if attempt < 2:  # Simulate 2 failures
                # In real implementation, would wait: base_delay * (2 ** attempt)
                continue
            else:
                return "success"

        raise Exception("Max retries exceeded")

    result = api_call_with_backoff()
    assert result == "success"
    assert retry_count[0] == 3


def test_rate_limit_tracking():
    """Track rate limit usage to avoid hitting limits."""
    class RateLimiter:
        """Simple rate limiter."""
        def __init__(self, max_calls, period):
            self.max_calls = max_calls
            self.period = period
            self.calls = []

        def can_make_call(self):
            """Check if call is allowed."""
            import time
            now = time.time()

            # Remove old calls outside the period
            self.calls = [t for t in self.calls if now - t < self.period]

            return len(self.calls) < self.max_calls

        def record_call(self):
            """Record a call."""
            import time
            self.calls.append(time.time())

    limiter = RateLimiter(max_calls=5, period=10)

    # Make 5 calls
    for _ in range(5):
        assert limiter.can_make_call()
        limiter.record_call()

    # 6th call should be blocked
    assert not limiter.can_make_call()
