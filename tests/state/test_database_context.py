"""Test Database context manager behavior."""

import pytest
from unittest.mock import MagicMock, patch
from python.state.database import Database


@patch('python.state.database.sqlite3.connect')
def test_database_context_manager(mock_connect):
    """Test Database works as context manager."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    with Database(':memory:') as db:
        assert db.conn is not None

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('python.state.database.sqlite3.connect')
def test_database_context_manager_exception(mock_connect):
    """Test context manager doesn't commit on exception."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    try:
        with Database(':memory:') as db:
            raise ValueError("Test error")
    except ValueError:
        pass

    mock_conn.commit.assert_not_called()
    mock_conn.close.assert_called_once()


@patch('python.state.database.sqlite3.connect')
def test_database_context_manager_nested_operations(mock_connect):
    """Test performing operations within context."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    with Database(':memory:') as db:
        conn = db.connect()
        conn.execute("SELECT 1")

    mock_conn.execute.assert_called()
