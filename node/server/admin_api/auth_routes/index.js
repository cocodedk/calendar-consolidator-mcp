/**
 * OAuth authentication routes - barrel export.
 */

import express from 'express';
import startFlowRouter from './start_flow.js';
import pollAuthRouter from './poll_auth.js';
import listCalendarsRouter from './list_calendars.js';
import icloudAuthRouter from './icloud_auth.js';

const router = express.Router();

// Mount sub-routes
router.use('/', startFlowRouter);
router.use('/', pollAuthRouter);
router.use('/', listCalendarsRouter);
router.use('/', icloudAuthRouter);

export default router;
