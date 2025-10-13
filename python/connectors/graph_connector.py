"""
Microsoft Graph calendar connector.
Implements calendar operations using Microsoft Graph API.
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .base_connector import BaseConnector
from .graph_auth import GraphAuthenticator


GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


class GraphConnector(BaseConnector):
    """Microsoft Graph API connector for calendar operations."""

    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialize Graph connector.

        Args:
            credentials: Dict with access_token, refresh_token, expires_at
        """
        self.credentials = credentials
        self.auth = GraphAuthenticator()
        self._ensure_token_valid()

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
        self.credentials['expires_at'] = (
            datetime.utcnow() + timedelta(seconds=result.get('expires_in', 3600))
        ).isoformat()

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with auth token."""
        return {
            'Authorization': f"Bearer {self.credentials['access_token']}",
            'Content-Type': 'application/json'
        }

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's calendars."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()

        calendars = response.json().get('value', [])
        return [
            {
                'id': cal['id'],
                'name': cal['name'],
                'canWrite': cal.get('canEdit', True)
            }
            for cal in calendars
        ]

    def get_events_delta(self, calendar_id: str,
                        sync_token: Optional[str] = None) -> Dict[str, Any]:
        """Get changed events using delta query."""
        if sync_token:
            url = sync_token
        else:
            url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/delta"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()

        data = response.json()
        events = data.get('value', [])

        # Get next sync token from deltaLink
        next_token = data.get('@odata.deltaLink', data.get('@odata.nextLink'))

        return {
            'events': events,
            'nextSyncToken': next_token
        }

    def create_event(self, calendar_id: str, event_data: Dict[str, Any]) -> str:
        """Create event in calendar."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events"
        response = requests.post(url, headers=self._get_headers(), json=event_data)
        response.raise_for_status()
        return response.json()['id']

    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """Update existing event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.patch(url, headers=self._get_headers(), json=event_data)
        response.raise_for_status()

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()

    def get_event(self, calendar_id: str, event_id: str) -> Optional[Dict[str, Any]]:
        """Get single event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
