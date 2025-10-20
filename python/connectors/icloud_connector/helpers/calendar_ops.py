"""Calendar listing and retrieval operations."""

from typing import List, Dict, Any
import caldav


class CalendarOps:
    """Handle calendar discovery, listing, and retrieval."""

    def __init__(self, client: Any):
        """
        Initialize with CalDAV client.

        Args:
            client: caldav.DAVClient instance
        """
        self.client = client
        self.principal = None

    def get_principal(self) -> Any:
        """Get or cache CalDAV principal."""
        if not self.principal:
            self.principal = self.client.principal()
        return self.principal

    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        List all calendars for user.

        Returns:
            List of calendar dicts with id, name, canWrite
        """
        principal = self.get_principal()
        calendars = principal.calendars()

        result = []
        for cal in calendars:
            try:
                props = cal.get_properties([
                    caldav.elements.dav.DisplayName(),
                ])
                name = props.get('{DAV:}displayname', 'Unnamed Calendar')
                result.append({
                    'id': str(cal.url),
                    'name': name,
                    'canWrite': True
                })
            except Exception as e:
                print(f"Warning: Skipped calendar: {e}")
                continue
        return result

    def get_calendar(self, calendar_url: str) -> Any:
        """Get calendar object by URL."""
        return caldav.Calendar(client=self.client, url=calendar_url)
