"""
CalDAV client wrapper for iCloud operations.
"""

import caldav
from typing import List, Dict, Any, Optional
from icalendar import Calendar as iCalendar, Event as iEvent
from datetime import datetime
import pytz


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
        self.principal = None

    def get_principal(self):
        """Get or cache CalDAV principal."""
        if not self.principal:
            self.principal = self.client.principal()
        return self.principal

    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        List all calendars for the user.

        Returns:
            List of calendar dicts with id, name, canWrite
        """
        principal = self.get_principal()
        calendars = principal.calendars()

        result = []
        for cal in calendars:
            try:
                # Get calendar properties
                props = cal.get_properties([
                    caldav.elements.dav.DisplayName(),
                ])

                name = props.get('{DAV:}displayname', 'Unnamed Calendar')

                result.append({
                    'id': str(cal.url),
                    'name': name,
                    'canWrite': True  # Assume writeable for user's calendars
                })
            except Exception as e:
                # Skip calendars we can't read
                print(f"Warning: Skipped calendar due to error: {e}")
                continue

        return result

    def get_calendar(self, calendar_url: str):
        """Get calendar object by URL."""
        return caldav.Calendar(client=self.client, url=calendar_url)

    def parse_ical_event(self, ical_data: str) -> Dict[str, Any]:
        """
        Parse iCalendar data to normalized event dict.

        Args:
            ical_data: iCalendar format string

        Returns:
            Normalized event dictionary
        """
        cal = iCalendar.from_ical(ical_data)

        for component in cal.walk():
            if component.name == "VEVENT":
                event = {}

                # UID
                event['uid'] = str(component.get('uid', ''))

                # Summary (title)
                event['subject'] = str(component.get('summary', ''))

                # Description
                event['body'] = str(component.get('description', ''))

                # Start and end times
                dtstart = component.get('dtstart')
                dtend = component.get('dtend')

                if dtstart:
                    dt = dtstart.dt
                    if isinstance(dt, datetime):
                        event['start'] = dt.isoformat()
                        event['isAllDay'] = False
                    else:
                        # Date only (all-day event)
                        event['start'] = dt.isoformat()
                        event['isAllDay'] = True

                if dtend:
                    dt = dtend.dt
                    if isinstance(dt, datetime):
                        event['end'] = dt.isoformat()
                    else:
                        event['end'] = dt.isoformat()

                # Location
                event['location'] = str(component.get('location', ''))

                return event

        return {}

    def event_to_ical(self, event_data: Dict[str, Any]) -> str:
        """
        Convert normalized event dict to iCalendar format.

        Args:
            event_data: Normalized event dictionary

        Returns:
            iCalendar format string
        """
        cal = iCalendar()
        cal.add('prodid', '-//Calendar Consolidator MCP//EN')
        cal.add('version', '2.0')

        event = iEvent()

        # Required fields
        if 'uid' in event_data:
            event.add('uid', event_data['uid'])

        if 'subject' in event_data:
            event.add('summary', event_data['subject'])

        # Start/End times
        if 'start' in event_data:
            start_dt = datetime.fromisoformat(
                event_data['start'].replace('Z', '+00:00')
            )
            event.add('dtstart', start_dt)

        if 'end' in event_data:
            end_dt = datetime.fromisoformat(
                event_data['end'].replace('Z', '+00:00')
            )
            event.add('dtend', end_dt)

        # Optional fields
        if 'body' in event_data and event_data['body']:
            event.add('description', event_data['body'])

        if 'location' in event_data and event_data['location']:
            event.add('location', event_data['location'])

        # Add event to calendar
        cal.add_component(event)

        return cal.to_ical().decode('utf-8')
