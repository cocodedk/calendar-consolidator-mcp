# High-Level Architecture - Calendar Consolidator MCP

## System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   MCP Server    │    │  Python Worker  │
│   (Frontend)    │◄──►│   (Node.js)     │◄──►│   (Sync Engine) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   HTTP API      │    │   Connectors    │
                       │   (Admin)       │    │   (Graph/CalDAV)│
                       └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SQLite DB     │    │   External APIs │
                       │   (Config/State)│    │   (Microsoft/   │
                       └─────────────────┘    │    iCloud)      │
                                             └─────────────────┘
```

## Component Layers

### Presentation Layer
- **Web UI**: Browser-based interface
- **Electron Window**: Desktop app wrapper (Phase 5)

### Application Layer
- **MCP Server**: Tool definitions and orchestration
- **HTTP API**: REST endpoints for UI
- **Python Bridge**: Subprocess/IPC to worker

### Business Logic Layer
- **Sync Engine**: Core sync algorithm
- **Connectors**: API-specific implementations
- **Event Model**: Normalized event representation

### Data Layer
- **SQLite Database**: Configuration and state
- **OS Keychain**: Credential storage
- **File System**: Logs and backups

### Integration Layer
- **Microsoft Graph API**: Cloud calendar access
- **CalDAV Protocol**: Standard calendar access
- **OAuth Providers**: Authentication services
