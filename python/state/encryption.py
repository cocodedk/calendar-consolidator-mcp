"""
Credential encryption module for Calendar Consolidator MCP.
Handles secure storage of OAuth tokens and credentials.
"""

import json
import keyring
from typing import Optional, Dict, Any


SERVICE_NAME = "calendar-consolidator-mcp"


def store_credentials(identifier: str, credentials: Dict[str, Any]) -> None:
    """
    Store credentials securely using OS keychain.

    Args:
        identifier: Unique identifier (e.g., "source-1", "target-1")
        credentials: Dictionary containing credential data
    """
    cred_json = json.dumps(credentials)
    keyring.set_password(SERVICE_NAME, identifier, cred_json)


def load_credentials(identifier: str) -> Optional[Dict[str, Any]]:
    """
    Load credentials from OS keychain.

    Args:
        identifier: Unique identifier

    Returns:
        Dictionary of credentials or None if not found
    """
    cred_json = keyring.get_password(SERVICE_NAME, identifier)
    if cred_json:
        return json.loads(cred_json)
    return None


def delete_credentials(identifier: str) -> None:
    """
    Delete credentials from OS keychain.

    Args:
        identifier: Unique identifier
    """
    try:
        keyring.delete_password(SERVICE_NAME, identifier)
    except keyring.errors.PasswordDeleteError:
        pass  # Already deleted or doesn't exist


def credentials_to_blob(credentials: Dict[str, Any]) -> bytes:
    """
    Convert credentials dict to blob for database storage.
    For OS keychain approach, this stores a reference.

    Args:
        credentials: Credential dictionary

    Returns:
        Blob data for database
    """
    # Store minimal reference in DB, actual data in keychain
    reference = {"keychain": True}
    return json.dumps(reference).encode('utf-8')


def blob_to_credentials(blob: bytes, identifier: str) -> Optional[Dict[str, Any]]:
    """
    Convert database blob to credentials dict.

    Args:
        blob: Blob data from database
        identifier: Identifier to load from keychain

    Returns:
        Credentials dictionary or None
    """
    reference = json.loads(blob.decode('utf-8'))
    if reference.get("keychain"):
        return load_credentials(identifier)
    return None
