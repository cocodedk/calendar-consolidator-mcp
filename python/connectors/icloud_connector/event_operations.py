"""Event CRUD operations for iCloud connector."""

from typing import Dict, Any, Optional
from .caldav_client import CalDAVClient
from .helpers import (
    parse_caldav_event,
    build_ical_event,
    generate_event_uid,
)


class EventOperations:
    """Handle event creation, reading, updating, deletion."""

    def __init__(self, client: CalDAVClient):
        """Initialize with CalDAV client."""
        self.client = client

    def create_event(self, calendar: Any, event_data: Dict[str, Any]) -> str:
        """Create new event in calendar. Returns event UID."""
        if 'uid' not in event_data:
            event_data['uid'] = generate_event_uid()
        ical_data = build_ical_event(event_data, self.client)
        calendar.save_event(ical_data)
        return event_data['uid']

    def update_event(self, calendar: Any, event_id: str,
                     event_data: Dict[str, Any]) -> None:
        """Update existing event by UID."""
        for caldav_event in calendar.events():
            ical_data = caldav_event.data
            parsed = parse_caldav_event(ical_data, self.client)
            if parsed and parsed.get('uid') == event_id:
                event_data['uid'] = event_id
                new_ical = build_ical_event(event_data, self.client)
                caldav_event.data = new_ical
                caldav_event.save()
                return
        raise Exception(f"Event {event_id} not found")

    def delete_event(self, calendar: Any, event_id: str) -> None:
        """Delete event by UID (idempotent)."""
        for caldav_event in calendar.events():
            ical_data = caldav_event.data
            parsed = parse_caldav_event(ical_data, self.client)
            if parsed and parsed.get('uid') == event_id:
                caldav_event.delete()
                return

    def get_event(self, calendar: Any,
                  event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single event by UID."""
        for caldav_event in calendar.events():
            ical_data = caldav_event.data
            parsed = parse_caldav_event(ical_data, self.client)
            if parsed and parsed.get('uid') == event_id:
                return parsed
        return None
