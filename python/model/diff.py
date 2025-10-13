"""
Diff computation module.
Computes creates, updates, and deletes for sync operations.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from .event import Event


@dataclass
class DiffResult:
    """Result of diff computation."""

    to_create: List[Event] = field(default_factory=list)
    to_update: List[tuple[Event, str]] = field(default_factory=list)  # (event, target_id)
    to_delete: List[str] = field(default_factory=list)  # target_event_ids

    def count_total(self) -> int:
        """Total number of changes."""
        return len(self.to_create) + len(self.to_update) + len(self.to_delete)

    def to_summary(self) -> Dict[str, Any]:
        """Convert to summary dict for API responses."""
        return {
            'wouldCreate': len(self.to_create),
            'wouldUpdate': len(self.to_update),
            'wouldDelete': len(self.to_delete),
            'sampleEvents': self._sample_events(5)
        }

    def _sample_events(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample events for preview."""
        samples = []

        for event in self.to_create[:limit]:
            samples.append({
                'action': 'create',
                'title': event.subject,
                'start': event.start.isoformat(),
                'end': event.end.isoformat()
            })

        for event, _ in self.to_update[:limit - len(samples)]:
            samples.append({
                'action': 'update',
                'title': event.subject,
                'start': event.start.isoformat(),
                'end': event.end.isoformat()
            })

        return samples


def compute_diff(source_events: List[Event],
                mappings: Dict[str, Dict[str, Any]],
                ignore_private: bool = False) -> DiffResult:
    """
    Compute diff between source events and existing mappings.

    Args:
        source_events: Events from source calendar
        mappings: Dict mapping source_event_uid -> mapping info
        ignore_private: Skip private events if True

    Returns:
        DiffResult with changes to apply
    """
    result = DiffResult()
    processed_uids = set()

    for event in source_events:
        if ignore_private and event.is_private:
            continue

        processed_uids.add(event.uid)
        mapping = mappings.get(event.uid)

        if event.is_cancelled:
            # Event deleted at source
            if mapping:
                result.to_delete.append(mapping['target_event_id'])
        elif not mapping:
            # New event
            result.to_create.append(event)
        else:
            # Check if event changed
            new_hash = event.compute_hash()
            if new_hash != mapping.get('last_hash'):
                result.to_update.append((event, mapping['target_event_id']))

    # Find deletions (mapped events not in source anymore)
    for uid, mapping in mappings.items():
        if uid not in processed_uids:
            result.to_delete.append(mapping['target_event_id'])

    return result
