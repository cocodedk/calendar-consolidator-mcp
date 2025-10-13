"""Tests for rate limiter implementation."""


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
