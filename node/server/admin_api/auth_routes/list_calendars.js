/**
 * List available calendars after authentication.
 */

import express from 'express';
import { callPythonFunction } from '../../python_bridge.js';
import { getSession, updateSessionCalendars } from './session_manager.js';

const router = express.Router();

router.get('/calendars/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;

    const session = getSession(sessionId);

    if (!session) {
      return res.status(404).json({
        error: 'Session not found or expired'
      });
    }

    if (session.status !== 'complete') {
      return res.status(400).json({
        error: 'Authentication not complete'
      });
    }

    // Return cached calendars if available
    if (session.calendars) {
      return res.json({ calendars: session.calendars });
    }

    // Determine connector module
    let connectorModule, connectorClass;

    if (session.type === 'graph') {
      connectorModule = 'python.connectors.graph_connector.connector';
      connectorClass = 'GraphConnector';
    } else if (session.type === 'google') {
      connectorModule = 'python.connectors.google_connector.connector';
      connectorClass = 'GoogleConnector';
    } else if (session.type === 'icloud') {
      connectorModule = 'python.connectors.icloud_connector.connector';
      connectorClass = 'ICloudConnector';
    } else {
      return res.status(400).json({ error: 'Unknown source type' });
    }

    // Create connector instance and list calendars
    const calendars = await callPythonFunction(
      connectorModule,
      'list_calendars',
      { credentials: session.credentials },
      connectorClass
    );

    // Cache calendars in session
    updateSessionCalendars(sessionId, calendars);

    res.json({ calendars });

  } catch (error) {
    console.error('Error listing calendars:', error);
    res.status(500).json({ error: error.message });
  }
});

export default router;
