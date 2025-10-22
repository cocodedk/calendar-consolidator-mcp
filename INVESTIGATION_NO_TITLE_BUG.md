# Investigation: "No title" on Target Calendar After Sync

## Issue
After syncing calendars, events on the target calendar are shown with "No title".

## Root Cause

The problem occurs when syncing to an **iCloud/CalDAV target calendar**. The issue is in the sync data flow:

### The Bug Flow

1. **In `diff_applier.py`** (lines 81-96):
   ```python
   def _to_provider_payload(self, event, connector) -> dict:
       """Convert Event to the payload format expected by the connector."""
       try:
           from ...connectors.graph_connector.connector import GraphConnector
           from ...connectors.google_connector.connector import GoogleConnector

           if isinstance(connector, GraphConnector):
               return event.to_graph()
           if isinstance(connector, GoogleConnector):
               return event.to_google()
       except Exception:
           pass

       # Default to Graph format
       return event.to_graph()
   ```

   **Problem**: The code only checks for `GraphConnector` and `GoogleConnector`. When the target is an `ICloudConnector`, it falls through to the default case and uses `event.to_graph()`.

2. **Graph format vs CalDAV format mismatch**:

   `Event.to_graph()` returns (lines 91-111 in `event.py`):
   ```python
   {
       'subject': 'Event Title',
       'start': {
           'dateTime': '2025-01-15T10:00:00+00:00',
           'timeZone': 'UTC'
       },
       'end': {
           'dateTime': '2025-01-15T11:00:00+00:00',
           'timeZone': 'UTC'
       },
       'isAllDay': False,
       'location': {'displayName': 'Location name'},
       'body': {'contentType': 'text', 'content': 'Description'}
   }
   ```

   But `event_to_ical()` in `ical_builder.py` expects (lines 8-54):
   ```python
   {
       'subject': 'Event Title',
       'start': '2025-01-15T10:00:00+00:00',  # Simple string!
       'end': '2025-01-15T11:00:00+00:00',    # Simple string!
       'location': 'Location name',           # Simple string!
       'body': 'Description'                  # Simple string!
   }
   ```

3. **The crash/error**:

   In `ical_builder.py` lines 32-36:
   ```python
   if 'start' in event_data:
       start_dt = datetime.fromisoformat(
           event_data['start'].replace('Z', '+00:00')  # ❌ Calls .replace() on a dict!
       )
       event.add('dtstart', start_dt)
   ```

   When `event_data['start']` is a dictionary `{'dateTime': ..., 'timeZone': ...}`, calling `.replace()` on it will cause an `AttributeError`.

4. **Result**: The event creation likely fails or creates a malformed iCalendar event, resulting in events with no title appearing on the target calendar.

## Missing Implementation

The `Event` class in `python/model/event.py` has:
- ✅ `from_graph()` - parse Graph API events
- ✅ `from_google()` - parse Google Calendar events
- ✅ `to_graph()` - convert to Graph API format
- ✅ `to_google()` - convert to Google Calendar format
- ❌ `to_caldav()` / `to_ical()` - **MISSING** - convert to CalDAV/iCalendar format

## Solution

Need to either:

### Option 1: Add `to_caldav()` method to Event class
Add a new method in `python/model/event.py`:
```python
def to_caldav(self) -> Dict[str, Any]:
    """Convert to CalDAV/iCalendar format (simple dict)."""
    event_data = {
        'subject': self.subject,
        'start': self.start.isoformat(),
        'end': self.end.isoformat(),
    }

    if self.location:
        event_data['location'] = self.location
    if self.description:
        event_data['body'] = self.description

    return event_data
```

Then update `diff_applier.py` to use it:
```python
def _to_provider_payload(self, event, connector) -> dict:
    """Convert Event to the payload format expected by the connector."""
    try:
        from ...connectors.graph_connector.connector import GraphConnector
        from ...connectors.google_connector.connector import GoogleConnector
        from ...connectors.icloud_connector.connector import ICloudConnector

        if isinstance(connector, GraphConnector):
            return event.to_graph()
        if isinstance(connector, GoogleConnector):
            return event.to_google()
        if isinstance(connector, ICloudConnector):
            return event.to_caldav()  # ✅ Use correct format
    except Exception:
        pass

    # Default to Graph format
    return event.to_graph()
```

### Option 2: Fix `event_to_ical()` to accept Graph format
Modify `ical_builder.py` to handle both simple strings and nested Graph API format.

**Recommendation**: Option 1 is cleaner and follows the existing pattern.

## Files Involved

- `python/sync/syncer/diff_applier.py` - Line 81-96 (`_to_provider_payload()`)
- `python/model/event.py` - Missing `to_caldav()` method
- `python/connectors/icloud_connector/helpers/ical_builder.py` - Lines 28-49 (expects simple format)
- `python/connectors/icloud_connector/event_operations.py` - Lines 19-25 (calls `build_ical_event()`)

## Why Errors Are Hidden

The bug is particularly insidious because of silent error handling:

1. **In `diff_applier.py` lines 77-78 and 62-78**: Exception handling catches and suppresses errors:
   ```python
   try:
       connector.delete_event(calendar_id, target_id)
       # ...
   except Exception:
       pass  # Event may already be deleted
   ```

2. **In `diff_applier.py` lines 92-93**: The try-except in `_to_provider_payload()` catches import errors but also suppresses any conversion errors.

3. This means when `event_to_ical()` fails due to the format mismatch, the error is likely caught somewhere in the call stack and the event either:
   - Creates with empty/default values (resulting in "No title")
   - Fails silently and doesn't create at all

## Testing Verification

To verify this is the issue, check:
1. Does the issue only occur when target is iCloud/CalDAV?
2. Does it work correctly when target is Graph API or Google Calendar?
3. Add debug logging in `event_to_ical()` to see what data it receives
4. Check if `start` and `end` fields are dictionaries instead of strings

## Impact

- ❌ Cannot sync events to iCloud/CalDAV target calendars
- ❌ Events show as "No title" on target
- ✅ Syncing to Graph API or Google Calendar targets works correctly
- ✅ Reading from iCloud/CalDAV sources works correctly
