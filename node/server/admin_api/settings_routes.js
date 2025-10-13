/**
 * Settings routes.
 */

import express from 'express';
import { callPythonFunction } from '../python_bridge.js';

const router = express.Router();

// Update settings
router.post('/settings', async (req, res) => {
  try {
    await callPythonFunction(
      'python.state.settings_store',
      'set_multiple',
      { settings: req.body }
    );
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
