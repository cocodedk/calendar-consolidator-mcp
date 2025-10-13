# Python Worker Component - Calendar Consolidator MCP

## Purpose
Sync engine and calendar API connectors

## Responsibilities

### Calendar Connectors
- Implement Microsoft Graph client
- Implement CalDAV client
- Handle OAuth token refresh
- Abstract provider differences

### Sync Logic
- Fetch changed events from sources
- Compute diff against target
- Execute create/update/delete
- Update mappings and tokens

### Event Model
- Normalize events across providers
- Handle timezone conversions
- Process recurrence rules
- Manage exceptions

### Config Store
- Read/write database
- Encrypt/decrypt credentials
- Manage sync tokens
- Log operations

## Technology

### Core Libraries
- `msal` - Microsoft auth
- `msgraph-core` - Graph API
- `caldav` - CalDAV protocol
- `keyring` - OS keychain

### Database
- `sqlite3` - Built-in SQLite support
- Direct SQL queries
- Transaction management

## Key Modules

### `/python/connectors/graph_connector.py`
- OAuth flow implementation
- Calendar listing
- Event CRUD operations
- Delta sync with tokens

### `/python/connectors/caldav_connector.py`
- CalDAV authentication
- Calendar discovery
- Event CRUD via CalDAV
- CTag/ETag tracking

### `/python/model/event.py`
- Event class definition
- Normalization logic
- Hash computation
- Timezone handling

### `/python/model/diff.py`
- Diff computation
- Create/update/delete detection
- Recurrence handling

### `/python/state/config_store.py`
- Database operations
- CRUD for sources/target
- Mapping management
- Log recording

### `/python/sync/syncer.py`
- Main sync algorithm
- Orchestrates connectors
- Updates database
- Error handling

### `/python/sync/dry_run_syncer.py`
- Preview mode
- No actual writes
- Returns diff summary
