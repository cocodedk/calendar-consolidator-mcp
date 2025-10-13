"""
iCloud authentication handler using CalDAV.
"""

import caldav
from typing import Dict, Any
from .config import CALDAV_URL, TIMEOUT


class ICloudAuthenticator:
    """Handles iCloud CalDAV authentication with app-specific passwords."""

    def __init__(self, caldav_url: str = CALDAV_URL):
        """
        Initialize iCloud authenticator.

        Args:
            caldav_url: CalDAV server URL (default: iCloud)
        """
        self.caldav_url = caldav_url

    def validate_credentials(self, apple_id: str,
                           app_password: str) -> Dict[str, Any]:
        """
        Validate credentials by attempting to connect to iCloud CalDAV.

        Args:
            apple_id: Apple ID email
            app_password: App-specific password (not regular password)

        Returns:
            Dict with credentials and connection status

        Raises:
            Exception: If credentials are invalid or connection fails
        """
        try:
            # Attempt to connect to CalDAV server
            client = caldav.DAVClient(
                url=self.caldav_url,
                username=apple_id,
                password=app_password,
                timeout=TIMEOUT
            )

            # Test connection by getting principal
            principal = client.principal()

            # If we get here, credentials are valid
            return {
                'username': apple_id,
                'password': app_password,
                'caldav_url': self.caldav_url,
                'principal_url': str(principal.url) if principal else None
            }

        except caldav.lib.error.AuthorizationError as e:
            raise Exception(
                "Invalid credentials. Please check your Apple ID and "
                "app-specific password."
            ) from e
        except Exception as e:
            raise Exception(
                f"Failed to connect to iCloud CalDAV: {str(e)}"
            ) from e

    def get_credentials_dict(self, apple_id: str,
                            app_password: str) -> Dict[str, Any]:
        """
        Get credentials dictionary for storage.

        Args:
            apple_id: Apple ID email
            app_password: App-specific password

        Returns:
            Credentials dict for storage
        """
        validated = self.validate_credentials(apple_id, app_password)

        return {
            'type': 'icloud',
            'username': validated['username'],
            'password': validated['password'],
            'caldav_url': validated['caldav_url']
        }
