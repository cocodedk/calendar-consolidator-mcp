"""
Normalized event model.
Represents calendar events in a provider-agnostic format.
"""

import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Event:
    """Normalized calendar event representation."""

    uid: str
    subject: str
    start: datetime
    end: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    is_all_day: bool = False
    is_cancelled: bool = False
    is_private: bool = False
    recurrence: Optional[str] = None
    recurrence_id: Optional[str] = None
    organizer: Optional[str] = None
    attendees: Optional[list] = None

    @classmethod
    def from_graph(cls, graph_event: Dict[str, Any]) -> 'Event':
        """Create Event from Microsoft Graph API format."""
        return cls(
            uid=graph_event['id'],
            subject=graph_event.get('subject', '(No title)'),
            start=datetime.fromisoformat(graph_event['start']['dateTime'].replace('Z', '+00:00')),
            end=datetime.fromisoformat(graph_event['end']['dateTime'].replace('Z', '+00:00')),
            location=graph_event.get('location', {}).get('displayName'),
            description=graph_event.get('bodyPreview'),
            is_all_day=graph_event.get('isAllDay', False),
            is_cancelled=graph_event.get('isCancelled', False),
            is_private=graph_event.get('sensitivity') == 'private',
            recurrence=json.dumps(graph_event.get('recurrence')) if graph_event.get('recurrence') else None,
            organizer=graph_event.get('organizer', {}).get('emailAddress', {}).get('address'),
            attendees=[a.get('emailAddress', {}).get('address') for a in graph_event.get('attendees', [])]
        )

    def to_graph(self) -> Dict[str, Any]:
        """Convert to Microsoft Graph API format."""
        event_data = {
            'subject': self.subject,
            'start': {
                'dateTime': self.start.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': self.end.isoformat(),
                'timeZone': 'UTC'
            },
            'isAllDay': self.is_all_day
        }

        if self.location:
            event_data['location'] = {'displayName': self.location}
        if self.description:
            event_data['body'] = {'contentType': 'text', 'content': self.description}
        if self.is_private:
            event_data['sensitivity'] = 'private'

        return event_data

    def compute_hash(self) -> str:
        """Compute hash of event content for change detection."""
        # Hash key fields for change detection
        hash_data = {
            'subject': self.subject,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'location': self.location,
            'description': self.description,
            'is_all_day': self.is_all_day,
            'recurrence': self.recurrence
        }

        hash_str = json.dumps(hash_data, sort_keys=True)
        return hashlib.sha256(hash_str.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        # Convert datetime to ISO format
        data['start'] = self.start.isoformat()
        data['end'] = self.end.isoformat()
        return data
