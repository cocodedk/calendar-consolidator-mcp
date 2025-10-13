# Error Handling - Calendar Consolidator MCP

## HTTP Status Codes

### Success Codes
- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully

### Client Error Codes
- `400 Bad Request` - Invalid parameters or malformed request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., target already set)
- `422 Unprocessable Entity` - Validation failed

### Server Error Codes
- `500 Internal Server Error` - Unexpected server error
- `503 Service Unavailable` - Service temporarily unavailable

## Error Response Format

### Standard Error Response
```typescript
interface ErrorResponse {
  error: string;        // Human-readable message
  code: string;         // Machine-readable error code
  details?: any;        // Additional context
}
```

### Example Responses

**Invalid Parameters**:
```json
{
  "error": "Missing required field: calendarId",
  "code": "INVALID_PARAMETERS",
  "details": {
    "field": "calendarId",
    "expected": "string"
  }
}
```

**Authentication Failed**:
```json
{
  "error": "OAuth token expired",
  "code": "AUTH_EXPIRED",
  "details": {
    "sourceId": 1,
    "expiresAt": "2024-01-01T12:00:00Z"
  }
}
```

**Sync Failed**:
```json
{
  "error": "Failed to sync calendar",
  "code": "SYNC_FAILED",
  "details": {
    "sourceId": 1,
    "reason": "Rate limit exceeded"
  }
}
```

## Error Codes

### Configuration Errors
- `INVALID_PARAMETERS` - Missing or invalid parameters
- `SOURCE_NOT_FOUND` - Source calendar not found
- `TARGET_NOT_SET` - Target calendar not configured
- `DUPLICATE_SOURCE` - Source already exists

### Authentication Errors
- `AUTH_FAILED` - Authentication failed
- `AUTH_EXPIRED` - Token expired
- `AUTH_INVALID` - Invalid credentials
- `AUTH_REQUIRED` - Re-authentication required

### Sync Errors
- `SYNC_FAILED` - Sync operation failed
- `SYNC_PARTIAL` - Some events failed to sync
- `SYNC_IN_PROGRESS` - Sync already running
- `RATE_LIMIT_EXCEEDED` - API rate limit hit

### System Errors
- `DATABASE_ERROR` - Database operation failed
- `PYTHON_WORKER_ERROR` - Python worker crashed
- `NETWORK_ERROR` - Network request failed
- `INTERNAL_ERROR` - Unexpected error

## Rate Limiting Headers

### Response Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

### Rate Limit Exceeded Response
```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "details": {
    "limit": 100,
    "resetAt": "2024-01-01T13:00:00Z"
  }
}
```
