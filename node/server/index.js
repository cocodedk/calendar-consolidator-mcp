#!/usr/bin/env node
/**
 * Main entry point for Calendar Consolidator MCP.
 * Starts both MCP server and HTTP admin API.
 */

import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import adminAPI from './admin_api.js';
import { startMCPServer } from './mcp_server.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';

// Check if running in MCP mode (stdio)
const isMCPMode = process.env.MCP_MODE === 'true' || process.argv.includes('--mcp');

if (isMCPMode) {
  // Start MCP server on stdio
  startMCPServer().catch(error => {
    console.error('Failed to start MCP server:', error);
    process.exit(1);
  });
} else {
  // Start HTTP server for UI
  const app = express();

  // Middleware
  app.use(cors());
  app.use(express.json());

  // Serve static files
  app.use(express.static(path.join(__dirname, '../static')));

  // API routes
  app.use('/api', adminAPI);

  // Health check
  app.get('/health', (req, res) => {
    res.json({ status: 'ok', version: '0.1.0' });
  });

  // Start server
  app.listen(PORT, HOST, () => {
    console.log(`Calendar Consolidator running at http://${HOST}:${PORT}`);
    console.log(`Web UI: http://${HOST}:${PORT}`);
    console.log(`API: http://${HOST}:${PORT}/api`);
  });
}
