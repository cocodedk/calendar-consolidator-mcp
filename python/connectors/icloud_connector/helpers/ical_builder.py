"""Build iCalendar VEVENT components from normalized event dictionaries."""

from typing import Dict, Any
from icalendar import Calendar as iCalendar, Event as iEvent
from datetime import datetime


def event_to_ical(event_data: Dict[str, Any]) -> str:
    """
    Convert normalized event dict to iCalendar format.

    Args:
        event_data: Normalized event dictionary

    Returns:
        iCalendar format string (VCALENDAR with VEVENT)
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
