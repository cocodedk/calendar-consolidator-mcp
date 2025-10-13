#!/bin/bash
# Run OAuth authentication tests

echo "Running Python tests..."
python -m pytest tests/api/ -v --tb=short

echo ""
echo "Running Node.js tests..."
npm test -- auth_routes
