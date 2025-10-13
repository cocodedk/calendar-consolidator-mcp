# Step 15: Google Calendar Setup

## Overview
Configure Google Cloud Project and OAuth credentials for Calendar API access.

## Prerequisites
- Google account
- Access to Google Cloud Console

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name: "Calendar Consolidator"
4. Click "Create"

### 2. Enable Google Calendar API
1. Navigate to "APIs & Services" → "Library"
2. Search "Google Calendar API"
3. Click "Enable"

### 3. Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" user type
3. Fill required fields:
   - App name: "Calendar Consolidator"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue"
5. Add scopes:
   - `https://www.googleapis.com/auth/calendar.readonly`
   - `https://www.googleapis.com/auth/calendar.events`
6. Add test users (during development)
7. Click "Save and Continue"

### 4. Create OAuth Client ID
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Calendar Consolidator Desktop"
5. Click "Create"
6. Download JSON file

### 5. Configure Application
Store client ID and secret in settings:
```python
# Add to database settings table
{
  "google_client_id": "your-client-id.apps.googleusercontent.com",
  "google_client_secret": "your-client-secret"
}
```

## Required OAuth Scopes

### calendar.readonly
Read access to calendars and events (for source calendars).

### calendar.events
Full access to events (for target calendar).

## Security Notes
- Keep client secret secure
- Store in encrypted settings
- Never commit credentials to version control
- Rotate secrets periodically

## Testing
During development, add test user emails in OAuth consent screen.
Production apps require Google verification for public access.

