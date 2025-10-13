# Sources Table - Calendar Consolidator MCP

## Purpose
Store configuration for source calendars

## Schema

```sql
CREATE TABLE sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL CHECK (type IN ('graph', 'caldav')),
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB NOT NULL,  -- Encrypted credentials
  sync_token TEXT,          -- For delta sync
  active BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Fields

### id
- **Type**: INTEGER
- **Purpose**: Primary key, auto-incrementing
- **Usage**: Unique identifier for each source

### type
- **Type**: TEXT
- **Constraint**: Must be 'graph' or 'caldav'
- **Purpose**: Calendar provider type

### calendar_id
- **Type**: TEXT
- **Purpose**: Provider-specific calendar identifier
- **Example**: Microsoft Graph calendar ID or CalDAV URL

### name
- **Type**: TEXT (nullable)
- **Purpose**: User-friendly name/alias for the source
- **Example**: "Work Calendar", "Personal"

### cred_blob
- **Type**: BLOB
- **Purpose**: Encrypted credential JSON
- **Content**: Access tokens, refresh tokens, etc.

### sync_token
- **Type**: TEXT (nullable)
- **Purpose**: Delta sync token from provider
- **Usage**: Track last sync position for incremental updates

### active
- **Type**: BOOLEAN
- **Default**: 1 (true)
- **Purpose**: Enable/disable source without deleting

### created_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track when source was added

### updated_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track last modification

## Indexes

```sql
CREATE INDEX idx_sources_type ON sources(type);
CREATE INDEX idx_sources_active ON sources(active);
```

## Usage Examples

### Insert Source
```sql
INSERT INTO sources (type, calendar_id, name, cred_blob, active)
VALUES ('graph', 'calendar-123', 'Work Calendar', ?, 1);
```

### Query Active Sources
```sql
SELECT * FROM sources WHERE active = 1;
```

### Update Sync Token
```sql
UPDATE sources
SET sync_token = ?, updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
```
