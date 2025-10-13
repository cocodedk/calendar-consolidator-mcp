"""
Google OAuth authenticator implementation.
"""

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from typing import Dict, Any
from .config import CLIENT_ID, CLIENT_SECRET, SCOPES
from .flow import create_flow, serialize_flow_state


class GoogleAuthenticator:
    """Handles Google OAuth authentication."""

    def __init__(self, client_id: str = CLIENT_ID,
                 client_secret: str = CLIENT_SECRET):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = SCOPES

    def get_device_code_flow(self) -> Dict[str, Any]:
        """
        Initiate device code flow.

        Returns:
            Device code flow info with user_code and verification_url
        """
        flow = create_flow(self.client_id, self.client_secret, self.scopes)
        auth_url, _ = flow.authorization_url(prompt='consent')

        return {
            'verification_url': auth_url,
            'user_code': 'manual',  # User manually visits URL
            'flow_state': serialize_flow_state(
                self.client_id, 
                self.client_secret
            )
        }

    def acquire_token_by_code(self, code: str) -> Dict[str, Any]:
        """
        Complete flow with authorization code.

        Returns:
            Token response with access_token and refresh_token
        """
        flow = create_flow(self.client_id, self.client_secret, self.scopes)
        flow.fetch_token(code=code)
        creds = flow.credentials

        return {
            'access_token': creds.token,
            'refresh_token': creds.refresh_token,
            'expires_at': creds.expiry.isoformat() if creds.expiry else None
        }

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Returns:
            New token response
        """
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        creds.refresh(Request())

        return {
            'access_token': creds.token,
            'refresh_token': creds.refresh_token or refresh_token,
            'expires_at': creds.expiry.isoformat() if creds.expiry else None
        }

