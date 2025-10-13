/**
 * MCP sync operation tools.
 * Provides preview and execute sync functionality.
 */

import { callPythonFunction } from '../python_bridge.js';

/**
 * Preview sync changes without applying them.
 */
export const previewSyncTool = {
  name: 'previewSync',
  description: 'Preview sync changes (dry run) for source calendars',
  inputSchema: {
    type: 'object',
    properties: {
      sourceId: {
        type: 'number',
        description: 'Source calendar ID to preview (optional, previews all if omitted)'
      }
    }
  },

  async handler(params) {
    try {
      if (params.sourceId) {
        const result = await callPythonFunction(
          'python.sync.dry_run_syncer',
          'preview_sync',
          { source_id: params.sourceId }
        );
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } else {
        const result = await callPythonFunction(
          'python.sync.dry_run_syncer',
          'preview_all_sources',
          {}
        );
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      }
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error previewing sync: ${error.message}` }],
        isError: true
      };
    }
  }
};

/**
 * Execute sync operation.
 */
export const syncOnceTool = {
  name: 'syncOnce',
  description: 'Execute calendar sync for a source or all sources',
  inputSchema: {
    type: 'object',
    properties: {
      sourceId: {
        type: 'number',
        description: 'Source calendar ID to sync (optional, syncs all if omitted)'
      }
    }
  },

  async handler(params) {
    try {
      const result = await callPythonFunction(
        'python.sync.syncer',
        'sync_once',
        { source_id: params.sourceId }
      );
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error executing sync: ${error.message}` }],
        isError: true
      };
    }
  }
};

/**
 * Get sync status.
 */
export const getSyncStatusTool = {
  name: 'getSyncStatus',
  description: 'Get current sync status and recent logs',
  inputSchema: {
    type: 'object',
    properties: {
      limit: {
        type: 'number',
        description: 'Number of recent logs to return (default: 10)',
        default: 10
      }
    }
  },

  async handler(params) {
    try {
      const result = await callPythonFunction(
        'python.state.log_store',
        'get_recent',
        { limit: params.limit || 10 }
      );
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error getting sync status: ${error.message}` }],
        isError: true
      };
    }
  }
};

export default [previewSyncTool, syncOnceTool, getSyncStatusTool];
