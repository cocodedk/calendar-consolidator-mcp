/**
 * Microsoft Graph OAuth authentication UI.
 */

import { updateModalBody } from '../modal.js';
import { pollAuthStatus } from './auth_status_poller.js';

/**
 * Display Graph authentication UI with device code flow.
 * @param {string} sessionId - Session ID
 * @param {string} userCode - Device code to enter
 * @param {string} verificationUrl - URL to authenticate at
 * @param {Function} onComplete - Callback when complete
 */
export function displayGraphAuth(sessionId, userCode, verificationUrl, onComplete) {
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
}
