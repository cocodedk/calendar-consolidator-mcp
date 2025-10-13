# OAuth Credentials UI Implementation Plan

## Overview
Add UI capability to configure OAuth credentials for calendar providers.

## Documentation Created
1. `03-implementation/16-step16-oauth-credentials-ui.md` - Implementation steps
2. `04-api-design/07-credentials-endpoints.md` - API specifications
3. `05-database/07-credentials-encryption.md` - Security implementation

## Modular Structure (All files <100 lines)

### Backend - Python
```
python/state/
├── credentials_manager.py      # CRUD operations
└── encryption.py               # AES-256-GCM encryption
```

### Backend - Node.js
```
node/server/admin_api/credentials/
├── get.js                      # GET /api/credentials
├── update.js                   # PUT /api/credentials
└── validate.js                 # Input validation
```

### Frontend
```
node/static/app/settings/
├── credentials_section.js      # Main credentials UI
├── google_credentials.js       # Google form
├── microsoft_credentials.js    # Microsoft form
├── icloud_credentials.js       # iCloud form (info only)
└── credentials_api.js          # API client
```

## Implementation Phases

### Phase 1: Backend Storage (2 hours)
- Encryption key generation
- Credentials manager with encrypt/decrypt
- Database integration

### Phase 2: Admin API (2 hours)
- GET endpoint (masked values)
- PUT endpoint (encrypted storage)
- Validation middleware

### Phase 3: Frontend UI (3 hours)
- Provider-specific credential forms
- Save/cancel functionality
- Success/error notifications

### Phase 4: Integration (1 hour)
- Connect to existing settings tab
- Test full flow
- Verify connector integration

## Security Features
- AES-256-GCM encryption at rest
- Masked credentials in GET responses
- Format validation before save
- Encryption key in gitignored file
- No credential logging

## Time Estimate
8 hours total

## Success Criteria
- Users can enter OAuth credentials via UI
- Credentials encrypted in database
- Connectors use stored credentials
- All files under 100 lines
