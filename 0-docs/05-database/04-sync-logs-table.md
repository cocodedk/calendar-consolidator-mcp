# Sync Logs Table - Calendar Consolidator MCP

## Purpose
Record history of sync operations for monitoring and debugging

## Schema

```sql
CREATE TABLE sync_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER,
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status TEXT NOT NULL CHECK (status IN ('success', 'error', 'partial')),
  created_count INTEGER DEFAULT 0,
  updated_count INTEGER DEFAULT 0,
  deleted_count INTEGER DEFAULT 0,
  error_message TEXT,
  duration_ms INTEGER,
  FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE SET NULL
);
```

## Fields

### id
- **Type**: INTEGER
- **Purpose**: Primary key, auto-incrementing
- **Usage**: Unique log entry identifier

### source_id
- **Type**: INTEGER (nullable)
- **Purpose**: Which source was synced
- **Constraint**: Foreign key, SET NULL on delete

### timestamp
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: When sync operation occurred

### status
- **Type**: TEXT
- **Constraint**: 'success', 'error', or 'partial'
- **Purpose**: Sync operation outcome

### created_count
- **Type**: INTEGER
- **Default**: 0
- **Purpose**: Number of events created

### updated_count
- **Type**: INTEGER
- **Default**: 0
- **Purpose**: Number of events updated

### deleted_count
- **Type**: INTEGER
- **Default**: 0
- **Purpose**: Number of events deleted

### error_message
- **Type**: TEXT (nullable)
- **Purpose**: Error details if status is 'error'

### duration_ms
- **Type**: INTEGER (nullable)
- **Purpose**: Sync duration in milliseconds

## Indexes

```sql
CREATE INDEX idx_sync_logs_timestamp ON sync_logs(timestamp);
CREATE INDEX idx_sync_logs_source ON sync_logs(source_id);
```

## Usage Examples

### Insert Log
```sql
INSERT INTO sync_logs
(source_id, status, created_count, updated_count, deleted_count, duration_ms)
VALUES (1, 'success', 5, 3, 1, 2340);
```

### Query Recent Logs
```sql
SELECT * FROM sync_logs
ORDER BY timestamp DESC
LIMIT 50;
```

### Query Logs for Source
```sql
SELECT * FROM sync_logs
WHERE source_id = ?
ORDER BY timestamp DESC;
```

### Query Recent Errors
```sql
SELECT * FROM sync_logs
WHERE status = 'error'
ORDER BY timestamp DESC
LIMIT 10;
```

### Get Statistics
```sql
SELECT
  status,
  COUNT(*) as count,
  SUM(created_count) as total_created,
  SUM(updated_count) as total_updated
FROM sync_logs
WHERE timestamp > datetime('now', '-7 days')
GROUP BY status;
```
