"""Test diff summary generation."""

import pytest
from datetime import datetime, timezone
from python.model.event import Event
from python.model.diff import DiffResult


def test_diff_result_count_total():
    """Test counting total changes in DiffResult."""
    result = DiffResult()
    result.to_create = [Mock() for _ in range(3)]
    result.to_update = [(Mock(), 'id1'), (Mock(), 'id2')]
    result.to_delete = ['id3', 'id4', 'id5']

    assert result.count_total() == 8


def test_diff_result_to_summary():
    """Test converting DiffResult to summary dict."""
    event = Event(
        uid='test-123',
        subject='Test Event',
        start=datetime(2025, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        end=datetime(2025, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
    )

    result = DiffResult()
    result.to_create = [event]
    result.to_update = [(event, 'target-id')]
    result.to_delete = ['old-id']

    summary = result.to_summary()

    assert summary['wouldCreate'] == 1
    assert summary['wouldUpdate'] == 1
    assert summary['wouldDelete'] == 1
    assert len(summary['sampleEvents']) == 2


def test_empty_diff_result():
    """Test empty DiffResult."""
    result = DiffResult()

    assert result.count_total() == 0
    summary = result.to_summary()
    assert summary['wouldCreate'] == 0
    assert len(summary['sampleEvents']) == 0


# Mock for testing
class Mock:
    pass
