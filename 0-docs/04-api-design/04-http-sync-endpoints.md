# HTTP Sync Endpoints - Calendar Consolidator MCP

## Purpose
REST API endpoints for sync operations

## Sync Operation Endpoints

### POST /api/preview
**Description**: Preview sync changes (dry run)

**Request Body**:
```json
{
  "sources": [1, 2],
  "target": 1
}
```

**Response**:
```json
{
  "wouldCreate": 5,
  "wouldUpdate": 3,
  "wouldDelete": 1,
  "sampleEvents": [
    {
      "action": "create",
      "title": "Team Meeting",
      "start": "2024-01-01T10:00:00Z"
    },
    ...
  ]
}
```

### POST /api/sync
**Description**: Execute sync operation

**Request Body**:
```json
{
  "sources": [1, 2],
  "target": 1
}
```

**Response**:
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

### GET /api/logs
**Description**: Get recent sync logs

**Query Parameters**:
- `limit`: Number of logs to return (default: 50)
- `sourceId`: Filter by source ID (optional)
- `since`: ISO timestamp for filtering (optional)

**Response**:
```json
{
  "logs": [
    {
      "id": 123,
      "sourceId": 1,
      "timestamp": "2024-01-01T12:00:00Z",
      "status": "success",
      "createdCount": 5,
      "updatedCount": 3,
      "deletedCount": 1,
      "errorMessage": null,
      "durationMs": 2340
    },
    ...
  ]
}
```

### GET /api/status
**Description**: Get system status

**Response**:
```json
{
  "activeSources": 2,
  "lastSync": "2024-01-01T12:00:00Z",
  "nextScheduledSync": "2024-01-01T12:05:00Z",
  "continuousSyncEnabled": false,
  "recentErrors": 0,
  "databaseSize": "1.2 MB",
  "pythonWorkerHealthy": true
}
```
