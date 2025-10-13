"""
Source calendar storage operations.
Handles CRUD operations for source calendars.
"""

from typing import Optional, List, Dict, Any
from .database import Database
from .encryption import (
    store_credentials, delete_credentials,
    credentials_to_blob, blob_to_credentials
)


class SourceStore:
    """Manages source calendar configurations."""

    def __init__(self, db: Database):
        self.db = db

    def add(self, source_type: str, calendar_id: str, name: str,
            credentials: Dict[str, Any], active: bool = True) -> int:
        """Add a new source calendar. Returns source ID."""
        conn = self.db.connect()
        cred_blob = credentials_to_blob(credentials)

        cursor = conn.execute(
            """INSERT INTO sources (type, calendar_id, name, cred_blob, active)
               VALUES (?, ?, ?, ?, ?)""",
            (source_type, calendar_id, name, cred_blob, active)
        )
        source_id = cursor.lastrowid
        conn.commit()

        store_credentials(f"source-{source_id}", credentials)
        return source_id

    def get(self, source_id: int) -> Optional[Dict[str, Any]]:
        """Get source by ID with credentials."""
        conn = self.db.connect()
        row = conn.execute(
            "SELECT * FROM sources WHERE id = ?", (source_id,)
        ).fetchone()

        if row:
            source = dict(row)
            source['credentials'] = blob_to_credentials(
                row['cred_blob'], f"source-{source_id}"
            )
            return source
        return None

    def get_active(self) -> List[Dict[str, Any]]:
        """Get all active sources with credentials."""
        conn = self.db.connect()
        rows = conn.execute(
            "SELECT * FROM sources WHERE active = 1"
        ).fetchall()

        sources = []
        for row in rows:
            source = dict(row)
            source['credentials'] = blob_to_credentials(
                row['cred_blob'], f"source-{row['id']}"
            )
            sources.append(source)
        return sources

    def update_token(self, source_id: int, sync_token: str):
        """Update sync token for incremental sync."""
        conn = self.db.connect()
        conn.execute(
            """UPDATE sources SET sync_token = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (sync_token, source_id)
        )
        conn.commit()

    def remove(self, source_id: int):
        """Remove source and its credentials."""
        delete_credentials(f"source-{source_id}")
        conn = self.db.connect()
        conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))
        conn.commit()

    def set_active(self, source_id: int, active: bool):
        """Enable or disable a source."""
        conn = self.db.connect()
        conn.execute(
            "UPDATE sources SET active = ? WHERE id = ?",
            (active, source_id)
        )
        conn.commit()

    def list(self) -> List[Dict[str, Any]]:
        """Get all sources (without credentials for API)."""
        conn = self.db.connect()
        rows = conn.execute("SELECT id, type, calendar_id, name, active, created_at FROM sources").fetchall()
        return [dict(row) for row in rows]


# API wrapper functions
def add(type: str, calendar_id: str, name: str, credentials: Dict[str, Any]) -> int:
    """API wrapper to add source."""
    db = Database()
    store = SourceStore(db)
    return store.add(type, calendar_id, name, credentials)


def remove(source_id: int):
    """API wrapper to remove source."""
    db = Database()
    store = SourceStore(db)
    store.remove(source_id)
    return {'success': True}
