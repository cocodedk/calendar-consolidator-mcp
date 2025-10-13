"""
Dry-run sync engine.
Computes changes without applying them (preview mode).
"""

from typing import Dict, Any
from ..state import ConfigStore
from ..connectors import GraphConnector
from ..model import Event, compute_diff


class DryRunSyncer:
    """Previews sync changes without applying them."""

    def __init__(self, config_store: ConfigStore):
        self.config = config_store

    def preview_sync(self, source_id: int) -> Dict[str, Any]:
        """
        Preview sync changes for a source.

        Returns:
            Diff summary with counts and sample events
        """
        # Load source and target
        source = self.config.sources.get(source_id)
        target = self.config.target.get()

        if not source or not target:
            raise Exception("Source or target not configured")

        # Get connector
        connector_source = self._get_connector(source)

        # Fetch changed events (using current sync token)
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

        # Return summary (no writes)
        return diff.to_summary()

    def preview_all_sources(self) -> Dict[str, Any]:
        """Preview sync for all active sources."""
        sources = self.config.sources.get_active()

        total_create = total_update = total_delete = 0
        all_samples = []

        for source in sources:
            summary = self.preview_sync(source['id'])
            total_create += summary['wouldCreate']
            total_update += summary['wouldUpdate']
            total_delete += summary['wouldDelete']
            all_samples.extend(summary['sampleEvents'])

        return {
            'wouldCreate': total_create,
            'wouldUpdate': total_update,
            'wouldDelete': total_delete,
            'sampleEvents': all_samples[:10]  # Limit samples
        }

    def _get_connector(self, config: Dict[str, Any]):
        """Get connector instance for calendar config."""
        if config['type'] == 'graph':
            return GraphConnector(config['credentials'])
        else:
            raise NotImplementedError(f"Connector type {config['type']} not implemented")
