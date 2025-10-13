# MCP Tools - Calendar Consolidator MCP

## Purpose
MCP tools expose calendar sync functionality to AI/agents

## Calendar Management Tools

### listCalendars
```typescript
listCalendars(sourceType: "graph" | "caldav") → CalendarInfo[]
```
**Description**: List available calendars for a source type

**Parameters**:
- `sourceType`: Type of calendar provider

**Returns**: Array of calendar information objects

**Example**:
```json
[
  {
    "id": "calendar-id-123",
    "name": "Work Calendar",
    "type": "graph",
    "canWrite": true
  }
]
```

### getEvent
```typescript
getEvent(target: TargetRef, eventId: string) → EventDetail
```
**Description**: Get specific event details from target calendar

**Parameters**:
- `target`: Target calendar reference
- `eventId`: Event identifier

**Returns**: Detailed event object

## Sync Operation Tools

### previewSync
```typescript
previewSync(sources: SourceRef[], target: TargetRef) → DiffSummary
```
**Description**: Preview sync without making changes (dry run)

**Parameters**:
- `sources`: Array of source calendar references
- `target`: Target calendar reference

**Returns**: Summary of pending changes

**Example**:
```json
{
  "wouldCreate": 5,
  "wouldUpdate": 3,
  "wouldDelete": 1,
  "sampleEvents": [...]
}
```

### syncOnce
```typescript
syncOnce(sources: SourceRef[], target: TargetRef) → SyncResult
```
**Description**: Execute actual sync operation

**Parameters**:
- `sources`: Array of source calendar references
- `target`: Target calendar reference

**Returns**: Sync operation results

**Example**:
```json
{
  "success": true,
  "created": 5,
  "updated": 3,
  "deleted": 1,
  "errors": [],
  "duration": 2340
}
```
