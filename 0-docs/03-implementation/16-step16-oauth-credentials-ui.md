# Step 16: OAuth Credentials UI

## Goal
Add UI capability to configure OAuth credentials for Google, Microsoft, and iCloud.

## Architecture

### Frontend (Settings Tab)
```
node/static/app/settings/
├── credentials_section.js      # OAuth credentials form section
├── google_credentials.js       # Google-specific fields
├── microsoft_credentials.js    # Microsoft-specific fields
├── icloud_credentials.js       # iCloud-specific fields
└── credentials_api.js          # API calls for credentials
```

### Backend (Admin API)
```
node/server/admin_api/credentials/
├── get.js                      # GET credentials (masked)
├── update.js                   # PUT credentials (encrypted)
└── validate.js                 # Validation logic
```

### Python Layer
```
python/state/
├── credentials_manager.py      # Load/save credentials
└── encryption.py               # Encrypt/decrypt secrets
```

## Tasks

### Phase 1: Backend Storage (2 hours)
- [ ] Create `python/state/credentials_manager.py`
- [ ] Create `python/state/encryption.py`
- [ ] Add encryption key generation
- [ ] Implement save/load with encryption
- [ ] Add credential validation

### Phase 2: Admin API (2 hours)
- [ ] Create `node/server/admin_api/credentials/` directory
- [ ] Implement GET endpoint (return masked values)
- [ ] Implement PUT endpoint (encrypt before save)
- [ ] Add validation middleware
- [ ] Add error handling

### Phase 3: Frontend UI (3 hours)
- [ ] Create `node/static/app/settings/` directory
- [ ] Build credentials section component
- [ ] Add Google credentials form
- [ ] Add Microsoft credentials form
- [ ] Add iCloud credentials form
- [ ] Add save/cancel buttons
- [ ] Integrate with settings tab

### Phase 4: Integration (1 hour)
- [ ] Update settings.js to use new modular structure
- [ ] Test credential save/load flow
- [ ] Test encryption/decryption
- [ ] Verify connectors use new credentials
- [ ] Add success/error notifications

## File Size Compliance
All files kept under 100 lines through modularization.

## Security Requirements
- Encrypt secrets at rest (AES-256)
- Mask credentials in GET responses
- Validate format before save
- Store encryption key separately
- Never log credentials

## Time Estimate
8 hours total
