"""
Google OAuth authentication module.
Handles device code flow and token management.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import Dict, Any, Optional
import json


# TODO: Configure in settings
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]


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
        client_config = {
            "installed": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
            }
        }

        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=self.scopes
        )

        # Use out-of-band flow for device code
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

        auth_url, _ = flow.authorization_url(prompt='consent')

        return {
            'verification_url': auth_url,
            'user_code': 'manual',  # User manually visits URL
            'flow_state': json.dumps({
                'client_id': self.client_id,
                'client_secret': self.client_secret
            })
        }

    def acquire_token_by_code(self, code: str) -> Dict[str, Any]:
        """
        Complete flow with authorization code.

        Returns:
            Token response with access_token and refresh_token
        """
        client_config = {
            "installed": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
            }
        }

        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=self.scopes
        )
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
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
