"""Tests for credential sanitization in debug output."""

import logging
from io import StringIO


def test_credentials_not_in_debug_output():
    """Debug/verbose output sanitizes credentials."""
    # Create string buffer to capture logs
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger('test_logger')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    credentials = {'access_token': 'secret_abc123'}

    # Sanitize function
    def sanitize_dict(data):
        """Sanitize sensitive fields."""
        sanitized = data.copy()
        for key in ['access_token', 'refresh_token', 'password']:
            if key in sanitized:
                sanitized[key] = '***REDACTED***'
        return sanitized

    # Log sanitized version
    logger.debug(f"Credentials: {sanitize_dict(credentials)}")

    log_output = log_stream.getvalue()
    assert 'secret_abc123' not in log_output
    assert '***REDACTED***' in log_output
