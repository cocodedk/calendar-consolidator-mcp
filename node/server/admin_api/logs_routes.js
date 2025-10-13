/**
 * Logs and status routes.
 */

import express from 'express';
import { callPythonFunction } from '../python_bridge.js';

const router = express.Router();

// Get sync logs
router.get('/logs', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const result = await callPythonFunction(
      'python.state.log_store',
      'get_recent',
      { limit }
    );
    res.json({ logs: result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get system status
router.get('/status', async (req, res) => {
  try {
    const result = await callPythonFunction(
      'python.state.config_store',
      'get_status',
      {}
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
