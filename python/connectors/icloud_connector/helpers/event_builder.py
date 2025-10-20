"""Build iCalendar format events from normalized dictionaries."""

from typing import Dict, Any


def build_ical_event(event_data: Dict[str, Any], client: Any) -> str:
    """
    Convert normalized event dict to iCalendar format.

    Args:
        event_data: Normalized event dictionary
        client: CalDAVClient instance with event_to_ical method

    Returns:
        iCalendar formatted string
    """
    return client.event_to_ical(event_data)
