# Mappings Table - Calendar Consolidator MCP

## Purpose
Track which source events are synced to which target events

## Schema

```sql
CREATE TABLE mappings (
  source_id INTEGER NOT NULL,
  source_event_uid TEXT NOT NULL,
  target_event_id TEXT NOT NULL,
  last_hash TEXT,           -- For change detection
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(source_id, source_event_uid),
  FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
);
```

## Fields

### source_id
- **Type**: INTEGER
- **Purpose**: Reference to sources table
- **Constraint**: Foreign key with CASCADE delete

### source_event_uid
- **Type**: TEXT
- **Purpose**: Unique event ID from source calendar
- **Example**: Graph event ID or iCalendar UID

### target_event_id
- **Type**: TEXT
- **Purpose**: Event ID in target calendar
- **Usage**: Used to update/delete target event

### last_hash
- **Type**: TEXT (nullable)
- **Purpose**: Hash of event content for change detection
- **Usage**: Detect if event changed since last sync

### created_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track when mapping created

### updated_at
- **Type**: DATETIME
- **Default**: CURRENT_TIMESTAMP
- **Purpose**: Track last sync/update

## Primary Key
Composite key on `(source_id, source_event_uid)` ensures:
- One mapping per source event
- Different sources can have same UID

## Foreign Key
```sql
FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
```
- Deleting source automatically removes its mappings

## Indexes

```sql
CREATE INDEX idx_mappings_source ON mappings(source_id);
CREATE INDEX idx_mappings_target ON mappings(target_event_id);
```

## Usage Examples

### Create Mapping
```sql
INSERT INTO mappings (source_id, source_event_uid, target_event_id, last_hash)
VALUES (1, 'source-event-123', 'target-event-456', 'hash123');
```

### Find Mapping
```sql
SELECT * FROM mappings
WHERE source_id = ? AND source_event_uid = ?;
```

### Update Hash
```sql
UPDATE mappings
SET last_hash = ?, updated_at = CURRENT_TIMESTAMP
WHERE source_id = ? AND source_event_uid = ?;
```

### Delete Mapping
```sql
DELETE FROM mappings
WHERE source_id = ? AND source_event_uid = ?;
```

### Get All Mappings for Source
```sql
SELECT * FROM mappings WHERE source_id = ?;
```
