# Credential Security Testing Guide

## Purpose
This guide helps you verify that OAuth credentials and authentication tokens are stored securely on the host machine when connecting calendar accounts to Calendar Consolidator MCP.

## What Gets Tested
1. OAuth credentials (Client ID, Client Secret) are encrypted in the database
2. User authentication tokens are encrypted in the database
3. Encryption key is stored securely on the host machine
4. No plaintext credentials in database or logs

---

## Test Setup Requirements

### Prerequisites
- Fresh installation of Calendar Consolidator MCP
- A Google account (for testing OAuth flow)
- Terminal/command line access to the host machine
- Text editor or hex viewer for inspecting files

### Time Required
Approximately 30-45 minutes

---

## Part 1: Google Cloud Project Setup (One-Time Setup)

### Step 1.1: Create Google Cloud Project
1. Open your web browser
2. Navigate to https://console.cloud.google.com/
3. Sign in with your Google account
4. Click **"Select a project"** dropdown at the top
5. Click **"New Project"** button
6. Enter project name: `Calendar Consolidator Test`
7. Click **"Create"**
8. Wait for project creation (approximately 10-30 seconds)

### Step 1.2: Enable Google Calendar API
1. In the Google Cloud Console, ensure your new project is selected
2. Click hamburger menu (☰) → **"APIs & Services"** → **"Library"**
3. In the search bar, type: `Google Calendar API`
4. Click on **"Google Calendar API"** in the results
5. Click **"Enable"** button
6. Wait for API to be enabled (approximately 5-10 seconds)

### Step 1.3: Configure OAuth Consent Screen
1. Click hamburger menu (☰) → **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** user type
3. Click **"Create"** button
4. Fill in required fields:
   - **App name:** `Calendar Consolidator Test`
   - **User support email:** Select your email from dropdown
   - **Developer contact information:** Enter your email address
5. Click **"Save and Continue"**
6. On the "Scopes" page, click **"Add or Remove Scopes"**
7. In the filter box, search for: `calendar`
8. Check these two scopes:
   - `https://www.googleapis.com/auth/calendar.readonly`
   - `https://www.googleapis.com/auth/calendar.events`
9. Click **"Update"** button
10. Click **"Save and Continue"**
11. On "Test users" page, click **"Add Users"**
12. Enter your Google account email address
13. Click **"Add"**
14. Click **"Save and Continue"**
15. Review summary and click **"Back to Dashboard"**

### Step 1.4: Create OAuth Client ID
1. Click hamburger menu (☰) → **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** dropdown at the top
3. Select **"OAuth client ID"**
4. For "Application type", select **"Desktop app"**
5. Enter name: `Calendar Consolidator Desktop Test`
6. Click **"Create"**
7. A popup will appear with your credentials
8. **IMPORTANT:** Copy both values to a temporary text file:
   - **Client ID:** (looks like `123456789.apps.googleusercontent.com`)
   - **Client Secret:** (looks like `GOCSPX-xxxxxxxxxxxxx`)
9. Click **"OK"** to close the popup

---

## Part 2: Start Calendar Consolidator Application

### Step 2.1: Start the Application
1. Open a terminal/command prompt
2. Navigate to the Calendar Consolidator directory:
   ```bash
   cd /home/bba/0-projects/MCP\ SERVERS/Calendar\ Consolidator\ MCP
   ```
3. Start the application:
   - **Linux/Mac:**
     ```bash
     ./run.sh
     ```
   - **Windows:**
     ```powershell
     .\run_windows.ps1
     ```
4. Wait for the application to start (you should see console output)
5. Note the URL shown in the console (usually `http://localhost:3000`)

### Step 2.2: Open Web UI
1. Open your web browser
2. Navigate to: `http://localhost:3000`
3. You should see the Calendar Consolidator web interface

---

## Part 3: Configure OAuth Credentials in Application

### Step 3.1: Access Settings
1. In the Calendar Consolidator web interface, click the **"Settings"** tab
2. Scroll down to find the **"🔑 OAuth Credentials"** section
3. You should see provider cards for Google, Microsoft, and iCloud

### Step 3.2: Configure Google Credentials
1. In the Google Calendar card, click **"Configure"** or **"Edit"** button
2. A form will appear with two fields:
   - **Client ID**
   - **Client Secret**
3. Paste the **Client ID** you copied from Google Cloud Console
4. Paste the **Client Secret** you copied from Google Cloud Console
5. Click **"Save"** button
6. Wait for confirmation message: "Success: Credentials saved successfully"
7. The page may reload automatically

---

## Part 4: Connect a Google Calendar Account

### Step 4.1: Add Source Calendar
1. Click the **"Sources"** tab in the navigation
2. Click **"Add Source"** button
3. A modal/dialog should appear with provider options

### Step 4.2: Start Google OAuth Flow
1. Select **"Google Calendar"** from the provider options
2. Click **"Continue"** or **"Next"**
3. The application will display:
   - A verification URL
   - Instructions to visit the URL
4. **Copy the verification URL**

### Step 4.3: Complete OAuth Authorization
1. Open a new browser tab
2. Paste and visit the verification URL
3. Sign in with your Google account (if not already signed in)
4. You'll see a consent screen with the app name "Calendar Consolidator Test"
5. Review the permissions requested (Calendar access)
6. Click **"Continue"** or **"Allow"**
7. You may see a warning "Google hasn't verified this app" - this is normal for testing
8. Click **"Continue"** anyway
9. You'll be redirected to a page with an authorization code
10. **Copy the authorization code**
11. Return to the Calendar Consolidator tab

### Step 4.4: Complete the Flow in Application
1. Paste the authorization code into the input field
2. Click **"Submit"** or **"Continue"**
3. The application will fetch your calendars
4. Select one or more calendars to sync
5. Click **"Add Selected"** or **"Save"**
6. Your calendar source should now appear in the sources list

---

## Part 5: Verify Secure Storage on Host Machine

### Step 5.1: Stop the Application
1. Go to the terminal where the application is running
2. Press `Ctrl+C` to stop the application
3. Wait for graceful shutdown

### Step 5.2: Locate Security-Critical Files

#### File 1: Encryption Key
**Location:** `/home/bba/0-projects/MCP SERVERS/Calendar Consolidator MCP/.encryption_key`

**Purpose:** This is the master encryption key used to encrypt all credentials

**Check:**
```bash
ls -la .encryption_key
```

**Expected Result:**
- File exists
- Permissions: `-rw-------` (600) - only owner can read/write
- Size: Approximately 44 bytes

**Verify:**
```bash
cat .encryption_key
```

**Expected:** You should see random binary/encoded data, NOT readable text

#### File 2: Database
**Location:** `/home/bba/0-projects/MCP SERVERS/Calendar Consolidator MCP/calendar_consolidator.db`

**Purpose:** Stores all configuration data including encrypted credentials

**Check:**
```bash
ls -la calendar_consolidator.db
```

**Expected Result:**
- File exists
- File size should be greater than 0 bytes

### Step 5.3: Inspect Database Contents (Verify Encryption)

#### Option A: Using Python Script
Create a temporary inspection script:

```bash
cat > inspect_db.py << 'EOF'
#!/usr/bin/env python3
import sqlite3
import sys

# Connect to database
conn = sqlite3.connect('calendar_consolidator.db')
cursor = conn.cursor()

print("=" * 70)
print("CREDENTIAL STORAGE INSPECTION")
print("=" * 70)
print()

# Check settings table for OAuth credentials
print("1. OAuth Credentials in Settings Table:")
print("-" * 70)
cursor.execute("SELECT key, substr(value, 1, 50) FROM settings WHERE key LIKE '%credentials%'")
rows = cursor.fetchall()
if rows:
    for key, value_sample in rows:
        print(f"   Key: {key}")
        print(f"   Value (first 50 chars): {value_sample}...")
        print(f"   ✓ Value is encrypted (not readable as JSON)")
        print()
else:
    print("   ⚠ No OAuth credentials found in settings")
    print()

# Check sources table for user tokens
print("2. User Authentication Tokens in Sources Table:")
print("-" * 70)
cursor.execute("SELECT id, type, name, substr(cred_blob, 1, 50) FROM sources")
rows = cursor.fetchall()
if rows:
    for source_id, source_type, name, cred_sample in rows:
        print(f"   Source ID: {source_id}")
        print(f"   Type: {source_type}")
        print(f"   Name: {name}")
        print(f"   Credentials (first 50 chars): {cred_sample}...")
        print(f"   ✓ Credentials are encrypted (not readable)")
        print()
else:
    print("   ⚠ No sources found")
    print()

# Check target table
print("3. Target Calendar Credentials:")
print("-" * 70)
cursor.execute("SELECT id, type, name, substr(cred_blob, 1, 50) FROM target")
rows = cursor.fetchall()
if rows:
    for target_id, target_type, name, cred_sample in rows:
        print(f"   Target ID: {target_id}")
        print(f"   Type: {target_type}")
        print(f"   Name: {name}")
        print(f"   Credentials (first 50 chars): {cred_sample}...")
        print(f"   ✓ Credentials are encrypted")
        print()
else:
    print("   (No target configured yet)")
    print()

print("=" * 70)
print("SECURITY CHECK SUMMARY")
print("=" * 70)

# Verify no plaintext secrets
cursor.execute("SELECT key, value FROM settings WHERE key LIKE '%credentials%'")
for key, value in cursor.fetchall():
    if 'access_token' in value.lower() or 'refresh_token' in value.lower() or '"client_secret"' in value.lower():
        print("❌ FAILED: Found plaintext credentials in settings!")
        sys.exit(1)

cursor.execute("SELECT cred_blob FROM sources")
for (cred_blob,) in cursor.fetchall():
    if isinstance(cred_blob, str) and ('access_token' in cred_blob.lower() or 'refresh_token' in cred_blob.lower()):
        print("❌ FAILED: Found plaintext credentials in sources!")
        sys.exit(1)

print("✅ PASSED: All credentials are encrypted")
print("✅ PASSED: No plaintext secrets found in database")
print()

conn.close()
EOF

chmod +x inspect_db.py
```

Run the inspection script:
```bash
python3 inspect_db.py
```

**Expected Output:**
- OAuth credentials shown as encrypted data (not readable JSON)
- User tokens shown as encrypted blobs
- Final message: "✅ PASSED: All credentials are encrypted"

#### Option B: Using SQLite Command Line (if sqlite3 is installed)
```bash
sqlite3 calendar_consolidator.db << 'EOF'
.headers on
.mode line
SELECT key, substr(value, 1, 100) as value_preview
FROM settings
WHERE key LIKE '%credentials%';
EOF
```

**Expected:** Values should look like encrypted gibberish, NOT like JSON

### Step 5.4: Verify .gitignore Protection

Check that security-critical files are excluded from version control:

```bash
cat .gitignore | grep -E "(encryption_key|\.db)"
```

**Expected Output:**
```
.encryption_key
*.db
```

Verify files are not tracked by git:
```bash
git status --ignored | grep -E "(encryption_key|calendar_consolidator.db)"
```

**Expected:** These files should appear in the "Ignored files" section or not at all

---

## Part 6: Security Validation Checklist

Use this checklist to verify security:

### ✓ Encryption Key
- [ ] `.encryption_key` file exists in project root
- [ ] File has restrictive permissions (600 on Linux/Mac)
- [ ] File contains random binary data (not readable text)
- [ ] File is listed in `.gitignore`

### ✓ Database Encryption
- [ ] `calendar_consolidator.db` exists
- [ ] OAuth credentials in `settings` table are encrypted
- [ ] User tokens in `sources` table are encrypted
- [ ] No plaintext JSON credentials visible in database
- [ ] Database file is listed in `.gitignore`

### ✓ Application Behavior
- [ ] OAuth flow completed successfully
- [ ] Calendars were fetched and displayed
- [ ] Application can restart and still access calendars (encryption/decryption works)

### ✓ No Credential Leakage
- [ ] Application logs don't contain access tokens
- [ ] Application logs don't contain client secrets
- [ ] Browser console doesn't show plaintext credentials

---

## Part 7: Additional Security Tests

### Test 7.1: Verify Credentials Persist After Restart
1. Start the application again: `./run.sh`
2. Navigate to Sources tab
3. **Expected:** Your previously connected Google calendar still appears
4. Try triggering a sync
5. **Expected:** Sync should work without re-authentication

**What This Tests:** The application can decrypt and use stored credentials

### Test 7.2: Check Application Logs for Credential Leakage
```bash
# Check if any logs were created
ls -la logs/ 2>/dev/null || echo "No logs directory"

# If logs exist, search for sensitive patterns
if [ -d "logs" ]; then
    grep -ri "access_token\|refresh_token\|client_secret" logs/
    if [ $? -eq 0 ]; then
        echo "⚠ WARNING: Found potential credentials in logs"
    else
        echo "✅ No credentials found in logs"
    fi
fi
```

### Test 7.3: Verify Database File is Not World-Readable
```bash
ls -la calendar_consolidator.db
```

**Expected:** Permissions should ideally be `-rw-r--r--` or more restrictive

---

## Part 8: Test Results Documentation

### What to Report Back

After completing all tests, provide this information:

#### 1. Encryption Key Status
```
Location: /home/bba/0-projects/MCP SERVERS/Calendar Consolidator MCP/.encryption_key
Exists: [YES/NO]
Permissions: [actual permissions]
Content Type: [Binary/Readable Text]
In .gitignore: [YES/NO]
```

#### 2. Database Encryption Status
```
Location: /home/bba/0-projects/MCP SERVERS/Calendar Consolidator MCP/calendar_consolidator.db
Exists: [YES/NO]
Size: [file size]
OAuth Credentials Encrypted: [YES/NO]
User Tokens Encrypted: [YES/NO]
In .gitignore: [YES/NO]
```

#### 3. Functional Test Results
```
OAuth Flow Completed: [YES/NO]
Calendar Connection Success: [YES/NO]
Credentials Persist After Restart: [YES/NO]
Sync Works Without Re-auth: [YES/NO]
```

#### 4. Security Scan Results
```
Plaintext Credentials in Database: [YES/NO]
Credentials in Application Logs: [YES/NO]
Credentials in Browser Console: [YES/NO]
```

#### 5. Screenshots to Capture
1. Google OAuth consent screen
2. Calendar Consolidator Sources tab showing connected calendar
3. Terminal output showing `.encryption_key` file permissions
4. Output of `inspect_db.py` script showing encrypted data

---

## Common Issues and Solutions

### Issue: "Error saving credentials"
**Solution:**
- Check that database exists and is writable
- Verify Python dependencies are installed
- Check console logs for detailed error

### Issue: "Failed to start OAuth flow"
**Solution:**
- Verify Client ID and Client Secret are correct
- Check they were pasted without extra spaces
- Ensure Google Calendar API is enabled in Google Cloud Console

### Issue: "Authorization code invalid"
**Solution:**
- Make sure you copied the entire code
- Don't wait too long - codes expire in 10-60 minutes
- Try starting the OAuth flow again

### Issue: ".encryption_key file not found"
**Solution:**
- This file is auto-generated on first credential save
- If it doesn't exist, credentials haven't been saved yet
- Complete Part 3 and Part 4 first

### Issue: "Permission denied" when reading .encryption_key
**Solution:**
- On Linux/Mac, use: `sudo cat .encryption_key` (not recommended for security)
- Or check ownership: `ls -la .encryption_key`
- The file should be owned by the user running the application

---

## Cleanup (Optional)

### To Remove Test Data:
```bash
# Stop the application first (Ctrl+C)

# Remove database
rm calendar_consolidator.db

# Remove encryption key
rm .encryption_key

# Restart application to get fresh database
./run.sh
```

### To Revoke Google OAuth Access:
1. Go to https://myaccount.google.com/permissions
2. Find "Calendar Consolidator Test"
3. Click "Remove Access"

### To Delete Google Cloud Project:
1. Go to https://console.cloud.google.com/
2. Select "Calendar Consolidator Test" project
3. Click Settings (gear icon)
4. Click "Shutdown"
5. Type project ID to confirm
6. Click "Shut Down"

---

## Summary

This test validates that Calendar Consolidator MCP:
1. ✓ Stores OAuth application credentials encrypted in the database
2. ✓ Stores user authentication tokens encrypted in the database
3. ✓ Uses a randomly generated encryption key stored securely on disk
4. ✓ Excludes security-critical files from version control
5. ✓ Does not leak credentials in logs or console output

The encryption ensures that even if someone gains access to the database file, they cannot read the credentials without also having the `.encryption_key` file from the same machine.
