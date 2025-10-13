# Step 8: UI Polish (Phase 2)

## Goal
Improve error handling UX and add missing UI features

## Tasks

### Error Handling UX
- [ ] Add toast notifications for errors
- [ ] Display detailed error messages
- [ ] Add retry buttons for failed operations
- [ ] Show network status indicator
- [ ] Add offline detection

### Reauthorization Flows
- [ ] Detect expired credentials
- [ ] Show "Reconnect" button for sources
- [ ] Trigger OAuth flow again
- [ ] Update credentials in place
- [ ] Test reauth without data loss

### Settings Management
- [ ] Expand settings view
- [ ] Add backup/restore settings
- [ ] Add export configuration
- [ ] Add import configuration
- [ ] Validate settings on save

### Sync Progress Indicators
- [ ] Add progress bar for sync
- [ ] Show current source being synced
- [ ] Display real-time event counts
- [ ] Add cancel sync button
- [ ] Show estimated time remaining

## Files to Update
- `node/static/app.js`
- `node/static/index.html`
- `node/static/styles.css`

## Testing Checklist
- [ ] Errors display clearly
- [ ] Reauth flow works smoothly
- [ ] Progress shows accurately
- [ ] Can cancel long-running sync
- [ ] Settings import/export works

## Time Estimate
- 6-8 hours
