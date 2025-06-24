# 🐝 SwarmRouter - AI Task Orchestration Platform
*it's a swarm router, it routes swarms.*

**Keep It Simple, Swarmers!**

*(originally "Project Waggle" after the famous bee dance)*

SwarmRouter is an AI orchestration platform that uses bee behavior metaphors to efficiently delegate tasks to different AI models. Think of it as a **digital beehive** where tasks are intelligently routed to the most appropriate AI agents based on complexity and coordination patterns.

## 🚀 Quick Start - Minimal MVP

Want to see SwarmRouter in action right now? We've created a minimal MVP that demonstrates all the core concepts with minimal setup:

```bash
cd swarmrouter-mcp
./start_minimal.sh
```

Or manually:
```bash
cd swarmrouter-mcp
pip install anthropic python-dotenv  # Optional
python minimal_mcp_server.py --demo
```

This will run an interactive demonstration showing how different types of tasks are:
- Analyzed for complexity (simple/medium/complex)
- Assigned bee dance patterns (waggle/round/scout/tremble/converge/disperse) 
- Routed to appropriate AI models (Claude Haiku/Sonnet/Opus)
- Executed with intelligent token optimization

## 📖 Documentation

- **[Minimal MVP Guide](swarmrouter-mcp/README_MINIMAL_MVP.md)** - Start here! Complete guide to the minimal implementation
- **[Project Context](CLAUDE.md)** - Full vision, architecture, and roadmap
- **[Examples](swarmrouter-mcp/examples.py)** - Programmatic usage examples

## 🏗️ Architecture Overview

### 🐝 The Bee-Llama Metaphor
- **Tasks** are like flowers that need to be visited
- **Bees** are AI agents that carry out specific subtasks  
- **Dances** are coordination patterns that determine how work is organized
- **The Hive** routes tasks to the most appropriate models based on complexity

### Six Dance Types

| Dance | Purpose | Token Savings | Example |
|-------|---------|---------------|---------|
| **WAGGLE** | Complex decomposition | 70% | "Build auth system" |
| **ROUND** | Simple notifications | 10% | "List files" |
| **SCOUT** | Research & exploration | 50% | "Find best practices" |
| **TREMBLE** | Error handling | 30% | "Debug timeout" |
| **CONVERGE** | Consensus building | 60% | "Choose framework" |
| **DISPERSE** | Parallel execution | 75% | "Process files" |

### Model Routing
- **Simple Tasks** → Claude 3 Haiku (fast, efficient)
- **Medium Tasks** → Claude 3 Sonnet (balanced)  
- **Complex Tasks** → Claude 3 Opus (maximum capability)

## 🛣️ Implementation Roadmap

1. **✅ Minimal MVP** - Stdout-based MCP server (current)
2. **🔄 FastAPI Integration** - Full web server with REST API
3. **📊 Visualization** - Real-time swarm monitoring dashboard
4. **🏢 Enterprise Features** - Authentication, persistence, scaling
5. **🌐 Multi-provider** - OpenAI, local models, custom integrations

## 🤝 Contributing

This project is designed to be educational and collaborative:
- Start with the minimal MVP to understand concepts
- Each component is well-documented and tested
- Clear extension points for adding new features
- Focus on learning AI orchestration patterns

## 📄 License

See LICENSE file for details.

---

**🐝 From simple stdout demos to enterprise orchestration - SwarmRouter grows with your needs!**
