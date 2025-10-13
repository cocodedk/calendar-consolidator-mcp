"""
Microsoft Graph calendar connector implementation.
"""

import requests
from typing import List, Dict, Any, Optional
from ..base_connector import BaseConnector
from ..graph_auth import GraphAuthenticator
from .token_manager import GraphTokenManager
from .config import GRAPH_API_ENDPOINT


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
        self.token_manager = GraphTokenManager(credentials, self.auth)
        self.token_manager.refresh_if_needed()

    def list_calendars(self) -> List[Dict[str, Any]]:
        """List user's calendars."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars"
        response = requests.get(url, headers=self.token_manager.get_headers())
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

        response = requests.get(url, headers=self.token_manager.get_headers())
        response.raise_for_status()

        data = response.json()
        events = data.get('value', [])
        next_token = data.get('@odata.deltaLink', data.get('@odata.nextLink'))

        return {
            'events': events,
            'nextSyncToken': next_token
        }

    def create_event(self, calendar_id: str, event_data: Dict[str, Any]) -> str:
        """Create event in calendar."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events"
        response = requests.post(
            url,
            headers=self.token_manager.get_headers(),
            json=event_data
        )
        response.raise_for_status()
        return response.json()['id']

    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """Update existing event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.patch(
            url,
            headers=self.token_manager.get_headers(),
            json=event_data
        )
        response.raise_for_status()

    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.delete(url, headers=self.token_manager.get_headers())
        response.raise_for_status()

    def get_event(self, calendar_id: str,
                  event_id: str) -> Optional[Dict[str, Any]]:
        """Get single event."""
        url = f"{GRAPH_API_ENDPOINT}/me/calendars/{calendar_id}/events/{event_id}"
        response = requests.get(url, headers=self.token_manager.get_headers())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
