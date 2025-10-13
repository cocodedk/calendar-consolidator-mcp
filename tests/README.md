# Calendar Consolidator MCP Tests

This directory contains comprehensive pytest-based tests for the Calendar Consolidator MCP project.

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures and test configuration
├── model/               # Event and diff computation tests
├── state/               # Database, encryption, and store tests
└── sync/                # Syncer and synchronization tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
pytest tests/model/test_event_creation.py
pytest tests/sync/
```

### Run with Coverage Report

```bash
pytest --cov=python --cov-report=html
```

Coverage report will be available in `htmlcov/index.html`.

### Run Specific Test Functions

```bash
pytest tests/model/test_event_hash.py::test_compute_hash_consistency
```

## Test Organization

Each test file focuses on a single aspect of functionality and contains 1-3 related test functions. Files are kept under 100 lines for maintainability.

### Model Tests
- **Event tests**: Creation, conversion (to/from Graph API), hashing
- **Diff tests**: Create/update/delete detection, private event filtering, summaries

### State Tests
- **Encryption tests**: Credential storage, loading, deletion with keyring
- **Store tests**: SourceStore and MappingStore CRUD operations
- **Database tests**: Connection management, context manager behavior

### Sync Tests
- **Syncer tests**: Initialization, event fetching, apply operations
- **Error handling**: Missing config, API errors, logging
- **Integration**: Full sync flow (mocked)

## Test Strategy

All tests use mocked external dependencies:
- Keyring operations are mocked
- SQLite connections are mocked
- HTTP API calls are mocked
- No actual external services are contacted

This ensures tests are:
- Fast (run in seconds)
- Reliable (no network dependencies)
- Repeatable (consistent results)

## Writing New Tests

Follow these guidelines:
1. Keep files under 100 lines
2. 1-3 related test functions per file
3. Use descriptive test names: `test_<what>_<scenario>`
4. Mock external dependencies
5. Use fixtures from `conftest.py`
6. Add docstrings explaining what is being tested
