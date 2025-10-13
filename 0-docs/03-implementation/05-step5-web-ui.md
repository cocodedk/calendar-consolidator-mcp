# Step 5: Basic Web UI

## Goal
Create simple browser-based UI for configuration and monitoring

## Tasks

### Dashboard Layout
- [ ] Create index.html structure
- [ ] Add basic CSS styling
- [ ] Create header with title
- [ ] Add navigation/tabs
- [ ] Create main content area
- [ ] Add footer with status

### Source Calendar Configuration
- [ ] Create "Sources" tab/view
- [ ] Display list of configured sources
- [ ] Add "Add Source" button/modal
- [ ] Implement source type selection
- [ ] Add OAuth flow trigger
- [ ] Show calendar selection UI
- [ ] Add enable/disable toggle per source
- [ ] Add delete source confirmation

### Target Calendar Setup
- [ ] Create "Target" tab/view
- [ ] Display current target calendar
- [ ] Add "Set Target" button
- [ ] Implement target auth flow
- [ ] Show target calendar selection
- [ ] Display target status

### Preview/Sync Controls
- [ ] Create "Sync" tab/view
- [ ] Add "Preview Sync" button
- [ ] Display diff summary:
  - Events to create count
  - Events to update count
  - Events to delete count
- [ ] Show sample event list
- [ ] Add "Sync Now" button
- [ ] Display sync progress
- [ ] Show sync results

### Sync Logs and Status
- [ ] Create "Logs" tab/view
- [ ] Fetch and display recent logs
- [ ] Show timestamp per log
- [ ] Display status (success/error)
- [ ] Show counts per sync
- [ ] Display error messages
- [ ] Add date filter
- [ ] Add auto-refresh option

### Settings View
- [ ] Create "Settings" tab/view
- [ ] Add continuous sync toggle
- [ ] Add sync interval input
- [ ] Add ignore private events checkbox
- [ ] Add max retry attempts input
- [ ] Save settings button
- [ ] Load current settings on page load

## Files to Create
- `node/static/index.html`
- `node/static/styles.css`
- `node/static/app.js`
- `node/static/api.js` (API client)
- `node/static/components/` (optional modular components)

## Testing Checklist
- [ ] UI loads in browser
- [ ] All tabs/views accessible
- [ ] Can add source calendar
- [ ] OAuth flow works from UI
- [ ] Can set target calendar
- [ ] Preview displays correctly
- [ ] Sync executes from UI
- [ ] Logs display and refresh
- [ ] Settings save and load
- [ ] Error messages display clearly

## Technology
- Vanilla JavaScript (no framework for MVP)
- Fetch API for HTTP requests
- CSS Grid/Flexbox for layout
- Keep it simple and functional

## Time Estimate
- 8-10 hours

## Notes
- Focus on functionality over aesthetics
- Make it work first, polish later
- Use browser's built-in features
- No build step required
