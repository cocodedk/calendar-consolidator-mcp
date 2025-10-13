"""Tests for max retry limits."""

import pytest


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
