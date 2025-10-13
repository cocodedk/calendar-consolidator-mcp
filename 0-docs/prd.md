# Product Requirements Document (Calendar-Consolidation MCP)

## 1. Overview & Purpose

### 1.1 Purpose

To build a lightweight, user-friendly system (MCP server + UI) that non-technical users can use to consolidate multiple calendars (Microsoft, iCloud/CalDAV, etc.) into a single unified calendar. The system should support one-way mirroring (source → target), incremental syncing, and an interface for configuration and monitoring. Optionally, a chat interface for management.

### 1.2 Goals & Non-Goals

**Goals (in scope):**

* Allow the user to **add calendar sources** (Microsoft Graph, iCloud / CalDAV).
* Allow the user to **select a target (destination) calendar** where events are copied or mirrored.
* Perform **incremental syncs**: new, updated, and deleted events.
* Maintain **mappings and deduplication** so duplicates are avoided and updates are consistent.
* Provide a simple **UI** for configuration, previews, and manual sync.
* Expose the sync functionality via MCP tools so an AI/agent can drive it.
* Persist all configuration state (sources, target, credentials, sync tokens, mappings) safely and durably.
* Provide basic error handling, logs, status views.

**Non-Goals (deferred / out of scope initially):**

* **Two-way sync** (edits in target going upstream).
* Advanced conflict resolution strategies (merging changes from multiple sources into a single event).
* Bulk import / export features.
* Full multi-tenant / user management.
* Desktop native apps beyond web UI.
* Offline synchronization or local-first modes.
* Real-time collaborative editing of events.
* Sophisticated heuristics (fuzzy matching, AI merging).
* UI features beyond basic configuration and logging.

---

## 2. User Stories & Workflows

### 2.1 User Stories

1. **As a user**, I want to connect my Outlook / Microsoft 365 calendar so it can be part of the consolidation.
2. **As a user**, I want to connect my iCloud (or CalDAV) calendar so it also contributes.
3. **As a user**, I want to choose one calendar as the destination / consolidated calendar.
4. **As a user**, I want to see which calendars are configured and whether they are active or disabled.
5. **As a user**, I want to preview what changes (create / update / delete) will happen before syncing.
6. **As a user**, I want to click “Sync now” to manually perform a sync.
7. **As a user**, I want to see a log of recent sync runs and any errors.
8. **As a user**, I want to modify or remove source calendars and change the target.
9. **(Later)** As a user, I want to ask via chat: “Show me the last sync summary” or “Add my iCloud calendar”.

### 2.2 High-level Workflows

#### Setup / Configuration

1. User visits web UI, is prompted to add a **Source Calendar**.
2. User picks a source type (Microsoft or iCloud/CalDAV).

   * If Microsoft: UI triggers OAuth flow, gets token, backend fetches list of calendars, user selects calendar(s).
   * If iCloud/CalDAV: UI prompts for credentials (app password, CalDAV server, username), backend tests and fetches available calendars, user picks one.
3. User names the source (alias) optionally.
4. User then configures the **Target Calendar** similarly (type, credentials, calendar selection).
5. UI shows the summary: Source(s) and Target, with ability to enable / disable / remove sources.

#### Preview / Sync Run

1. User clicks “Preview Sync”.
2. Backend runs a **dry-run** of the sync logic without writing, computing:

   * Events to create
   * Events to update
   * Events to delete
3. UI presents the counts and optionally a small example list.
4. User clicks “Sync Now”.
5. Backend runs **syncOnce**: executes the real changes, updates mappings, tokens, logs.
6. UI shows summary: how many created / updated / deleted, any errors.

#### Ongoing Operation / Continuous Sync

* Optionally the user can enable continuous syncing (e.g. every 5 min).
* The backend scheduler / loop runs sync for each source, handles new data.
* UI shows last sync timestamp, next scheduled run, and any errors.

#### Reconfiguration

* User can add new sources or remove existing ones.
* Changing the target calendar triggers a full resync (or mapping reset).
* The UI should warn “Changing target will re-create events / remove old ones from prior target”.

---

## 3. Data & Persistence

### 3.1 Entities & Schema

You’ll maintain the following data entities:

* **SourceConfig**: id, type (“graph” or “caldav”), calendar_id, alias/name, credentials (token / settings), sync_token, active flag
* **TargetConfig**: id, type, calendar_id, alias, credentials
* **Mapping**: source_id, source_event_uid → target_event_id, last_hash
* **SyncLog**: timestamp, counts, errors, status
* **Rules / Settings**: dedupe thresholds, ignore private events, etc.

### 3.2 Storage Design

* Use **SQLite** database (file) as the core store.
* All configuration (sources, target) and state (sync tokens, mappings, logs) live in the SQLite DB.
* Credentials (access tokens, refresh tokens, secrets) stored encrypted (or at least obfuscated) in the database (or optionally in an OS keychain / vault).
* On startup, backend loads configuration from DB via a **ConfigStore** module.
* Provide APIs to mutate these configs (add source, set target, deactivate source, etc.).

### 3.3 Schema Example (simplified)

```sql
CREATE TABLE sources (
  id INTEGER PRIMARY KEY,
  type TEXT NOT NULL,
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB,
  sync_token TEXT,
  active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE target (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  type TEXT NOT NULL,
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB
);

CREATE TABLE mappings (
  source_id INTEGER NOT NULL,
  source_event_uid TEXT NOT NULL,
  target_event_id TEXT NOT NULL,
  last_hash TEXT,
  PRIMARY KEY(source_id, source_event_uid),
  FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
);

CREATE TABLE sync_logs (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME NOT NULL,
  created_count INTEGER,
  updated_count INTEGER,
  deleted_count INTEGER,
  error_message TEXT
);

CREATE TABLE settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
```

* The `target` table is forced to only allow one row (id = 1) for MVP.
* `cred_blob` holds encrypted JSON blobs with tokens.
* `settings` stores global flags (e.g. `continuous_sync_enabled`, `sync_interval_minutes`).

---

## 4. Module / Component Design (Python + Node)

### 4.1 Python Worker (Sync Engine & Connectors)

**Packages / modules:**

* `connectors/graph_connector.py` — Graph auth, delta fetch, write (create/update/delete)
* `connectors/caldav_connector.py` — CalDAV sync, write methods
* `model/event.py` — Event class, recurrence, exceptions
* `model/diff.py` — Diff logic: compute creates, updates, deletes
* `state/config_store.py` — ConfigStore interface for sources, target, tokens, mappings
* `sync/syncer.py` — Main sync logic (syncOnce)
* `sync/dry_run_syncer.py` — Dry-run variant for preview
* `sync/scheduler.py` — Loop / periodic sync (optional)

Each module should be limited in size; if a file goes large, split (e.g. `graph_read.py`, `graph_write.py`).

### 4.2 Node MCP Server + UI Layer

**Packages / modules:**

* `server/index.js` — Entry point, bootstrap MCP server and admin HTTP API
* `server/tools/` — MCP tool definitions (listCalendars, syncOnce, previewSync, etc.)
* `server/admin_api.js` — HTTP routes for UI actions (add source, get config, trigger sync, logs)
* `server/cli_launcher.js` — Spawn / invoke Python worker commands (via child_process or RPC)
* `server/static/` — Frontend static files (HTML, CSS, JS) for UI
* `server/shared/` — JSON schema, types shared between UI and tools

UI (frontend) can be a minimal single-page app (React, Vue, or simple vanilla JS) to display forms and status.

---

## 5. APIs & Tool Interfaces

### 5.1 MCP Tools (Node side)

* `listCalendars(sourceType: "graph"|"caldav") → CalendarInfo[]`
* `previewSync(sources: SourceRef[], target: TargetRef) → DiffSummary`
* `syncOnce(sources: SourceRef[], target: TargetRef) → SyncResult`
* `getEvent(target: TargetRef, eventId: string) → EventDetail`
* `setRules(rules: RuleConfig) → Success`
* `addSource(sourceConfig) → Success`
* `removeSource(sourceId) → Success`
* `setTarget(targetConfig) → Success`

These tools internally call the Python worker (or orchestrate operations) and return JSON serializable objects.

### 5.2 Admin HTTP API (for UI)

* `GET /api/config` → returns current sources, target, status
* `POST /api/source` → body: type, credentials (or token), selected calendar_id(s) → adds a source
* `DELETE /api/source/:sourceId` → remove a source
* `POST /api/target` → set or change target calendar
* `POST /api/preview` → triggers previewSync, returns diff summary
* `POST /api/sync` → triggers syncOnce, returns sync result
* `GET /api/logs` → returns recent sync logs
* `POST /api/settings` → adjust settings like sync interval

The UI frontend calls these endpoints to configure and control the sync.

---

## 6. Sync Logic & Edge Cases

### 6.1 Sync / Diff Algorithm (syncOnce)

For each active source:

1. Fetch changed events (delta or sync) since last sync token.
2. For each event change:

   * Normalize to `Event` model.
   * Lookup mapping via `source_id + source_event_uid`.
   * Compute a hash of “key attributes” (start, end, summary, etc.).
   * If mapping absent and event not deleted → **create** in target, insert mapping.
   * If mapping exists:

     * If marked deleted upstream → **delete** target, remove mapping.
     * Else if hash changed → **update** target event, update mapping.
   * Else (mapping exists, no change) → skip.
3. After processing, update the source’s sync token in config store.
4. Return counts and any errors.

### 6.2 Preview (dry run)

Same as above, but instead of writing to target or updating mapping, just simulate and return a diff summary (what *would* happen).

### 6.3 Handling Recurrence / Exceptions

* Recurring series should use iCalendar-style `RRULE`, `EXDATE` / `EXCEPTIONS` handling.
* If a specific instance in a series is modified or deleted (via `RECURRENCE-ID`), your logic should treat it as an “exception” event.
* Mapping should consider `source_event_uid` including `RECURRENCE-ID` when present.

### 6.4 Deletions / Tombstones

* Graph delta and CalDAV sync APIs typically indicate deletions; treat them to delete the target event and mapping.
* If mapping exists but no corresponding source event or tombstone, you may want to periodically “clean up” stale mappings (e.g. full reconciliation scan).

### 6.5 Time Zones & DST

* Store times in UTC internally (or with timezone info).
* Convert appropriately when writing to target calendar (ensuring correct local times).
* Handle daylight savings shifts properly (test recurring events that span DST boundaries).

### 6.6 Visibility / Privacy / Confidential Events

* If a source event is private / marked “busy only”, the consolidated target event might choose to redact details (e.g. only “Busy” with no summary).
* The user can configure via rules whether to include private events or not.

### 6.7 Error Handling & Retry

* On API errors (rate limits, transient network), retry with exponential backoff.
* On credentials expiration, detect and surface UI prompts to reauthorize.
* Log detailed error messages to sync_logs.
* If a particular event write fails repeatedly, skip and continue (don’t block the entire sync).

---

## 7. UI / UX Design

### 7.1 Layout & Screens

* **Dashboard / Status**: shows last sync time, upcoming scheduled sync, error indicator
* **Sources & Target**: list of configured calendars, with “edit / remove / disable” controls
* **Add Source / Add Target Wizard**: multi-step form for selecting type, authenticating, picking calendar
* **Preview & Sync Controls**: buttons to preview and sync, show summaries
* **Log / Error View**: timestamped list of recent sync logs and error messages
* **Settings / Rules**: configurable options (ignore private, dedupe windows)

### 7.2 Flow Examples

* When user clicks “Add Source → Microsoft”, UI opens OAuth login (popup or redirect). On success, backend stores and returns list of calendars; UI shows checkboxes to pick which ones.
* On “Preview Sync”, UI fetches diff summary via `/api/preview` and displays counts, maybe 5 sample event titles.
* On “Sync Now”, UI calls `/api/sync` and displays a toast or modal with results or any errors.
* If credentials expire, UI shows a “Reconnect / Reauthorize” button next to that calendar.

---

## 8. Security & Permissions

* Protect the UI (admin pages) behind a **local password / token** so casual users don’t tamper.
* Encrypt stored credentials (use symmetric encryption with a key derived from user password or OS keychain).
* Use least-privilege OAuth scopes (only calendar read/write).
* Sanitize all inputs to avoid injection or malformed data.
* Ensure HTTP admin API is only exposed locally (bind to `localhost`) unless user explicitly enables remote access.
* Log and monitor errors without exposing raw tokens.

---

## 9. MVP & Iteration Priorities

1. **Core sync pipeline**: Graph source → Graph target, syncOnce & preview.
2. **Config persistence**: add / remove sources, set target, store sync tokens / mappings.
3. **UI for configuration / sync / preview**.
4. **CalDAV connector** for a second source type.
5. **Continuous / scheduled sync**.
6. **Error handling, logs, reauthorization flows**.
7. **Chat interface** wrap (UI / agent-based).

Focus first on what’s absolutely required to prove the concept and get a usable MVP. Defer fancy UI and extra features until core sync is stable.
