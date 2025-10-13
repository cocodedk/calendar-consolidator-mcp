/**
 * Start OAuth device code flow.
 */

import express from 'express';
import { callPythonFunction } from '../../python_bridge.js';
import { createSession } from './session_manager.js';
import { startBackgroundPolling } from './polling_helper.js';

const router = express.Router();

router.post('/start', async (req, res) => {
  try {
    const { type } = req.body;

    if (!type || !['graph', 'google'].includes(type)) {
      return res.status(400).json({
        error: 'Invalid type. Must be "graph" or "google"'
      });
    }

    // Determine which authenticator to use
    const authModule = type === 'graph'
      ? 'python.connectors.graph_auth'
      : 'python.connectors.google_auth.authenticator';

    const authClass = type === 'graph'
      ? 'GraphAuthenticator'
      : 'GoogleAuthenticator';

    // Call Python to get device code flow
    const flowData = await callPythonFunction(
      authModule,
      'get_device_code_flow',
      {},
      authClass
    );

    // Create session to track this flow
    const sessionId = createSession(type, flowData);

    // Start polling in background
    startBackgroundPolling(sessionId, type, flowData);

    // Return session ID and user instructions
    res.json({
      sessionId,
      userCode: flowData.user_code || flowData.userCode,
      verificationUrl: flowData.verification_url || flowData.verification_uri || flowData.verificationUrl
    });

  } catch (error) {
    console.error('Error starting OAuth flow:', error);
    res.status(500).json({ error: error.message });
  }
});

export default router;
