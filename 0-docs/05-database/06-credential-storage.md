# Credential Storage - Calendar Consolidator MCP

## Purpose
Securely store OAuth tokens and calendar credentials

## Single-User Simplified Approach

For single-user desktop tool, two options:

## Option 1: OS Keychain (Recommended)

### Advantages
- Uses native OS security
- Well-tested and audited
- User-transparent
- No custom encryption code

### Implementation
Use `keyring` Python library:

```python
import keyring
import json

def store_credentials(source_id: int, creds: dict):
    cred_json = json.dumps(creds)
    keyring.set_password(
        "calendar-consolidator",
        f"source-{source_id}",
        cred_json
    )

def load_credentials(source_id: int) -> dict:
    cred_json = keyring.get_password(
        "calendar-consolidator",
        f"source-{source_id}"
    )
    return json.loads(cred_json) if cred_json else None
```

### Platform Support
- **macOS**: Keychain Access
- **Windows**: Credential Manager
- **Linux**: Secret Service API (libsecret)

## Option 2: Local Encryption

### When to Use
- OS keychain not available
- Need portable database file
- Simpler deployment

### Implementation
```python
from cryptography.fernet import Fernet
import json
import base64

def get_encryption_key():
    # Derive from machine ID + salt
    import uuid
    machine_id = str(uuid.getnode())
    # Use proper key derivation (PBKDF2)
    # This is simplified example
    return base64.urlsafe_b64encode(
        hashlib.sha256(machine_id.encode()).digest()
    )

def encrypt_credentials(creds: dict) -> bytes:
    key = get_encryption_key()
    f = Fernet(key)
    cred_json = json.dumps(creds)
    return f.encrypt(cred_json.encode())

def decrypt_credentials(cred_blob: bytes) -> dict:
    key = get_encryption_key()
    f = Fernet(key)
    cred_json = f.decrypt(cred_blob).decode()
    return json.loads(cred_json)
```

### Storage in Database
```sql
-- Store as BLOB
INSERT INTO sources (..., cred_blob) VALUES (..., ?);
```

## Credential Structure

### Microsoft Graph
```json
{
  "type": "graph",
  "access_token": "eyJ0eXAiOiJKV1QiLCJub...",
  "refresh_token": "0.AXEAn...",
  "expires_at": "2024-01-01T13:00:00Z",
  "tenant_id": "common"
}
```

### CalDAV
```json
{
  "type": "caldav",
  "username": "user@example.com",
  "password": "app-specific-password",
  "server_url": "https://caldav.icloud.com/"
}
```

## MVP Recommendation

Start with **OS Keychain** (Option 1):
- More secure
- Simpler code
- Better user experience
- Single dependency: `keyring`

Use Option 2 only if OS keychain unavailable.
