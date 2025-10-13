# Credentials Manager Test Plan

Tests for `python/state/credentials_manager.py`

## Test Files (3 files)

### test_credentials_manager_save.py
**Purpose**: Verify saving credentials to database

**Tests**:
1. `test_save_credentials_success` - Saves encrypted data
2. `test_save_credentials_upsert` - Updates existing credentials
3. `test_save_credentials_encryption_called` - Uses encryption
4. `test_save_credentials_database_error` - Handles DB errors

**Mocks**: Database connection, encryption

### test_credentials_manager_load.py
**Purpose**: Verify loading credentials from database

**Tests**:
1. `test_load_credentials_success` - Returns decrypted dict
2. `test_load_credentials_not_found` - Returns None if missing
3. `test_load_credentials_decryption_called` - Uses decryption
4. `test_load_credentials_database_error` - Handles DB errors

**Mocks**: Database connection, decryption

### test_credentials_manager_masked.py
**Purpose**: Verify masked credential retrieval

**Tests**:
1. `test_get_masked_credentials_masks_secrets` - Masks sensitive fields
2. `test_get_masked_credentials_preserves_ids` - IDs not masked
3. `test_get_masked_credentials_not_found` - Returns None
4. `test_delete_credentials_success` - Removes from database

**Mocks**: Database connection, load_credentials

## Fixtures Needed
- `mock_db_connection` - Mocked SQLite connection
- `mock_cursor` - Mocked database cursor
- `sample_google_creds` - Google credentials dict
- `sample_microsoft_creds` - Microsoft credentials dict

## Coverage Target: 90%+
