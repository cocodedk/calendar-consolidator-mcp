"""
Token validation and refresh management for Google Calendar.
"""

from datetime import datetime, timedelta, timezone
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
        if 'expires_at' not in self.credentials or not self.credentials.get('expires_at'):
            return False

        exp_str = self.credentials['expires_at']
        # Normalize common ISO formats: handle trailing 'Z' and naive datetimes
        try:
            if isinstance(exp_str, str):
                iso = exp_str.replace('Z', '+00:00')
                expires_at = datetime.fromisoformat(iso)
            elif isinstance(exp_str, (int, float)):
                # Epoch seconds
                expires_at = datetime.fromtimestamp(float(exp_str), tz=timezone.utc)
            else:
                # Unsupported type; assume not expired
                return False

            if expires_at.tzinfo is None:
                # Assume UTC if no timezone info
                expires_at = expires_at.replace(tzinfo=timezone.utc)
        except Exception:
            # If parsing fails, assume not expired to avoid hard failures
            return False

        return datetime.now(timezone.utc) >= (expires_at - timedelta(minutes=5))

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
