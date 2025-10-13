# Step 6: CalDAV Support (Phase 2)

## Goal
Add CalDAV connector for iCloud and other CalDAV calendars

## Tasks

### CalDAV Connector
- [ ] Create CalDAVConnector class
- [ ] Implement CalDAV authentication
- [ ] Handle different auth methods (basic, OAuth)
- [ ] Test connection to server

### Calendar Discovery
- [ ] Implement PROPFIND for calendar list
- [ ] Parse calendar properties
- [ ] Return normalized calendar info
- [ ] Test with iCloud account

### Event CRUD Operations
- [ ] Implement create_event() via PUT
- [ ] Implement update_event() via PUT
- [ ] Implement delete_event() via DELETE
- [ ] Implement get_event() via GET
- [ ] Test all operations

### Sync Support
- [ ] Implement CTag tracking for changes
- [ ] Implement ETag per-event tracking
- [ ] Implement REPORT query for events
- [ ] Handle time-range queries
- [ ] Parse iCalendar format (.ics)
- [ ] Test incremental sync

### Event Normalization
- [ ] Add CalDAV format to Event.from_caldav()
- [ ] Parse VEVENT components
- [ ] Handle VTIMEZONE
- [ ] Normalize to Event model
- [ ] Test conversion both ways

## Files to Create
- `python/connectors/caldav_connector.py`
- `python/model/icalendar_parser.py`

## Testing Checklist
- [ ] Can connect to iCloud CalDAV
- [ ] Can list calendars
- [ ] Can read events
- [ ] Can create events
- [ ] Can update events
- [ ] Can delete events
- [ ] CTag/ETag sync works
- [ ] Events normalize correctly
- [ ] Multi-source sync works (Graph + CalDAV)

## Dependencies
- `caldav` - CalDAV Python library
- `icalendar` - iCalendar format parsing

## Time Estimate
- 10-12 hours

## Notes
- CalDAV is more complex than Graph API
- No built-in delta sync like Graph
- Need to track CTags manually
- iCloud has specific quirks
