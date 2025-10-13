/**
 * Preview sync tool.
 */

import { callPythonFunction } from '../../python_bridge.js';

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
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      } else {
        const result = await callPythonFunction(
          'python.sync.dry_run_syncer',
          'preview_all_sources',
          {}
        );
        return {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
      }
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error previewing sync: ${error.message}`
        }],
        isError: true
      };
    }
  }
};
