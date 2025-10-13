# Step 3: Event Model & Sync Logic

## Goal
Create normalized event model and core sync algorithm

## Tasks

### Event Class
- [ ] Define Event class with all fields
- [ ] Add normalization from Graph format
- [ ] Add normalization from CalDAV format (future)
- [ ] Implement timezone conversion
- [ ] Handle all-day events
- [ ] Test event creation and parsing

### Hash Computation
- [ ] Define which fields to hash
- [ ] Implement compute_hash() method
- [ ] Test hash stability
- [ ] Test hash changes on updates

### Recurrence Handling
- [ ] Parse RRULE from both formats
- [ ] Normalize recurrence rules
- [ ] Handle EXDATE (exception dates)
- [ ] Handle single instance modifications
- [ ] Test recurring event scenarios

### Diff Computation
- [ ] Create Diff class
- [ ] Implement compute_diff() function
- [ ] Detect events to create
- [ ] Detect events to update
- [ ] Detect events to delete
- [ ] Return structured diff summary

### Sync Once Implementation
- [ ] Create Syncer class
- [ ] Load configuration from database
- [ ] Fetch delta from source
- [ ] Compute diff against mappings
- [ ] Apply changes to target
- [ ] Update mappings table
- [ ] Save sync token
- [ ] Log results

### Dry Run Implementation
- [ ] Create DryRunSyncer subclass
- [ ] Override write methods to no-op
- [ ] Collect changes without applying
- [ ] Return preview summary

## Files to Create
- `python/model/event.py`
- `python/model/diff.py`
- `python/sync/syncer.py`
- `python/sync/dry_run_syncer.py`

## Testing Checklist
- [ ] Events normalize correctly from Graph
- [ ] Hash computation is consistent
- [ ] Hash changes when event modified
- [ ] Diff correctly identifies creates
- [ ] Diff correctly identifies updates
- [ ] Diff correctly identifies deletes
- [ ] Sync creates events in target
- [ ] Sync updates existing events
- [ ] Sync deletes removed events
- [ ] Mappings updated correctly
- [ ] Dry run returns accurate preview
- [ ] Recurring events handled properly

## Time Estimate
- 10-12 hours

## Notes
- Start simple, handle edge cases later
- Defer complex recurrence to Phase 2
- Focus on non-recurring events for MVP
