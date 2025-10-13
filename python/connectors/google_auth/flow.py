"""
OAuth flow utilities for Google authentication.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Dict, Any
import json
from .config import OAUTH_CONFIG


def create_client_config(client_id: str, client_secret: str) -> Dict[str, Any]:
    """
    Create OAuth client configuration.

    Args:
        client_id: Google OAuth client ID
        client_secret: Google OAuth client secret

    Returns:
        Client configuration dict
    """
    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            **OAUTH_CONFIG
        }
    }


def create_flow(client_id: str, client_secret: str,
                scopes: list) -> InstalledAppFlow:
    """
    Create OAuth flow instance.

    Args:
        client_id: Google OAuth client ID
        client_secret: Google OAuth client secret
        scopes: List of OAuth scopes

    Returns:
        Configured InstalledAppFlow
    """
    config = create_client_config(client_id, client_secret)
    flow = InstalledAppFlow.from_client_config(config, scopes=scopes)
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    return flow


def serialize_flow_state(client_id: str, client_secret: str) -> str:
    """
    Serialize flow state for storage.

    Args:
        client_id: Google OAuth client ID
        client_secret: Google OAuth client secret

    Returns:
        JSON string of flow state
    """
    return json.dumps({
        'client_id': client_id,
        'client_secret': client_secret
    })
