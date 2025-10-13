#!/bin/bash
# Run Calendar Consolidator MCP with virtual environment activated

set -e

echo "🚀 Starting Calendar Consolidator MCP..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Verify Python can find the python module
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"

# Check if database exists
if [ ! -f "calendar_consolidator.db" ]; then
    echo "💾 Database not found. Initializing..."
    python3 python/init_db.py
fi

# Start the server
echo "🌐 Starting server on http://127.0.0.1:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run npm start (this will keep running)
npm start
