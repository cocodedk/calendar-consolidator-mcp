"""
Sync log storage operations.
Records history of sync operations for monitoring.
"""

from typing import Optional, List, Dict, Any
from .database import Database


class LogStore:
    """Manages sync operation logs."""

    def __init__(self, db: Database):
        self.db = db

    def log_sync(self, source_id: Optional[int], status: str,
                 created: int = 0, updated: int = 0, deleted: int = 0,
                 error_message: Optional[str] = None,
                 duration_ms: Optional[int] = None) -> int:
        """Record sync operation. Returns log ID."""
        conn = self.db.connect()
        cursor = conn.execute(
            """INSERT INTO sync_logs
               (source_id, status, created_count, updated_count, deleted_count,
                error_message, duration_ms)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (source_id, status, created, updated, deleted, error_message, duration_ms)
        )
        log_id = cursor.lastrowid
        conn.commit()
        return log_id

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent sync logs."""
        conn = self.db.connect()
        rows = conn.execute(
            "SELECT * FROM sync_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_for_source(self, source_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get logs for specific source."""
        conn = self.db.connect()
        rows = conn.execute(
            """SELECT * FROM sync_logs
               WHERE source_id = ?
               ORDER BY timestamp DESC LIMIT ?""",
            (source_id, limit)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent error logs."""
        conn = self.db.connect()
        rows = conn.execute(
            """SELECT * FROM sync_logs
               WHERE status = 'error'
               ORDER BY timestamp DESC LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get sync statistics for last N days."""
        conn = self.db.connect()
        row = conn.execute(
            """SELECT
                 COUNT(*) as total_syncs,
                 SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                 SUM(created_count) as total_created,
                 SUM(updated_count) as total_updated,
                 SUM(deleted_count) as total_deleted
               FROM sync_logs
               WHERE timestamp > datetime('now', '-' || ? || ' days')""",
            (days,)
        ).fetchone()
        return dict(row) if row else {}
