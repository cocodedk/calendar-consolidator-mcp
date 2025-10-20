"""
Google OAuth configuration constants.
"""

import os

# Read credentials from environment when available to avoid hardcoding secrets.
# Fallbacks keep previous behavior for development if env vars are not set.
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

OAUTH_CONFIG = {
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    # Note: OOB is used by the current manual flow. If Google blocks OOB
    # for your client, we can migrate this to a localhost loopback flow.
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
}
