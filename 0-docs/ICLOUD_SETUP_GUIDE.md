# iCloud Calendar Setup Guide

## Prerequisites

1. **Apple ID with Two-Factor Authentication (2FA) Enabled**
   - iCloud CalDAV requires 2FA to be enabled on your Apple ID
   - Visit [Apple ID Account](https://appleid.apple.com/) to enable 2FA if not already enabled

2. **App-Specific Password**
   - You cannot use your regular Apple ID password for CalDAV access
   - You must generate an app-specific password specifically for Calendar Consolidator

## Step 1: Generate App-Specific Password

1. Go to [Apple ID Account Management](https://appleid.apple.com/)
2. Sign in with your Apple ID
3. In the "Sign-In and Security" section, select "App-Specific Passwords"
4. Click the "+" button or "Generate an app-specific password"
5. Enter a label (e.g., "Calendar Consolidator")
6. Click "Create"
7. **Copy the generated password** (format: xxxx-xxxx-xxxx-xxxx)
   - You won't be able to see it again!
   - Store it securely

Official Apple Guide: https://support.apple.com/en-us/HT204397

## Step 2: Add iCloud Calendar in Calendar Consolidator

1. **Open Calendar Consolidator Web UI**
   - Navigate to your Calendar Consolidator MCP instance

2. **Go to Sources Section**
   - Click on the "Sources" tab

3. **Add New Source**
   - Click "Add Source" button

4. **Select iCloud Calendar**
   - Choose "iCloud Calendar" from the provider options

5. **Enter Credentials**
   - **Apple ID:** Your full iCloud email (e.g., yourname@icloud.com)
   - **App-Specific Password:** The password you generated in Step 1
   - Click "Continue"

6. **Select Calendars**
   - After validation, you'll see a list of your iCloud calendars
   - Check the calendars you want to sync
   - Click "Add Selected"

## Step 3: Verify Setup

1. **Check Sources List**
   - Your selected iCloud calendars should appear in the sources list
   - Status should show as "Active"

2. **Run Initial Sync**
   - Navigate to "Dashboard" or "Sync" section
   - Trigger a sync operation
   - Events should start appearing in your target calendar

## Troubleshooting

### "Invalid credentials" Error

**Causes:**
- Using regular Apple ID password instead of app-specific password
- Incorrect Apple ID email
- App-specific password expired or revoked

**Solutions:**
1. Verify you're using the app-specific password, not your regular password
2. Check your Apple ID email is correct
3. Generate a new app-specific password and try again

### "Failed to connect to iCloud CalDAV" Error

**Causes:**
- Network connectivity issues
- iCloud services temporarily unavailable
- Firewall blocking CalDAV connections

**Solutions:**
1. Check your internet connection
2. Verify you can access https://caldav.icloud.com/ in your browser
3. Check firewall settings to allow HTTPS connections
4. Wait a few minutes and try again (iCloud may be experiencing issues)

### No Calendars Showing

**Causes:**
- No calendars created in iCloud
- Calendar permissions issue
- CalDAV sync not enabled for account

**Solutions:**
1. Visit iCloud.com and verify you have calendars
2. Ensure calendars are not shared/read-only calendars
3. Try creating a new calendar in iCloud and retry

### Events Not Syncing

**Causes:**
- Calendar marked as inactive
- Sync errors
- Target calendar not configured

**Solutions:**
1. Check source calendar status is "Active"
2. Review sync logs for error messages
3. Ensure target calendar is properly configured
4. Try removing and re-adding the source

## Security Notes

- **App-specific passwords are secure:** They provide limited access and can be revoked anytime
- **Credentials are encrypted:** Your password is stored securely in your system keychain
- **No data retention:** Credentials are only used for CalDAV connections
- **Revoke access:** You can revoke app-specific passwords at appleid.apple.com anytime

## Limitations

- **Full sync only:** iCloud CalDAV doesn't support delta sync like Google Calendar
  - All events are fetched each time
  - May be slower for calendars with many events

- **No attachment support:** Event attachments are not synced

- **Basic event properties:** Only core event fields are synced:
  - Title, description, location
  - Start/end times
  - All-day event flag

## Advanced Configuration

### Multiple iCloud Accounts

You can add calendars from multiple iCloud accounts:
1. Generate separate app-specific passwords for each account
2. Add sources separately for each account
3. Select calendars from each account

### Calendar Selection

You can add multiple calendars from the same iCloud account:
- Each calendar becomes a separate source
- Sources sync independently
- You can enable/disable individual calendars

### Updating Credentials

If you need to change the password:
1. Remove the existing iCloud source
2. Generate a new app-specific password
3. Add the source again with the new credentials

## Support

For issues specific to:
- **Apple ID/2FA:** Contact Apple Support
- **App-specific passwords:** Visit support.apple.com
- **Calendar Consolidator:** Check project documentation or file an issue

## Related Documentation

- [Add Source Implementation](./ADD_SOURCE_IMPLEMENTATION_SUMMARY.md)
- [iCloud Implementation Summary](./ICLOUD_IMPLEMENTATION_SUMMARY.md)
- [Apple CalDAV Documentation](https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/iCalendarServerProtocol/)
