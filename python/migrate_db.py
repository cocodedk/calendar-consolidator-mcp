#!/usr/bin/env python3
"""
Database migration script to add 'google' and 'icloud' to type CHECK constraints.
"""

import sqlite3
import sys
from pathlib import Path

def migrate():
    """Migrate database schema to support Google and iCloud calendar types."""

    config_dir = Path.home() / ".calendar-consolidator"
    db_path = config_dir / "config.db"

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)

    print(f"Migrating database at {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION")

        # 1. Backup existing data
        print("Backing up sources table...")
        sources_data = list(conn.execute("""
            SELECT id, type, calendar_id, name, cred_blob, sync_token,
                   active, created_at, updated_at
            FROM sources
        """).fetchall())
        print(f"  Found {len(sources_data)} sources to migrate")

        print("Backing up target table...")
        target_data = list(conn.execute("""
            SELECT id, type, calendar_id, name, cred_blob, created_at, updated_at
            FROM target
        """).fetchall())
        print(f"  Found {len(target_data)} target to migrate")

        print("Backing up mappings table...")
        mappings_data = list(conn.execute("""
            SELECT source_id, source_event_uid, target_event_id,
                   last_hash, created_at, updated_at
            FROM mappings
        """).fetchall())
        print(f"  Found {len(mappings_data)} mappings to migrate")

        # 2. Drop old tables
        print("\nDropping old tables...")
        conn.execute("DROP TABLE IF EXISTS sources")
        conn.execute("DROP TABLE IF EXISTS target")
        conn.execute("DROP TABLE IF EXISTS mappings")

        # 3. Create new tables with updated schema
        print("Creating new tables with updated schema...")

        conn.execute("""
            CREATE TABLE sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('graph', 'caldav', 'google', 'icloud')),
                calendar_id TEXT NOT NULL,
                name TEXT,
                cred_blob BLOB NOT NULL,
                sync_token TEXT,
                active BOOLEAN NOT NULL DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("CREATE INDEX idx_sources_type ON sources(type)")
        conn.execute("CREATE INDEX idx_sources_active ON sources(active)")

        conn.execute("""
            CREATE TABLE target (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                type TEXT NOT NULL CHECK (type IN ('graph', 'caldav', 'google', 'icloud')),
                calendar_id TEXT NOT NULL,
                name TEXT,
                cred_blob BLOB NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE mappings (
                source_id INTEGER NOT NULL,
                source_event_uid TEXT NOT NULL,
                target_event_id TEXT NOT NULL,
                last_hash TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(source_id, source_event_uid),
                FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
            )
        """)

        conn.execute("CREATE INDEX idx_mappings_source ON mappings(source_id)")
        conn.execute("CREATE INDEX idx_mappings_target ON mappings(target_event_id)")

        # 4. Restore data
        print("\nRestoring data...")

        for row in sources_data:
            conn.execute("""
                INSERT INTO sources
                (id, type, calendar_id, name, cred_blob, sync_token,
                 active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        print(f"  Restored {len(sources_data)} sources")

        for row in target_data:
            conn.execute("""
                INSERT INTO target
                (id, type, calendar_id, name, cred_blob, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(row))
        print(f"  Restored {len(target_data)} target(s)")

        for row in mappings_data:
            conn.execute("""
                INSERT INTO mappings
                (source_id, source_event_uid, target_event_id,
                 last_hash, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, tuple(row))
        print(f"  Restored {len(mappings_data)} mappings")

        # 5. Commit transaction
        conn.commit()

        print("\n✓ Migration completed successfully!")
        print("  - sources table now supports: graph, caldav, google, icloud")
        print("  - target table now supports: graph, caldav, google, icloud")

    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print("  Rolling back changes...")
        conn.rollback()
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
