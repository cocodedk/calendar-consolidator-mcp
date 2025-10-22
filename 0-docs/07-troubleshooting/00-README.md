# Troubleshooting Guide

Common issues and solutions for Calendar Consolidator.

## By Provider

### Google Calendar
- [Google Calendar Issues Index](01-google-calendar-issues.md) - Overview of all issues
- [API Not Enabled (HTTP 403)](02-google-api-not-enabled.md) ⚠️ Most common!
- [Invalid Grant Error](03-google-invalid-grant.md) - Token expired/revoked
- [Redirect URI Mismatch](04-google-redirect-uri.md) - OAuth configuration

### Other Providers
- Microsoft/Azure Calendar Issues - Coming soon
- iCloud Calendar Issues - Coming soon

## By Category

### Authentication Issues
- **403 Forbidden**: API not enabled → See Google Calendar Issues
- **401 Unauthorized**: Token expired or invalid
- **Redirect URI mismatch**: OAuth configuration problem

### Sync Issues
- Events not appearing in target
- Duplicate events
- Sync timing problems
- Private events handling

### Configuration Issues
- Database connection errors
- Credential storage problems
- Settings not persisting

## Quick Diagnostic Steps

1. **Check Logs Page**: Most errors show detailed information
2. **Verify API Enablement**: Especially for new Google Cloud projects
3. **Re-authenticate**: Delete and re-add the source
4. **Check Permissions**: Ensure calendar sharing is configured
5. **Wait**: Some API changes take 2-5 minutes to propagate

## Most Common Issue

**Google Calendar API Not Enabled**
- Affects: New Google Cloud projects
- Error: HTTP 403 "API has not been used in project..."
- Fix: Enable API in Google Cloud Console
- Details: [Google Calendar Issues](01-google-calendar-issues.md)

## Support Resources

- Implementation docs: `/0-docs/03-implementation/`
- User guides: `/0-docs/06-user-guides/`
- API documentation: `/0-docs/04-api-design/`
