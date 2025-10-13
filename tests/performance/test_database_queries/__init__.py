"""Database query performance tests - modular structure."""

from .fixtures import db_with_many_mappings
from .test_get_mappings import (
    test_get_all_mappings_performance,
    test_get_single_mapping_performance
)
from .test_bulk_operations import test_bulk_insert_mappings
from .test_indexed_queries import test_query_with_index_performance

__all__ = [
    'db_with_many_mappings',
    'test_get_all_mappings_performance',
    'test_get_single_mapping_performance',
    'test_bulk_insert_mappings',
    'test_query_with_index_performance'
]
