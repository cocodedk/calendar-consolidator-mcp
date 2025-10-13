# Data Flow - Calendar Consolidator MCP

## Configuration Flow

### Add Source Calendar
1. User clicks "Add Source" in UI
2. UI sends POST to `/api/source`
3. Node server triggers OAuth flow
4. User authenticates in browser
5. OAuth redirect captured by Node server
6. Python worker lists available calendars
7. Node returns calendar list to UI
8. User selects calendar
9. Credentials encrypted and stored in SQLite
10. UI refreshes to show new source

### Set Target Calendar
1. User clicks "Set Target" in UI
2. Similar OAuth flow as add source
3. Only one target allowed (enforced by DB)
4. UI shows target calendar details

## Sync Flow

### Preview Sync
1. User clicks "Preview Sync" in UI
2. UI sends POST to `/api/preview`
3. Node spawns Python dry-run worker
4. Python loads config from SQLite
5. Python fetches delta from each source
6. Python computes diff (no writes)
7. Python returns diff summary
8. Node sends summary to UI
9. UI displays counts and samples

### Execute Sync
1. User clicks "Sync Now" in UI
2. UI sends POST to `/api/sync`
3. Node spawns Python sync worker
4. Python loads config from SQLite
5. For each active source:
   - Fetch delta using sync token
   - Normalize events
   - Compute diff
   - Apply changes to target
   - Update mappings
   - Save new sync token
6. Python logs results to sync_logs
7. Python returns summary
8. Node sends results to UI
9. UI displays sync results

## Status/Log Flow

### View Logs
1. UI polls `/api/logs` periodically
2. Node queries SQLite sync_logs table
3. Node returns recent logs
4. UI displays log entries

### Get Status
1. UI requests `/api/status`
2. Node queries SQLite for sources/target
3. Node checks last sync timestamp
4. Node returns status object
5. UI updates dashboard
