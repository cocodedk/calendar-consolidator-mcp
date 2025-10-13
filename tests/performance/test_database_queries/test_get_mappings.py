"""Tests for mapping retrieval performance."""

import time
from python.state.mapping_store import MappingStore


def test_get_all_mappings_performance(db_with_many_mappings):
    """Fetching all mappings is performant."""
    store = MappingStore(db_with_many_mappings)

    start = time.time()
    mappings = store.get_all_for_source(1)
    elapsed = time.time() - start

    assert len(mappings) == 1000
    assert elapsed < 1.0  # Should complete in under 1 second


def test_get_single_mapping_performance(db_with_many_mappings):
    """Single mapping lookup is fast."""
    store = MappingStore(db_with_many_mappings)

    start = time.time()
    mapping = store.get(1, 'event_500')
    elapsed = time.time() - start

    assert mapping is not None
    assert elapsed < 0.1  # Should be instant with proper indexing
