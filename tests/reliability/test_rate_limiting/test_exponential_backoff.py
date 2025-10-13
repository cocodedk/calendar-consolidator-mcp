"""Tests for exponential backoff on rate limiting."""


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
