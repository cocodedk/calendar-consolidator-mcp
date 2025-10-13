"""Test GoogleConnector error handling."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta, timezone
from python.connectors.google_connector import GoogleConnector


@pytest.fixture
def valid_credentials():
    """Valid credentials fixture."""
    return {
        'access_token': 'access123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }


@pytest.fixture
def expired_credentials():
    """Expired credentials fixture."""
    return {
        'access_token': 'expired_token',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    }


@patch('python.connectors.google_connector.service.build')
def test_token_refresh_on_expired(mock_build, expired_credentials):
    """Connector refreshes token when expired."""
    with patch('python.connectors.google_connector.token_manager.TokenManager.refresh_if_needed') as mock_refresh:
        connector = GoogleConnector(expired_credentials)
        mock_refresh.assert_called()


@patch('python.connectors.google_connector.service.build')
def test_missing_refresh_token(mock_build):
    """Connector raises error when refresh token missing."""
    credentials = {
        'access_token': 'access123',
        'expires_at': (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    }

    with pytest.raises(Exception, match="No refresh token"):
        connector = GoogleConnector(credentials)


@patch('python.connectors.google_connector.service.build')
def test_api_error_propagates(mock_build, valid_credentials):
    """API errors are propagated to caller."""
    mock_service = Mock()
    mock_events = Mock()
    mock_events.list().execute.side_effect = Exception("API quota exceeded")
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service

    connector = GoogleConnector(valid_credentials)
    with pytest.raises(Exception, match="API quota exceeded"):
        connector.get_events_delta('cal1')
