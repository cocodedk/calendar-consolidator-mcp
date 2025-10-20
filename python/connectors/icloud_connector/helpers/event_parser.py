"""Parse CalDAV iCalendar events into normalized dictionaries."""

from typing import Dict, Any, Optional


def parse_caldav_event(ical_data: str, client: Any) -> Optional[Dict[str, Any]]:
    """
    Parse iCalendar data using CalDAV client parser.

    Args:
        ical_data: Raw iCalendar data string
        client: CalDAVClient instance with parse_ical_event method

    Returns:
        Parsed event dict with _raw_data field, or None if parsing fails
    """
    try:
        event = client.parse_ical_event(ical_data)
        if event and event.get('uid'):
            event['_raw_data'] = ical_data
            return event
        return None
    except Exception as e:
        print(f"Warning: Failed to parse event: {e}")
        return None
