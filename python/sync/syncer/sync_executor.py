"""
Sync execution logic.
"""

import time
from typing import Dict, Any
from ...model import Event, compute_diff
from .connector_factory import get_connector
from .diff_applier import DiffApplier


class SyncExecutor:
    """Handles the core sync execution logic."""

    def __init__(self, config_store, source_id: int):
        self.config = config_store
        self.source_id = source_id

    def execute(self, start_time: float) -> Dict[str, Any]:
        """Execute the synchronization logic."""
        # Load and validate configuration
        source, target = self._load_config()

        # Get connectors
        connector_source = get_connector(source)
        connector_target = get_connector(target)

        # Fetch and process events
        delta_result = self._fetch_events(connector_source, source)
        source_events = self._normalize_events(delta_result['events'])

        # Compute changes
        diff = self._compute_diff(source_events)

        # Apply changes to target
        created, updated, deleted = self._apply_changes(
            diff, connector_target, target['calendar_id']
        )

        # Update sync token
        self._update_sync_token(delta_result.get('nextSyncToken'))

        return self._build_result(created, updated, deleted, start_time)

    def _load_config(self):
        """Load and validate source and target config."""
        source = self.config.sources.get(self.source_id)
        target = self.config.target.get()

        if not source or not target:
            raise Exception("Source or target not configured")

        return source, target

    def _fetch_events(self, connector, source):
        """Fetch changed events from source."""
        return connector.get_events_delta(
            source['calendar_id'],
            source.get('sync_token')
        )

    def _normalize_events(self, raw_events):
        """Normalize events to internal format."""
        return [
            Event.from_graph(e) for e in raw_events
            if not e.get('@removed')
        ]

    def _compute_diff(self, source_events):
        """Compute diff against existing mappings."""
        all_mappings = self.config.mappings.get_all_for_source(self.source_id)
        mappings_dict = {m['source_event_uid']: m for m in all_mappings}
        ignore_private = self.config.settings.get_bool('ignore_private_events')
        return compute_diff(source_events, mappings_dict, ignore_private)

    def _apply_changes(self, diff, connector, calendar_id):
        """Apply changes to target calendar."""
        applier = DiffApplier(self.config, self.source_id)
        return applier.apply(diff, connector, calendar_id)

    def _update_sync_token(self, next_token):
        """Update source sync token if provided."""
        if next_token:
            self.config.sources.update_token(self.source_id, next_token)

    def _build_result(self, created, updated, deleted, start_time):
        """Build sync result dictionary."""
        duration_ms = int((time.time() - start_time) * 1000)
        return {
            'success': True,
            'created': created,
            'updated': updated,
            'deleted': deleted,
            'errors': [],
            'duration': duration_ms
        }

