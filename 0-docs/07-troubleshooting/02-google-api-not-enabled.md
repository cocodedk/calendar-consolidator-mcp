# Google Calendar API Not Enabled (HTTP 403)

## Error Message

```
Error listing calendars: Error: Python process exited with code 1:
{"error": "<HttpError 403 when requesting
https://www.googleapis.com/calendar/v3/users/me/calendarList?alt=json
returned \"Google Calendar API has not been used in project [PROJECT_ID]
before or it is disabled..."
```

## What This Means

The Google Calendar API hasn't been activated in your Google Cloud project.
This is the **#1 most common setup issue** for new Google Calendar integrations.

## Quick Fix (Recommended)

1. **Use the direct link from the error message:**
   - The error includes a URL like:
     `https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview?project=XXXXXX`
   - Click that link (or copy-paste into browser)
   - Click the blue "Enable" button
   - Wait 2-3 minutes for propagation

2. **Try again:**
   - Return to Calendar Consolidator
   - Attempt to list calendars again
   - Should work after the propagation delay

## Alternative Method

If the direct link doesn't work:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (check project ID matches error)
3. Click hamburger menu → "APIs & Services" → "Library"
4. Search for "Google Calendar API"
5. Click on it and press the blue "Enable" button
6. Wait 2-3 minutes

## Why This Happens

When you create a new Google Cloud project, **no APIs are enabled by default**.
You must explicitly enable each API your application needs.

Many developers skip Step 2 in the setup guide or forget to wait for propagation.

## Prevention

Before adding a Google Calendar source:

- [ ] Google Cloud project created
- [ ] **Google Calendar API enabled** ⚠️ Critical!
- [ ] Waited 2-3 minutes after enabling
- [ ] OAuth consent screen configured
- [ ] OAuth Client ID created

## Related Documentation

- [Google Setup Guide](../03-implementation/15-step15-google-setup.md)
- [Troubleshooting Index](00-README.md)
