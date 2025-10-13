"""Test credential blob conversion functions."""

import pytest
import json
from unittest.mock import patch
from python.state.encryption import credentials_to_blob, blob_to_credentials


def test_credentials_to_blob():
    """Test converting credentials to blob."""
    creds = {'access_token': 'abc', 'refresh_token': 'xyz'}

    blob = credentials_to_blob(creds)

    assert isinstance(blob, bytes)
    data = json.loads(blob.decode('utf-8'))
    assert data['keychain'] is True


def test_credentials_to_blob_consistent():
    """Test blob conversion is consistent."""
    creds = {'token': 'value'}

    blob1 = credentials_to_blob(creds)
    blob2 = credentials_to_blob(creds)

    assert blob1 == blob2


@patch('python.state.encryption.load_credentials')
def test_blob_to_credentials(mock_load):
    """Test converting blob back to credentials."""
    reference = {'keychain': True}
    blob = json.dumps(reference).encode('utf-8')
    mock_load.return_value = {'token': 'restored'}

    result = blob_to_credentials(blob, 'source-1')

    assert result == {'token': 'restored'}
    mock_load.assert_called_once_with('source-1')


@patch('python.state.encryption.load_credentials')
def test_blob_to_credentials_none(mock_load):
    """Test blob conversion when credentials not found."""
    blob = json.dumps({'keychain': True}).encode('utf-8')
    mock_load.return_value = None

    result = blob_to_credentials(blob, 'nonexistent')

    assert result is None
