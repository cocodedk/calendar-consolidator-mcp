#!/usr/bin/env python3
"""
Database initialization script.
Creates SQLite database with schema at ~/.calendar-consolidator/config.db
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from python.state import ConfigStore


def main():
    """Initialize database with schema."""
    print("Initializing Calendar Consolidator database...")

    config_dir = Path.home() / ".calendar-consolidator"
    db_path = config_dir / "config.db"

    print(f"Database location: {db_path}")

    # Create config store and initialize
    store = ConfigStore()
    store.initialize()

    print("✓ Database created successfully")
    print("✓ Schema initialized")
    print("✓ Default settings inserted")
    print("\nReady to configure calendars!")

    store.close()


if __name__ == "__main__":
    main()
