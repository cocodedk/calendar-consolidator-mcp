"""
Main sync engine implementation.
"""

import time
from typing import Dict, Any
from ...state import ConfigStore
from .connector_factory import get_connector
from .diff_applier import DiffApplier
from .sync_executor import SyncExecutor


class Syncer:
    """Executes calendar synchronization operations."""

    def __init__(self, config_store: ConfigStore):
        self.config = config_store

    def _apply_changes(self, diff, connector, calendar_id: str,
                       source_id: int) -> tuple:
        """
        Backward compatibility wrapper for tests.
        Delegates to DiffApplier.
        """
        applier = DiffApplier(self.config, source_id)
        return applier.apply(diff, connector, calendar_id)

    def _get_connector(self, config: Dict[str, Any]):
        """
        Backward compatibility wrapper for tests.
        Delegates to connector_factory.
        """
        return get_connector(config)

    def sync_once(self, source_id: int) -> Dict[str, Any]:
        """
        Execute sync for a single source.

        Returns:
            Sync result with counts and status
        """
        start_time = time.time()

        try:
            executor = SyncExecutor(self.config, source_id)
            result = executor.execute(start_time)
            self._log_success(source_id, result)
            return result

        except Exception as e:
            self._log_error(source_id, e, start_time)
            raise

    def _log_success(self, source_id: int, result: Dict[str, Any]) -> None:
        """Log successful sync operation."""
        self.config.logs.log_sync(
            source_id, 'success',
            result['created'], result['updated'], result['deleted'],
            duration_ms=result['duration']
        )

    def _log_error(self, source_id: int, error: Exception,
                   start_time: float) -> None:
        """Log failed sync operation."""
        duration_ms = int((time.time() - start_time) * 1000)
        self.config.logs.log_sync(
            source_id, 'error', 0, 0, 0,
            error_message=str(error),
            duration_ms=duration_ms
        )
