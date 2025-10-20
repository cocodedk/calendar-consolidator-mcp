/**
 * Complete OAuth for flows that return an authorization code (e.g., Google OOB).
 */

import express from 'express';
import { callPythonFunction } from '../../python_bridge.js';
import { getSession, updateSessionCredentials, updateSessionError } from './session_manager.js';

const router = express.Router();

router.post('/complete', async (req, res) => {
  try {
    const { sessionId, type, code } = req.body || {};

    if (!sessionId || !type) {
      return res.status(400).json({ error: 'Missing sessionId or type' });
    }

    const session = getSession(sessionId);
    if (!session) {
      return res.status(404).json({ error: 'Session not found or expired' });
    }

    if (type !== 'google') {
      return res.status(400).json({ error: 'Completion endpoint is only for Google flows' });
    }

    if (!code || typeof code !== 'string') {
      return res.status(400).json({ error: 'Missing authorization code' });
    }

    // Exchange authorization code for tokens via Python authenticator
    const result = await callPythonFunction(
      'python.connectors.google_auth.authenticator',
      'acquire_token_by_code',
      { code },
      'GoogleAuthenticator'
    );

    if (!result || (!result.access_token && !result.accessToken)) {
      updateSessionError(sessionId, 'Failed to acquire tokens');
      return res.status(500).json({ error: 'Failed to acquire tokens' });
    }

    updateSessionCredentials(sessionId, result);
    return res.json({ success: true });
  } catch (error) {
    console.error('Error completing OAuth:', error);
    return res.status(500).json({ error: error.message });
  }
});

export default router;

