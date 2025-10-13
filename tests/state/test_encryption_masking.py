"""
Tests for secret masking functionality.
"""

import pytest
from python.state.encryption import mask_secret


def test_mask_secret_short_string():
    """Test that short strings return ***."""
    short_secret = 'abc'

    masked = mask_secret(short_secret)

    assert masked == '***'


def test_mask_secret_long_string():
    """Test that long strings show prefix and suffix."""
    long_secret = 'GOCSPX-1234567890abcdefghij'

    masked = mask_secret(long_secret)

    assert masked.startswith('GOC')
    assert masked.endswith('hij')
    assert '***...***' in masked


def test_mask_secret_empty_string():
    """Test that empty string returns ***."""
    masked = mask_secret('')

    assert masked == '***'


def test_mask_secret_default_chars():
    """Test that default show_chars is 3."""
    secret = '1234567890'

    masked = mask_secret(secret)

    assert masked == '123***...***890'


def test_mask_secret_custom_chars():
    """Test that custom show_chars works."""
    secret = '1234567890abcd'

    masked = mask_secret(secret, show_chars=5)

    assert masked == '12345***...***0abcd'


def test_mask_secret_none_input():
    """Test that None input returns ***."""
    masked = mask_secret(None)

    assert masked == '***'


def test_mask_secret_exactly_double_show_chars():
    """Test edge case where length equals 2 * show_chars."""
    secret = '123456'  # Length 6, default show_chars=3, 2*3=6

    masked = mask_secret(secret)

    assert masked == '***'
