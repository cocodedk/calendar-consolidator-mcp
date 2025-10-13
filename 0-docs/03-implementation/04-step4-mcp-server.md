# Step 4: MCP Server (Node.js)

## Goal
Create Node.js MCP server with HTTP API and Python bridge

## Tasks

### MCP Server Framework
- [ ] Initialize Node project with package.json
- [ ] Install MCP SDK
- [ ] Create server/index.js entry point
- [ ] Setup MCP server bootstrap
- [ ] Test basic MCP connection

### Core MCP Tools
- [ ] Implement listCalendars tool
- [ ] Implement previewSync tool
- [ ] Implement syncOnce tool
- [ ] Implement addSource tool
- [ ] Implement removeSource tool
- [ ] Implement setTarget tool
- [ ] Implement getSyncStatus tool
- [ ] Test each tool individually

### Python Worker Bridge
- [ ] Create python_bridge.js module
- [ ] Implement spawn Python process
- [ ] Pass JSON parameters to Python
- [ ] Capture Python stdout/stderr
- [ ] Parse Python JSON output
- [ ] Handle Python errors
- [ ] Test bridge with simple script

### HTTP Admin API
- [ ] Setup Express.js server
- [ ] Implement GET /api/config
- [ ] Implement POST /api/source
- [ ] Implement DELETE /api/source/:id
- [ ] Implement POST /api/target
- [ ] Implement POST /api/preview
- [ ] Implement POST /api/sync
- [ ] Implement GET /api/logs
- [ ] Implement GET /api/status
- [ ] Add error handling middleware

### Static File Serving
- [ ] Configure Express static middleware
- [ ] Create node/static/ directory
- [ ] Test serving index.html

## Files to Create
- `node/package.json`
- `node/server/index.js`
- `node/server/mcp_server.js`
- `node/server/tools/calendar_tools.js`
- `node/server/tools/sync_tools.js`
- `node/server/tools/config_tools.js`
- `node/server/admin_api.js`
- `node/server/python_bridge.js`

## Testing Checklist
- [ ] MCP server starts successfully
- [ ] Can connect MCP client
- [ ] Each tool returns valid response
- [ ] HTTP API endpoints respond
- [ ] Python bridge executes commands
- [ ] Errors handled gracefully
- [ ] Static files served correctly

## Dependencies
- MCP SDK
- Express.js
- Body-parser middleware

## Time Estimate
- 8-10 hours
