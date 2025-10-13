# Deployment Model - Calendar Consolidator MCP

## Phase 0: MVP (Local Development)

### Setup
- Requires Python 3.10+ and Node 18+ installed
- Run with `npm start` / `python sync.py`
- Manual dependency installation

### Target Users
- Developer (you)
- Technical testers who can run Python + Node

### Installation Time
- < 5 minutes from git clone to running

## Phase 4: Docker (Optional)

### Setup
- Requires Docker Desktop
- Run with `docker-compose up`
- Handles OAuth redirect complexities

### Target Users
- Docker-savvy users
- Users wanting isolated environments
- CI/CD pipelines

### Challenges
- OAuth localhost redirects from container
- May need device code flow
- Volume mounting for persistence

## Phase 5: Electron (End-User)

### Setup
- Native installers (.dmg, .exe, .AppImage)
- Double-click to install
- No dependencies required

### Target Users
- Non-technical end users
- "Just works" experience required

### Features
- Python bundled with PyInstaller
- Auto-updates
- System tray integration
- Launch at startup option

### Installation Time
- < 2 minutes from download to running
