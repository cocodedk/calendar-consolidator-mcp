"""
Sync engine module - barrel exports.
"""

from typing import Dict, Any
from .syncer import Syncer

__all__ = ['Syncer', 'sync_once']


# API wrapper function
def sync_once(source_id: int) -> Dict[str, Any]:
    """API wrapper to execute sync."""
    from ...state import ConfigStore
    config = ConfigStore()
    syncer = Syncer(config)
    return syncer.sync_once(source_id)
