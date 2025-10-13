# API Endpoint Test Plan

Tests for credentials API endpoints

## Test Files (4 files)

### test_credentials_get_endpoint.py
**Purpose**: Test GET /api/credentials

**Tests**:
1. `test_get_credentials_returns_all_providers` - Returns 3 providers
2. `test_get_credentials_masks_secrets` - Secrets are masked
3. `test_get_credentials_configured_status` - Shows config status
4. `test_get_credentials_not_configured` - Handles missing creds
5. `test_get_credentials_error_handling` - Returns 500 on error

**Mocks**: Python credentials_manager calls

### test_credentials_put_endpoint.py
**Purpose**: Test PUT /api/credentials

**Tests**:
1. `test_put_credentials_google_success` - Saves Google creds
2. `test_put_credentials_microsoft_success` - Saves Microsoft creds
3. `test_put_credentials_validates_format` - Calls validation
4. `test_put_credentials_encrypts_data` - Data is encrypted
5. `test_put_credentials_returns_success_message` - Proper response

**Mocks**: Validation, save_credentials

### test_credentials_error_handling.py
**Purpose**: Test error scenarios

**Tests**:
1. `test_put_invalid_provider_400` - Rejects unknown provider
2. `test_put_invalid_format_400` - Rejects bad format
3. `test_put_validation_error_message` - Returns validation error
4. `test_put_database_error_500` - Handles save failure
5. `test_get_python_error_500` - Handles Python errors

**Mocks**: All external dependencies

### test_credentials_integration.py
**Purpose**: Full flow integration test

**Tests**:
1. `test_full_flow_google` - Save and retrieve Google creds
2. `test_full_flow_microsoft` - Save and retrieve Microsoft creds
3. `test_update_existing_credentials` - Upsert behavior
4. `test_credentials_persist_across_requests` - State maintained

**Mocks**: Database only (test full API flow)

## Coverage Target: 90%+
