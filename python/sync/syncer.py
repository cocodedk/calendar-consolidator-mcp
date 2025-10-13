"""
Main sync engine - re-export from modular structure.
Note: This file is shadowed by the syncer/ directory.
"""

from .syncer import Syncer, sync_once

__all__ = ['Syncer', 'sync_once']
