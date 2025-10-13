"""
Google Calendar connector.
Implements calendar operations using Google Calendar API v3.
"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .base_connector import BaseConnector
from .google_auth import GoogleAuthenticator


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
        self._ensure_token_valid()
        self.service = self._build_service()

    def _ensure_token_valid(self):
        """Check and refresh token if needed."""
        if 'expires_at' in self.credentials:
            expires_at = datetime.fromisoformat(self.credentials['expires_at'])
            if datetime.utcnow() >= expires_at - timedelta(minutes=5):
                self._refresh_token()

    def _refresh_token(self):
        """Refresh access token."""
        refresh_token = self.credentials.get('refresh_token')
        if not refresh_token:
            raise Exception("No refresh token available")

        result = self.auth.refresh_token(refresh_token)
        self.credentials['access_token'] = result['access_token']
        self.credentials['expires_at'] = result['expires_at']

    def _build_service(self):
        """Build Google Calendar API service."""
        creds = Credentials(token=self.credentials['access_token'])
        return build('calendar', 'v3', credentials=creds)

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
