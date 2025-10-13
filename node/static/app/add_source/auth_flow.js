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
    displayDeviceCode(userCode, verificationUrl);
    pollAuthStatus(sessionId, onComplete);
  } catch (error) {
    showError(`Authentication error: ${error.message}`);
  }
}

/**
 * Display device code to user.
 */
function displayDeviceCode(userCode, verificationUrl) {
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
