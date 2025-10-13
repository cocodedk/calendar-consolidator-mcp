# Validation Logic Test Plan

Tests for `node/server/admin_api/credentials/validate.js`

## Test Files (2 files)

### test_credentials_validate_google.py
**Purpose**: Verify Google credentials validation

**Tests**:
1. `test_validate_google_valid_credentials` - Accepts valid format
2. `test_validate_google_invalid_client_id` - Rejects bad client_id
3. `test_validate_google_invalid_client_secret` - Rejects bad secret
4. `test_validate_google_missing_fields` - Rejects incomplete data
5. `test_validate_google_error_messages` - Descriptive errors

**Mocks**: None (unit tests of validation logic)

### test_credentials_validate_microsoft.py
**Purpose**: Verify Microsoft credentials validation

**Tests**:
1. `test_validate_microsoft_valid_credentials` - Accepts valid GUIDs
2. `test_validate_microsoft_common_tenant` - Accepts "common"
3. `test_validate_microsoft_invalid_client_id` - Rejects bad GUID
4. `test_validate_microsoft_invalid_tenant_id` - Rejects bad tenant
5. `test_validate_microsoft_short_secret` - Rejects short secret
6. `test_validate_microsoft_missing_fields` - Rejects incomplete

**Mocks**: None (unit tests)

## Test Data
- Valid Google credentials
- Invalid Google credentials (various)
- Valid Microsoft credentials
- Invalid Microsoft credentials (various)
- Edge cases (empty, null, special chars)

## Coverage Target: 100%
