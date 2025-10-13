"""
Google Calendar connector implementation.
"""

from typing import List, Dict, Any, Optional
from ..base_connector import BaseConnector
from ..google_auth import GoogleAuthenticator
from .token_manager import TokenManager
from .service import build_calendar_service


class GoogleConnector(BaseConnector):
    """Google Calendar API connector for calendar operations."""

    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialize Google connector.

        Args:
            credentials: Dict with access_token, refresh_token, expires_at
        """
        self.credentials = credentials
        self.auth = GoogleAuthenticator()
        self.token_manager = TokenManager(credentials, self.auth)
        self.token_manager.refresh_if_needed()
        self.service = build_calendar_service(
            self.token_manager.get_access_token()
        )

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's calendars."""
        result = self.service.calendarList().list().execute()
        calendars = result.get('items', [])

        return [
            {
                'id': cal['id'],
                'name': cal.get('summary', ''),
                'canWrite': cal.get('accessRole') in ['owner', 'writer']
            }
            for cal in calendars
        ]

    def get_events_delta(self, calendar_id: str,
                        sync_token: Optional[str] = None) -> Dict[str, Any]:
        """Get changed events using sync token."""
        params = {'calendarId': calendar_id}

        if sync_token:
            params['syncToken'] = sync_token

        result = self.service.events().list(**params).execute()
        events = result.get('items', [])
        next_token = result.get('nextSyncToken')

        return {
            'events': events,
            'nextSyncToken': next_token
        }

    def create_event(self, calendar_id: str, event_data: Dict[str, Any]) -> str:
        """Create event in calendar."""
        result = self.service.events().insert(
            calendarId=calendar_id,
            body=event_data
        ).execute()
        return result['id']

    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """Update existing event."""
        self.service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event_data
        ).execute()

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete event."""
        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()

    def get_event(self, calendar_id: str,
                  event_id: str) -> Optional[Dict[str, Any]]:
        """Get single event by ID."""
        try:
            result = self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            return result
        except Exception as e:
            if 'not found' in str(e).lower():
                return None
            raise

