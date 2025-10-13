"""
Encryption utilities for storing sensitive credentials.
"""

import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Optional


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

    # Generate new key
    key = generate_encryption_key()

    # Save it
    with open(key_file, 'wb') as f:
        f.write(key)

    # Secure permissions (Unix only)
    if hasattr(os, 'chmod'):
        os.chmod(key_file, 0o600)

    return key


def get_fernet() -> Fernet:
    """Get Fernet cipher instance."""
    key = load_or_create_key()
    return Fernet(key)


def encrypt_credentials(data: dict) -> str:
    """Encrypt credentials dictionary."""
    f = get_fernet()
    json_str = json.dumps(data)
    encrypted = f.encrypt(json_str.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_credentials(encrypted_str: str) -> Optional[dict]:
    """Decrypt credentials string."""
    try:
        f = get_fernet()
        encrypted = base64.b64decode(encrypted_str.encode())
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"Decryption error: {e}")
        return None


def mask_secret(secret: str, show_chars: int = 3) -> str:
    """Mask a secret string for display."""
    if not secret or len(secret) <= show_chars * 2:
        return "***"

    prefix = secret[:show_chars]
    suffix = secret[-show_chars:]
    return f"{prefix}***...***{suffix}"


# Legacy functions for backward compatibility with existing code
def credentials_to_blob(credentials: dict) -> str:
    """Convert credentials dict to encrypted blob (legacy)."""
    return encrypt_credentials(credentials)


def blob_to_credentials(blob: str) -> Optional[dict]:
    """Convert encrypted blob to credentials dict (legacy)."""
    return decrypt_credentials(blob)


def store_credentials(key: str, credentials: dict) -> bool:
    """Store credentials in keyring (legacy - uses credentials_manager)."""
    try:
        from .credentials_manager import save_credentials
        return save_credentials(key, credentials)
    except ImportError:
        return False


def delete_credentials(key: str) -> bool:
    """Delete credentials from keyring (legacy - uses credentials_manager)."""
    try:
        from .credentials_manager import delete_credentials as delete_creds
        return delete_creds(key)
    except ImportError:
        return False
