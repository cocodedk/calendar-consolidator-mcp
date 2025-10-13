"""Test Syncer initialization."""

import pytest
from unittest.mock import Mock
from python.sync.syncer import Syncer


def test_syncer_init():
    """Test Syncer initialization with ConfigStore."""
    mock_config = Mock()

    syncer = Syncer(mock_config)

    assert syncer.config == mock_config


def test_syncer_has_sync_once_method():
    """Test Syncer has sync_once method."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    assert hasattr(syncer, 'sync_once')
    assert callable(syncer.sync_once)


def test_syncer_has_get_connector_method():
    """Test Syncer has _get_connector method."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    assert hasattr(syncer, '_get_connector')
    assert callable(syncer._get_connector)


def test_syncer_has_apply_changes_method():
    """Test Syncer has _apply_changes method."""
    mock_config = Mock()
    syncer = Syncer(mock_config)

    assert hasattr(syncer, '_apply_changes')
    assert callable(syncer._apply_changes)
