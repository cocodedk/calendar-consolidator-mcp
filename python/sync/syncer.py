"""
Main sync engine.
Orchestrates calendar synchronization from sources to target.
"""

import time
from typing import Dict, Any, List
from ..state import ConfigStore
from ..connectors import GraphConnector
from ..model import Event, compute_diff


class Syncer:
    """Executes calendar synchronization operations."""

    def __init__(self, config_store: ConfigStore):
        self.config = config_store

    def sync_once(self, source_id: int) -> Dict[str, Any]:
        """
        Execute sync for a single source.

        Returns:
            Sync result with counts and status
        """
        start_time = time.time()

        try:
            # Load source and target
            source = self.config.sources.get(source_id)
            target = self.config.target.get()

            if not source or not target:
                raise Exception("Source or target not configured")

            # Get connector
            connector_source = self._get_connector(source)
            connector_target = self._get_connector(target)

            # Fetch changed events
            delta_result = connector_source.get_events_delta(
                source['calendar_id'],
                source.get('sync_token')
            )

            # Normalize events
            source_events = [
                Event.from_graph(e) for e in delta_result['events']
                if not e.get('@removed')
            ]

            # Load existing mappings
            all_mappings = self.config.mappings.get_all_for_source(source_id)
            mappings_dict = {m['source_event_uid']: m for m in all_mappings}

            # Compute diff
            ignore_private = self.config.settings.get_bool('ignore_private_events')
            diff = compute_diff(source_events, mappings_dict, ignore_private)

            # Apply changes
            created, updated, deleted = self._apply_changes(
                diff, connector_target, target['calendar_id'], source_id
            )

            # Update sync token
            if delta_result.get('nextSyncToken'):
                self.config.sources.update_token(source_id, delta_result['nextSyncToken'])

            duration_ms = int((time.time() - start_time) * 1000)

            # Log success
            self.config.logs.log_sync(
                source_id, 'success',
                created, updated, deleted,
                duration_ms=duration_ms
            )

            return {
                'success': True,
                'created': created,
                'updated': updated,
                'deleted': deleted,
                'errors': [],
                'duration': duration_ms
            }

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            self.config.logs.log_sync(
                source_id, 'error', 0, 0, 0,
                error_message=str(e),
                duration_ms=duration_ms
            )
            raise

    def _get_connector(self, config: Dict[str, Any]):
        """Get connector instance for calendar config."""
        if config['type'] == 'graph':
            return GraphConnector(config['credentials'])
        else:
            raise NotImplementedError(f"Connector type {config['type']} not implemented")

    def _apply_changes(self, diff, connector, calendar_id: str, source_id: int) -> tuple:
        """Apply diff changes to target calendar."""
        created = updated = deleted = 0

        # Create new events
        for event in diff.to_create:
            event_data = event.to_graph()
            target_id = connector.create_event(calendar_id, event_data)
            self.config.mappings.create(
                source_id, event.uid, target_id, event.compute_hash()
            )
            created += 1

        # Update events
        for event, target_id in diff.to_update:
            event_data = event.to_graph()
            connector.update_event(calendar_id, target_id, event_data)
            self.config.mappings.update_hash(source_id, event.uid, event.compute_hash())
            updated += 1

        # Delete events
        for target_id in diff.to_delete:
            try:
                connector.delete_event(calendar_id, target_id)
                # Find and delete mapping
                for uid, mapping in {}.items():  # TODO: improve this
                    if mapping.get('target_event_id') == target_id:
                        self.config.mappings.delete(source_id, uid)
                        break
                deleted += 1
            except Exception:
                pass  # Event may already be deleted

        return created, updated, deleted
