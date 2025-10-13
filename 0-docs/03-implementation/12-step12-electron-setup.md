# Step 12: Electron Setup (Phase 5)

## Goal
Package application as desktop app with Electron

## Tasks

### Electron Project Structure
- [ ] Initialize Electron project
- [ ] Create main process file
- [ ] Create preload script
- [ ] Setup IPC communication
- [ ] Configure security settings

### Python Bundling
- [ ] Install PyInstaller
- [ ] Create PyInstaller spec file
- [ ] Bundle Python with dependencies
- [ ] Test standalone Python executable
- [ ] Include in Electron resources

### Electron Builder Configuration
- [ ] Install electron-builder
- [ ] Create builder config
- [ ] Configure app metadata
- [ ] Setup icon assets
- [ ] Configure build targets

### OAuth Integration
- [ ] Implement BrowserWindow auth flow
- [ ] Handle OAuth redirects in Electron
- [ ] Store tokens securely
- [ ] Test auth flow in packaged app

### Node Server Integration
- [ ] Start Node server in main process
- [ ] Configure localhost binding
- [ ] Load UI in renderer process
- [ ] Handle server shutdown gracefully

## Files to Create
- `electron/main.js`
- `electron/preload.js`
- `electron/builder-config.json`
- `python/build.spec` (PyInstaller)

## Testing Checklist
- [ ] Electron app launches
- [ ] UI loads correctly
- [ ] Python worker executes
- [ ] OAuth flow works
- [ ] Sync operations function
- [ ] App closes cleanly

## Dependencies
- `electron`
- `electron-builder`
- PyInstaller

## Time Estimate
- 10-12 hours
