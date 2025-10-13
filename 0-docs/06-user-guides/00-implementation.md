# In-App User Guides Implementation

## Overview
Expandable help panels on each page provide comprehensive, user-friendly
guidance explaining concepts and workflows.

## Components

### Help System (`node/static/app/help/`)
- `help_panel.js` - Core UI component for expandable panels
- `help_storage.js` - localStorage manager for panel state
- `help_content.js` - Content registry mapping pages to guides
- `index.js` - Barrel exports

### Guide Content (`node/static/app/help/guides/`)
Seven guide files covering all pages:
- `dashboard_guide.js` - Dashboard overview and Quick Sync
- `sources_guide.js` - Adding/managing source calendars
- `target_guide.js` - Configuring target calendar
- `sync_guide.js` - Preview and execute synchronization
- `logs_guide.js` - Reading logs and troubleshooting
- `settings_guide.js` - All settings explained
- `add_source_guide.js` - Step-by-step OAuth flow

### Styling
`help-panel.css` - Collapsible panels, dark mode compatible

## Features
- Toggle button on each page ("?" icon + "Help" label)
- Smooth expand/collapse animations
- Per-page state persistence in localStorage
- Default expanded for first-time users
- Comprehensive beginner-friendly content
- Tips, warnings, and step-by-step instructions

## Integration
Each page module imports and initializes help panel on first load.
Modal flows include contextual help.
