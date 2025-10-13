"""
Configuration store wrapper for API access.
Provides unified config retrieval across sources, target, and settings.
"""

from typing import Dict, Any, List
from .database import Database
from .source_store import SourceStore
from .target_store import TargetStore
from .settings_store import SettingsStore


def get_all_config() -> Dict[str, Any]:
    """
    Get all configuration including sources, target, and settings.
    Returns a dictionary with complete system configuration.
    """
    db = Database()
    source_store = SourceStore(db)
    target_store = TargetStore(db)
    settings_store = SettingsStore(db)

    # Get all sources
    sources = []
    for source in source_store.list():
        sources.append({
            'id': source['id'],
            'type': source['type'],
            'name': source['name'],
            'calendar_id': source['calendar_id'],
            'enabled': bool(source['enabled']),
            'created_at': source['created_at']
        })

    # Get target
    target = target_store.get()
    target_info = None
    if target:
        target_info = {
            'type': target['type'],
            'name': target['name'],
            'calendar_id': target['calendar_id'],
            'created_at': target['created_at']
        }

    # Get settings
    settings = settings_store.get_all()

    return {
        'sources': sources,
        'target': target_info,
        'settings': settings
    }


def get_sources() -> List[Dict[str, Any]]:
    """Get all source calendars."""
    db = Database()
    source_store = SourceStore(db)

    sources = []
    for source in source_store.list():
        sources.append({
            'id': source['id'],
            'type': source['type'],
            'name': source['name'],
            'calendar_id': source['calendar_id'],
            'enabled': bool(source['enabled']),
            'created_at': source['created_at']
        })

    return sources


def get_target() -> Dict[str, Any]:
    """Get target calendar."""
    db = Database()
    target_store = TargetStore(db)
    target = target_store.get()

    if not target:
        return {}

    return {
        'type': target['type'],
        'name': target['name'],
        'calendar_id': target['calendar_id'],
        'created_at': target['created_at']
    }


def get_settings() -> Dict[str, str]:
    """Get all settings."""
    db = Database()
    settings_store = SettingsStore(db)
    return settings_store.get_all()


def get_status() -> Dict[str, Any]:
    """Get system status including counts and last sync."""
    db = Database()
    source_store = SourceStore(db)
    log_store = LogStore(db)

    sources = source_store.list()
    recent_logs = log_store.get_recent(1)
    recent_errors = log_store.get_recent_errors(10)

    last_sync = recent_logs[0]['timestamp'] if recent_logs else None

    return {
        'source_count': len(sources),
        'active_sources': len([s for s in sources if s.get('active')]),
        'last_sync': last_sync,
        'error_count': len(recent_errors)
    }
