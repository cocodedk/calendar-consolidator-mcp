# Security Model - Calendar Consolidator MCP

## Network Security

### Local-Only Binding
- HTTP API binds to `127.0.0.1` (localhost)
- No external network exposure
- Physical machine access required

### No Remote Access
- No cloud/remote connections by default
- User can explicitly enable if needed
- Document security implications clearly

## Authentication

### Single-User Model
- Physical machine access = authorized user
- No login screen required for MVP
- Optional password protection for Phase 5

### OAuth Credentials
- Microsoft: OAuth 2.0 with PKCE
- CalDAV: App-specific passwords
- Minimal scope requests (calendar only)

## Credential Storage

### Option 1: OS Keychain (Recommended)
- macOS: Keychain Access
- Windows: Credential Manager
- Linux: Secret Service API (libsecret)
- Python library: `keyring`

### Option 2: Database Encryption
- AES-256-GCM encryption
- Key derived from machine ID
- Random IV per credential
- Stored as BLOB in SQLite

### Token Refresh
- Refresh tokens stored securely
- Auto-refresh on expiration
- Re-auth prompt if refresh fails

## Data Protection

### Input Validation
- Sanitize all user inputs
- Validate calendar IDs
- Reject malformed data

### SQL Injection Prevention
- Parameterized queries only
- No string concatenation in SQL
- Use SQLite's built-in protection

### API Rate Limiting
- Respect provider rate limits
- Exponential backoff on errors
- Avoid hammering APIs

## Privacy

### Event Data
- Only calendar events synced
- No collection of analytics
- All data stays local

### Logging
- No sensitive tokens in logs
- Sanitize error messages
- Log only necessary information

## Future Considerations

### Phase 5 (Electron)
- Optional master password
- Encrypted database backups
- Secure auto-update channel
