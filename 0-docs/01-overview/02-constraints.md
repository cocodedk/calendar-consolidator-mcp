# Key Constraints - Calendar Consolidator MCP

## Technical Constraints

### MVP Focus
- **Graph → Graph sync first**
- Microsoft 365 calendars only initially
- CalDAV support deferred to Phase 2

### Storage
- **SQLite storage**: Single-file database
- Location: `~/.calendar-consolidator/config.db`
- No external database servers required

### Security
- **Local-only**: Bind to localhost for security
- No remote access without explicit configuration
- Physical machine access = authorized user

### Architecture
- **Modular design**: Small files, single responsibility
- Each module under 100 lines where possible
- Clear separation of concerns

## Functional Constraints

### Sync Direction
- **No two-way sync**: Source → Target only
- Read from sources, write to target
- Target calendar changes NOT synced back

### User Model
- **Single-user**: Personal desktop tool
- Not multi-tenant SaaS
- One user per installation

### Performance Targets
- < 5 seconds for 100 events
- Incremental sync using delta APIs
- Minimal API calls to avoid rate limits
