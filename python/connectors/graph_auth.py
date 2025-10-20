"""
Microsoft Graph OAuth authentication module.
Handles device code flow and token management.
"""

import msal
from typing import Dict, Any, Optional


def _load_stored_ms_creds() -> Optional[Dict[str, str]]:
    """Load stored Microsoft credentials from the encrypted settings DB.

    Returns client_id and tenant_id when available. Swallows errors so tests
    and environments without an initialized DB are unaffected.
    """
    try:
        # Absolute import works because PYTHONPATH includes project root
        from python.state.credentials_manager import load_credentials  # type: ignore
        return load_credentials('microsoft')
    except Exception:
        return None

CLIENT_ID = "YOUR_APP_CLIENT_ID"  # TODO: Configure in settings
AUTHORITY = "https://login.microsoftonline.com/common"
# MSAL forbids reserved scopes like 'offline_access', 'openid', 'profile'.
# Request only resource scopes here; refresh capability is handled by MSAL.
SCOPES = ["Calendars.ReadWrite"]


class GraphAuthenticator:
    """Handles Microsoft Graph OAuth authentication."""

    def __init__(self, client_id: str = CLIENT_ID):
        self.client_id = client_id
        self.authority = AUTHORITY
        self.scopes = SCOPES

        # Override defaults with stored credentials when available
        stored = _load_stored_ms_creds()
        if stored:
            cid = stored.get('client_id')
            tenant = stored.get('tenant_id') or 'common'
            if cid:
                self.client_id = cid
            if tenant:
                self.authority = f"https://login.microsoftonline.com/{tenant}"

    def get_device_code_flow(self) -> Dict[str, Any]:
        """
        Initiate device code flow.

        Returns:
            Device code flow info with user_code and verification_uri
        """
        app = msal.PublicClientApplication(
            self.client_id,
            authority=self.authority
        )

        flow = app.initiate_device_flow(scopes=self.scopes)

        if "user_code" not in flow:
            details = flow.get('error_description') or flow.get('error') or 'Unknown error'
            raise Exception(f"Failed to create device flow: {details}")

        return flow

    def acquire_token_by_device_flow(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete device code flow and get tokens.

        Returns:
            Token response with access_token and refresh_token
        """
        app = msal.PublicClientApplication(
            self.client_id,
            authority=self.authority
        )

        result = app.acquire_token_by_device_flow(flow)

        if "access_token" not in result:
            err = result.get('error')
            desc = result.get('error_description', 'Unknown error')
            if err:
                raise Exception(f"Authentication failed: {err}: {desc}")
            raise Exception(f"Authentication failed: {desc}")

        return result

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Returns:
            New token response
        """
        app = msal.PublicClientApplication(
            self.client_id,
            authority=self.authority
        )

        accounts = app.get_accounts()

        if accounts:
            result = app.acquire_token_silent(self.scopes, account=accounts[0])
            if result and "access_token" in result:
                return result

        # Fallback to refresh token
        result = app.acquire_token_by_refresh_token(refresh_token, self.scopes)

        if "access_token" not in result:
            raise Exception("Token refresh failed")

        return result
