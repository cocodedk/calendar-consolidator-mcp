# Credentials API Endpoints

## GET /api/credentials
Get OAuth credentials (masked).

### Response
```json
{
  "google": {
    "client_id": "123456...googleusercontent.com",
    "client_secret": "GOC***...***xyz",
    "configured": true
  },
  "microsoft": {
    "client_id": "abc123...456",
    "client_secret": "MSC***...***xyz",
    "tenant_id": "tenant...789",
    "configured": true
  },
  "icloud": {
    "configured": false
  }
}
```

## PUT /api/credentials
Update OAuth credentials.

### Request
```json
{
  "provider": "google",
  "credentials": {
    "client_id": "123456.apps.googleusercontent.com",
    "client_secret": "GOCSPX-..."
  }
}
```

### Response
```json
{
  "success": true,
  "message": "Credentials updated successfully"
}
```

## Validation Rules

### Google
- `client_id`: Must end with `.apps.googleusercontent.com`
- `client_secret`: Must start with `GOCSPX-`

### Microsoft
- `client_id`: GUID format
- `tenant_id`: GUID format or "common"
- `client_secret`: Non-empty string

### iCloud
- No credentials needed (user-specific passwords)

## Error Codes
- 400: Invalid format
- 500: Encryption failed
