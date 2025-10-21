"""
Sync engine module - barrel exports.
"""

from typing import Dict, Any
from .syncer import Syncer

__all__ = ['Syncer', 'sync_once', 'sync_all']


# API wrapper function
def sync_once(source_id: int) -> Dict[str, Any]:
    """API wrapper to execute sync for a single source."""
    from ...state import ConfigStore
    config = ConfigStore()
    syncer = Syncer(config)
    return syncer.sync_once(source_id)


def sync_all() -> Dict[str, Any]:
    """API wrapper to execute sync for all active sources and aggregate results."""
    from ...state import ConfigStore
    config = ConfigStore()
    syncer = Syncer(config)

    total_created = total_updated = total_deleted = 0
    errors = []

    for source in config.sources.get_active():
        sid = source['id']
        try:
            result = syncer.sync_once(sid)
            total_created += result.get('created', 0)
            total_updated += result.get('updated', 0)
            total_deleted += result.get('deleted', 0)
        except Exception as e:
            errors.append({'sourceId': sid, 'error': str(e)})

    return {
        'success': len(errors) == 0,
        'created': total_created,
        'updated': total_updated,
        'deleted': total_deleted,
        'errors': errors,
        'duration': 0
    }
