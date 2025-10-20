"""
CalDAV client wrapper for iCloud operations - aggregates modular helpers.
"""

from typing import List, Dict, Any
import caldav
from .helpers import CalendarOps, parse_ical_event, event_to_ical


class CalDAVClient:
    """Wrapper for caldav library with iCloud-specific operations."""

    def __init__(self, username: str, password: str, caldav_url: str):
        """
        Initialize CalDAV client.

        Args:
            username: Apple ID email
            password: App-specific password
            caldav_url: CalDAV server URL
        """
        self.client = caldav.DAVClient(
            url=caldav_url,
            username=username,
            password=password
        )
        self.calendar_ops = CalendarOps(self.client)

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List all calendars for the user."""
        return self.calendar_ops.list_calendars()

    def get_calendar(self, calendar_url: str) -> Any:
        """Get calendar object by URL."""
        return self.calendar_ops.get_calendar(calendar_url)

    def parse_ical_event(self, ical_data: str) -> Dict[str, Any]:
        """Parse iCalendar data to normalized event dict."""
        return parse_ical_event(ical_data)

    def event_to_ical(self, event_data: Dict[str, Any]) -> str:
        """Convert normalized event dict to iCalendar format."""
        return event_to_ical(event_data)
