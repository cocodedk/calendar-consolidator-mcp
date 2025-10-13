# OAuth Credentials Feature - Test Plan

Comprehensive test plan for OAuth credentials functionality.

## Test Categories

### Python Unit Tests (pytest)
- Encryption module tests
- Credentials manager tests
- Integration tests

### Node.js API Tests (Jest/Mocha)
- Validation logic tests
- API endpoint tests
- Error handling tests

### Playwright E2E Tests
- UI interaction tests
- Form submission tests
- Visual validation tests

## Test Files to Create (15 total)

### Python Tests (6 files)
```
tests/state/
├── test_encryption_key_generation.py      # Key creation
├── test_encryption_encrypt_decrypt.py     # Encryption flow
├── test_encryption_masking.py             # Secret masking
├── test_credentials_manager_save.py       # Save credentials
├── test_credentials_manager_load.py       # Load credentials
└── test_credentials_manager_masked.py     # Masked retrieval
```

### Node.js Tests (6 files)
```
tests/api/
├── test_credentials_validate_google.py    # Google validation
├── test_credentials_validate_microsoft.py # Microsoft validation
├── test_credentials_get_endpoint.py       # GET endpoint
├── test_credentials_put_endpoint.py       # PUT endpoint
├── test_credentials_error_handling.py     # Error cases
└── test_credentials_integration.py        # Full flow
```

### Playwright Tests (3 files)
```
tests-e2e/tests/
├── credentials-ui.spec.js                 # UI elements
├── credentials-forms.spec.js              # Form interaction
└── credentials-visual.spec.js             # Visual validation
```

## Test Coverage Goals

### Encryption Module (90%+)
- Key generation and storage
- Encrypt/decrypt roundtrip
- Error handling for invalid data
- Masking different secret formats

### Credentials Manager (90%+)
- CRUD operations
- Database integration
- Encryption integration
- Error handling

### API Validation (100%)
- Google format validation
- Microsoft format validation
- Error messages
- Edge cases

### API Endpoints (90%+)
- GET returns masked credentials
- PUT saves encrypted credentials
- Error responses (400, 500)
- Provider validation

### E2E UI (80%+)
- Settings tab navigation
- Form display
- Input validation
- Save/cancel buttons
- Success/error feedback

## Time Estimate
- Python tests: 4 hours
- Node.js tests: 3 hours
- Playwright tests: 3 hours
- **Total: 10 hours**
