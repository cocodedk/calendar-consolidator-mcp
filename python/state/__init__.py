"""
State management module.
Provides database access and configuration storage.
"""

from .database import Database
from .source_store import SourceStore
from .target_store import TargetStore
from .mapping_store import MappingStore
from .log_store import LogStore
from .settings_store import SettingsStore


class ConfigStore:
    """
    Unified configuration store interface.
    Provides access to all storage modules.
    """

    def __init__(self, db_path: str = None):
        self.db = Database(db_path)
        self.sources = SourceStore(self.db)
        self.target = TargetStore(self.db)
        self.mappings = MappingStore(self.db)
        self.logs = LogStore(self.db)
        self.settings = SettingsStore(self.db)

    def initialize(self):
        """Initialize database schema."""
        self.db.initialize_schema()

    def close(self):
        """Close database connection."""
        self.db.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


__all__ = [
    'ConfigStore',
    'Database',
    'SourceStore',
    'TargetStore',
    'MappingStore',
    'LogStore',
    'SettingsStore'
]
