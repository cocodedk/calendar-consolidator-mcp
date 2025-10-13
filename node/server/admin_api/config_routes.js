/**
 * Configuration routes (config, sources, target).
 */

import express from 'express';
import { callPythonFunction } from '../python_bridge.js';
import { getSession } from './auth_routes/session_manager.js';

const router = express.Router();

// Get all configuration
router.get('/config', async (req, res) => {
  try {
    const result = await callPythonFunction(
      'python.state.config_store',
      'get_all_config',
      {}
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Add source calendar
router.post('/source', async (req, res) => {
  try {
    const { type, calendarId, name, credentials, sessionId } = req.body;

    // If sessionId provided, retrieve credentials from session
    let creds = credentials;
    if (sessionId) {
      const session = getSession(sessionId);
      if (!session || !session.credentials) {
        return res.status(400).json({ error: 'Invalid session or missing credentials' });
      }
      creds = session.credentials;
    }

    if (!creds) {
      return res.status(400).json({ error: 'Missing credentials' });
    }

    const result = await callPythonFunction(
      'python.state.source_store',
      'add',
      { type, calendar_id: calendarId, name, credentials: creds }
    );
    res.json({ success: true, sourceId: result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Remove source calendar
router.delete('/source/:id', async (req, res) => {
  try {
    await callPythonFunction(
      'python.state.source_store',
      'remove',
      { source_id: parseInt(req.params.id) }
    );
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Set target calendar
router.post('/target', async (req, res) => {
  try {
    const { type, calendarId, name, credentials } = req.body;
    await callPythonFunction(
      'python.state.target_store',
      'set',
      { type, calendar_id: calendarId, name, credentials }
    );
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
