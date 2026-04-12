"""
Encryption utilities for storing sensitive credentials.

Two storage strategies coexist:
- **Keyring** (preferred): secrets stored in the OS keychain; the database
  holds only a lightweight pointer blob `{"keychain": true}`.
- **Fernet** (legacy / OAuth provider creds): AES-encrypted blobs stored
  directly in SQLite, keyed by a file-based encryption key.
"""

import os
import json
import base64
import keyring
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Optional

_KEYRING_SERVICE = 'calendar-consolidator-mcp'


# ---------------------------------------------------------------------------
# Fernet key management
# ---------------------------------------------------------------------------

def get_key_file_path() -> Path:
    """Get path to encryption key file."""
    return Path(__file__).parent.parent.parent / '.encryption_key'


def generate_encryption_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()


def load_or_create_key() -> bytes:
    """Load existing key or create new one."""
    key_file = get_key_file_path()

    if key_file.exists():
        with open(key_file, 'rb') as f:
            return f.read()

    key = generate_encryption_key()

    with open(key_file, 'wb') as f:
        f.write(key)

    if hasattr(os, 'chmod'):
        os.chmod(key_file, 0o600)

    return key


def get_fernet() -> Fernet:
    """Get Fernet cipher instance."""
    key = load_or_create_key()
    return Fernet(key)


# ---------------------------------------------------------------------------
# Fernet encrypt / decrypt (used by credentials_manager for provider creds)
# ---------------------------------------------------------------------------

def encrypt_credentials(data: dict) -> str:
    """Encrypt credentials dictionary to a base64 string."""
    f = get_fernet()
    json_str = json.dumps(data)
    encrypted = f.encrypt(json_str.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_credentials(encrypted_str: str) -> Optional[dict]:
    """Decrypt a base64 credentials string back to a dict."""
    try:
        f = get_fernet()
        encrypted = base64.b64decode(encrypted_str.encode())
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"Decryption error: {e}")
        return None


# ---------------------------------------------------------------------------
# Keyring helpers (used for calendar-source credentials)
# ---------------------------------------------------------------------------

def store_credentials(key: str, credentials: dict) -> None:
    """Store credentials dict in the system keyring under *key*."""
    keyring.set_password(_KEYRING_SERVICE, key, json.dumps(credentials))


def load_credentials(source_id: str) -> Optional[dict]:
    """Load credentials for *source_id* from the system keyring.

    Args:
        source_id: Identifier for the calendar source.

    Returns:
        Credentials dict if found, None otherwise.
    """
    raw = keyring.get_password(_KEYRING_SERVICE, source_id)
    if raw is None:
        return None
    return json.loads(raw)


def delete_credentials(key: str) -> None:
    """Delete credentials for *key* from the system keyring."""
    try:
        keyring.delete_password(_KEYRING_SERVICE, key)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Blob helpers (lightweight database pointer for keyring-stored creds)
# ---------------------------------------------------------------------------

def credentials_to_blob(credentials: dict) -> bytes:  # noqa: ARG001
    """Return a keychain-pointer blob (not the credentials themselves).

    The blob is stored in SQLite; the real secrets stay in the keyring.
    *credentials* is accepted for API compatibility but not embedded.
    """
    return json.dumps({'keychain': True}).encode('utf-8')


def blob_to_credentials(blob: bytes, source_id: str) -> Optional[dict]:
    """Restore credentials from a keychain-pointer blob + source_id."""
    try:
        data = json.loads(blob.decode('utf-8'))
        if data.get('keychain'):
            return load_credentials(source_id)
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Masking helper
# ---------------------------------------------------------------------------

def mask_secret(secret: str, show_chars: int = 3) -> str:
    """Mask a secret string for display."""
    if not secret or len(secret) <= show_chars * 2:
        return "***"

    prefix = secret[:show_chars]
    suffix = secret[-show_chars:]
    return f"{prefix}***...***{suffix}"
