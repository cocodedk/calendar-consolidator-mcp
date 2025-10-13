<!-- 8b8054c8-ef9e-4e40-aecf-efc8c35cf653 68905b06-864d-47de-a539-7781e03ac77f -->
# Dark Mode Implementation Plan

## Overview

Add dark mode support to the Calendar Consolidator UI with a toggle button in the header, automatic system preference detection, and persistence via localStorage.

## Implementation Steps

### 1. CSS Architecture Update

**File: `node/static/styles.css`**

- Convert hardcoded colors to CSS custom properties (variables)
- Define light theme colors (`:root`)
- Define dark theme colors (`[data-theme="dark"]`)
- Key color mappings:
- Background: `#f5f5f5` → `#1a1a1a`
- Cards/surfaces: `white` → `#2d2d2d`
- Text primary: `#333` → `#e5e5e5`
- Text secondary: `#666` → `#a0a0a0`
- Primary blue: `#2563eb` (keep consistent or adjust brightness)
- Borders: `#eee` → `#404040`

### 2. Toggle Button UI

**File: `node/static/index.html`**

- Add dark mode toggle button in header next to status bar (line ~15)
- Use icon-based button (☀️/🌙 or text "Light/Dark")
- Add `id="theme-toggle"` for JavaScript targeting

### 3. Theme Manager JavaScript

**File: Create `node/static/app/theme.js`**

- Detect system preference: `window.matchMedia('(prefers-color-scheme: dark)')`
- Check localStorage for saved preference: `localStorage.getItem('theme')`
- Apply theme on page load before content renders (avoid flash)
- Toggle function that:
- Switches `data-theme` attribute on `<html>` element
- Saves preference to localStorage
- Updates toggle button appearance
- Listen for system preference changes

**File: `node/static/index.html`**

- Import theme.js before other scripts (line ~106)
- Add inline script in `<head>` to prevent flash of wrong theme

### 4. E2E Tests

**File: Create `tests-e2e/tests/dark-mode.spec.js`**

- Test initial theme respects system preference
- Test toggle button switches theme
- Test localStorage persistence (reload page, theme persists)
- Test visual elements in both modes (check computed styles)
- Test all tabs render correctly in dark mode
- Test toggle button appearance updates

### 5. Documentation

**File: `0-docs/03-implementation/dark-mode.md`**

- Document dark mode architecture
- Explain CSS variable structure
- Document localStorage key and values
- Note system preference integration

## Key Files to Modify

- `node/static/styles.css` (~150 lines → ~200 lines)
- `node/static/index.html` (add toggle button + script)
- `node/static/app/theme.js` (new file, ~60 lines)
- `tests-e2e/tests/dark-mode.spec.js` (new file, ~80 lines)
- `0-docs/03-implementation/dark-mode.md` (new file)

## Technical Considerations

- Use `data-theme` attribute on `<html>` for theme switching
- Initialize theme ASAP to prevent flash
- Use CSS custom properties for maintainability
- Ensure WCAG contrast ratios maintained in dark mode
- Keep existing functionality intact

### To-dos

- [ ] Refactor styles.css to use CSS custom properties and define dark theme
- [ ] Add dark mode toggle button to header in index.html
- [ ] Create theme.js with localStorage persistence and system preference detection
- [ ] Add inline script in HTML head to initialize theme before render
- [ ] Create dark-mode.spec.js with comprehensive Playwright tests
- [ ] Create dark-mode.md documentation in 0-docs/03-implementation/