"""Shared fixtures for incremental sync tests."""

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_config_with_token():
    """Mock config with existing sync token."""
    config = Mock()
    config.sources = Mock()
    config.target = Mock()
    config.mappings = Mock()
    config.settings = Mock()
    config.logs = Mock()
    return config
