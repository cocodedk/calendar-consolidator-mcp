# Calendar Consolidator MCP

A lightweight system to consolidate multiple calendars (Microsoft 365, iCloud/CalDAV) into a single unified calendar with one-way mirroring and incremental syncing.

## Features

- **Multi-source support**: Microsoft Graph, CalDAV (coming soon)
- **One-way sync**: Source → Target calendar mirroring
- **Incremental updates**: Delta sync with change detection
- **MCP integration**: AI/agent control via MCP protocol
- **Web UI**: Simple browser-based configuration
- **Local-first**: SQLite database, no cloud dependencies

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Installation

1. **Clone repository**:
```bash
git clone <repo-url>
cd calendar-consolidator-mcp
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
# Or with virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install Node dependencies**:
```bash
npm install
```

4. **Initialize database**:
```bash
python python/init_db.py
```

### Running the Application

**Start web UI** (recommended):
```bash
npm start
```
Then open http://localhost:3000 in your browser.

**Start as MCP server** (for AI/agent integration):
```bash
MCP_MODE=true node node/server/index.js
```

### MCP Tools Available

The MCP server exposes the following tools for AI/agent control:

**Configuration Tools:**
- `listCalendars` - List available calendars from Microsoft Graph, Google, iCloud, or CalDAV
- `getConfig` - Get current sources, target, and settings configuration

**Sync Operation Tools:**
- `previewSync` - Preview sync changes without making changes (dry run)
- `syncOnce` - Execute calendar sync for a source or all sources
- `getSyncStatus` - Get current sync status and recent logs

For detailed tool schemas and examples, see `0-docs/04-api-design/01-mcp-tools.md`

### MCP Configuration Setup

To use this MCP server with Claude Desktop or Cursor, add the following to your MCP configuration:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "calendar-consolidator": {
      "command": "node",
      "args": [
        "/absolute/path/to/calendar-consolidator-mcp/node/server/index.js"
      ],
      "env": {
        "MCP_MODE": "true"
      }
    }
  }
}
```

**For Cursor** (`.cursor/mcp.json` in your workspace):
```json
{
  "mcpServers": {
    "calendar-consolidator": {
      "command": "node",
      "args": [
        "node/server/index.js"
      ],
      "env": {
        "MCP_MODE": "true"
      }
    }
  }
}
```

Replace `/absolute/path/to/calendar-consolidator-mcp` with the actual path to your installation.

## Project Structure

```
calendar-consolidator-mcp/
├── python/               # Python sync engine
│   ├── connectors/      # API connectors (Graph, CalDAV)
│   ├── model/           # Event model and diff logic
│   ├── state/           # Database and config management
│   └── sync/            # Sync execution engine
├── node/                # Node.js MCP server
│   ├── server/          # Express server and MCP tools
│   └── static/          # Web UI files
├── database/            # Database schema
└── 0-docs/              # Comprehensive documentation
```

## Configuration

### Microsoft Graph Setup

1. Register app in Azure AD
2. Configure redirect URIs for localhost
3. Request `Calendars.ReadWrite` scope
4. Use device code flow for authentication

See `0-docs/03-implementation/02-step2-graph-connector.md` for details.

## Documentation

Comprehensive documentation in `0-docs/`:

- **Overview**: Purpose, constraints, tech stack
- **Architecture**: System design and components
- **Implementation**: Step-by-step guides
- **API Design**: MCP tools and HTTP endpoints
- **Database**: Schema and storage details

Start with: `0-docs/README.md`

## Development

The project follows strict modularization guidelines:
- Files under 100 lines each
- Single responsibility per module
- Clear separation of concerns

## Testing

**Python Unit Tests**:
```bash
bash run_tests.sh
```

**Playwright E2E Tests**:
```bash
bash run_e2e_tests.sh
```

See `tests/` for Python tests and `tests-e2e/` for Playwright tests.

## License

MIT License - Copyright (c) 2025 Babak Bandpey - cocode.dk

See [LICENSE](LICENSE) file for details.

## Status

**Phase 0 - MVP Development** ✅
- Core database and state management
- Microsoft Graph connector
- Google Calendar connector
- iCloud CalDAV connector
- Sync engine (manual sync + preview)
- MCP server with tools
- Comprehensive web UI with dark mode
- OAuth credentials management

**Feature Implementation**:
- ✅ **CalDAV Support**: Fully implemented with iCloud connector
- ✅ **OAuth Flow UI**: Complete device code flow with session management
- ⚠️ **Error Handling**: Basic logging implemented, retry logic needs development
- ❌ **Continuous Sync Scheduler**: Database schema ready, scheduler module not yet built

**Coming Next**:
- Continuous sync scheduler with configurable intervals
- Advanced error handling with exponential backoff and retry logic
- Additional CalDAV providers (Nextcloud, etc.)
- Conflict resolution strategies
