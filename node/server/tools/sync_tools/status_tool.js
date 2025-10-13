/**
 * Get sync status tool.
 */

import { callPythonFunction } from '../../python_bridge.js';

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
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error getting sync status: ${error.message}`
        }],
        isError: true
      };
    }
  }
};
