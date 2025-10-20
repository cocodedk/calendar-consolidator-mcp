"""Parse iCalendar VEVENT components to normalized event dictionaries."""

from typing import Dict, Any
from icalendar import Calendar as iCalendar
from datetime import datetime


def parse_ical_event(ical_data: str) -> Dict[str, Any]:
    """
    Parse iCalendar data to normalized event dict.

    Args:
        ical_data: iCalendar format string

    Returns:
        Normalized event dictionary with standard fields
    """
    cal = iCalendar.from_ical(ical_data)

    for component in cal.walk():
        if component.name == "VEVENT":
            return _extract_event_fields(component)

    return {}


def _extract_event_fields(component: Any) -> Dict[str, Any]:
    """Extract fields from VEVENT component."""
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
