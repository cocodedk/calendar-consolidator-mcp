"""
Google OAuth configuration constants.
"""

# TODO: Configure in settings or environment variables
# Replace these with your actual Google OAuth credentials
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your Client ID
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"  # Replace with your Client Secret

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

OAUTH_CONFIG = {
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
}
