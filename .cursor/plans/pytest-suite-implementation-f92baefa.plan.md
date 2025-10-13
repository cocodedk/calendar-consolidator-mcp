<!-- f92baefa-8ac6-49b9-b249-ae782df3c88c 1147555d-c673-43da-88c1-28bb19dbe382 -->
# Pytest Suite for Calendar Consolidator MCP

## Test Structure

Create `tests/` directory with organized subdirectories mirroring the `python/` structure:

- `tests/model/` - Event and diff tests
- `tests/sync/` - Syncer tests  
- `tests/state/` - Encryption and store tests
- `tests/conftest.py` - Shared fixtures

## Test Files to Create

### Setup & Configuration (2 files)

1. `tests/conftest.py` - Shared fixtures (mock db, events, credentials)
2. `tests/requirements-test.txt` - Test dependencies (pytest, pytest-cov, pytest-mock)

### Model Tests (6-8 files)

3. `tests/model/test_event_creation.py` - Event initialization and from_graph
4. `tests/model/test_event_to_graph.py` - to_graph conversion
5. `tests/model/test_event_hash.py` - compute_hash functionality
6. `tests/model/test_diff_create.py` - Diff for new events
7. `tests/model/test_diff_update.py` - Diff for updated events  
8. `tests/model/test_diff_delete.py` - Diff for deleted events
9. `tests/model/test_diff_private.py` - Private event filtering
10. `tests/model/test_diff_summary.py` - Summary generation

### State/Encryption Tests (4-5 files)

11. `tests/state/test_encryption_store.py` - store_credentials with keyring mock
12. `tests/state/test_encryption_load.py` - load_credentials with keyring mock
13. `tests/state/test_encryption_delete.py` - delete_credentials
14. `tests/state/test_encryption_blob.py` - blob conversion functions

### State/Store Tests (6-8 files)

15. `tests/state/test_source_add.py` - SourceStore.add
16. `tests/state/test_source_get.py` - SourceStore.get methods
17. `tests/state/test_source_update.py` - SourceStore.update_token
18. `tests/state/test_mapping_create.py` - MappingStore.create
19. `tests/state/test_mapping_get.py` - MappingStore.get methods
20. `tests/state/test_mapping_update.py` - MappingStore.update_hash

### Sync Tests (5-7 files)

21. `tests/sync/test_syncer_init.py` - Syncer initialization
22. `tests/sync/test_syncer_fetch.py` - Fetch events from source
23. `tests/sync/test_syncer_apply_create.py` - Apply create operations
24. `tests/sync/test_syncer_apply_update.py` - Apply update operations
25. `tests/sync/test_syncer_apply_delete.py` - Apply delete operations
26. `tests/sync/test_syncer_error.py` - Error handling and logging
27. `tests/sync/test_syncer_integration.py` - Full sync_once flow (mocked)

### Database Tests (2-3 files)

28. `tests/state/test_database_init.py` - Database connection and schema
29. `tests/state/test_database_context.py` - Context manager behavior

## Key Testing Strategies

- **Mock external dependencies**: keyring, sqlite3, HTTP calls
- **Use pytest fixtures**: Reusable mock objects, sample data
- **Parametrize tests**: Test multiple scenarios in compact form
- **Focus on edge cases**: Empty data, None values, error conditions
- **Each file**: 20-80 lines, 1-3 related test functions max

## Files that need pytest dependency additions

- Add to `requirements.txt`: pytest, pytest-cov, pytest-mock, freezegun (for datetime testing)

### To-dos

- [ ] Create tests/ directory structure and conftest.py with shared fixtures
- [ ] Create Event model tests (creation, conversion, hashing)
- [ ] Create diff computation tests (create/update/delete scenarios)
- [ ] Create encryption module tests with keyring mocks
- [ ] Create state store tests (SourceStore, MappingStore)
- [ ] Create Syncer tests with full mocking
- [ ] Create Database class tests
- [ ] Add pytest dependencies to requirements.txt
- [ ] 