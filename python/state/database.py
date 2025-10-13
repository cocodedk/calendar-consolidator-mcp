"""
Database connection and initialization module.
Handles SQLite connection and schema setup.
"""

import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    """SQLite database connection manager."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database. Defaults to ~/.calendar-consolidator/config.db
        """
        if db_path is None:
            config_dir = Path.home() / ".calendar-consolidator"
            config_dir.mkdir(exist_ok=True)
            db_path = str(config_dir / "config.db")

        self.db_path = db_path
        self.conn = None

    def connect(self) -> sqlite3.Connection:
        """Get database connection with row factory and foreign keys enabled."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_schema(self):
        """Initialize database schema from schema.sql file."""
        schema_path = Path(__file__).parent.parent.parent / "database" / "schema.sql"

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        conn = self.connect()
        conn.executescript(schema_sql)
        conn.commit()

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type is None:
            if self.conn:
                self.conn.commit()
        self.close()
