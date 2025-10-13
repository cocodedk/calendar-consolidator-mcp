"""Multi-source sync tests - modular structure."""

from .fixtures import mock_config_multi_source
from .test_event_aggregation import test_sync_all_sources_aggregates_events
from .test_mapping_isolation import test_multi_source_maintains_separate_mappings

__all__ = [
    'mock_config_multi_source',
    'test_sync_all_sources_aggregates_events',
    'test_multi_source_maintains_separate_mappings'
]
