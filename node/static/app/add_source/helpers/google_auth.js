/**
 * Google OAuth authentication UI.
 */

import { updateModalBody, showError } from '../modal.js';

/**
 * Display Google authentication UI with authorization code paste.
 * @param {string} sessionId - Session ID
 * @param {string} verificationUrl - Google consent page URL
 * @param {Function} onComplete - Callback when complete
 */
export function displayGoogleAuth(sessionId, verificationUrl, onComplete) {
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
  attachGoogleCodeHandler(sessionId, onComplete);
}

/**
 * Attach event handler for Google code submission.
 * @private
 */
function attachGoogleCodeHandler(sessionId, onComplete) {
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
        await submitGoogleCode(sessionId, code, btn, status, onComplete);
      });
    }
  }, 0);
}

/**
 * Submit authorization code to backend.
 * @private
 */
async function submitGoogleCode(sessionId, code, btn, status, onComplete) {
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
}
