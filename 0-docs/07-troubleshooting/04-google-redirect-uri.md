# Google Redirect URI Mismatch

## Error Message

```
redirect_uri_mismatch: The redirect URI in the request does not match
the authorized redirect URIs configured for the OAuth application.
```

## Cause

The OAuth redirect URI your application is using doesn't match what's configured
in your Google Cloud Console OAuth 2.0 Client ID settings.

## Solution

### For Desktop Applications

1. **Go to Google Cloud Console**
   - [console.cloud.google.com](https://console.cloud.google.com/)
   - Select your project

2. **Navigate to Credentials**
   - Menu → "APIs & Services" → "Credentials"
   - Find your OAuth 2.0 Client ID
   - Click the pencil (edit) icon

3. **Check Authorized Redirect URIs**

   For **desktop apps**, you need one of:
   - `http://localhost` (for localhost redirect)
   - `http://localhost:PORT` (if specific port, e.g., `http://localhost:8080`)
   - `urn:ietf:wg:oauth:2.0:oob` (for out-of-band/OOB flow)

4. **Add Missing URI**
   - Click "Add URI"
   - Enter the correct redirect URI
   - Click "Save"
   - Wait 2-3 minutes for propagation

5. **Try Authentication Again**
   - Return to Calendar Consolidator
   - Attempt OAuth flow again

## Common Mistakes

### Wrong Application Type
- If you created a "Web application" instead of "Desktop app"
- **Fix**: Create a new OAuth 2.0 Client ID with correct type

### HTTPS vs HTTP
- Using `https://localhost` when should be `http://localhost`
- **Fix**: Ensure HTTP (not HTTPS) for localhost

### Port Mismatch
- App uses `http://localhost:8080` but configured `http://localhost:3000`
- **Fix**: Match the port exactly

## Verification

After fixing:
1. Clear browser cache (if browser-based OAuth)
2. Delete and re-add source in Calendar Consolidator
3. Complete OAuth flow
4. Should succeed without redirect_uri_mismatch

## Related Documentation

- [Google Setup Guide](../03-implementation/15-step15-google-setup.md)
- [OAuth Configuration](../03-implementation/15-step15-google-setup.md#4-create-oauth-client-id)
- [Troubleshooting Index](00-README.md)
