/**
 * Auth status polling logic.
 */

import { showError } from '../modal.js';

/**
 * Poll for authentication completion.
 * @param {string} sessionId - Session ID to poll
 * @param {Function} onComplete - Callback when auth completes
 */
export async function pollAuthStatus(sessionId, onComplete) {
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
