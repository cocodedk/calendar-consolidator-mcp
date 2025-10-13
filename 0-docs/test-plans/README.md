# OAuth Credentials Test Plans

Detailed test plans for OAuth credentials feature.

## Overview
Comprehensive testing strategy covering unit, integration, and E2E tests.

## Test Categories

### Python Unit Tests (6 files)
- **Encryption**: Key generation, encrypt/decrypt, masking
- **Credentials Manager**: Save, load, masked retrieval

### Node.js API Tests (6 files)
- **Validation**: Google and Microsoft format validation
- **Endpoints**: GET and PUT operations
- **Integration**: Full API flow

### Playwright E2E Tests (3 files)
- **UI Elements**: Navigation and visibility
- **Form Interaction**: Input and submission
- **Visual**: Styling and theming

## Test Files: 15 total

### Python (6)
1. `test_encryption_key_generation.py`
2. `test_encryption_encrypt_decrypt.py`
3. `test_encryption_masking.py`
4. `test_credentials_manager_save.py`
5. `test_credentials_manager_load.py`
6. `test_credentials_manager_masked.py`

### Node.js/Python API (6)
7. `test_credentials_validate_google.py`
8. `test_credentials_validate_microsoft.py`
9. `test_credentials_get_endpoint.py`
10. `test_credentials_put_endpoint.py`
11. `test_credentials_error_handling.py`
12. `test_credentials_integration.py`

### Playwright (3)
13. `credentials-ui.spec.js`
14. `credentials-forms.spec.js`
15. `credentials-visual.spec.js`

## Coverage Goals
- Python: 90%+
- Node.js: 90%+
- E2E: 80%+

## Time Estimate
10 hours total

## Documentation
- [Main Test Plan](../OAUTH_CREDENTIALS_TEST_PLAN.md)
- [Encryption Tests](./encryption-tests.md)
- [Credentials Manager Tests](./credentials-manager-tests.md)
- [Validation Tests](./validation-tests.md)
- [API Endpoint Tests](./api-endpoint-tests.md)
- [Playwright E2E Tests](./playwright-e2e-tests.md)
