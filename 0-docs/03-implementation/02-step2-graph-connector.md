# Step 2: Microsoft Graph Connector

## Goal
Implement Microsoft Graph API integration for calendar access

## Tasks

### OAuth Flow
- [ ] Implement device code flow for auth
- [ ] Handle OAuth redirect (localhost callback)
- [ ] Store access token securely
- [ ] Store refresh token securely
- [ ] Test auth flow end-to-end

### Graph API Client
- [ ] Create base GraphConnector class
- [ ] Initialize MSAL client
- [ ] Implement token refresh logic
- [ ] Handle token expiration
- [ ] Add error handling and retries

### Calendar Listing
- [ ] Implement list_calendars() method
- [ ] Parse calendar response
- [ ] Return normalized calendar info
- [ ] Test with real Microsoft account

### Event CRUD Operations
- [ ] Implement create_event() method
- [ ] Implement update_event() method
- [ ] Implement delete_event() method
- [ ] Implement get_event() method
- [ ] Test all operations

### Delta Sync Support
- [ ] Implement get_events_delta() method
- [ ] Handle delta link/token
- [ ] Parse delta response
- [ ] Handle deleted events (tombstones)
- [ ] Test incremental sync

## Files to Create
- `python/connectors/graph_connector.py`
- `python/connectors/graph_auth.py`
- `python/connectors/base_connector.py`

## Testing Checklist
- [ ] OAuth flow completes successfully
- [ ] Can list user's calendars
- [ ] Can create test event
- [ ] Can update existing event
- [ ] Can delete event
- [ ] Delta sync returns only changed events
- [ ] Token refresh works
- [ ] Handles rate limits gracefully

## Dependencies
- `msal` - Microsoft authentication library
- `msgraph-core` - Graph API client
- `requests` - HTTP client

## Time Estimate
- 8-10 hours

## Notes
- Use minimal OAuth scopes: `Calendars.ReadWrite`
- Test with personal Microsoft account first
- Handle pagination for large calendars
- Respect rate limits (exponential backoff)
