/**
 * OAuth authentication flow step.
 */

import { updateModalBody, showError, showLoading } from './modal.js';

/**
 * Start OAuth flow and display device code.
 */
export async function startAuthFlow(type, onComplete) {
  showLoading('Starting authentication...');
  try {
    const response = await fetch('/api/auth/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type })
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to start authentication');
    }
    const { sessionId, userCode, verificationUrl } = await response.json();
    displayAuthUI(type, sessionId, userCode, verificationUrl, onComplete);
  } catch (error) {
    showError(`Authentication error: ${error.message}`);
  }
}

/**
 * Display auth UI based on provider type.
 */
function displayAuthUI(type, sessionId, userCode, verificationUrl, onComplete) {
  if (type === 'graph') {
    const content = `
      <div class="auth-flow">
        <h4>Complete Authentication</h4>
        <p>Please follow these steps:</p>
        <ol class="auth-steps">
          <li>Click the button below to open the authentication page</li>
          <li>Sign in with your account</li>
          <li>Enter this code when prompted:</li>
        </ol>
        <div class="device-code">
          <code>${userCode}</code>
          <button class="btn-copy" onclick="navigator.clipboard.writeText('${userCode}')">Copy</button>
        </div>
        <a href="${verificationUrl}" target="_blank" class="btn btn-primary">
          Open Authentication Page
        </a>
        <div class="polling-status">
          <div class="spinner"></div>
          <p>Waiting for authentication...</p>
        </div>
      </div>
    `;
    updateModalBody(content);
    pollAuthStatus(sessionId, onComplete);
    return;
  }

  // Google uses authorization code pasted back into the app (OOB)
  if (type === 'google') {
    const content = `
      <div class="auth-flow">
        <h4>Complete Google Authentication</h4>
        <p>1) Click the button to open Google's consent page.</p>
        <p>2) Approve access, then copy the authorization code you receive.</p>
        <a href="${verificationUrl}" target="_blank" class="btn btn-primary" style="margin-bottom: 12px;">
          Open Google Consent Page
        </a>
        <div class="form-group">
          <label for="google-auth-code">Paste authorization code</label>
          <input type="text" id="google-auth-code" placeholder="Paste code here" style="width:100%;" />
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" id="submit-google-code">Submit Code</button>
          <button class="btn btn-secondary" onclick="window.closeAddSourceModal()">Cancel</button>
        </div>
        <div id="google-auth-status" class="polling-status" style="display:none;">
          <div class="spinner"></div>
          <p>Exchanging code, please wait...</p>
        </div>
      </div>
    `;
    updateModalBody(content);

    // Attach handler
    setTimeout(() => {
      const btn = document.getElementById('submit-google-code');
      const input = document.getElementById('google-auth-code');
      const status = document.getElementById('google-auth-status');
      if (btn && input) {
        btn.addEventListener('click', async () => {
          const code = (input.value || '').trim();
          if (!code) {
            alert('Please paste the authorization code');
            return;
          }
          btn.disabled = true;
          status.style.display = 'block';
          try {
            const resp = await fetch('/api/auth/complete', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ sessionId, type: 'google', code })
            });
            const data = await resp.json();
            if (!resp.ok) {
              throw new Error(data.error || 'Failed to complete authentication');
            }
            onComplete(sessionId);
          } catch (err) {
            btn.disabled = false;
            status.style.display = 'none';
            showError(`Authentication failed: ${err.message}`);
          }
        });
      }
    }, 0);
    return;
  }

  // Fallback UI
  updateModalBody('<p>Unsupported provider type.</p>');
}

/**
 * Poll for authentication completion.
 */
async function pollAuthStatus(sessionId, onComplete) {
  const maxAttempts = 60;
  let attempts = 0;
  const pollInterval = setInterval(async () => {
    attempts++;
    if (attempts > maxAttempts) {
      clearInterval(pollInterval);
      showError('Authentication timeout. Please try again.');
      return;
    }
    try {
      const response = await fetch(`/api/auth/poll/${sessionId}`);
      const { status, error } = await response.json();
      if (status === 'complete') {
        clearInterval(pollInterval);
        onComplete(sessionId);
      } else if (status === 'error') {
        clearInterval(pollInterval);
        showError(`Authentication failed: ${error}`);
      }
    } catch (error) {
      clearInterval(pollInterval);
      showError(`Polling error: ${error.message}`);
    }
  }, 5000);
}
