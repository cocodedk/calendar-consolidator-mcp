"""Test BaseConnector abstract interface."""

import pytest
from python.connectors.base_connector import BaseConnector


def test_base_connector_is_abstract():
    """BaseConnector cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseConnector()


def test_base_connector_requires_list_calendars():
    """Subclass must implement list_calendars."""
    class IncompleteConnector(BaseConnector):
        def get_events_delta(self, calendar_id, sync_token=None):
            pass
        def create_event(self, calendar_id, event_data):
            pass
        def update_event(self, calendar_id, event_id, event_data):
            pass
        def delete_event(self, calendar_id, event_id):
            pass
        def get_event(self, calendar_id, event_id):
            pass
    
    with pytest.raises(TypeError):
        IncompleteConnector()


def test_base_connector_all_methods_required():
    """All abstract methods must be implemented."""
    class CompleteConnector(BaseConnector):
        def list_calendars(self):
            return []
        def get_events_delta(self, calendar_id, sync_token=None):
            return {'events': [], 'nextSyncToken': None}
        def create_event(self, calendar_id, event_data):
            return "event123"
        def update_event(self, calendar_id, event_id, event_data):
            pass
        def delete_event(self, calendar_id, event_id):
            pass
        def get_event(self, calendar_id, event_id):
            return None
    
    connector = CompleteConnector()
    assert connector is not None
    assert connector.list_calendars() == []

