/**
 * MCP server implementation.
 * Registers tools and handles MCP protocol.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import syncTools from './tools/sync_tools.js';
import configTools from './tools/config_tools.js';

// Combine all tools
const allTools = [...syncTools, ...configTools];

/**
 * Create and configure MCP server.
 */
export function createMCPServer() {
  const server = new Server(
    {
      name: 'calendar-consolidator-mcp',
      version: '0.1.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List tools handler
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: allTools.map(tool => ({
        name: tool.name,
        description: tool.description,
        inputSchema: tool.inputSchema,
      })),
    };
  });

  // Call tool handler
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const tool = allTools.find(t => t.name === request.params.name);

    if (!tool) {
      throw new Error(`Unknown tool: ${request.params.name}`);
    }

    return await tool.handler(request.params.arguments || {});
  });

  return server;
}

/**
 * Start MCP server with stdio transport.
 */
export async function startMCPServer() {
  const server = createMCPServer();
  const transport = new StdioServerTransport();

  await server.connect(transport);

  console.error('Calendar Consolidator MCP server running on stdio');
}

export default { createMCPServer, startMCPServer };
