#!/usr/bin/env node

/**
 * Shadow Clone MCP Server
 * 
 * An educational MCP server that demonstrates task delegation using the Shadow Clone technique.
 * This server showcases how complex tasks can be broken down and distributed across
 * specialized "ninja clones" for efficient parallel processing.
 * 
 * Perfect for coding education and demonstrating swarm intelligence concepts.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { CodingSensei } from './lib/ninja.js';
import { ShadowCloneManager } from './lib/shadowclone.js';

// Initialize the main ninja (coding sensei)
const codingSensei = new CodingSensei('Master Sensei', {
  specialization: 'Full-Stack Development',
  experience: 'Expert',
  focus: 'Educational Coding'
});

const cloneManager = new ShadowCloneManager(codingSensei);

const server = new Server(
  {
    name: 'shadowclone-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'create_shadow_clones',
        description: 'Break down a complex task and execute it using Shadow Clone technique for efficient parallel processing. Great for learning task decomposition.',
        inputSchema: {
          type: 'object',
          properties: {
            mission: {
              type: 'string',
              description: 'The main task or mission to accomplish'
            },
            maxTokens: {
              type: 'number',
              description: 'Maximum tokens to allocate (default: 1000)',
              default: 1000
            }
          },
          required: ['mission']
        }
      },
      {
        name: 'code_review_ninja',
        description: 'Deploy a specialized code review ninja to analyze code quality, security, performance, and best practices. Perfect for learning code review skills.',
        inputSchema: {
          type: 'object',
          properties: {
            code: {
              type: 'string',
              description: 'Code to review'
            },
            language: {
              type: 'string',
              description: 'Programming language (e.g., javascript, python, java)',
              default: 'javascript'
            },
            focus: {
              type: 'string',
              description: 'Review focus: security, performance, readability, or all',
              enum: ['security', 'performance', 'readability', 'all'],
              default: 'all'
            }
          },
          required: ['code']
        }
      },
      {
        name: 'debug_ninja',
        description: 'Summon a debugging specialist ninja to identify and solve code issues. Excellent for learning debugging techniques.',
        inputSchema: {
          type: 'object',
          properties: {
            debugInfo: {
              type: 'string',
              description: 'Description of the bug, error message, or problematic code'
            },
            language: {
              type: 'string',
              description: 'Programming language',
              default: 'javascript'
            },
            context: {
              type: 'string',
              description: 'Additional context about the environment or setup'
            }
          },
          required: ['debugInfo']
        }
      },
      {
        name: 'research_ninja',
        description: 'Deploy a research specialist to gather information on technical topics, best practices, and implementation strategies.',
        inputSchema: {
          type: 'object',
          properties: {
            topic: {
              type: 'string',
              description: 'Research topic or technology to investigate'
            },
            depth: {
              type: 'string',
              description: 'Research depth: basic, intermediate, or advanced',
              enum: ['basic', 'intermediate', 'advanced'],
              default: 'intermediate'
            },
            focusAreas: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['implementation', 'best-practices', 'performance', 'security', 'examples']
              },
              description: 'Specific areas to focus research on'
            }
          },
          required: ['topic']
        }
      },
      {
        name: 'refactor_ninja',
        description: 'Send in a refactoring expert to improve code structure, performance, and maintainability. Great for learning clean code principles.',
        inputSchema: {
          type: 'object',
          properties: {
            codeToRefactor: {
              type: 'string',
              description: 'Code that needs refactoring'
            },
            language: {
              type: 'string',
              description: 'Programming language',
              default: 'javascript'
            },
            goals: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['performance', 'readability', 'maintainability', 'testing', 'design-patterns']
              },
              description: 'Refactoring goals to focus on'
            }
          },
          required: ['codeToRefactor']
        }
      },
      {
        name: 'testing_ninja',
        description: 'Deploy a testing strategist to create comprehensive testing plans and strategies. Perfect for learning testing methodologies.',
        inputSchema: {
          type: 'object',
          properties: {
            featureDescription: {
              type: 'string',
              description: 'Description of the feature or system to test'
            },
            testTypes: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['unit', 'integration', 'e2e', 'security', 'performance']
              },
              description: 'Types of tests to include in strategy'
            },
            framework: {
              type: 'string',
              description: 'Preferred testing framework (optional)'
            }
          },
          required: ['featureDescription']
        }
      },
      {
        name: 'architect_ninja',
        description: 'Summon an architecture expert to analyze system design, scalability, and architectural patterns.',
        inputSchema: {
          type: 'object',
          properties: {
            systemDescription: {
              type: 'string',
              description: 'Description of the system or component to analyze'
            },
            concerns: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['scalability', 'security', 'performance', 'maintainability', 'integration']
              },
              description: 'Specific architectural concerns to address'
            }
          },
          required: ['systemDescription']
        }
      },
      {
        name: 'task_planner_ninja',
        description: 'Deploy a planning specialist to break down complex tasks into manageable subtasks with dependencies.',
        inputSchema: {
          type: 'object',
          properties: {
            mainTask: {
              type: 'string',
              description: 'The main task to break down'
            },
            complexity: {
              type: 'string',
              description: 'Task complexity level',
              enum: ['simple', 'moderate', 'complex', 'very-complex'],
              default: 'moderate'
            },
            targetSubtasks: {
              type: 'number',
              description: 'Target number of subtasks (default: 5)',
              default: 5
            }
          },
          required: ['mainTask']
        }
      },
      {
        name: 'sensei_status',
        description: 'Check the status of the coding sensei and all active shadow clones. Useful for monitoring delegation efficiency.',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'create_shadow_clones': {
        const { mission, maxTokens = 1000 } = args;
        
        console.log(`🎯 Sensei received mission: ${mission}`);
        const result = await cloneManager.createClones(mission, maxTokens);
        
        return {
          content: [
            {
              type: 'text',
              text: `🥷 Shadow Clone Technique Executed!\n\n` +
                   `📋 Mission: ${result.originalMission}\n` +
                   `🔥 Jutsu Used: ${result.jutsuType}\n` +
                   `👥 Clones Created: ${result.cloneCount}\n` +
                   `✅ Successful: ${result.successfulClones}\n` +
                   `❌ Failed: ${result.failedClones}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}%\n` +
                   `💰 Tokens Saved: ${result.tokenStats.saved}\n\n` +
                   `📊 Results:\n${result.results.map(r => `• Clone ${r.cloneId}: ${r.output}`).join('\n')}\n\n` +
                   `🕐 Completed: ${result.completedAt}`
            }
          ]
        };
      }

      case 'code_review_ninja': {
        const { code, language = 'javascript', focus = 'all' } = args;
        
        const result = await cloneManager.createSpecializedClone('code_reviewer', 
          `Review this ${language} code with focus on ${focus}`, 
          { code, language, focus, maxTokens: 600 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `🔍 Code Review Ninja Report\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'debug_ninja': {
        const { debugInfo, language = 'javascript', context } = args;
        
        const result = await cloneManager.createSpecializedClone('debugger_ninja',
          `Debug this ${language} issue: ${debugInfo}`,
          { debugInfo, language, context, maxTokens: 500 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `🐛 Debug Ninja Analysis\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'research_ninja': {
        const { topic, depth = 'intermediate', focusAreas } = args;
        
        const result = await cloneManager.createSpecializedClone('research_ninja',
          `Research ${topic} at ${depth} level`,
          { topic, depth, focusAreas, maxTokens: 800 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `📚 Research Ninja Report\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'refactor_ninja': {
        const { codeToRefactor, language = 'javascript', goals } = args;
        
        const result = await cloneManager.createSpecializedClone('refactor_ninja',
          `Refactor this ${language} code`,
          { codeToRefactor, language, goals, maxTokens: 600 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `⚙️ Refactor Ninja Plan\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'testing_ninja': {
        const { featureDescription, testTypes, framework } = args;
        
        const result = await cloneManager.createSpecializedClone('testing_ninja',
          `Create testing strategy for: ${featureDescription}`,
          { featureDescription, testTypes, framework, maxTokens: 700 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `🧪 Testing Ninja Strategy\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'architect_ninja': {
        const { systemDescription, concerns } = args;
        
        const result = await cloneManager.createSpecializedClone('architect_ninja',
          `Analyze architecture for: ${systemDescription}`,
          { systemDescription, concerns, maxTokens: 800 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `🏗️ Architecture Ninja Analysis\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'task_planner_ninja': {
        const { mainTask, complexity = 'moderate', targetSubtasks = 5 } = args;
        
        const result = await cloneManager.createSpecializedClone('planner_ninja',
          `Break down task: ${mainTask}`,
          { mainTask, complexity, targetSubtasks, maxTokens: 600 }
        );
        
        return {
          content: [
            {
              type: 'text',
              text: `📋 Task Planner Ninja Breakdown\n\n` +
                   `${result.output}\n\n` +
                   `⚡ Token Efficiency: ${result.tokenStats.efficiency}% (${result.tokenStats.saved} tokens saved)\n` +
                   `🕐 ${result.timestamp}`
            }
          ]
        };
      }

      case 'sensei_status': {
        const status = cloneManager.getStatus();
        const senseiInfo = codingSensei.getInfo();
        
        return {
          content: [
            {
              type: 'text',
              text: `🥷 Coding Sensei Status Report\n\n` +
                   `👨‍🏫 Sensei: ${senseiInfo.name}\n` +
                   `🎯 Specialization: ${senseiInfo.specialization}\n` +
                   `📊 Experience: ${senseiInfo.experience}\n` +
                   `🎌 Focus: ${senseiInfo.focus}\n\n` +
                   `👥 Active Clones: ${status.activeClones}\n` +
                   `✅ Completed Missions: ${status.completedMissions}\n\n` +
                   `📈 Clone Status Breakdown:\n` +
                   `• Created: ${status.clonesByStatus.created}\n` +
                   `• Executing: ${status.clonesByStatus.executing}\n` +
                   `• Completed: ${status.clonesByStatus.completed}\n` +
                   `• Failed: ${status.clonesByStatus.failed}\n\n` +
                   `🎓 Educational Note: This demonstrates efficient task delegation and parallel processing!`
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
          text: `❌ Ninja technique failed: ${error.message}\n\nThe shadow clone encountered an unexpected obstacle. Please check your input and try again.`
        }
      ],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('🥷 Shadow Clone MCP Server running and ready for missions!');
  console.error('🎓 Perfect for learning task delegation and parallel processing concepts.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error('Failed to start server:', error);
    process.exit(1);
  });
}