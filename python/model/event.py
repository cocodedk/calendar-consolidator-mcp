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

    @classmethod
    def from_google(cls, google_event: Dict[str, Any]) -> 'Event':
        """Create Event from Google Calendar API format."""
        # Determine all-day vs timed
        start_obj = google_event.get('start', {})
        end_obj = google_event.get('end', {})

        if 'dateTime' in start_obj:
            start_str = start_obj['dateTime']
            # Normalize Z suffix for fromisoformat
            start_str = start_str.replace('Z', '+00:00')
            start_dt = datetime.fromisoformat(start_str)
            is_all_day = False
        else:
            # All-day event: use midnight UTC
            start_dt = datetime.fromisoformat(start_obj.get('date', '') + 'T00:00:00+00:00')
            is_all_day = True

        if 'dateTime' in end_obj:
            end_str = end_obj['dateTime']
            end_str = end_str.replace('Z', '+00:00')
            end_dt = datetime.fromisoformat(end_str)
        else:
            end_dt = datetime.fromisoformat(end_obj.get('date', '') + 'T00:00:00+00:00')

        return cls(
            uid=google_event['id'],
            subject=google_event.get('summary', '(No title)'),
            start=start_dt,
            end=end_dt,
            location=google_event.get('location'),
            description=google_event.get('description'),
            is_all_day=is_all_day,
            is_cancelled=google_event.get('status') == 'cancelled',
            is_private=google_event.get('visibility') == 'private',
            recurrence=json.dumps(google_event.get('recurrence')) if google_event.get('recurrence') else None,
            organizer=(google_event.get('organizer') or {}).get('email'),
            attendees=[(a or {}).get('email') for a in (google_event.get('attendees') or [])]
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

    def to_google(self) -> Dict[str, Any]:
        """Convert to Google Calendar API format."""
        event_data: Dict[str, Any] = {
            'summary': self.subject,
        }

        if self.is_all_day:
            event_data['start'] = { 'date': self.start.date().isoformat() }
            event_data['end'] = { 'date': self.end.date().isoformat() }
        else:
            event_data['start'] = { 'dateTime': self.start.isoformat(), 'timeZone': 'UTC' }
            event_data['end'] = { 'dateTime': self.end.isoformat(), 'timeZone': 'UTC' }

        if self.location:
            event_data['location'] = self.location
        if self.description:
            event_data['description'] = self.description
        if self.is_private:
            event_data['visibility'] = 'private'

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
