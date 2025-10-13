"""
Tests for iCloud CalDAV connector.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from python.connectors.icloud_connector.connector import ICloudConnector


class TestICloudConnector:
    """Test iCloud connector functionality."""

    @pytest.fixture
    def credentials(self):
        """Sample credentials for testing."""
        return {
            'username': 'test@icloud.com',
            'password': 'abcd-efgh-ijkl-mnop',
            'caldav_url': 'https://caldav.icloud.com/'
        }

    @pytest.fixture
    def mock_client(self):
        """Mock CalDAV client."""
        with patch('python.connectors.icloud_connector.connector.CalDAVClient') as mock:
            yield mock

    def test_init(self, credentials, mock_client):
        """Test connector initialization."""
        connector = ICloudConnector(credentials)
        assert connector.credentials == credentials
        mock_client.assert_called_once()

    def test_list_calendars(self, credentials, mock_client):
        """Test listing calendars."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_instance.list_calendars.return_value = [
            {'id': 'cal1', 'name': 'Personal', 'canWrite': True},
            {'id': 'cal2', 'name': 'Work', 'canWrite': True}
        ]

        # Test
        connector = ICloudConnector(credentials)
        calendars = connector.list_calendars()

        # Assert
        assert len(calendars) == 2
        assert calendars[0]['name'] == 'Personal'
        assert calendars[1]['name'] == 'Work'

    def test_get_events_delta(self, credentials, mock_client):
        """Test getting events delta."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_calendar = Mock()
        mock_event = Mock()
        mock_event.data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:event123
SUMMARY:Test Event
DTSTART:20250101T100000Z
DTEND:20250101T110000Z
END:VEVENT
END:VCALENDAR"""
        mock_calendar.events.return_value = [mock_event]
        mock_instance.get_calendar.return_value = mock_calendar

        # Mock parse_ical_event
        mock_instance.parse_ical_event.return_value = {
            'uid': 'event123',
            'subject': 'Test Event',
            'start': '2025-01-01T10:00:00Z',
            'end': '2025-01-01T11:00:00Z'
        }

        # Test
        connector = ICloudConnector(credentials)
        result = connector.get_events_delta('cal1')

        # Assert
        assert 'events' in result
        assert 'nextSyncToken' in result
        assert len(result['events']) > 0

    def test_create_event(self, credentials, mock_client):
        """Test creating an event."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_calendar = Mock()
        mock_instance.get_calendar.return_value = mock_calendar
        mock_instance.event_to_ical.return_value = "VCALENDAR..."

        # Test
        connector = ICloudConnector(credentials)
        event_data = {
            'uid': 'event123',
            'subject': 'New Event',
            'start': '2025-01-01T10:00:00Z',
            'end': '2025-01-01T11:00:00Z'
        }
        event_id = connector.create_event('cal1', event_data)

        # Assert
        assert event_id == 'event123'
        mock_calendar.save_event.assert_called_once()

    def test_delete_event(self, credentials, mock_client):
        """Test deleting an event."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_calendar = Mock()
        mock_event = Mock()
        mock_calendar.events.return_value = [mock_event]
        mock_instance.get_calendar.return_value = mock_calendar
        mock_instance.parse_ical_event.return_value = {'uid': 'event123'}

        # Test
        connector = ICloudConnector(credentials)
        connector.delete_event('cal1', 'event123')

        # Assert
        mock_event.delete.assert_called_once()

    def test_get_event(self, credentials, mock_client):
        """Test getting a single event."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_calendar = Mock()
        mock_event = Mock()
        mock_calendar.events.return_value = [mock_event]
        mock_instance.get_calendar.return_value = mock_calendar
        mock_instance.parse_ical_event.return_value = {
            'uid': 'event123',
            'subject': 'Test Event'
        }

        # Test
        connector = ICloudConnector(credentials)
        event = connector.get_event('cal1', 'event123')

        # Assert
        assert event is not None
        assert event['uid'] == 'event123'

    def test_get_event_not_found(self, credentials, mock_client):
        """Test getting a non-existent event."""
        # Setup mock
        mock_instance = mock_client.return_value
        mock_calendar = Mock()
        mock_calendar.events.return_value = []
        mock_instance.get_calendar.return_value = mock_calendar

        # Test
        connector = ICloudConnector(credentials)
        event = connector.get_event('cal1', 'nonexistent')

        # Assert
        assert event is None
