/**
 * Execute sync tool.
 */

import { callPythonFunction } from '../../python_bridge.js';

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
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error executing sync: ${error.message}`
        }],
        isError: true
      };
    }
  }
};
