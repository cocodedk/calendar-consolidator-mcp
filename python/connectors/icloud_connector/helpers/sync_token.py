"""Generate sync tokens for CalDAV operations."""

import time


def get_sync_token() -> str:
    """
    Generate sync token using current timestamp.

    CalDAV doesn't have proper sync tokens like Graph API,
    so we use timestamp-based approach.

    Returns:
        Current timestamp as string
    """
    return str(int(time.time()))
