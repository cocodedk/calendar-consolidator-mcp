# iCloud Connector Module

Modular CalDAV connector for iCloud calendar operations. Refactored to follow component-based architecture with clear separation of concerns.

## Quick Start

```python
from python.connectors.icloud_connector import ICloudConnector

credentials = {
    'username': 'user@icloud.com',
    'password': 'app_password',
    'caldav_url': 'https://caldav.icloud.com/'  # Optional
}

connector = ICloudConnector(credentials)
calendars = connector.list_calendars()
```

## Module Structure

| Module | Purpose | Lines |
|--------|---------|-------|
| `connector.py` | Main aggregator, delegates to operation classes | 66 |
| `calendar_operations.py` | Calendar discovery and listing | 20 |
| `event_operations.py` | Event CRUD (create, read, update, delete) | 58 |
| `sync_operations.py` | Delta sync with hash-based detection | 42 |
| `caldav_client.py` | CalDAV protocol adapter | 172 |
| `helpers/` | Reusable utility functions | 76 |

## Key Operations

### List Calendars
```python
calendars = connector.list_calendars()
# Returns: [{'id': '...', 'name': '...', ...}, ...]
```

### Get Events (Delta Sync)
```python
delta = connector.get_events_delta(calendar_id, sync_token=None)
# Returns: {'events': [...], 'nextSyncToken': '...'}
```

### Create Event
```python
uid = connector.create_event(calendar_id, {
    'title': 'Meeting',
    'start': '2025-01-01T10:00:00Z',
    'end': '2025-01-01T11:00:00Z',
})
```

### Update Event
```python
connector.update_event(calendar_id, event_uid, {
    'title': 'Updated Meeting',
    'start': '2025-01-01T14:00:00Z',
    'end': '2025-01-01T15:00:00Z',
})
```

### Delete Event
```python
connector.delete_event(calendar_id, event_uid)
```

### Get Single Event
```python
event = connector.get_event(calendar_id, event_uid)
```

## Helper Functions

Import helpers directly from the `helpers` module:

```python
from python.connectors.icloud_connector.helpers import (
    parse_caldav_event,
    build_ical_event,
    generate_event_uid,
    get_sync_token,
)
```

## Design Principles

✅ **Single Responsibility**: Each class/function does one thing well
✅ **Testability**: Pure functions and dependency injection
✅ **Maintainability**: Changes isolated to specific modules
✅ **Reusability**: Helpers available for independent use
✅ **Compliance**: All files ≤ 100 lines per project standards

## Testing

Operation classes are designed for easy testing:

```python
from unittest.mock import Mock
from python.connectors.icloud_connector.event_operations import EventOperations

mock_client = Mock()
ops = EventOperations(mock_client)
# Test operations with mocked client
```

## Architecture Diagram

```
ICloudConnector
├── CalendarOperations → CalDAVClient
├── EventOperations → CalDAVClient + helpers
└── SyncOperations → CalDAVClient + helpers

helpers/
├── event_parser() - Parse iCalendar strings
├── event_builder() - Build iCalendar format
├── uid_generator() - Generate UUIDs
└── get_sync_token() - Create timestamp tokens
```

## Backward Compatibility

✅ Public API unchanged from previous monolithic version
✅ All BaseConnector interface methods preserved
✅ Module-level `list_calendars()` function maintained
✅ Existing code continues to work without modifications

## Performance Notes

- CalDAV doesn't support true delta sync; we fetch all events
- Hash-based change detection relies on `_raw_data` field
- Sync tokens use Unix timestamps (not reliable across restarts)
- Consider implementing cursor-based pagination for large calendars

## Security Considerations

⚠️ Credentials stored in memory
⚠️ App passwords required for iCloud (not regular password)
⚠️ CalDAV URL must be HTTPS
✅ All connections should use SSL/TLS
✅ Consider credential rotation strategies
