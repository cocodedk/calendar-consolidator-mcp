"""Test hash stability across serialization."""

from python.model.event import Event
from datetime import datetime


def test_hash_stable_across_serialization():
    """Event hash remains stable after to_graph/from_graph round-trip."""
    original = Event(
        uid='evt1',
        subject='Meeting',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Office',
        description='Discussion',
        is_private=False
    )

    original_hash = original.compute_hash()

    # Convert to Graph format and back
    graph_data = original.to_graph()
    graph_data['id'] = original.uid  # Add ID for round-trip
    # Add bodyPreview since from_graph reads from that, not body
    if 'body' in graph_data:
        graph_data['bodyPreview'] = graph_data['body']['content']
    restored = Event.from_graph(graph_data)
    restored_hash = restored.compute_hash()

    # Hashes should match
    assert original_hash == restored_hash
