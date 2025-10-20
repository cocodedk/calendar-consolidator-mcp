# Auth Flow Helpers

Provider-specific OAuth authentication UI modules and polling utilities.

## Module Overview

| Module | Purpose | Lines |
|--------|---------|-------|
| `index.js` | Barrel exports for clean imports | 7 |
| `graph_auth.js` | Microsoft Graph device flow UI | 40 |
| `google_auth.js` | Google OAuth authorization code UI | 85 |
| `auth_status_poller.js` | Unified polling for auth completion | 37 |

## Usage

### Import Helpers
```javascript
import { displayGraphAuth, displayGoogleAuth, pollAuthStatus } from './helpers/index.js';
```

### Display Graph Auth
```javascript
displayGraphAuth(
  sessionId,        // string
  userCode,         // string - code user enters at verification URL
  verificationUrl,  // string - URL where user authenticates
  onComplete        // function(sessionId) - called on success
);
```

Features:
- Device code display with copy button
- Link to Microsoft authentication page
- Automatic polling for completion

### Display Google Auth
```javascript
displayGoogleAuth(
  sessionId,        // string
  verificationUrl,  // string - Google consent page URL
  onComplete        // function(sessionId) - called on success
);
```

Features:
- Google consent page link
- Authorization code input field
- Automatic code submission and exchange

### Poll Auth Status
```javascript
pollAuthStatus(
  sessionId,        // string - ID to poll
  onComplete        // function(sessionId) - called on completion
);
```

Behavior:
- Polls `/api/auth/poll/{sessionId}` every 5 seconds
- Timeout after 60 attempts (5 minutes)
- Calls `onComplete()` on success
- Displays error on failure or timeout

## Design Principles

✅ **Single Responsibility**: Each module handles one provider or operation
✅ **Provider Abstraction**: Main flow doesn't know provider details
✅ **Error Handling**: Provider-specific error handling
✅ **UI Isolation**: HTML/DOM logic contained per provider
✅ **Reusable Polling**: Polling logic works for all providers

## Flow Diagrams

### Microsoft Graph Flow
```
displayGraphAuth()
├─ Render device code UI
├─ Show verification URL link
└─ pollAuthStatus()
   └─ Fetch /api/auth/poll/{sessionId} every 5s
      ├─ On complete: call onComplete()
      └─ On error: show error message
```

### Google OAuth Flow
```
displayGoogleAuth()
├─ Render consent page link
├─ Render code input field
├─ Attach submit handler
└─ submitGoogleCode()
   └─ Fetch /api/auth/complete (POST)
      ├─ On success: call onComplete()
      └─ On error: show error, allow retry
```

## Integration Example

```javascript
// In add_source.js or similar
import { startAuthFlow } from './auth_flow.js';

async function handleAddSource(type) {
  // Google or Graph OAuth
  await startAuthFlow(type, (sessionId) => {
    console.log('Auth complete:', sessionId);
    // Proceed with adding source
    loadSource(sessionId);
  });
}
```

## Error Handling

All modules handle errors gracefully:
- Network errors → Show error message, allow retry
- Timeout → Show timeout error after 5 minutes
- Invalid code (Google) → Show error, allow re-entry
- API errors → Display server error message

## Testing Notes

Modules designed for easy testing:

```javascript
// Mock modal updates
import * as modal from '../modal.js';
modal.updateModalBody = jest.fn();
modal.showError = jest.fn();

// Mock fetch for polling
global.fetch = jest.fn()
  .mockResolvedValue({
    json: () => ({ status: 'complete' })
  });

// Test polling completes
await pollAuthStatus('session-123', mockCallback);
expect(mockCallback).toHaveBeenCalledWith('session-123');
```

## Future Enhancements

1. **Extract Polling Config**: Move polling interval/attempts to config
2. **Cancellation**: Add abort signals for polling cleanup
3. **Retry Logic**: Exponential backoff for failed requests
4. **New Providers**: Easy to add Apple, Microsoft Account, etc.
5. **Analytics**: Track auth flow steps and errors

## Debugging

Enable debug logging:
```javascript
// In auth_status_poller.js
if (DEBUG) console.log(`Poll attempt ${attempts}...`);
```

Check browser DevTools:
1. Network tab: Monitor `/api/auth/start`, `/api/auth/poll/`, `/api/auth/complete` requests
2. Console: Error messages from showError()
3. Elements: Verify DOM updates via updateModalBody()

## Performance Considerations

- Graph auth: ~30 seconds typical user response
- Google auth: Faster (immediate code entry)
- Polling timeout: 5 minutes (300 seconds)
- Poll interval: 5 seconds (300ms max latency)
- Max network requests: ~60 per auth flow

## Security Notes

✅ Session IDs used for state verification
✅ Authorization codes exchanged server-side only
✅ HTTPS required for OAuth URLs
✅ HTTPS required for API calls
⚠️ User codes displayed in client (by design for device flow)
