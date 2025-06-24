# SwarmRouter Minimal MVP - MCP Server

A minimal implementation of the SwarmRouter concept that demonstrates AI task delegation using the bee/hive metaphor with stdout-based MCP (Model Context Protocol) communication.

## 🐝 What is SwarmRouter?

SwarmRouter is an AI orchestration platform that uses bee behavior metaphors to efficiently delegate tasks to different AI models. Think of it as a **digital beehive** where:

- **Tasks** are like flowers that need to be visited
- **Bees** are AI agents that carry out specific subtasks
- **Dances** are coordination patterns that determine how work is organized
- **The Hive** routes tasks to the most appropriate models based on complexity

## 🎯 Key Features

- **Stdout-based MCP Communication**: Simple, lightweight protocol without FastAPI dependencies
- **Anthropic Claude Integration**: Routes tasks to different Claude models based on complexity
- **Bee Dance Patterns**: Six different coordination strategies for different types of work
- **Token Optimization**: Estimates and tracks token savings through intelligent delegation
- **Educational Focus**: Heavily commented code that teaches MCP concepts
- **Minimal Dependencies**: Uses Python standard library as much as possible

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Optional: Anthropic API key for real AI integration (otherwise uses simulated responses)

### Installation

1. Clone or download the repository
2. Navigate to the `swarmrouter-mcp` directory
3. Install minimal dependencies:

```bash
pip install anthropic python-dotenv  # Optional for real AI integration
```

### Running the Demo

```bash
python minimal_mcp_server.py --demo
```

This runs an interactive demonstration showing how different types of tasks are:
- Analyzed for complexity
- Assigned appropriate dance patterns
- Delegated to suitable AI models
- Executed with token optimization

### Example Output

```
🐝 SwarmRouter Minimal MVP - Interactive Demo
==================================================

Demo 1: List all files in a directory
Expected: simple complexity, round dance
--------------------------------------------------
✅ Task ID: task_0001
🎭 Dance Type: round
🧠 Complexity: simple
🐝 Bees Assigned: 1
💰 Token Savings: 90.0%
📋 Task delegated to 1 bees using round dance pattern

🐝 Bee Details:
  • bee_task_0001_1: Execute: List all files in a directory
    Model: claude-3-haiku-20240307 | Status: completed
    Result: [Actual Claude response or simulated result]
```

## 🏗️ Architecture Overview

### Bee Dance Types

The system uses six different "dance" patterns inspired by real bee behavior:

| Dance Type | Use Case | Token Savings | Example Tasks |
|------------|----------|---------------|---------------|
| **WAGGLE** | Complex decomposition | 70% | "Build authentication system" |
| **ROUND** | Simple notifications | 10% | "List files in directory" |
| **SCOUT** | Research & exploration | 50% | "Research API best practices" |
| **TREMBLE** | Error handling | 30% | "Debug connection timeout" |
| **CONVERGE** | Consensus building | 60% | "Choose frontend framework" |
| **DISPERSE** | Parallel execution | 75% | "Process multiple files" |

### Model Routing

Tasks are automatically routed to appropriate Claude models based on complexity:

- **Simple Tasks** → Claude 3 Haiku (fast, efficient)
- **Medium Tasks** → Claude 3 Sonnet (balanced performance)
- **Complex Tasks** → Claude 3 Opus (maximum capability)

### Task Flow

1. **Task Analysis**: Determine complexity level and coordination pattern
2. **Bee Creation**: Generate subtasks and assign to specialized bees
3. **Model Selection**: Route each bee to appropriate Claude model
4. **Execution**: Process subtasks with token tracking
5. **Aggregation**: Combine results and calculate savings

## 🛠️ Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Logging Level
LOG_LEVEL=INFO
```

If no API key is provided, the system will use simulated responses to demonstrate the concepts.

## 📖 Usage Examples

### As a Standalone Demo

```bash
# Run interactive demonstration
python minimal_mcp_server.py --demo
```

### As an MCP Server

```bash
# Run as MCP server (stdin/stdout protocol)
python minimal_mcp_server.py --server
```

### Programmatic Usage

```python
from minimal_mcp_server import MinimalSwarmRouter
import asyncio

async def example():
    router = MinimalSwarmRouter()
    
    # Delegate a complex task
    task = await router.delegate_task(
        "Design and implement a REST API for user management",
        max_tokens=15000
    )
    
    print(f"Task {task.task_id} completed with {len(task.bees)} bees")
    print(f"Token savings: {task.calculate_token_savings():.1f}%")

asyncio.run(example())
```

## 🧪 Testing Different Task Types

Try these example tasks to see different dance patterns in action:

```python
# ROUND dance (simple tasks)
"Show current system status"
"List available endpoints"

# WAGGLE dance (complex decomposition)
"Build a complete user authentication system with JWT"
"Create a microservices architecture for e-commerce"

# SCOUT dance (research tasks)
"Research best practices for API security"
"Find optimal database design patterns"

# TREMBLE dance (debugging/fixing)
"Debug memory leak in user service"
"Fix the connection timeout errors"

# CONVERGE dance (decision making)
"Help team choose between React and Vue"
"Decide on deployment strategy for production"

# DISPERSE dance (parallel work)
"Process multiple data files concurrently"
"Generate reports for all departments"
```

## 🎓 Educational Value

This implementation teaches several important concepts:

### MCP Protocol Basics
- JSON-RPC message structure
- Tool registration and execution
- Resource management
- Error handling

### AI Orchestration Patterns
- Task complexity analysis
- Model selection strategies
- Token optimization techniques
- Result aggregation

### System Design
- Modular architecture
- Clean separation of concerns
- Extensible design patterns
- Configuration management

## 🔍 Code Structure

```
minimal_mcp_server.py
├── DanceType (enum)          # Bee coordination patterns
├── TaskComplexity (enum)     # Complexity classification
├── BeeAgent (class)          # Individual AI agents
├── SwarmTask (class)         # Task management
├── MinimalSwarmRouter (class) # Core delegation logic
├── MCPServer (class)         # Protocol handling
└── Demo functions            # Interactive examples
```

## 🚧 Extending the System

### Adding New Dance Types

```python
class DanceType(str, Enum):
    # ... existing types ...
    CUSTOM = "custom"

# Add keywords for detection
self.dance_keywords[DanceType.CUSTOM] = ["custom", "special", "unique"]

# Add subtask templates
def generate_subtasks(self, description: str, dance_type: DanceType) -> List[str]:
    templates = {
        # ... existing templates ...
        DanceType.CUSTOM: [f"Custom task 1: {description}", ...]
    }
```

### Adding New Models

```python
# Add to model routing
self.model_routing = {
    TaskComplexity.SIMPLE: "gpt-3.5-turbo",     # Example: OpenAI
    TaskComplexity.MEDIUM: "gpt-4",             # models
    TaskComplexity.COMPLEX: "claude-3-opus"
}
```

### Custom Complexity Analysis

```python
def analyze_task_complexity(self, description: str) -> TaskComplexity:
    # Implement custom logic
    # Could use ML models, regex patterns, etc.
    pass
```

## 🔗 Integration with Full SwarmRouter

This minimal MVP serves as a foundation for the complete SwarmRouter system described in the repository. Key concepts demonstrated here scale to:

- **Ring Architecture**: Hierarchical security and capability layers
- **FastAPI Integration**: Full web server with API endpoints
- **Advanced Visualization**: Real-time swarm monitoring
- **Database Persistence**: Task and bee state management
- **Multi-model Support**: Integration with multiple AI providers

## 📋 Next Steps

To evolve this MVP into a full SwarmRouter implementation:

1. **Add FastAPI Layer**: REST API for web integration
2. **Implement Database**: Persistent task and bee storage
3. **Add Authentication**: Secure access controls
4. **Create Visualization**: Real-time swarm monitoring dashboard
5. **Multi-provider Support**: Integration with OpenAI, Anthropic, local models
6. **Advanced Routing**: Machine learning-based task analysis

## 🤝 Contributing

This minimal implementation is designed to be:
- **Educational**: Easy to understand and modify
- **Extensible**: Clear extension points for new features
- **Maintainable**: Well-documented and tested

Feel free to experiment, extend, and improve upon this foundation!

## 📄 License

See the main repository LICENSE file for licensing information.

---

**🐝 Keep It Simple, Swarmers!** 

This minimal MVP demonstrates that powerful AI orchestration concepts can be implemented with surprisingly little code when you focus on the core ideas rather than infrastructure complexity.