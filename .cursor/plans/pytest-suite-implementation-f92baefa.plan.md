<!-- f92baefa-8ac6-49b9-b249-ae782df3c88c 1147555d-c673-43da-88c1-28bb19dbe382 -->
# Pytest Suite for Calendar Consolidator MCP

## Overview

Comprehensive pytest suite expanding from 29 to ~74 test files covering:

- Core model, sync, and state management (29 files)
- Connectors and Graph API integration (8 files)
- CLI and database initialization (4 files)
- Integration and end-to-end tests (5 files)
- Validation and edge cases (7 files)
- Performance, reliability, and security (9 files)

## Test Structure

Create `tests/` directory with organized subdirectories:

- `tests/model/` - Event and diff tests
- `tests/sync/` - Syncer and DryRunSyncer tests
- `tests/state/` - Encryption, database, and all store tests
- `tests/connectors/` - Base connector, Graph auth, and Graph connector tests
- `tests/integration/` - End-to-end and multi-source sync tests
- `tests/validation/` - Edge cases and data validation tests
- `tests/performance/` - Bulk operations and query performance tests
- `tests/reliability/` - Retry logic and error recovery tests
- `tests/security/` - Credential isolation tests
- `tests/integrity/` - Transaction and data consistency tests
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

### Connector Tests (6-8 files)

30. `tests/connectors/test_base_connector.py` - Base connector interface/abstract methods
31. `tests/connectors/test_graph_auth_init.py` - OAuth device flow initialization
32. `tests/connectors/test_graph_auth_token.py` - Token acquisition and refresh
33. `tests/connectors/test_graph_connector_fetch.py` - Fetch events from Graph API
34. `tests/connectors/test_graph_connector_create.py` - Create events in Graph
35. `tests/connectors/test_graph_connector_update.py` - Update events in Graph
36. `tests/connectors/test_graph_connector_delete.py` - Delete events in Graph
37. `tests/connectors/test_graph_connector_error.py` - API error handling (429, 401, 500)

### Missing State Store Tests (6-8 files)

38. `tests/state/test_target_add.py` - TargetStore.add
39. `tests/state/test_target_get.py` - TargetStore.get methods
40. `tests/state/test_target_update.py` - TargetStore.update operations
41. `tests/state/test_log_store_create.py` - LogStore.create_log
42. `tests/state/test_log_store_query.py` - LogStore.get_logs with filtering
43. `tests/state/test_settings_get.py` - SettingsStore.get_setting
44. `tests/state/test_settings_set.py` - SettingsStore.set_setting
45. `tests/state/test_settings_defaults.py` - Default values handling

### DryRun Syncer Tests (3-4 files)

46. `tests/sync/test_dry_run_init.py` - DryRunSyncer initialization
47. `tests/sync/test_dry_run_operations.py` - Verify no actual changes made
48. `tests/sync/test_dry_run_preview.py` - Preview generation
49. `tests/sync/test_dry_run_comparison.py` - Compare with regular syncer

### CLI & Initialization Tests (3-4 files)

50. `tests/test_cli_wrapper.py` - CLI argument parsing and command routing
51. `tests/test_init_db_schema.py` - Database schema creation
52. `tests/test_init_db_idempotent.py` - Multiple init_db runs
53. `tests/test_init_db_migration.py` - Schema version handling (if applicable)

### Integration Tests (4-6 files)

54. `tests/integration/test_end_to_end_sync.py` - Full sync flow with mocked Graph API
55. `tests/integration/test_auth_to_sync.py` - Authentication through sync
56. `tests/integration/test_multi_source_sync.py` - Multiple sources to one target
57. `tests/integration/test_conflict_resolution.py` - Handle conflicting updates
58. `tests/integration/test_incremental_sync.py` - Subsequent syncs after initial

### Edge Case & Validation Tests (5-7 files)

59. `tests/validation/test_event_validation.py` - Invalid event data handling
60. `tests/validation/test_date_timezone.py` - Timezone conversion edge cases
61. `tests/validation/test_recurrence_patterns.py` - Recurring event handling
62. `tests/validation/test_large_descriptions.py` - Long text field handling
63. `tests/validation/test_special_characters.py` - Unicode, emojis in event data
64. `tests/validation/test_null_values.py` - Missing/optional field handling
65. `tests/validation/test_malformed_api_responses.py` - Unexpected API response formats

### Performance & Reliability Tests (6-9 files)

66. `tests/performance/test_bulk_operations.py` - Sync 100+ events
67. `tests/performance/test_database_queries.py` - Query performance with large datasets
68. `tests/reliability/test_retry_logic.py` - Retry on transient failures
69. `tests/reliability/test_rate_limiting.py` - Handle 429 responses gracefully
70. `tests/reliability/test_partial_failures.py` - Continue sync after individual event failures

### Security & Data Integrity Tests (3-4 files)

71. `tests/security/test_credential_isolation.py` - Credentials not leaked in logs/errors
72. `tests/security/test_encryption_strength.py` - Encryption key handling
73. `tests/integrity/test_transaction_rollback.py` - Database rollback on errors
74. `tests/integrity/test_data_consistency.py` - Verify hash consistency after updates

## Priority Levels

**High Priority (Core Functionality)**:

- Connector tests (30-37) - Critical external API interactions
- Missing state store tests (38-45) - Complete state management coverage
- DryRun syncer tests (46-49) - Important user-facing feature

**Medium Priority (Robustness)**:

- Integration tests (54-58) - End-to-end validation
- Validation tests (59-65) - Edge case handling
- CLI tests (50-53) - User interface

**Lower Priority (Advanced)**:

- Performance tests (66-67) - Optimization validation
- Reliability tests (68-70) - Advanced error handling
- Security/Integrity tests (71-74) - Additional safety nets

## Key Testing Strategies

- **Mock external dependencies**: keyring, sqlite3, HTTP calls
- **Use pytest fixtures**: Reusable mock objects, sample data
- **Parametrize tests**: Test multiple scenarios in compact form
- **Focus on edge cases**: Empty data, None values, error conditions
- **Each file**: 20-80 lines, 1-3 related test functions max

## Files that need pytest dependency additions

Core testing libraries:

- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking utilities
- `pytest-asyncio` - Async test support (if needed)

Specialized testing libraries:

- `freezegun` - Datetime mocking and testing
- `responses` - Mock HTTP requests/responses for Graph API tests
- `faker` - Generate realistic test data (names, emails, dates)
- `pytest-timeout` - Timeout handling for long-running tests
- `pytest-xdist` - Parallel test execution (optional, for speed)

Additional test dependencies:

- Add `requests-mock` or `responses` for HTTP mocking in connector tests
- Consider `hypothesis` for property-based testing (edge cases)
- Consider `pytest-benchmark` for performance tests

### To-dos

- [ ] Create tests/ directory structure and conftest.py with shared fixtures
- [ ] Add pytest dependencies to requirements.txt
- [ ] Create Event model tests (creation, conversion, hashing)
- [ ] Create diff computation tests (create/update/delete scenarios)
- [ ] Create encryption module tests with keyring mocks
- [ ] Create state store tests (SourceStore, MappingStore, TargetStore)
- [ ] Create log store and settings store tests
- [ ] Create Database class tests
- [ ] Create Syncer tests with full mocking
- [ ] Create DryRunSyncer tests
- [ ] Create connector tests (base, graph_auth, graph_connector)
- [ ] Create connector error handling tests
- [ ] Create CLI wrapper and init_db tests
- [ ] Create integration tests (end-to-end sync flows)
- [ ] Create multi-source and conflict resolution tests
- [ ] Create validation tests (event, dates, timezones)
- [ ] Create edge case tests (special chars, null values, large data)
- [ ] Create malformed API response tests
- [ ] Create performance tests (bulk operations, query performance)
- [ ] Create reliability tests (retry logic, rate limiting, partial failures)
- [ ] Create security tests (credential isolation, encryption)
- [ ] Create data integrity tests (transactions, consistency)