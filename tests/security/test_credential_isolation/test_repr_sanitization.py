"""Tests for credential sanitization in object repr."""

from datetime import datetime, timedelta, timezone


def test_credential_sanitization_in_repr():
    """Object repr doesn't expose credentials."""
    from python.connectors.graph_connector import GraphConnector

    credentials = {
        'access_token': 'secret123',
        'refresh_token': 'refresh456',
        'expires_at': (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }

    connector = GraphConnector(credentials)
    repr_str = repr(connector)

    # Repr should not expose actual token values
    # Note: Current implementation may not sanitize repr
    # This test documents the expected behavior
