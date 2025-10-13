"""
Applies diff changes to target calendar.
"""

from typing import Any


class DiffApplier:
    """Applies calendar event differences to target."""

    def __init__(self, config_store, source_id: int):
        self.config = config_store
        self.source_id = source_id

    def apply(self, diff, connector, calendar_id: str) -> tuple:
        """
        Apply diff changes to target calendar.

        Args:
            diff: Computed diff object
            connector: Target calendar connector
            calendar_id: Target calendar ID

        Returns:
            Tuple of (created, updated, deleted) counts
        """
        created = self._apply_creates(diff.to_create, connector, calendar_id)
        updated = self._apply_updates(diff.to_update, connector, calendar_id)
        deleted = self._apply_deletes(diff.to_delete, connector, calendar_id)

        return created, updated, deleted

    def _apply_creates(self, events, connector, calendar_id: str) -> int:
        """Create new events in target."""
        count = 0
        for event in events:
            event_data = event.to_graph()
            target_id = connector.create_event(calendar_id, event_data)
            self.config.mappings.create(
                self.source_id, event.uid, target_id, event.compute_hash()
            )
            count += 1
        return count

    def _apply_updates(self, event_pairs, connector, calendar_id: str) -> int:
        """Update existing events in target."""
        count = 0
        for event, target_id in event_pairs:
            event_data = event.to_graph()
            connector.update_event(calendar_id, target_id, event_data)
            self.config.mappings.update_hash(
                self.source_id, event.uid, event.compute_hash()
            )
            count += 1
        return count

    def _apply_deletes(self, target_ids, connector, calendar_id: str) -> int:
        """Delete events from target."""
        count = 0

        for target_id in target_ids:
            try:
                connector.delete_event(calendar_id, target_id)
                # Try to find and delete mapping
                try:
                    mappings = self.config.mappings.get_all_for_source(self.source_id)
                    for mapping in mappings:
                        if mapping.get('target_event_id') == target_id:
                            self.config.mappings.delete(
                                self.source_id,
                                mapping['source_event_uid']
                            )
                            break
                except Exception:
                    pass  # Mapping may not exist or already deleted
                count += 1
            except Exception:
                pass  # Event may already be deleted
        return count
