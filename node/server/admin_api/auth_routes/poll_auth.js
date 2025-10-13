/**
 * Poll OAuth authentication status.
 */

import express from 'express';
import { getSession } from './session_manager.js';

const router = express.Router();

router.get('/poll/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = getSession(sessionId);

    if (!session) {
      return res.status(404).json({
        status: 'error',
        error: 'Session not found or expired'
      });
    }

    // Return current status
    res.json({
      status: session.status,
      error: session.error
    });

  } catch (error) {
    console.error('Error polling auth status:', error);
    res.status(500).json({
      status: 'error',
      error: error.message
    });
  }
});

export default router;
