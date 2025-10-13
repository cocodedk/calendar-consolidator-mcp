# Documentation Index - Calendar Consolidator MCP

## Overview

This documentation is organized into micro-focused files following modular guidelines (< 100 lines per file, single purpose).

## Documentation Structure

### 01-overview/
Project overview and context
- **[01-purpose.md](01-overview/01-purpose.md)** - What this project does
- **[02-constraints.md](01-overview/02-constraints.md)** - Technical and functional constraints
- **[03-tech-stack.md](01-overview/03-tech-stack.md)** - Technology choices
- **[04-deployment-model.md](01-overview/04-deployment-model.md)** - Deployment phases
- **[05-success-criteria.md](01-overview/05-success-criteria.md)** - Success metrics per phase

### 02-architecture/
System design and components
- **[01-high-level.md](02-architecture/01-high-level.md)** - System architecture diagram
- **[02-web-ui.md](02-architecture/02-web-ui.md)** - Frontend component
- **[03-mcp-server.md](02-architecture/03-mcp-server.md)** - Node.js MCP server
- **[04-python-worker.md](02-architecture/04-python-worker.md)** - Python sync engine
- **[05-data-flow.md](02-architecture/05-data-flow.md)** - Data flow diagrams
- **[06-security-model.md](02-architecture/06-security-model.md)** - Security design

### 03-implementation/
Step-by-step implementation plan
- **[00-phase0-setup.md](03-implementation/00-phase0-setup.md)** - MVP development environment
- **[01-step1-database.md](03-implementation/01-step1-database.md)** - Database setup
- **[02-step2-graph-connector.md](03-implementation/02-step2-graph-connector.md)** - Microsoft Graph connector
- **[03-step3-event-model.md](03-implementation/03-step3-event-model.md)** - Event model & sync logic
- **[04-step4-mcp-server.md](03-implementation/04-step4-mcp-server.md)** - MCP server implementation
- **[05-step5-web-ui.md](03-implementation/05-step5-web-ui.md)** - Web UI implementation
- **[06-step6-caldav.md](03-implementation/06-step6-caldav.md)** - CalDAV support
- **[07-step7-advanced-sync.md](03-implementation/07-step7-advanced-sync.md)** - Advanced sync features
- **[08-step8-ui-polish.md](03-implementation/08-step8-ui-polish.md)** - UI polish
- **[09-step9-security-monitoring.md](03-implementation/09-step9-security-monitoring.md)** - Security & monitoring
- **[10-step10-testing-docs.md](03-implementation/10-step10-testing-docs.md)** - Testing & documentation
- **[11-step11-docker.md](03-implementation/11-step11-docker.md)** - Docker containerization
- **[12-step12-electron-setup.md](03-implementation/12-step12-electron-setup.md)** - Electron setup
- **[13-step13-cross-platform.md](03-implementation/13-step13-cross-platform.md)** - Cross-platform builds
- **[14-step14-distribution.md](03-implementation/14-step14-distribution.md)** - Distribution & polish

### 04-api-design/
API specifications
- **[01-mcp-tools.md](04-api-design/01-mcp-tools.md)** - MCP calendar & sync tools
- **[02-mcp-config-tools.md](04-api-design/02-mcp-config-tools.md)** - MCP configuration tools
- **[03-http-config-endpoints.md](04-api-design/03-http-config-endpoints.md)** - HTTP configuration API
- **[04-http-sync-endpoints.md](04-api-design/04-http-sync-endpoints.md)** - HTTP sync API
- **[05-data-types.md](04-api-design/05-data-types.md)** - TypeScript interfaces
- **[06-error-handling.md](04-api-design/06-error-handling.md)** - Error codes & handling

### 05-database/
Database schema and storage
- **[01-sources-table.md](05-database/01-sources-table.md)** - Sources table schema
- **[02-target-table.md](05-database/02-target-table.md)** - Target table schema
- **[03-mappings-table.md](05-database/03-mappings-table.md)** - Mappings table schema
- **[04-sync-logs-table.md](05-database/04-sync-logs-table.md)** - Sync logs table schema
- **[05-settings-table.md](05-database/05-settings-table.md)** - Settings table schema
- **[06-credential-storage.md](05-database/06-credential-storage.md)** - Credential encryption

### Testing Documentation
- **[PYTEST_COMPLETE.md](PYTEST_COMPLETE.md)** - Test suite summary (81 tests, 100% passing)
- **[TEST_SUITE_SUMMARY.md](TEST_SUITE_SUMMARY.md)** - Detailed test coverage breakdown
- **[TEST_INVENTORY.md](TEST_INVENTORY.md)** - File-by-file test inventory
- **[TESTING_QUICKSTART.md](TESTING_QUICKSTART.md)** - Quick start guide for running tests
- **[TEST_REPORT.md](TEST_REPORT.md)** - Initial implementation test report

### Legacy Documents
- **[prd.md](prd.md)** - Original Product Requirements Document (reference)

## Quick Start

For immediate setup instructions, see: **[00-phase0-setup.md](03-implementation/00-phase0-setup.md)**

## Reading Order

### For Developers Starting Implementation
1. 01-overview/01-purpose.md
2. 01-overview/02-constraints.md
3. 02-architecture/01-high-level.md
4. 03-implementation/00-phase0-setup.md
5. Follow steps 01-05 in 03-implementation/

### For Understanding the System
1. 01-overview/ (all files)
2. 02-architecture/ (all files)
3. 05-database/ (all files)
4. 04-api-design/ (all files)

### For Planning Features
1. 03-implementation/ (all steps)
2. 01-overview/05-success-criteria.md
3. 04-api-design/ (all files)

## Documentation Principles

- **Micro-focused**: Each file < 100 lines
- **Single purpose**: One topic per file
- **Modular**: Easy to navigate and update
- **Actionable**: Clear steps and examples
