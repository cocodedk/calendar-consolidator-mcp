"""
Data model modules.
Provides event normalization and diff computation.
"""

from .event import Event
from .diff import DiffResult, compute_diff

__all__ = ['Event', 'DiffResult', 'compute_diff']
