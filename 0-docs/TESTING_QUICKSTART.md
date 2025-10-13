# Testing Quickstart Guide

Get up and running with the test suite in 2 minutes.

## Prerequisites

- Python 3.10+
- Virtual environment (recommended)

## Installation

```bash
# Activate virtual environment (if using venv)
source venv/bin/activate

# Install all dependencies including test tools
pip install -r requirements.txt
```

This installs:
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Enhanced mocking
- `freezegun` - Time manipulation (for future use)

## Running Tests

### Option 1: Use the Test Script (Recommended)

```bash
# Run all tests with coverage
./run_tests.sh

# Run specific category
./run_tests.sh model
./run_tests.sh state
./run_tests.sh sync

# Quick check without coverage
./run_tests.sh fast
```

### Option 2: Use pytest Directly

```bash
# All tests
pytest

# With coverage report
pytest --cov=python --cov-report=html

# Specific directory
pytest tests/model/

# Specific file
pytest tests/model/test_event_creation.py

# Verbose output
pytest -v

# Show print statements
pytest -s
```

## Understanding the Output

### Successful Test Run
```
tests/model/test_event_creation.py::test_event_basic_creation PASSED
tests/model/test_event_creation.py::test_event_from_graph PASSED
...
======================== 27 passed in 2.34s =========================
```

### Coverage Report
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
python/model/event.py                96      5    95%   42-45
python/model/diff.py                 98      0   100%
...
---------------------------------------------------------------
TOTAL                               850     23    97%
```

### Failed Test
```
FAILED tests/model/test_event_hash.py::test_compute_hash_consistency
    assert computed_hash == expected_hash
    AssertionError: hash mismatch
```

## Test Structure

```
tests/
├── model/          # Event and diff logic (8 files)
├── state/          # Storage and encryption (13 files)
└── sync/           # Synchronization (7 files)
```

Each file tests 1-3 related functions and is under 100 lines.

## Common Tasks

### Add a New Test

1. Create file in appropriate directory:
   ```bash
   touch tests/model/test_new_feature.py
   ```

2. Use this template:
   ```python
   """Test new feature functionality."""

   import pytest
   from python.module import YourClass

   def test_feature_works():
       """Test that feature does what it should."""
       result = YourClass().method()
       assert result == expected
   ```

3. Run it:
   ```bash
   pytest tests/model/test_new_feature.py -v
   ```

### Debug a Failing Test

```bash
# Run with detailed output
pytest tests/path/to/test.py -v -s

# Drop into debugger on failure
pytest --pdb

# Run only failed tests from last run
pytest --lf

# Show local variables on failure
pytest -l
```

### Check Code Coverage

```bash
# Generate HTML report
pytest --cov=python --cov-report=html

# Open in browser
firefox htmlcov/index.html  # or your browser

# Show missing lines in terminal
pytest --cov=python --cov-report=term-missing
```

### Run Tests on File Change

```bash
# Install pytest-watch
pip install pytest-watch

# Auto-run tests
ptw
```

## Troubleshooting

### "No module named 'python'"

**Problem**: Python can't find the source modules.

**Solution**: Run from project root or set PYTHONPATH:
```bash
cd /path/to/Calendar\ Consolidator\ MCP
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### "ModuleNotFoundError: No module named 'pytest'"

**Problem**: pytest not installed.

**Solution**:
```bash
pip install -r requirements.txt
```

### "Import error: keyring"

**Problem**: Missing dependencies.

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Tests run but all skip

**Problem**: Test discovery issue.

**Solution**: Run from project root:
```bash
cd /path/to/project
pytest tests/
```

## What the Tests Cover

- ✅ **Event Model**: Creation, conversion, hashing
- ✅ **Diff Logic**: Create/update/delete detection
- ✅ **Encryption**: Credential storage (mocked keyring)
- ✅ **Stores**: Source and mapping CRUD operations
- ✅ **Database**: Connection and transaction management
- ✅ **Syncer**: Fetch, apply changes, error handling

## What the Tests DON'T Do

- ❌ Call real Microsoft Graph API
- ❌ Access actual keyring
- ❌ Create real database files (uses mocks)
- ❌ Require network connection
- ❌ Require authentication

All external dependencies are mocked for fast, reliable tests.

## CI/CD Integration

Tests run automatically on GitHub:
- On every push to `main` or `develop`
- On every pull request
- See `.github/workflows/test.yml`

## Next Steps

1. **Explore Tests**: Look at `tests/model/test_event_creation.py` as an example
2. **Read Details**: See `TEST_SUITE_SUMMARY.md` for comprehensive overview
3. **Check Inventory**: See `TEST_INVENTORY.md` for file-by-file breakdown
4. **Write Tests**: Follow patterns in existing tests

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest --cov=python` | With coverage |
| `pytest tests/model/` | Run category |
| `pytest -k "hash"` | Run tests matching name |
| `pytest --lf` | Run last failed |
| `pytest --pdb` | Debug on failure |
| `./run_tests.sh` | Full suite with coverage |

## Performance

Expected test execution time:
- **All tests**: ~2-5 seconds
- **Single category**: ~1 second
- **Single file**: <1 second

If tests run slower, check for:
- Actual I/O operations (should be mocked)
- Network calls (should be mocked)
- Large data processing (should use minimal fixtures)

## Getting Help

1. Check test output messages
2. Review test code for examples
3. Check `tests/README.md` for detailed guide
4. Review `conftest.py` for available fixtures
5. See existing tests for patterns

## Example Session

```bash
# Activate environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run tests
pytest

# Output:
# ======================== 27 passed in 2.34s =========================

# Generate coverage report
pytest --cov=python --cov-report=html

# Open coverage report
firefox htmlcov/index.html

# Success! 🎉
```

You're ready to test! 🚀
