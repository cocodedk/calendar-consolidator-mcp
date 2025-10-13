#!/bin/bash
# Run Playwright E2E tests

set -e

echo "🎭 Running Playwright E2E Tests..."
echo ""

cd tests-e2e

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if Playwright browsers are installed
if [ ! -d "node_modules/.cache/ms-playwright" ]; then
    echo "🌐 Installing Playwright browsers..."
    npx playwright install chromium
fi

echo ""
echo "Running tests..."
echo ""

# Run tests
npm test

echo ""
echo "✅ E2E tests complete!"
echo ""
echo "To view the report: cd tests-e2e && npm run report"

