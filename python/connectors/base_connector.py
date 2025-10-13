"""
Base connector interface for calendar providers.
Defines common interface for Graph and CalDAV connectors.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseConnector(ABC):
    """Abstract base class for calendar connectors."""

    @abstractmethod
    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        List available calendars.

        Returns:
            List of calendar info dicts with id, name, canWrite
        """
        pass

    @abstractmethod
    def get_events_delta(self, calendar_id: str,
                        sync_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get changed events since last sync.

        Args:
            calendar_id: Calendar identifier
            sync_token: Last sync token (None for initial sync)

        Returns:
            Dict with 'events' list and 'nextSyncToken'
        """
        pass

    @abstractmethod
    def create_event(self, calendar_id: str, event_data: Dict[str, Any]) -> str:
        """
        Create new event.

        Returns:
            Event ID in target calendar
        """
        pass

    @abstractmethod
    def update_event(self, calendar_id: str, event_id: str,
                    event_data: Dict[str, Any]) -> None:
        """Update existing event."""
        pass

    @abstractmethod
    def delete_event(self, calendar_id: str, event_id: str) -> None:
        """Delete event."""
        pass

    @abstractmethod
    def get_event(self, calendar_id: str, event_id: str) -> Optional[Dict[str, Any]]:
        """Get single event by ID."""
        pass
