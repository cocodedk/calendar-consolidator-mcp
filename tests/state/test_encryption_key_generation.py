"""
Tests for encryption key generation and loading.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from python.state.encryption import (
    generate_encryption_key,
    load_or_create_key,
    get_key_file_path
)


def test_generate_encryption_key_format():
    """Test that generated key is valid Fernet key format."""
    key = generate_encryption_key()

    assert isinstance(key, bytes)
    assert len(key) == 44  # Fernet keys are 44 bytes base64 encoded


def test_load_or_create_key_creates_new(tmp_path):
    """Test that load_or_create_key creates new key if none exists."""
    key_file = tmp_path / '.encryption_key'

    with patch('python.state.encryption.get_key_file_path', return_value=key_file):
        key = load_or_create_key()

        assert key_file.exists()
        assert isinstance(key, bytes)
        assert len(key) == 44


def test_load_or_create_key_loads_existing(tmp_path):
    """Test that load_or_create_key reuses existing key."""
    key_file = tmp_path / '.encryption_key'
    existing_key = b'test_key_12345678901234567890123456789012'
    key_file.write_bytes(existing_key)

    with patch('python.state.encryption.get_key_file_path', return_value=key_file):
        key = load_or_create_key()

        assert key == existing_key


@patch('os.chmod')
@patch('os.hasattr')
def test_key_file_permissions(mock_hasattr, mock_chmod, tmp_path):
    """Test that Unix permissions are set to 600."""
    key_file = tmp_path / '.encryption_key'
    mock_hasattr.return_value = True

    with patch('python.state.encryption.get_key_file_path', return_value=key_file):
        load_or_create_key()

        mock_chmod.assert_called_once_with(key_file, 0o600)


def test_get_key_file_path_returns_path():
    """Test that get_key_file_path returns valid Path object."""
    path = get_key_file_path()

    assert isinstance(path, Path)
    assert path.name == '.encryption_key'
