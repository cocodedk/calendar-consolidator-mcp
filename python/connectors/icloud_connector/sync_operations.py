"""Sync operations for iCloud connector."""

from typing import Dict, Any, List
from .caldav_client import CalDAVClient
from .helpers import parse_caldav_event, get_sync_token


class SyncOperations:
    """Handle calendar synchronization operations."""

    def __init__(self, client: CalDAVClient):
        """Initialize with CalDAV client."""
        self.client = client

    def get_events_delta(self, calendar: Any,
                         sync_token: str = None) -> Dict[str, Any]:
        """
        Get events from calendar with hash-based change detection.

        CalDAV doesn't have delta sync like Graph API.
        Fetches all events and relies on hash comparison for changes.

        Args:
            calendar: Calendar object
            sync_token: Not used for CalDAV (for interface compatibility)

        Returns:
            Dict with 'events' list and 'nextSyncToken'
        """
        caldav_events = calendar.events()
        events: List[Dict[str, Any]] = []

        for caldav_event in caldav_events:
            ical_data = caldav_event.data
            event = parse_caldav_event(ical_data, self.client)
            if event:
                events.append(event)

        return {
            'events': events,
            'nextSyncToken': get_sync_token(),
        }
