"""Generate unique identifiers for iCloud events."""

import uuid


def generate_event_uid() -> str:
    """Generate a unique event UID using UUID v4."""
    return str(uuid.uuid4())
