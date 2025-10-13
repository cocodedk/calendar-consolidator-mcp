"""Tests for exponential backoff retry logic."""

import time


def test_exponential_backoff_retry():
    """Retry logic uses exponential backoff."""
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
