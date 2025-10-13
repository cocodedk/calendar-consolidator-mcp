"""
Token validation and refresh management for Google Calendar.
"""

from datetime import datetime, timedelta
from typing import Dict, Any


class TokenManager:
    """Manages token validation and refresh."""

    def __init__(self, credentials: Dict[str, Any], auth_handler):
        """
        Initialize token manager.

        Args:
            credentials: Credential dictionary
            auth_handler: GoogleAuthenticator instance
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
        return datetime.utcnow() >= expires_at - timedelta(minutes=5)

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
        self.credentials['expires_at'] = result['expires_at']

    def get_access_token(self) -> str:
        """
        Get valid access token.

        Returns:
            Current access token
        """
        self.refresh_if_needed()
        return self.credentials['access_token']

