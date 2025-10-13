"""
Google Calendar API service builder.
"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Any


def build_calendar_service(access_token: str) -> Any:
    """
    Build Google Calendar API service.

    Args:
        access_token: OAuth access token

    Returns:
        Google Calendar API service instance
    """
    creds = Credentials(token=access_token)
    return build('calendar', 'v3', credentials=creds)

