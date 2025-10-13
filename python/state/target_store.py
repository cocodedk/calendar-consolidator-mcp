"""
Target calendar storage operations.
Handles configuration for the single target calendar.
"""

from typing import Optional, Dict, Any
from .database import Database
from .encryption import (
    store_credentials,
    credentials_to_blob,
    blob_to_credentials
)


class TargetStore:
    """Manages target calendar configuration (single target only)."""

    def __init__(self, db: Database):
        self.db = db

    def set(self, target_type: str, calendar_id: str, name: str,
            credentials: Dict[str, Any]):
        """Set or replace target calendar (only one allowed)."""
        conn = self.db.connect()
        cred_blob = credentials_to_blob(credentials)

        conn.execute(
            """INSERT OR REPLACE INTO target (id, type, calendar_id, name, cred_blob)
               VALUES (1, ?, ?, ?, ?)""",
            (target_type, calendar_id, name, cred_blob)
        )
        conn.commit()

        store_credentials("target-1", credentials)

    def get(self) -> Optional[Dict[str, Any]]:
        """Get target calendar configuration with credentials."""
        conn = self.db.connect()
        row = conn.execute("SELECT * FROM target WHERE id = 1").fetchone()

        if row:
            target = dict(row)
            target['credentials'] = blob_to_credentials(
                row['cred_blob'], "target-1"
            )
            return target
        return None

    def exists(self) -> bool:
        """Check if target is configured."""
        conn = self.db.connect()
        row = conn.execute("SELECT COUNT(*) as count FROM target WHERE id = 1").fetchone()
        return row['count'] > 0
