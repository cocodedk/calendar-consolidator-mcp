"""
iCloud CalDAV connector implementation.
"""

from typing import List, Dict, Any, Optional
from ..base_connector import BaseConnector
from .caldav_client import CalDAVClient
import hashlib


class ICloudConnector(BaseConnector):
    """iCloud CalDAV connector for calendar operations."""

    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialize iCloud connector.

        Args:
            credentials: Dict with username, password, caldav_url
        """
        self.credentials = credentials
        self.client = CalDAVClient(
            username=credentials['username'],
            password=credentials['password'],
            caldav_url=credentials.get('caldav_url',
                                      'https://caldav.icloud.com/')
        )

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's iCloud calendars via CalDAV."""
        return self.client.list_calendars()

    def get_events_delta(self, calendar_id: str,
                        sync_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get events from calendar.

        Note: CalDAV doesn't have delta sync like Graph API.
        We fetch all events and rely on hash comparison for changes.

        Args:
            calendar_id: Calendar URL
            sync_token: Not used for CalDAV (hash-based sync)

        Returns:
            Dict with 'events' list and 'nextSyncToken'
        """
        calendar = self.client.get_calendar(calendar_id)

        # Fetch all events
        caldav_events = calendar.events()

        events = []
        for caldav_event in caldav_events:
            try:
                ical_data = caldav_event.data
                event = self.client.parse_ical_event(ical_data)

                if event and event.get('uid'):
                    # Store raw data for hash calculation
                    event['_raw_data'] = ical_data
                    events.append(event)
            except Exception as e:
                print(f"Warning: Failed to parse event: {e}")
                continue

        # Use timestamp as sync token (CalDAV doesn't have proper sync tokens)
        import time
        next_token = str(int(time.time()))

        return {
            'events': events,
            'nextSyncToken': next_token
        }

    def create_event(self, calendar_id: str,
                    event_data: Dict[str, Any]) -> str:
        """
        Create event in iCloud calendar.

        Args:
            calendar_id: Calendar URL
            event_data: Normalized event dictionary

        Returns:
            Event UID
        """
        calendar = self.client.get_calendar(calendar_id)

        # Generate UID if not present
        if 'uid' not in event_data:
            import uuid
            event_data['uid'] = str(uuid.uuid4())

        # Convert to iCalendar format
        ical_data = self.client.event_to_ical(event_data)

        # Create event
        calendar.save_event(ical_data)

        return event_data['uid']

    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """
        Update existing event.

        Args:
            calendar_id: Calendar URL
            event_id: Event UID
            event_data: Updated event data
        """
        calendar = self.client.get_calendar(calendar_id)

        # Find event by UID
        caldav_events = calendar.events()
        for caldav_event in caldav_events:
            ical_data = caldav_event.data
            parsed = self.client.parse_ical_event(ical_data)

            if parsed.get('uid') == event_id:
                # Update the event
                event_data['uid'] = event_id
                new_ical = self.client.event_to_ical(event_data)
                caldav_event.data = new_ical
                caldav_event.save()
                return

        raise Exception(f"Event {event_id} not found in calendar")

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """
        Delete event from calendar.

        Args:
            calendar_id: Calendar URL
            event_id: Event UID
        """
        calendar = self.client.get_calendar(calendar_id)

        # Find and delete event by UID
        caldav_events = calendar.events()
        for caldav_event in caldav_events:
            ical_data = caldav_event.data
            parsed = self.client.parse_ical_event(ical_data)

            if parsed.get('uid') == event_id:
                caldav_event.delete()
                return

        # Event not found - this is okay for delete operations
        pass

    def get_event(self, calendar_id: str,
                  event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get single event by UID.

        Args:
            calendar_id: Calendar URL
            event_id: Event UID

        Returns:
            Event dict or None if not found
        """
        calendar = self.client.get_calendar(calendar_id)

        # Find event by UID
        caldav_events = calendar.events()
        for caldav_event in caldav_events:
            try:
                ical_data = caldav_event.data
                parsed = self.client.parse_ical_event(ical_data)

                if parsed.get('uid') == event_id:
                    return parsed
            except Exception:
                continue

        return None
