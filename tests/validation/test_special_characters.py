"""Test handling of Unicode, emojis, and special characters."""

import pytest
from python.model.event import Event
from datetime import datetime


def test_event_with_emoji_in_subject():
    """Event handles emoji characters in subject."""
    event = Event(
        uid='evt1',
        subject='🎉 Team Party 🎈',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description=None,
        is_private=False
    )

    assert '🎉' in event.subject
    assert event.compute_hash() is not None


def test_event_with_unicode_characters():
    """Event handles various Unicode characters."""
    event = Event(
        uid='evt1',
        subject='Réunion avec François à Zürich',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Zürich, Genève',
        description='Discussion about café and naïve approaches',
        is_private=False
    )

    assert 'Réunion' in event.subject
    assert 'Zürich' in event.location


def test_event_with_chinese_characters():
    """Event handles CJK (Chinese, Japanese, Korean) characters."""
    event = Event(
        uid='evt1',
        subject='会议 ミーティング 회의',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='北京 東京 서울',
        description=None,
        is_private=False
    )

    assert '会议' in event.subject


def test_event_with_special_json_characters():
    """Event handles characters that need JSON escaping."""
    event = Event(
        uid='evt1',
        subject='Meeting "Important" \\Discussion\\',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location=None,
        description='Line 1\nLine 2\tTabbed',
        is_private=False
    )

    graph_data = event.to_graph()
    assert graph_data is not None


def test_event_with_html_entities():
    """Event handles HTML entities and special characters."""
    event = Event(
        uid='evt1',
        subject='Meeting <script>alert("test")</script>',
        start=datetime.fromisoformat('2024-01-15T10:00:00Z'),
        end=datetime.fromisoformat('2024-01-15T11:00:00Z'),
        location='Room A & B',
        description='Cost: €50 £40 $60 ¥500',
        is_private=False
    )

    assert '&' in event.location
    assert '€' in event.description
