/**
 * Background polling helper for OAuth completion.
 */

import { callPythonFunction } from '../../python_bridge.js';
import { getSession, updateSessionCredentials, updateSessionError } from './session_manager.js';

/**
 * Start polling for OAuth completion in background.
 */
export async function startBackgroundPolling(sessionId, type, flowData) {
  const authModule = type === 'graph'
    ? 'python.connectors.graph_auth'
    : 'python.connectors.google_auth.authenticator';

  const authClass = type === 'graph'
    ? 'GraphAuthenticator'
    : 'GoogleAuthenticator';

  const maxAttempts = 60; // 5 minutes with 5 second intervals
  let attempts = 0;

  const pollInterval = setInterval(async () => {
    attempts++;

    const session = getSession(sessionId);
    if (!session || session.status !== 'pending') {
      clearInterval(pollInterval);
      return;
    }

    if (attempts > maxAttempts) {
      updateSessionError(sessionId, 'Authentication timeout');
      clearInterval(pollInterval);
      return;
    }

    try {
      const result = await callPythonFunction(
        authModule,
        'acquire_token_by_device_flow',
        { flow: flowData },
        authClass
      );

      if (result.access_token || result.accessToken) {
        updateSessionCredentials(sessionId, result);
        clearInterval(pollInterval);
      }
    } catch (error) {
      // Continue polling on errors (user may not have completed auth yet)
      if (error.message.includes('expired') || error.message.includes('denied')) {
        updateSessionError(sessionId, error.message);
        clearInterval(pollInterval);
      }
    }
  }, 5000);
}
