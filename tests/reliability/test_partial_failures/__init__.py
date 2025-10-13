"""Partial failure tests - modular structure."""

from .test_single_event_failure import test_sync_continues_after_single_event_failure
from .test_batch_operations import test_batch_operation_collects_errors
from .test_failure_logging import test_partial_sync_logs_failures
from .test_transaction_rollback import test_transaction_rollback_on_critical_failure

__all__ = [
    'test_sync_continues_after_single_event_failure',
    'test_batch_operation_collects_errors',
    'test_partial_sync_logs_failures',
    'test_transaction_rollback_on_critical_failure'
]
