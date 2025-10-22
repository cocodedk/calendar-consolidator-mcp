# Google Calendar Troubleshooting Index

## Quick Reference

This is the index for Google Calendar-related issues. Click the links below for
detailed guides on specific problems.

## Common Issues

### 1. [API Not Enabled (HTTP 403)](02-google-api-not-enabled.md) ⚠️ Most Common!

**Quick Summary**: Google Calendar API not enabled in project.

**Quick Fix**: Click URL from error message → Enable → Wait 2-3 minutes

**When**: Setting up Google Calendar for the first time, new Google Cloud project

---

### 2. [Invalid Grant Error](03-google-invalid-grant.md)

**Quick Summary**: Token expired or revoked.

**Quick Fix**: Delete source → Re-add → Complete OAuth flow again

**When**: After extended period, credentials changed, user revoked access

---

### 3. [Redirect URI Mismatch](04-google-redirect-uri.md)

**Quick Summary**: OAuth redirect URI doesn't match configuration.

**Quick Fix**: Update redirect URIs in Google Cloud Console to match app

**When**: During OAuth flow, after changing application configuration

---

### 4. Calendar Not Found

**Error**: `Calendar not found or access denied`

**Causes**:
- Calendar was deleted
- Sharing permissions changed
- Calendar owner removed access

**Quick Fix**:
1. Verify calendar exists in Google Calendar web interface
2. Check sharing permissions (must have write access for target)
3. Re-authenticate the source if needed

---

## Prevention Checklist

Before adding a Google Calendar source:

- [ ] Google Cloud project created
- [ ] **Google Calendar API enabled** ⚠️ Most important!
- [ ] OAuth consent screen configured
- [ ] OAuth Client ID created (Desktop app type)
- [ ] Client credentials downloaded
- [ ] Credentials added to Calendar Consolidator settings

---

## Getting Help

If issues persist after trying these solutions:

1. Check Logs page in Calendar Consolidator
2. Look for detailed error messages
3. Verify all setup steps in `/0-docs/03-implementation/15-step15-google-setup.md`
4. Ensure test user added to OAuth consent screen (during development)
