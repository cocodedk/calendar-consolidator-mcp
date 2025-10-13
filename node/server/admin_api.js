/**
 * HTTP Admin API for Web UI.
 * REST endpoints for configuration and sync operations.
 */

import express from 'express';
import { callPythonFunction } from './python_bridge.js';

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
    const { type, calendarId, name, credentials } = req.body;
    const result = await callPythonFunction(
      'python.state.source_store',
      'add',
      { type, calendar_id: calendarId, name, credentials }
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
