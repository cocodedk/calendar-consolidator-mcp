"""Calendar listing operations for iCloud connector."""

from typing import List, Dict, Any
from .caldav_client import CalDAVClient


class CalendarOperations:
    """Handle calendar discovery and listing."""

    def __init__(self, client: CalDAVClient):
        """Initialize with CalDAV client."""
        self.client = client

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's iCloud calendars via CalDAV."""
        return self.client.list_calendars()

    def get_calendar(self, calendar_id: str) -> Any:
        """Get calendar object by ID."""
        return self.client.get_calendar(calendar_id)
