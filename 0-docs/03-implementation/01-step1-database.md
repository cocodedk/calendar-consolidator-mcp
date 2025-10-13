# Step 1: Database Setup

## Goal
Create SQLite database foundation with all tables and encryption

## Tasks

### Create Schema File
- [ ] Write `database/schema.sql` with all tables
- [ ] Add indexes for performance
- [ ] Insert default settings
- [ ] Test schema creation

### Implement ConfigStore Module
- [ ] Create `/python/state/config_store.py`
- [ ] Add database connection management
- [ ] Implement source CRUD operations
- [ ] Implement target CRUD operations
- [ ] Add mapping operations (create/read/update/delete)
- [ ] Add sync log operations
- [ ] Add settings operations

### Credential Encryption
- [ ] Choose encryption method (OS keychain vs local)
- [ ] Implement encrypt_credentials() function
- [ ] Implement decrypt_credentials() function
- [ ] Test with sample credentials
- [ ] Handle encryption errors gracefully

### Database Migrations
- [ ] Create migration system structure
- [ ] Add schema version tracking
- [ ] Implement init_db.py script
- [ ] Implement migrate.py script
- [ ] Test migration rollback

## Files to Create
- `database/schema.sql`
- `python/state/config_store.py`
- `python/state/encryption.py`
- `python/state/migrations/001_initial.py`
- `python/init_db.py`
- `python/migrate.py`

## Testing Checklist
- [ ] Database creates successfully
- [ ] All tables present
- [ ] Indexes created
- [ ] Default settings inserted
- [ ] Can insert/retrieve source
- [ ] Can set/retrieve target
- [ ] Can create/retrieve mappings
- [ ] Credentials encrypt/decrypt correctly
- [ ] Foreign keys enforce integrity

## Dependencies
- Python `sqlite3` (built-in)
- Python `keyring` (for OS keychain)
- Python `cryptography` (if using local encryption)

## Time Estimate
- 4-6 hours
