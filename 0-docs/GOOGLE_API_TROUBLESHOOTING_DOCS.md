# Google API Troubleshooting Documentation

## Summary

Added comprehensive troubleshooting documentation for the most common Google Calendar setup issue: **API not enabled (HTTP 403 error)**.

## Files Created/Updated

### 1. Enhanced Google Setup Guide
**File**: `03-implementation/15-step15-google-setup.md` (90 lines)
- ⚠️ Added critical warning to Step 2 (Enable Google Calendar API)
- Added quick enable link with project ID placeholder
- Links to detailed troubleshooting guides

### 2. New Troubleshooting Section
**Directory**: `07-troubleshooting/`

#### Created Files (all under 100 lines):
- **00-README.md** (50 lines) - Troubleshooting index with categories
- **01-google-calendar-issues.md** (77 lines) - Google Calendar issues index
- **02-google-api-not-enabled.md** (64 lines) - HTTP 403 API not enabled guide
- **03-google-invalid-grant.md** (71 lines) - Invalid grant/token errors
- **04-google-redirect-uri.md** (72 lines) - OAuth redirect URI issues

### 3. Updated Main Documentation
**Files**: `README.md` and `0-docs/README.md`
- Added Troubleshooting section with quick fix
- Added links to all specific troubleshooting guides
- Emphasized most common issue (HTTP 403)

## Key Content Added

### The Most Common Issue
**Error**: `HttpError 403: Google Calendar API has not been used in project...`

**Quick Fix**:
1. Click the URL from error message
2. Enable the API
3. Wait 2-3 minutes
4. Retry

### Additional Coverage
- Invalid grant errors (expired/revoked tokens)
- Redirect URI mismatch
- Calendar not found
- Prevention checklist

## Documentation Structure

```
0-docs/
├── 07-troubleshooting/
│   ├── 00-README.md                   # Troubleshooting index (50 lines)
│   ├── 01-google-calendar-issues.md   # Google issues index (77 lines)
│   ├── 02-google-api-not-enabled.md   # HTTP 403 guide (64 lines)
│   ├── 03-google-invalid-grant.md     # Token errors (71 lines)
│   └── 04-google-redirect-uri.md      # OAuth errors (72 lines)
├── 03-implementation/
│   └── 15-step15-google-setup.md      # Enhanced guide (90 lines)
└── README.md                          # Updated with troubleshooting
```

All files comply with the 100-line modularization guideline.

## User Experience Improvements

1. **Immediate Help**: Quick fix in main README for fast resolution
2. **Comprehensive Guide**: Detailed troubleshooting in dedicated section
3. **Prevention**: Checklist to avoid issues during setup
4. **Clear Navigation**: Multiple entry points to find help

## Impact

- Reduces setup friction for new users
- Provides self-service troubleshooting
- Documents the #1 most common error
- Establishes pattern for future troubleshooting docs
