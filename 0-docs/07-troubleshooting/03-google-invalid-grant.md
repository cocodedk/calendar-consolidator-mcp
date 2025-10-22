# Google Invalid Grant Error

## Error Message

```
invalid_grant: Token has been expired or revoked
```

## Causes

- **OAuth token expired**: Typical after 1 hour for access tokens
- **User revoked access**: User removed app from Google account settings
- **Credentials changed**: Client ID/Secret modified in Google Cloud Console
- **OAuth consent screen modified**: Changes to scopes or configuration

## Solution

### Quick Fix
1. **Delete the source** in Calendar Consolidator
2. **Re-add** the Google Calendar source
3. **Complete OAuth flow** again with fresh credentials

### Detailed Steps

1. **In Calendar Consolidator:**
   - Go to Sources page
   - Find the Google Calendar source
   - Click "Delete" or "Remove"

2. **Re-authenticate:**
   - Click "Add Source"
   - Select "Google Calendar"
   - Follow OAuth flow
   - Sign in with Google account
   - Grant permissions
   - Select calendars

3. **Verify:**
   - Check that calendars list properly
   - Try a test sync

## Prevention

### For Token Expiration
- Application should refresh tokens automatically
- If not, re-authenticate when errors occur

### For Revoked Access
- Educate users not to revoke access through Google settings
- Instead, use application's "Delete Source" feature

### For Credential Changes
- Never modify credentials while sources are active
- If you must change credentials:
  1. Delete all Google sources
  2. Update credentials in application settings
  3. Re-add sources with new OAuth flow

## Related Errors

- `Token has been revoked`
- `invalid_client`
- `unauthorized_client`

All follow similar resolution: delete source and re-authenticate.

## Related Documentation

- [Google Setup Guide](../03-implementation/15-step15-google-setup.md)
- [Troubleshooting Index](00-README.md)
