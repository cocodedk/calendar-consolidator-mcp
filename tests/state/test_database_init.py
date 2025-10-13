"""Test Database initialization and connection."""

import pytest
import sqlite3
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from python.state.database import Database


def test_database_init_default_path():
    """Test Database initializes with default path."""
    db = Database()

    assert db.db_path is not None
    assert '.calendar-consolidator' in db.db_path
    assert db.conn is None


def test_database_init_custom_path():
    """Test Database initializes with custom path."""
    db = Database('/tmp/test.db')

    assert db.db_path == '/tmp/test.db'


@patch('python.state.database.sqlite3.connect')
def test_database_connect(mock_connect):
    """Test database connection setup."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    db = Database(':memory:')
    conn = db.connect()

    assert conn == mock_conn
    mock_connect.assert_called_once_with(':memory:')
    mock_conn.execute.assert_called_with("PRAGMA foreign_keys = ON")


@patch('python.state.database.sqlite3.connect')
def test_database_connect_reuses_connection(mock_connect):
    """Test database reuses existing connection."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    db = Database(':memory:')
    conn1 = db.connect()
    conn2 = db.connect()

    assert conn1 == conn2
    assert mock_connect.call_count == 1


@patch('python.state.database.sqlite3.connect')
def test_database_close(mock_connect):
    """Test database connection closing."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    db = Database(':memory:')
    db.connect()
    db.close()

    mock_conn.close.assert_called_once()
    assert db.conn is None
