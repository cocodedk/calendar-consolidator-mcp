# Step 13: Cross-Platform Builds (Phase 5)

## Goal
Create installers for macOS, Windows, and Linux

## Tasks

### macOS Build
- [ ] Configure .dmg generation
- [ ] Create app icons (.icns)
- [ ] Setup code signing (Developer ID)
- [ ] Enable macOS notarization
- [ ] Test on macOS 10.15+
- [ ] Verify app launches correctly

### Windows Build
- [ ] Configure .exe installer (InnoSetup/NSIS)
- [ ] Create app icons (.ico)
- [ ] Setup code signing (certificate)
- [ ] Test on Windows 10/11
- [ ] Verify installer works
- [ ] Test auto-start on login

### Linux Build
- [ ] Configure .AppImage generation
- [ ] Create .deb package
- [ ] Create .rpm package (optional)
- [ ] Test on Ubuntu/Debian
- [ ] Test on Fedora (if .rpm)
- [ ] Verify desktop integration

### Auto-Update Mechanism
- [ ] Configure electron-updater
- [ ] Setup update server/CDN
- [ ] Implement update checking
- [ ] Add update notifications
- [ ] Test update flow on each platform

## Files to Create
- `electron/icons/icon.icns` (macOS)
- `electron/icons/icon.ico` (Windows)
- `electron/icons/icon.png` (Linux)
- `electron/updater-config.json`

## Testing Checklist
- [ ] macOS .dmg installs and runs
- [ ] Windows .exe installs and runs
- [ ] Linux AppImage runs
- [ ] Code signing verified
- [ ] Updates download and install
- [ ] No permission issues

## Platform-Specific Considerations
- **macOS**: Requires Apple Developer account for signing
- **Windows**: Requires code signing certificate
- **Linux**: Various distro testing needed

## Time Estimate
- 12-16 hours
