# Web UI Component - Calendar Consolidator MCP

## Purpose
Browser-based interface for configuration and monitoring

## Technology
- Vanilla JavaScript or React (keep simple)
- Served as static files by Node server
- No complex build process for MVP

## Core Views

### Dashboard
- Last sync timestamp
- Next scheduled sync (if continuous enabled)
- Error indicator/count
- Quick sync button

### Source Management
- List of configured source calendars
- Add new source button
- Edit/disable/remove actions per source
- Active/inactive status indicator

### Target Configuration
- Current target calendar display
- Change target button
- Authentication status

### Preview & Sync
- Preview sync button
- Summary of pending changes:
  - Events to create (count)
  - Events to update (count)
  - Events to delete (count)
- Sample event list (5-10 examples)
- Execute sync button

### Sync Logs
- Timestamped list of sync operations
- Status (success/error/partial)
- Counts per operation
- Error messages
- Filter by date/source

### Settings
- Continuous sync toggle
- Sync interval slider
- Ignore private events checkbox
- Retry attempts setting

## User Interactions

### Add Source Calendar
1. Click "Add Source"
2. Select type (Microsoft/CalDAV)
3. Complete OAuth or enter credentials
4. Select calendar from list
5. Name/alias the source

### Execute Sync
1. Click "Preview Sync"
2. Review changes
3. Click "Sync Now"
4. View results
