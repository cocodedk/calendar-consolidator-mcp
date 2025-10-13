# Dark Mode Implementation

## Overview
Dark mode support with toggle button, system preference detection, and localStorage persistence.

## Architecture

### CSS Variables
Theme colors defined in `theme-variables.css`:
- Light theme in `:root`
- Dark theme in `[data-theme="dark"]`
- All colors use CSS custom properties (e.g., `var(--bg-primary)`)

### JavaScript Modules

**theme.js** - Main theme manager class
- Initializes theme on page load
- Handles toggle button events
- Listens for system preference changes

**theme-storage.js** - localStorage operations
- `getSavedTheme()` - Retrieve saved preference
- `saveTheme(theme)` - Persist theme choice
- `getInitialTheme()` - Get saved or system preference

**theme-ui.js** - Visual updates
- `applyThemeToDocument(theme)` - Set data-theme attribute
- `updateToggleButton(theme)` - Update toggle icon (🌙/☀️)

## Usage

### Toggle Button
Located in header, switches between themes with smooth transition.

### localStorage Key
`theme` - Values: `'light'` or `'dark'`

### System Preference
Respects `prefers-color-scheme` media query on first load. Manual toggle overrides system preference.

## Flash Prevention
Inline script in HTML `<head>` applies theme before page render.

## Testing
E2E tests in three files:
- `dark-mode-toggle.spec.js` - Toggle functionality
- `dark-mode-system.spec.js` - System preference and persistence
- `dark-mode-visual.spec.js` - Visual rendering validation

## Color Palette

### Light Theme
- Background: `#f5f5f5`
- Cards: `#ffffff`
- Text: `#333333`
- Borders: `#eeeeee`

### Dark Theme
- Background: `#1a1a1a`
- Cards: `#2d2d2d`
- Text: `#e5e5e5`
- Borders: `#404040`
