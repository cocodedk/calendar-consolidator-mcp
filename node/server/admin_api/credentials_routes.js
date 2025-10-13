/**
 * Credentials API routes.
 */

import express from 'express';
import { handleGetCredentials } from './credentials/get.js';
import { handleUpdateCredentials } from './credentials/update.js';

const router = express.Router();

/**
 * GET /api/credentials
 * Get masked credentials for all providers.
 */
router.get('/credentials', handleGetCredentials);

/**
 * PUT /api/credentials
 * Update credentials for a provider.
 */
router.put('/credentials', handleUpdateCredentials);

export default router;
