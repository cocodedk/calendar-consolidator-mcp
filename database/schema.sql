-- Calendar Consolidator MCP - Database Schema
-- SQLite 3 schema for configuration and state storage

-- Sources table: Store source calendar configurations
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL CHECK (type IN ('graph', 'caldav', 'google')),
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB NOT NULL,
  sync_token TEXT,
  active BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(type);
CREATE INDEX IF NOT EXISTS idx_sources_active ON sources(active);

-- Target table: Store target calendar configuration (single row)
CREATE TABLE IF NOT EXISTS target (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  type TEXT NOT NULL CHECK (type IN ('graph', 'caldav', 'google')),
  calendar_id TEXT NOT NULL,
  name TEXT,
  cred_blob BLOB NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Mappings table: Track source → target event mappings
CREATE TABLE IF NOT EXISTS mappings (
  source_id INTEGER NOT NULL,
  source_event_uid TEXT NOT NULL,
  target_event_id TEXT NOT NULL,
  last_hash TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(source_id, source_event_uid),
  FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_mappings_source ON mappings(source_id);
CREATE INDEX IF NOT EXISTS idx_mappings_target ON mappings(target_event_id);

-- Sync logs table: Record sync operation history
CREATE TABLE IF NOT EXISTS sync_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER,
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status TEXT NOT NULL CHECK (status IN ('success', 'error', 'partial')),
  created_count INTEGER DEFAULT 0,
  updated_count INTEGER DEFAULT 0,
  deleted_count INTEGER DEFAULT 0,
  error_message TEXT,
  duration_ms INTEGER,
  FOREIGN KEY(source_id) REFERENCES sources(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_sync_logs_timestamp ON sync_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_sync_logs_source ON sync_logs(source_id);

-- Settings table: Global configuration
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default settings
INSERT OR IGNORE INTO settings (key, value) VALUES
  ('continuous_sync_enabled', 'false'),
  ('sync_interval_minutes', '5'),
  ('ignore_private_events', 'false'),
  ('max_retry_attempts', '3'),
  ('encryption_key_id', 'default');
