# Encryption Module Test Plan

Tests for `python/state/encryption.py`

## Test Files (3 files)

### test_encryption_key_generation.py
**Purpose**: Verify encryption key creation and loading

**Tests**:
1. `test_generate_encryption_key_format` - Key is valid Fernet key
2. `test_load_or_create_key_creates_new` - Creates key if none exists
3. `test_load_or_create_key_loads_existing` - Reuses existing key
4. `test_key_file_permissions` - Unix permissions set to 600

**Mocks**: File system operations, os.chmod

### test_encryption_encrypt_decrypt.py
**Purpose**: Verify encryption/decryption flow

**Tests**:
1. `test_encrypt_credentials_returns_string` - Output is base64 string
2. `test_decrypt_credentials_returns_dict` - Decrypts to original dict
3. `test_encrypt_decrypt_roundtrip` - Data integrity preserved
4. `test_decrypt_invalid_data_returns_none` - Handles corruption

**Mocks**: Fernet cipher

### test_encryption_masking.py
**Purpose**: Verify secret masking for display

**Tests**:
1. `test_mask_secret_short_string` - Returns *** for short strings
2. `test_mask_secret_long_string` - Shows prefix/suffix
3. `test_mask_secret_empty_string` - Handles empty input
4. `test_mask_secret_default_chars` - Uses 3 chars by default

**Mocks**: None (pure function)

## Fixtures Needed
- `temp_key_file` - Temporary encryption key file
- `sample_credentials` - Test credential dictionaries
- `mock_fernet` - Mocked Fernet cipher

## Coverage Target: 95%+
