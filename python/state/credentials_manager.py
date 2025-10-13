"""
Credentials manager for OAuth provider credentials.
"""

import sqlite3
from typing import Optional, Dict, Any
from pathlib import Path
from .encryption import encrypt_credentials, decrypt_credentials, mask_secret


def get_db_path() -> Path:
    """Get database path."""
    return Path(__file__).parent.parent.parent / 'calendar_consolidator.db'


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def save_credentials(provider: str, credentials: dict) -> bool:
    """Save encrypted credentials for a provider."""
    try:
        encrypted = encrypt_credentials(credentials)
        key = f"{provider}_credentials"

        conn = get_connection()
        cursor = conn.cursor()

        # Upsert
        cursor.execute("""
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, encrypted))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving credentials: {e}")
        return False


def load_credentials(provider: str) -> Optional[dict]:
    """Load and decrypt credentials for a provider."""
    try:
        key = f"{provider}_credentials"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return decrypt_credentials(row['value'])
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None


def get_masked_credentials(provider: str) -> Optional[dict]:
    """Get credentials with secrets masked."""
    creds = load_credentials(provider)
    if not creds:
        return None

    masked = {}
    for key, value in creds.items():
        if 'secret' in key.lower() or 'password' in key.lower():
            masked[key] = mask_secret(value)
        else:
            masked[key] = value

    return masked


def delete_credentials(provider: str) -> bool:
    """Delete credentials for a provider."""
    try:
        key = f"{provider}_credentials"

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM settings WHERE key = ?", (key,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting credentials: {e}")
        return False
