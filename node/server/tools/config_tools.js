/**
 * MCP configuration tools.
 * Manages sources, target, and settings.
 */

import { callPythonFunction } from '../python_bridge.js';

/**
 * List available calendars for a source type.
 */
export const listCalendarsTool = {
  name: 'listCalendars',
  description: 'List available calendars from Microsoft Graph or CalDAV',
  inputSchema: {
    type: 'object',
    properties: {
      sourceType: {
        type: 'string',
        enum: ['graph', 'caldav'],
        description: 'Calendar source type'
      },
      credentials: {
        type: 'object',
        description: 'Credentials for authentication'
      }
    },
    required: ['sourceType', 'credentials']
  },

  async handler(params) {
    try {
      const result = await callPythonFunction(
        'python.connectors.graph_connector',
        'list_calendars',
        { credentials: params.credentials }
      );
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error listing calendars: ${error.message}` }],
        isError: true
      };
    }
  }
};

/**
 * Get current configuration.
 */
export const getConfigTool = {
  name: 'getConfig',
  description: 'Get current sources, target, and settings',
  inputSchema: {
    type: 'object',
    properties: {}
  },

  async handler() {
    try {
      const result = await callPythonFunction(
        'python.state.config_store',
        'get_all_config',
        {}
      );
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (error) {
      return {
        content: [{ type: 'text', text: `Error getting config: ${error.message}` }],
        isError: true
      };
    }
  }
};

export default [listCalendarsTool, getConfigTool];
