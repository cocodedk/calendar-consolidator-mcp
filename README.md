# Calendar Consolidator MCP

A lightweight system to consolidate multiple calendars (Microsoft 365, iCloud/CalDAV) into a single unified calendar with one-way mirroring and incremental syncing.

## 🚀 Quick Start

```bash
# Prerequisites: Python 3.10+, Node 18+
git clone <repo-url>
cd calendar-consolidator
pip install -r requirements.txt
npm install
npm start
```

Opens http://localhost:3000 - Follow the UI to add calendars and sync!

**[→ Full Setup Guide](0-docs/03-implementation/00-phase0-setup.md)**

## 📖 Documentation

Complete documentation in the `0-docs/` directory, organized as micro-focused files:

**Quick Links:**
- **[Setup Guide](0-docs/03-implementation/00-phase0-setup.md)** - Start here
- **[Documentation Index](0-docs/README.md)** - Complete documentation map

**Documentation Sections:**
- **[01-overview/](0-docs/01-overview/)** - Purpose, constraints, tech stack
- **[02-architecture/](0-docs/02-architecture/)** - System design and components
- **[03-implementation/](0-docs/03-implementation/)** - Step-by-step implementation (14 steps)
- **[04-api-design/](0-docs/04-api-design/)** - MCP tools and HTTP API specs
- **[05-database/](0-docs/05-database/)** - Database schema and storage

All files follow modular guidelines: < 100 lines, single purpose, focused content.

## ✨ Features

- ✅ **One-way sync** from multiple sources to single target
- ✅ **Incremental updates** with change detection
- ✅ **Microsoft 365** calendar support
- ✅ **CalDAV/iCloud** calendar support (planned)
- ✅ **MCP integration** for AI/agent control
- ✅ **Web UI** for configuration and monitoring
- ✅ **SQLite database** for configuration and state

## 🎯 Current Status

**Phase 0: MVP Development**

This is a single-user desktop tool currently in active development. The MVP focuses on:
- Local setup (Python + Node.js)
- Microsoft Graph → Microsoft Graph sync
- Basic web UI for configuration
- Manual sync operations

**Future Phases:**
- Phase 4: Docker containerization (optional)
- Phase 5: Electron desktop app for non-technical users

## 🛠️ Technology Stack

- **Backend**: Python 3.10+ (sync engine) + Node.js 18+ (MCP server)
- **Database**: SQLite with encrypted credentials
- **Frontend**: Simple web UI (vanilla JS/React)
- **APIs**: Microsoft Graph, CalDAV
- **Security**: OAuth, local-only access

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   MCP Server    │    │  Python Worker  │
│   (Frontend)    │◄──►│   (Node.js)     │◄──►│   (Sync Engine) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SQLite DB     │    │   External APIs │
                       │   (Config/State)│    │   (Microsoft/   │
                       └─────────────────┘    │    iCloud)      │
                                             └─────────────────┘
```

## 🔧 Development

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- Git

### Setup
```bash
# Clone repository
git clone <repo-url>
cd calendar-consolidator

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Initialize database
python python/init_db.py

# Start development server
npm start
```

### Testing
```bash
# Python tests
cd python && pytest

# Node tests
cd node && npm test
```

## 📝 License

[License TBD]

## 🙏 Acknowledgments

Inspired by [Planner-Task-Creator-CLI-MCP](https://github.com/cocodedk/Planner-Task-Creator-CLI-MCP) for its excellent modular architecture and documentation structure.

## 🚧 Project Status

This project is in **active development**. The core functionality is being built, and the API may change. Not recommended for production use yet.

**Current Phase**: Phase 0 - MVP Development
**Next Milestone**: Graph → Graph sync working end-to-end

---

For detailed information, see the [documentation](0-docs/) directory.
