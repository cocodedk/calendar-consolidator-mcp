# Test File Structure

Directory structure for OAuth credentials tests.

## Python Tests

```
tests/
├── state/
│   ├── test_encryption_key_generation.py        # 4 tests
│   ├── test_encryption_encrypt_decrypt.py       # 4 tests
│   ├── test_encryption_masking.py               # 4 tests
│   ├── test_credentials_manager_save.py         # 4 tests
│   ├── test_credentials_manager_load.py         # 4 tests
│   └── test_credentials_manager_masked.py       # 4 tests
│
└── api/
    ├── test_credentials_validate_google.py      # 5 tests
    ├── test_credentials_validate_microsoft.py   # 6 tests
    ├── test_credentials_get_endpoint.py         # 5 tests
    ├── test_credentials_put_endpoint.py         # 5 tests
    ├── test_credentials_error_handling.py       # 5 tests
    └── test_credentials_integration.py          # 4 tests
```

## Playwright Tests

```
tests-e2e/
└── tests/
    ├── credentials-ui.spec.js                   # 7 tests
    ├── credentials-forms.spec.js                # 7 tests
    └── credentials-visual.spec.js               # 6 tests
```

## Total Test Count
- Python unit tests: 24 tests
- Python API tests: 30 tests
- Playwright E2E: 20 tests
- **Total: 74 tests**

## File Size
All test files designed to be under 100 lines.

## Naming Conventions
- Python: `test_<module>_<scenario>.py`
- Playwright: `<feature>-<aspect>.spec.js`

## Test Organization
Each file focuses on specific aspect of functionality:
- Single module or endpoint
- Related test scenarios
- Clear test names
- Comprehensive coverage
