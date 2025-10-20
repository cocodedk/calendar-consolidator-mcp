/**
 * OAuth authentication flow orchestrator.
 * Delegates to provider-specific helpers for UI rendering and status polling.
 */

import { showError, showLoading } from './modal.js';
import { displayGraphAuth, displayGoogleAuth } from './helpers/index.js';

/**
 * Start OAuth flow and display provider-specific UI.
 * @param {string} type - Provider type ('graph' or 'google')
 * @param {Function} onComplete - Callback when authentication completes
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
 * @private
 */
function displayAuthUI(type, sessionId, userCode, verificationUrl, onComplete) {
  if (type === 'graph') {
    displayGraphAuth(sessionId, userCode, verificationUrl, onComplete);
    return;
  }

  if (type === 'google') {
    displayGoogleAuth(sessionId, verificationUrl, onComplete);
    return;
  }

  showError('Unsupported provider type.');
}
