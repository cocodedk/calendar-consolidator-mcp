"""
iCloud CalDAV connector implementation - aggregates modular operations.
"""

from typing import List, Dict, Any, Optional
from ..base_connector import BaseConnector
from .caldav_client import CalDAVClient
from .calendar_operations import CalendarOperations
from .event_operations import EventOperations
from .sync_operations import SyncOperations


class ICloudConnector(BaseConnector):
    """iCloud CalDAV connector for calendar operations."""

    def __init__(self, credentials: Dict[str, Any]):
        """Initialize iCloud connector with credentials."""
        self.credentials = credentials
        self.client = CalDAVClient(
            username=credentials['username'],
            password=credentials['password'],
            caldav_url=credentials.get('caldav_url',
                                      'https://caldav.icloud.com/')
        )
        self.calendar_ops = CalendarOperations(self.client)
        self.event_ops = EventOperations(self.client)
        self.sync_ops = SyncOperations(self.client)

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's iCloud calendars via CalDAV."""
        return self.calendar_ops.list_calendars()

    def get_events_delta(self, calendar_id: str,
                        sync_token: Optional[str] = None) -> Dict[str, Any]:
        """Get events from calendar via sync operations."""
        calendar = self.calendar_ops.get_calendar(calendar_id)
        return self.sync_ops.get_events_delta(calendar, sync_token)

    def create_event(self, calendar_id: str,
                    event_data: Dict[str, Any]) -> str:
        """Create event in iCloud calendar."""
        calendar = self.calendar_ops.get_calendar(calendar_id)
        return self.event_ops.create_event(calendar, event_data)

    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """Update existing event."""
        calendar = self.calendar_ops.get_calendar(calendar_id)
        self.event_ops.update_event(calendar, event_id, event_data)

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete event from calendar."""
        calendar = self.calendar_ops.get_calendar(calendar_id)
        self.event_ops.delete_event(calendar, event_id)

    def get_event(self, calendar_id: str,
                  event_id: str) -> Optional[Dict[str, Any]]:
        """Get single event by UID."""
        calendar = self.calendar_ops.get_calendar(calendar_id)
        return self.event_ops.get_event(calendar, event_id)


def list_calendars(credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Module-level helper for Node bridge: construct and list calendars."""
    connector = ICloudConnector(credentials)
    return connector.list_calendars()
