# MCP Configuration Tools - Calendar Consolidator MCP

## Purpose
MCP tools for managing calendar sources and target

## Configuration Management Tools

### addSource
```typescript
addSource(sourceConfig: SourceConfig) → Success
```
**Description**: Add new source calendar

**Parameters**:
- `sourceConfig`: Source calendar configuration

**Returns**: Success status

**Example Input**:
```json
{
  "type": "graph",
  "calendarId": "calendar-123",
  "name": "Work Calendar",
  "credentials": {...},
  "active": true
}
```

### removeSource
```typescript
removeSource(sourceId: string) → Success
```
**Description**: Remove source calendar

**Parameters**:
- `sourceId`: Source identifier

**Returns**: Success status

### setTarget
```typescript
setTarget(targetConfig: TargetConfig) → Success
```
**Description**: Set target calendar

**Parameters**:
- `targetConfig`: Target calendar configuration

**Returns**: Success status

**Example Input**:
```json
{
  "type": "graph",
  "calendarId": "target-calendar-456",
  "name": "Consolidated Calendar",
  "credentials": {...}
}
```

### setRules
```typescript
setRules(rules: RuleConfig) → Success
```
**Description**: Configure sync rules

**Parameters**:
- `rules`: Sync rule configuration

**Returns**: Success status

**Example Input**:
```json
{
  "ignorePrivateEvents": true,
  "timeWindowDays": 90,
  "maxRetryAttempts": 3
}
```

### getSyncStatus
```typescript
getSyncStatus() → StatusInfo
```
**Description**: Get current sync status

**Returns**: Status information

**Example Output**:
```json
{
  "lastSync": "2024-01-01T12:00:00Z",
  "nextSync": "2024-01-01T12:05:00Z",
  "activeSources": 2,
  "recentErrors": 0,
  "continuousSyncEnabled": false
}
```
