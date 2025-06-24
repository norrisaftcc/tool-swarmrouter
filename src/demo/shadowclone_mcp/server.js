#!/usr/bin/env node

/**
 * Shadow Clone MCP Server
 * 
 * A lightweight MCP server demonstrating task delegation using the Naruto
 * shadow clone metaphor. This server accepts missions and delegates them
 * to shadow clones for efficient execution.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { MainNinja } from './lib/ninja.js';

// Initialize the main ninja
const naruto = new MainNinja('Naruto Uzumaki', 'Hidden Leaf Village');

// Create MCP server
const server = new Server(
  {
    name: 'shadowclone-mcp-server',
    version: '1.0.0',
    description: 'Task delegation server using shadow clone jutsu'
  },
  {
    capabilities: {
      tools: {},
      logging: {},
      prompts: {}
    }
  }
);

// Tool: Execute Mission
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'execute_mission',
        description: 'Execute a mission using shadow clone jutsu for efficient task delegation',
        inputSchema: {
          type: 'object',
          properties: {
            mission: {
              type: 'string',
              description: 'The mission description to execute'
            },
            max_tokens: {
              type: 'number',
              description: 'Maximum tokens (chakra) to use for the mission',
              default: 1000
            },
            priority: {
              type: 'string',
              enum: ['low', 'normal', 'high', 'critical'],
              description: 'Mission priority level',
              default: 'normal'
            }
          },
          required: ['mission']
        }
      },
      {
        name: 'ninja_status',
        description: 'Get the current status of the ninja and active shadow clones',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'mission_history',
        description: 'Get the history of completed missions',
        inputSchema: {
          type: 'object',
          properties: {
            limit: {
              type: 'number',
              description: 'Number of recent missions to return',
              default: 10
            }
          },
          required: []
        }
      },
      {
        name: 'dispel_clones',
        description: 'Dispel all active shadow clones (emergency cleanup)',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'execute_mission': {
        const { mission, max_tokens = 1000, priority = 'normal' } = args;
        
        if (!mission || typeof mission !== 'string') {
          throw new Error('Mission description is required and must be a string');
        }

        console.log(`📥 Received mission: ${mission.substring(0, 100)}...`);
        
        const result = await naruto.executeMission(mission, {
          maxTokens: max_tokens,
          priority
        });

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      }

      case 'ninja_status': {
        const status = naruto.getStatus();
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(status, null, 2)
            }
          ]
        };
      }

      case 'mission_history': {
        const { limit = 10 } = args;
        const history = naruto.getMissionHistory(limit);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(history, null, 2)
            }
          ]
        };
      }

      case 'dispel_clones': {
        naruto.dispelAllClones();
        
        return {
          content: [
            {
              type: 'text',
              text: 'All shadow clones have been dispelled'
            }
          ]
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    console.error(`Error executing tool ${name}:`, error);
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

// Handle logging
server.setNotificationHandler('notifications/message', async (notification) => {
  console.log(`📨 ${notification.params.level}: ${notification.params.message}`);
});

// Start the server
async function main() {
  console.log('🥷 Shadow Clone MCP Server starting...');
  console.log(`🔥 Main Ninja: ${naruto.name} from ${naruto.village}`);
  console.log('📡 Listening for missions via stdio...');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.log('✅ Server ready! Waiting for missions...');
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down Shadow Clone MCP Server...');
  naruto.dispelAllClones();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 Shutting down Shadow Clone MCP Server...');
  naruto.dispelAllClones();
  process.exit(0);
});

// Start the server
main().catch((error) => {
  console.error('❌ Failed to start server:', error);
  process.exit(1);
});