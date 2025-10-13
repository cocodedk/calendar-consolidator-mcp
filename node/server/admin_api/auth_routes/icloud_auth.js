/**
 * iCloud authentication endpoint (app-specific password).
 */

import express from 'express';
import { callPythonFunction } from '../../python_bridge.js';
import { createSession, updateSessionCredentials } from './session_manager.js';

const router = express.Router();

router.post('/icloud/validate', async (req, res) => {
  try {
    const { appleId, appPassword } = req.body;

    if (!appleId || !appPassword) {
      return res.status(400).json({
        error: 'Apple ID and app-specific password are required'
      });
    }

    // Call Python to validate credentials
    const credentials = await callPythonFunction(
      'python.connectors.icloud_auth.authenticator',
      'get_credentials_dict',
      {
        apple_id: appleId,
        app_password: appPassword
      },
      'ICloudAuthenticator'
    );

    // Create session with validated credentials
    const sessionId = createSession('icloud', { credentials });

    // Mark session as complete immediately (no async OAuth flow)
    updateSessionCredentials(sessionId, credentials);

    // Return session ID
    res.json({
      sessionId,
      status: 'complete'
    });

  } catch (error) {
    console.error('Error validating iCloud credentials:', error);
    res.status(500).json({
      error: error.message || 'Failed to validate credentials'
    });
  }
});

export default router;
