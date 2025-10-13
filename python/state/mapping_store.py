"""
Event mapping storage operations.
Tracks source events to target events mappings.
"""

from typing import Optional, Dict, Any, List
from .database import Database


class MappingStore:
    """Manages event mappings between source and target calendars."""

    def __init__(self, db: Database):
        self.db = db

    def create(self, source_id: int, source_event_uid: str,
               target_event_id: str, last_hash: str):
        """Create new event mapping."""
        conn = self.db.connect()
        conn.execute(
            """INSERT INTO mappings (source_id, source_event_uid, target_event_id, last_hash)
               VALUES (?, ?, ?, ?)""",
            (source_id, source_event_uid, target_event_id, last_hash)
        )
        conn.commit()

    def get(self, source_id: int, source_event_uid: str) -> Optional[Dict[str, Any]]:
        """Get mapping for a source event."""
        conn = self.db.connect()
        row = conn.execute(
            """SELECT * FROM mappings
               WHERE source_id = ? AND source_event_uid = ?""",
            (source_id, source_event_uid)
        ).fetchone()
        return dict(row) if row else None

    def update_hash(self, source_id: int, source_event_uid: str, last_hash: str):
        """Update hash for change detection."""
        conn = self.db.connect()
        conn.execute(
            """UPDATE mappings SET last_hash = ?, updated_at = CURRENT_TIMESTAMP
               WHERE source_id = ? AND source_event_uid = ?""",
            (last_hash, source_id, source_event_uid)
        )
        conn.commit()

    def delete(self, source_id: int, source_event_uid: str):
        """Delete mapping."""
        conn = self.db.connect()
        conn.execute(
            "DELETE FROM mappings WHERE source_id = ? AND source_event_uid = ?",
            (source_id, source_event_uid)
        )
        conn.commit()

    def get_all_for_source(self, source_id: int) -> List[Dict[str, Any]]:
        """Get all mappings for a source."""
        conn = self.db.connect()
        rows = conn.execute(
            "SELECT * FROM mappings WHERE source_id = ?", (source_id,)
        ).fetchall()
        return [dict(row) for row in rows]

    def count_for_source(self, source_id: int) -> int:
        """Count mappings for a source."""
        conn = self.db.connect()
        row = conn.execute(
            "SELECT COUNT(*) as count FROM mappings WHERE source_id = ?",
            (source_id,)
        ).fetchone()
        return row['count']
