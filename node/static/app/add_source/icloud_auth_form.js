/**
 * iCloud authentication form step.
 */

import { updateModalBody, showError, showLoading } from './modal.js';

/**
 * Show iCloud authentication form.
 */
export function showICloudAuthForm(onComplete) {
  const content = `
    <div class="icloud-auth-form">
      <h4>iCloud Calendar Authentication</h4>
      <p>Enter your Apple ID and app-specific password:</p>

      <div class="form-group">
        <label for="apple-id">Apple ID (Email)</label>
        <input
          type="email"
          id="apple-id"
          placeholder="your@email.com"
          required
          autocomplete="email"
        >
      </div>

      <div class="form-group">
        <label for="app-password">App-Specific Password</label>
        <input
          type="password"
          id="app-password"
          placeholder="xxxx-xxxx-xxxx-xxxx"
          required
          autocomplete="off"
        >
      </div>

      <div class="info-box">
        <p><strong>Note:</strong> You must use an app-specific password, not your regular Apple ID password.</p>
        <p>
          <a href="https://support.apple.com/en-us/HT204397" target="_blank" rel="noopener">
            How to generate an app-specific password →
          </a>
        </p>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="window.closeAddSourceModal()">Cancel</button>
        <button class="btn btn-primary" id="validate-icloud">Continue</button>
      </div>
    </div>
  `;

  updateModalBody(content);

  // Attach form submit handler
  document.getElementById('validate-icloud').addEventListener('click', () => {
    validateICloudCredentials(onComplete);
  });

  // Allow Enter key to submit
  const inputs = document.querySelectorAll('#apple-id, #app-password');
  inputs.forEach(input => {
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        validateICloudCredentials(onComplete);
      }
    });
  });
}

/**
 * Validate iCloud credentials and proceed.
 */
async function validateICloudCredentials(onComplete) {
  const appleId = document.getElementById('apple-id').value.trim();
  const appPassword = document.getElementById('app-password').value.trim();

  if (!appleId || !appPassword) {
    alert('Please enter both Apple ID and app-specific password');
    return;
  }

  showLoading('Validating credentials...');

  try {
    const response = await fetch('/api/auth/icloud/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ appleId, appPassword })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to validate credentials');
    }

    const { sessionId } = await response.json();
    onComplete(sessionId);

  } catch (error) {
    showError(`Authentication failed: ${error.message}`);
  }
}
