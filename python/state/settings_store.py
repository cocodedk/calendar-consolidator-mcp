"""
Settings storage operations.
Manages global configuration settings.
"""

from typing import Optional, Dict
from .database import Database


class SettingsStore:
    """Manages global application settings."""

    def __init__(self, db: Database):
        self.db = db

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get setting value by key."""
        conn = self.db.connect()
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
        return row['value'] if row else default

    def set(self, key: str, value: str):
        """Set setting value."""
        conn = self.db.connect()
        conn.execute(
            """INSERT OR REPLACE INTO settings (key, value, updated_at)
               VALUES (?, ?, CURRENT_TIMESTAMP)""",
            (key, value)
        )
        conn.commit()

    def get_all(self) -> Dict[str, str]:
        """Get all settings as dictionary."""
        conn = self.db.connect()
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        return {row['key']: row['value'] for row in rows}

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean setting."""
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes')

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer setting."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def set_bool(self, key: str, value: bool):
        """Set boolean setting."""
        self.set(key, 'true' if value else 'false')

    def set_int(self, key: str, value: int):
        """Set integer setting."""
        self.set(key, str(value))
