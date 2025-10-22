import sqlite3, pathlib
home = pathlib.Path.home()
db_path = home/'.calendar-consolidator'/'config.db'
print('DB:', db_path)
if not db_path.exists():
    print('DB not found')
    raise SystemExit
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cur = conn.cursor()
print('\nSources:')
for row in cur.execute('SELECT id, type, calendar_id, name, sync_token, active FROM sources'):
    print(dict(row))
print('\nTarget:')
row = cur.execute('SELECT type, calendar_id, name FROM target').fetchone()
print(dict(row) if row else None)
print('\nMappings (count):', cur.execute('SELECT COUNT(*) FROM mappings').fetchone()[0])
for row in cur.execute('SELECT source_id, source_event_uid, target_event_id, substr(last_hash,1,8) AS h, created_at, updated_at FROM mappings LIMIT 50'):
    print(dict(row))
print('\nRecent sync logs:')
for row in cur.execute('SELECT timestamp, status, created_count, updated_count, deleted_count, error_message FROM sync_logs ORDER BY timestamp DESC LIMIT 5'):
    print(dict(row))
