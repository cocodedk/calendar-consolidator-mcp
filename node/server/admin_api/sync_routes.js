/**
 * Sync operation routes (preview, sync).
 */

import express from 'express';
import { callPythonFunction } from '../python_bridge.js';

const router = express.Router();

// Preview sync
router.post('/preview', async (req, res) => {
  try {
    const { sourceId } = req.body;
    const result = await callPythonFunction(
      'python.sync.dry_run_syncer',
      'preview_sync',
      { source_id: sourceId }
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Execute sync
router.post('/sync', async (req, res) => {
  try {
    const { sourceId } = req.body;
    const result = await callPythonFunction(
      'python.sync.syncer',
      'sync_once',
      { source_id: sourceId }
    );
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
