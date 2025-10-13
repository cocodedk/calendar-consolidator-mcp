"""
Token management for Microsoft Graph connector.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any


class GraphTokenManager:
    """Manages token validation and refresh for Graph API."""

    def __init__(self, credentials: Dict[str, Any], auth_handler):
        """
        Initialize token manager.

        Args:
            credentials: Credential dictionary
            auth_handler: GraphAuthenticator instance
        """
        self.credentials = credentials
        self.auth_handler = auth_handler

    def is_token_expired(self) -> bool:
        """
        Check if token is expired or will expire soon.

        Returns:
            True if token needs refresh
        """
        if 'expires_at' not in self.credentials:
            return False

        expires_at = datetime.fromisoformat(self.credentials['expires_at'])
        return datetime.now(timezone.utc) >= expires_at - timedelta(minutes=5)

    def refresh_if_needed(self) -> None:
        """Refresh token if expired."""
        if self.is_token_expired():
            self.refresh()

    def refresh(self) -> None:
        """Force refresh the access token."""
        refresh_token = self.credentials.get('refresh_token')
        if not refresh_token:
            raise Exception("No refresh token available")

        result = self.auth_handler.refresh_token(refresh_token)
        self.credentials['access_token'] = result['access_token']
        self.credentials['expires_at'] = (
            datetime.now(timezone.utc) + timedelta(seconds=result.get('expires_in', 3600))
        ).isoformat()

    def get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with auth token.

        Returns:
            Headers dict with authorization and content type
        """
        self.refresh_if_needed()
        return {
            'Authorization': f"Bearer {self.credentials['access_token']}",
            'Content-Type': 'application/json'
        }
