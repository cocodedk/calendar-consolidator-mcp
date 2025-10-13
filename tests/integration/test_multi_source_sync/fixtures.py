"""Fixtures for multi-source sync tests."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_config_multi_source():
    """Mock config with multiple sources."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    config.logs = Mock()

    config.sources.get_active.return_value = [
        {
            'id': 1,
            'type': 'graph',
            'calendar_id': 'work_cal',
            'credentials': {'access_token': 'token1'}
        },
        {
            'id': 2,
            'type': 'graph',
            'calendar_id': 'personal_cal',
            'credentials': {'access_token': 'token2'}
        }
    ]

    config.target.get.return_value = {
        'type': 'graph',
        'calendar_id': 'consolidated_cal',
        'credentials': {'access_token': 'target_token'}
    }

    return config
