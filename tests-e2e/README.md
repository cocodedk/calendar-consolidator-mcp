# End-to-End Tests

Playwright tests for Calendar Consolidator MCP web interface.

## Setup

```bash
cd tests-e2e
npm install
npx playwright install chromium
```

## Running Tests

```bash
# Run all tests (headless)
npm test

# Run with visible browser
npm run test:headed

# Run with Playwright UI
npm run test:ui

# Debug mode
npm run test:debug

# View last test report
npm run report
```

## Test Structure

- `tests/navigation.spec.js` - Tab navigation tests
- `tests/buttons.spec.js` - Button click interactions
- `tests/dashboard.spec.js` - Dashboard element tests
- `tests/visual.spec.js` - Visual and styling tests

## Features

These tests verify:
- ✅ Tab navigation works
- ✅ All buttons are clickable
- ✅ UI elements are visible
- ✅ Proper styling and layout
- ❌ No form filling or submission
- ❌ No API validation

## Server

Tests automatically start the server on `http://127.0.0.1:3000` if not running.

## CI/CD

Tests are configured to run in CI with retry logic and proper error handling.

