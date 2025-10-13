"""
Tests for encryption and decryption operations.
"""

import pytest
from unittest.mock import patch, MagicMock
from python.state.encryption import (
    encrypt_credentials,
    decrypt_credentials,
    get_fernet
)


@pytest.fixture
def sample_credentials():
    """Sample credentials dictionary."""
    return {
        'client_id': '12345.apps.googleusercontent.com',
        'client_secret': 'GOCSPX-test_secret'
    }


def test_encrypt_credentials_returns_string(sample_credentials):
    """Test that encrypt_credentials returns base64 string."""
    encrypted = encrypt_credentials(sample_credentials)

    assert isinstance(encrypted, str)
    assert len(encrypted) > 0


def test_decrypt_credentials_returns_dict(sample_credentials):
    """Test that decrypt_credentials returns original dict."""
    encrypted = encrypt_credentials(sample_credentials)
    decrypted = decrypt_credentials(encrypted)

    assert isinstance(decrypted, dict)
    assert decrypted == sample_credentials


def test_encrypt_decrypt_roundtrip(sample_credentials):
    """Test that encryption-decryption preserves data integrity."""
    encrypted = encrypt_credentials(sample_credentials)
    decrypted = decrypt_credentials(encrypted)

    assert decrypted['client_id'] == sample_credentials['client_id']
    assert decrypted['client_secret'] == sample_credentials['client_secret']


def test_decrypt_invalid_data_returns_none():
    """Test that decrypting invalid data returns None."""
    invalid_encrypted = 'invalid_base64_data'

    result = decrypt_credentials(invalid_encrypted)

    assert result is None


def test_encrypt_different_data_different_output():
    """Test that different data produces different encrypted output."""
    data1 = {'key': 'value1'}
    data2 = {'key': 'value2'}

    encrypted1 = encrypt_credentials(data1)
    encrypted2 = encrypt_credentials(data2)

    assert encrypted1 != encrypted2


def test_get_fernet_returns_fernet_instance():
    """Test that get_fernet returns Fernet cipher instance."""
    fernet = get_fernet()

    assert fernet is not None
    assert hasattr(fernet, 'encrypt')
    assert hasattr(fernet, 'decrypt')
