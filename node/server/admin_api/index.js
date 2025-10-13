/**
 * Admin API module - combine all routes.
 */

import express from 'express';
import configRoutes from './config_routes.js';
import syncRoutes from './sync_routes.js';
import logsRoutes from './logs_routes.js';
import settingsRoutes from './settings_routes.js';
import authRoutes from './auth_routes/index.js';
import credentialsRoutes from './credentials_routes.js';

const router = express.Router();

// Mount route modules
router.use(configRoutes);
router.use(syncRoutes);
router.use(logsRoutes);
router.use(settingsRoutes);
router.use('/auth', authRoutes);
router.use(credentialsRoutes);

export default router;
