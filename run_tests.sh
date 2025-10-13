#!/bin/bash
# Test runner script for Calendar Consolidator MCP

set -e

echo "======================================"
echo "Calendar Consolidator MCP Test Suite"
echo "======================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "   Run: source venv/bin/activate"
    echo ""
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Display test structure
echo "📁 Test Structure:"
echo "   - Model tests: $(find tests/model -name 'test_*.py' | wc -l) files"
echo "   - State tests: $(find tests/state -name 'test_*.py' | wc -l) files"
echo "   - Sync tests: $(find tests/sync -name 'test_*.py' | wc -l) files"
echo "   Total: $(find tests -name 'test_*.py' | wc -l) test files"
echo ""

# Run tests based on argument
case "${1:-all}" in
    all)
        echo "🧪 Running all tests with coverage..."
        pytest --cov=python --cov-report=term-missing --cov-report=html
        ;;
    model)
        echo "🧪 Running model tests..."
        pytest tests/model/ -v
        ;;
    state)
        echo "🧪 Running state tests..."
        pytest tests/state/ -v
        ;;
    sync)
        echo "🧪 Running sync tests..."
        pytest tests/sync/ -v
        ;;
    fast)
        echo "🧪 Running fast check (no coverage)..."
        pytest --tb=short
        ;;
    *)
        echo "❌ Unknown option: $1"
        echo "Usage: $0 [all|model|state|sync|fast]"
        exit 1
        ;;
esac

echo ""
echo "✅ Tests completed!"
if [ "${1:-all}" = "all" ]; then
    echo "📊 Coverage report: htmlcov/index.html"
fi
