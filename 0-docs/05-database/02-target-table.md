# Target Table - Calendar Consolidator MCP

## Purpose
Store configuration for target (destination) calendar

## Schema

```sql
CREATE TABLE target (
  id INTEGER PRIMARY KEY CHECK (id = 1),  -- Only one target allowed
  type TEXT NOT NULL CHECK (type IN ('graph', 'caldav')),
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB NOT NULL,  -- Encrypted credentials
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Fields

### id
- **Type**: INTEGER
- **Constraint**: CHECK (id = 1)
- **Purpose**: Only allow single target row
- **Usage**: Always use id=1

### type
- **Type**: TEXT
- **Constraint**: Must be 'graph' or 'caldav'
- **Purpose**: Calendar provider type

### calendar_id
- **Type**: TEXT
- **Purpose**: Provider-specific calendar identifier
- **Example**: Target calendar ID or URL

### name
- **Type**: TEXT (nullable)
- **Purpose**: User-friendly name for target
- **Example**: "Consolidated Calendar"

### cred_blob
- **Type**: BLOB
- **Purpose**: Encrypted credential JSON
- **Content**: Access tokens for write access

### created_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track when target was set

### updated_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track last modification

## Single Target Enforcement

The `CHECK (id = 1)` constraint ensures only one target exists.

### Set Target (Insert or Replace)
```sql
INSERT OR REPLACE INTO target (id, type, calendar_id, name, cred_blob)
VALUES (1, 'graph', 'target-123', 'Consolidated', ?);
```

### Query Target
```sql
SELECT * FROM target WHERE id = 1;
```

### Check if Target Exists
```sql
SELECT COUNT(*) FROM target WHERE id = 1;
```

## Notes

- Only one target calendar allowed per installation
- Changing target requires clearing or migrating mappings
- Target must have write permissions
