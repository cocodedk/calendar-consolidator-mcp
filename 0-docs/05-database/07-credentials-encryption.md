# Credentials Encryption

## Storage Location
Settings table with encrypted JSON values.

## Encryption Method
AES-256-GCM with unique key per installation.

## Key Management
```
.encryption_key (gitignored)
- Generated on first run
- 256-bit random key
- Base64 encoded
```

## Database Schema
```sql
-- In settings table
INSERT INTO settings (key, value) VALUES
  ('google_credentials', '{"encrypted": true, "data": "..."}'),
  ('microsoft_credentials', '{"encrypted": true, "data": "..."}');
```

## Encryption Flow
1. User submits credentials via UI
2. Backend encrypts using installation key
3. Store encrypted blob in database
4. Return success to UI

## Decryption Flow
1. Connector requests credentials
2. credentials_manager loads from database
3. Decrypts using installation key
4. Returns plain credentials to connector

## Security Notes
- Key file must be in .gitignore
- Rotate key requires re-entering all credentials
- Backup key separately from database
- Use environment variable for production

## Implementation
```python
# python/state/encryption.py
from cryptography.fernet import Fernet

def encrypt_credentials(data: dict) -> str:
    key = load_encryption_key()
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_credentials(encrypted: str) -> dict:
    key = load_encryption_key()
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted))
```
