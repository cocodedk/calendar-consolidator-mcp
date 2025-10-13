# HTTP Configuration Endpoints - Calendar Consolidator MCP

## Purpose
REST API endpoints for web UI configuration

## Configuration Endpoints

### GET /api/config
**Description**: Get all sources, target, and status

**Response**:
```json
{
  "sources": [
    {
      "id": 1,
      "type": "graph",
      "calendarId": "calendar-123",
      "name": "Work Calendar",
      "active": true,
      "lastSync": "2024-01-01T12:00:00Z"
    }
  ],
  "target": {
    "id": 1,
    "type": "graph",
    "calendarId": "target-456",
    "name": "Consolidated Calendar"
  },
  "settings": {
    "continuousSyncEnabled": false,
    "syncIntervalMinutes": 5
  }
}
```

### POST /api/source
**Description**: Add new source calendar

**Request Body**:
```json
{
  "type": "graph",
  "calendarId": "calendar-123",
  "name": "Work Calendar",
  "credentials": {...}
}
```

**Response**:
```json
{
  "success": true,
  "sourceId": 1
}
```

### DELETE /api/source/:id
**Description**: Remove source calendar

**Parameters**:
- `id`: Source ID

**Response**:
```json
{
  "success": true
}
```

### POST /api/target
**Description**: Set/change target calendar

**Request Body**:
```json
{
  "type": "graph",
  "calendarId": "target-456",
  "name": "Consolidated Calendar",
  "credentials": {...}
}
```

**Response**:
```json
{
  "success": true
}
```

### POST /api/settings
**Description**: Update global settings

**Request Body**:
```json
{
  "continuousSyncEnabled": true,
  "syncIntervalMinutes": 5,
  "ignorePrivateEvents": false
}
```

**Response**:
```json
{
  "success": true
}
```
