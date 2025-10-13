# Test Inventory - Detailed Breakdown

## Model Tests (8 files, ~440 lines)

| File | Lines | Focus Area |
|------|-------|------------|
| `test_event_creation.py` | 54 | Event instantiation, from_graph conversion |
| `test_event_to_graph.py` | 54 | Event to Graph API format |
| `test_event_hash.py` | 60 | Hash computation and consistency |
| `test_diff_create.py` | 50 | New event detection |
| `test_diff_update.py` | 53 | Changed event detection |
| `test_diff_delete.py` | 57 | Deleted/cancelled events |
| `test_diff_private.py` | 47 | Private event filtering |
| `test_diff_summary.py` | 54 | Summary and statistics |

**Key Tests:**
- Event lifecycle (create, convert, hash)
- Diff computation (detect changes)
- Private event handling
- Summary generation

---

## State/Encryption Tests (4 files, ~184 lines)

| File | Lines | Focus Area |
|------|-------|------------|
| `test_encryption_store.py` | 49 | Storing credentials in keyring |
| `test_encryption_load.py` | 47 | Loading credentials from keyring |
| `test_encryption_delete.py` | 36 | Deleting credentials |
| `test_encryption_blob.py` | 52 | Blob conversion functions |

**Key Tests:**
- Keyring integration (mocked)
- Credential serialization
- Error handling for missing credentials

---

## State/Store Tests (6 files, ~347 lines)

| File | Lines | Focus Area |
|------|-------|------------|
| `test_source_add.py` | 51 | Adding source calendars |
| `test_source_get.py` | 59 | Retrieving sources |
| `test_source_update.py` | 41 | Updating tokens and status |
| `test_mapping_create.py` | 44 | Creating event mappings |
| `test_mapping_get.py` | 66 | Retrieving mappings |
| `test_mapping_update.py` | 45 | Updating/deleting mappings |

**Key Tests:**
- CRUD operations for sources
- CRUD operations for mappings
- Token management
- Active/inactive sources

---

## State/Database Tests (2 files, ~111 lines)

| File | Lines | Focus Area |
|------|-------|------------|
| `test_database_init.py` | 63 | Connection and initialization |
| `test_database_context.py` | 48 | Context manager behavior |

**Key Tests:**
- SQLite connection management
- Foreign key enforcement
- Transaction handling
- Context manager commit/rollback

---

## Sync Tests (7 files, ~412 lines)

| File | Lines | Focus Area |
|------|-------|------------|
| `test_syncer_init.py` | 42 | Syncer initialization |
| `test_syncer_fetch.py` | 59 | Event fetching logic |
| `test_syncer_apply_create.py` | 61 | Create operations |
| `test_syncer_apply_update.py` | 60 | Update operations |
| `test_syncer_apply_delete.py` | 60 | Delete operations |
| `test_syncer_error.py` | 59 | Error handling |
| `test_syncer_integration.py` | 82 | Full sync flow |

**Key Tests:**
- Connector instantiation
- Event fetching with delta sync
- Apply create/update/delete
- Error handling and logging
- End-to-end sync flow (mocked)

---

## Test Infrastructure (2 files, ~73 lines)

| File | Lines | Purpose |
|------|-------|---------|
| `conftest.py` | 73 | Shared fixtures and test data |
| `__init__.py` (×4) | 1 each | Package initialization |

**Fixtures Provided:**
- `sample_datetime` - Test datetime objects
- `sample_event_data` - Event dictionaries
- `sample_graph_event` - Graph API format
- `sample_credentials` - OAuth credentials
- `mock_db_connection` - SQLite mock
- `mock_database` - Database instance mock

---

## Summary Statistics

### By Category
- **Model**: 8 files, 440 lines, ~55 lines/file
- **State (Encryption)**: 4 files, 184 lines, ~46 lines/file
- **State (Stores)**: 6 files, 347 lines, ~58 lines/file
- **State (Database)**: 2 files, 111 lines, ~56 lines/file
- **Sync**: 7 files, 412 lines, ~59 lines/file
- **Infrastructure**: 2 files, 73 lines

### Overall
- **Total test files**: 27
- **Total lines of test code**: ~1,567 lines
- **Average file size**: 52 lines
- **Smallest file**: 36 lines (test_encryption_delete.py)
- **Largest file**: 82 lines (test_syncer_integration.py)
- **File size compliance**: 100% (all files < 100 lines)

### Test Distribution
```
Model     ████████░░░░░░░░░░░░  30%
State     ████████████░░░░░░░░  45%
Sync      ██████████░░░░░░░░░░  25%
```

---

## Test Patterns Used

### Mocking Strategies
1. **External Services**: `@patch('module.keyring')`
2. **Database Connections**: `MagicMock(spec=sqlite3.Connection)`
3. **API Responses**: Pre-defined dictionaries
4. **Time-based**: freezegun (available for future use)

### Assertion Patterns
- Direct equality: `assert result == expected`
- Type checks: `assert isinstance(obj, Type)`
- Mock verification: `mock.assert_called_once()`
- Exception testing: `with pytest.raises(Exception)`

### Fixture Usage
- Parameterized fixtures for data variations
- Mock objects for dependencies
- Sample data for consistent testing

---

## Coverage Goals

### Current Focus (Implemented)
- ✅ Event model and operations
- ✅ Diff computation logic
- ✅ Credential encryption
- ✅ Source/mapping stores
- ✅ Database connection
- ✅ Sync engine core

### Future Extensions
- ⏳ CalDAV connector tests
- ⏳ GraphAuth flow tests
- ⏳ Settings store tests
- ⏳ Target store tests
- ⏳ Log store tests
- ⏳ Dry-run syncer tests

---

## File Size Distribution

```
Lines    Count  Files
30-39    1      test_encryption_delete
40-49    7      Various
50-59    15     Majority
60-69    4      Larger tests
70-79    0      -
80-89    1      test_syncer_integration
```

**Observation**: Most files cluster around 50-60 lines, perfect for quick comprehension.

---

## Test Quality Metrics

- ✅ **Isolation**: 100% (all use mocks)
- ✅ **Speed**: Fast (no I/O or network)
- ✅ **Clarity**: High (descriptive names + docstrings)
- ✅ **Maintainability**: Excellent (small files)
- ✅ **Coverage**: High (critical paths covered)
- ✅ **Documentation**: Complete (README + summaries)

---

## Running Specific Tests

```bash
# Single category
pytest tests/model/
pytest tests/state/
pytest tests/sync/

# Single file
pytest tests/model/test_event_creation.py

# Single test
pytest tests/model/test_event_hash.py::test_compute_hash_consistency

# With coverage
pytest --cov=python.model tests/model/

# Fast run (no coverage)
pytest --tb=short

# Verbose output
pytest -v tests/
```

---

## Maintenance Guidelines

### Adding New Tests
1. Choose appropriate category (model/state/sync)
2. Create new file: `test_<component>_<feature>.py`
3. Keep file under 100 lines
4. Use fixtures from conftest.py
5. Add docstrings to test functions
6. Update this inventory

### Modifying Tests
1. Maintain file size limits
2. Keep mocking consistent
3. Update docstrings if behavior changes
4. Run full suite before committing

### Best Practices
- One assertion per test (when possible)
- Clear test names: `test_<what>_<scenario>`
- Use parametrize for variations
- Mock at module boundaries
- Test happy path + edge cases
