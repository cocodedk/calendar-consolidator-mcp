# Technology Stack - Calendar Consolidator MCP

## Backend

### Python (Sync Engine)
- **Version**: Python 3.10+
- **Purpose**: Calendar sync logic and connectors
- **Key Libraries**:
  - `msal` - Microsoft authentication
  - `msgraph-core` - Microsoft Graph API
  - `caldav` - CalDAV protocol
  - `cryptography` - Credential encryption
  - `keyring` - OS keychain integration

### Node.js (MCP Server)
- **Version**: Node 18+
- **Purpose**: MCP server and HTTP API
- **Key Libraries**:
  - MCP SDK - Tool definitions
  - Express - HTTP server (or similar)
  - Child process - Python worker bridge

## Database

### SQLite
- **Version**: SQLite 3
- **Location**: `~/.calendar-consolidator/config.db`
- **Features Used**:
  - Foreign keys for referential integrity
  - Indexes for performance
  - Transactions for consistency
  - WAL mode for concurrency

## Frontend

### Web UI
- **Technology**: Vanilla JS or React (TBD)
- **Hosting**: Static files served by Node server
- **Target**: Modern browsers only
- **No Build Step**: Keep it simple for MVP

## External APIs

### Microsoft Graph API
- OAuth 2.0 authentication
- Calendar delta sync
- Event CRUD operations

### CalDAV Protocol
- HTTP-based calendar access
- CalDAV REPORT queries
- iCloud compatibility
