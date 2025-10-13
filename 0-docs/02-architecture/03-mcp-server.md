# MCP Server Component - Calendar Consolidator MCP

## Purpose
Node.js server providing MCP tools and HTTP API

## Responsibilities

### MCP Tool Exposure
- Define MCP tool schemas
- Route tool calls to Python worker
- Return JSON-serializable results
- Handle tool errors gracefully

### HTTP API Server
- Serve REST endpoints for web UI
- Handle configuration requests
- Trigger sync operations
- Stream sync logs

### Python Worker Bridge
- Spawn Python processes for sync
- Pass configuration/parameters
- Capture output and errors
- Handle process failures

### Static File Serving
- Serve web UI HTML/CSS/JS
- Provide assets (icons, etc.)
- Handle SPA routing if needed

## Technology

### Framework
- Express.js or similar HTTP framework
- MCP SDK for tool definitions
- Child process for Python calls

### Port
- Default: 3000
- Bind to localhost only
- No remote access unless configured

## Key Modules

### `/server/index.js`
- Bootstrap server
- Initialize MCP
- Start HTTP server
- Handle shutdown gracefully

### `/server/tools/`
- MCP tool definitions
- One file per tool or tool group
- Schema validation
- Error handling

### `/server/admin_api.js`
- HTTP route handlers
- Configuration CRUD
- Sync triggers
- Log queries

### `/server/python_bridge.js`
- Python subprocess management
- Parameter serialization
- Output parsing
- Error mapping
