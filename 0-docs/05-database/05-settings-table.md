# Settings Table - Calendar Consolidator MCP

## Purpose
Store global configuration settings

## Schema

```sql
CREATE TABLE settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Fields

### key
- **Type**: TEXT
- **Purpose**: Setting name (primary key)
- **Example**: 'continuous_sync_enabled'

### value
- **Type**: TEXT
- **Purpose**: Setting value (stored as string)
- **Note**: Parse to appropriate type in application

### updated_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track last modification

## Default Settings

```sql
INSERT INTO settings (key, value) VALUES
  ('continuous_sync_enabled', 'false'),
  ('sync_interval_minutes', '5'),
  ('ignore_private_events', 'false'),
  ('max_retry_attempts', '3'),
  ('encryption_key_id', 'default');
```

## Setting Definitions

### continuous_sync_enabled
- **Type**: boolean ('true'/'false')
- **Purpose**: Enable automatic periodic sync
- **Default**: 'false'

### sync_interval_minutes
- **Type**: integer
- **Purpose**: Minutes between automatic syncs
- **Default**: '5'
- **Range**: 1-60

### ignore_private_events
- **Type**: boolean
- **Purpose**: Skip private/confidential events
- **Default**: 'false'

### max_retry_attempts
- **Type**: integer
- **Purpose**: Max retries on transient errors
- **Default**: '3'
- **Range**: 0-10

### encryption_key_id
- **Type**: string
- **Purpose**: Identifier for encryption key
- **Default**: 'default'
- **Note**: For single-user, can be simplified

## Usage Examples

### Get Setting
```sql
SELECT value FROM settings WHERE key = ?;
```

### Set Setting
```sql
INSERT OR REPLACE INTO settings (key, value, updated_at)
VALUES (?, ?, CURRENT_TIMESTAMP);
```

### Get All Settings
```sql
SELECT key, value FROM settings;
```

### Delete Setting (Reset to Default)
```sql
DELETE FROM settings WHERE key = ?;
-- Then re-insert default value
```

## Python Helper

```python
def get_setting(key: str, default=None):
    result = db.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = result.fetchone()
    return row[0] if row else default

def set_setting(key: str, value: str):
    db.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (key, value)
    )
```
