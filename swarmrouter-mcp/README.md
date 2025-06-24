# SwarmRouter MCP Server

A Model Context Protocol (MCP) server that demonstrates efficient task delegation using a bee swarm metaphor. This server shows how complex AI tasks can be broken down and delegated to specialized agents (bees) for significant token savings.

## Overview

SwarmRouter uses nature-inspired coordination patterns based on how bees communicate:

- **🕺 Waggle Dance**: Complex task decomposition (70%+ token savings)
- **⭕ Round Dance**: Simple notifications (10-20% token savings)
- **🔍 Scout Dance**: Research and exploration (50% token savings)
- **🚨 Tremble Dance**: Error handling (30% token savings)
- **🤝 Converge Dance**: Consensus building (60% token savings)
- **📊 Disperse Dance**: Parallel execution (75% token savings)

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/norrisaftcc/tool-swarmrouter.git
cd tool-swarmrouter/swarmrouter-mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys (if needed for future features)
```

### Running the Server

#### Using MCP CLI (Recommended)

```bash
# Start the server
mcp run src/server.py

# Or use the inspector for testing
mcp dev src/server.py
```

#### Testing without MCP

```bash
# Run in test mode
python -m src.server
```

## Usage

### Basic Task Delegation

```python
# Example: Delegate a complex task
result = await delegate_task(
    task_description="Build a user authentication system with JWT tokens",
    task_type="waggle",  # Complex task decomposition
    priority="high",
    max_tokens=15000
)

# Result:
{
    "task_id": "task_abc123",
    "dance_type": "waggle",
    "assigned_bees": 4,
    "estimated_token_savings": 73.0,
    "message": "Task delegated to 4 bees using waggle dance"
}
```

### Available Tools

#### `delegate_task`
Delegates a task to the bee swarm.

Parameters:
- `task_description` (required): Description of the task
- `task_type` (optional): Dance type (waggle, round, scout, tremble, converge, disperse)
- `priority` (optional): Task priority (low, medium, high, critical)
- `max_tokens` (optional): Maximum token budget (default: 10000)
- `subtasks` (optional): List of subtasks (auto-generated if not provided)

#### `get_task_status`
Check the status of a delegated task.

Parameters:
- `task_id` (required): The task ID to check

### Available Resources

- `swarm://status` - Get overall swarm statistics
- `swarm://tasks` - List all tasks in the system

## Architecture

```
swarmrouter-mcp/
├── src/
│   ├── server.py      # Main MCP server
│   ├── models.py      # Data models (Task, Bee, etc.)
│   └── delegation.py  # Task delegation logic
├── tests/             # Test suite
├── examples/          # Usage examples
└── README.md         # This file
```

## How It Works

1. **Task Analysis**: When a task is submitted, the system analyzes it to determine the optimal coordination pattern (dance type).

2. **Bee Assignment**: Based on the dance type, appropriate "bees" (AI agents) are created with specific roles and token budgets.

3. **Task Decomposition**: Complex tasks are automatically broken down into subtasks, each assigned to a different bee.

4. **Token Optimization**: The system estimates token usage and optimizes allocation to achieve the target 73% average savings.

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Code Style

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
ruff check src/
```

### Contributing

1. Create a feature branch
2. Make your changes with tests
3. Ensure all tests pass
4. Submit a PR with clear description

## Educational Notes

This server is designed as a learning tool to demonstrate:

1. **MCP Protocol**: How to build servers that integrate with AI systems
2. **Task Decomposition**: Breaking complex problems into manageable pieces
3. **Swarm Intelligence**: Coordinating multiple agents efficiently
4. **Token Optimization**: Reducing AI costs through smart delegation

### Understanding the Bee Metaphor

Real bees use different dances to communicate:
- **Waggle dance** tells other bees about distant food sources with precise directions
- **Round dance** indicates nearby food sources
- **Tremble dance** signals that more receiver bees are needed

We use these patterns to coordinate AI agents:
- **Waggle** = Complex tasks needing detailed instructions
- **Round** = Simple tasks with straightforward execution
- **Tremble** = Tasks requiring error handling or debugging

## Troubleshooting

### MCP not found
```bash
pip install 'mcp[cli]'
```

### Import errors
Ensure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Server won't start
Check the logs:
```bash
export LOG_LEVEL=DEBUG
mcp run src/server.py
```

## Future Enhancements

- [ ] Persistent task storage
- [ ] Real AI model integration
- [ ] WebSocket streaming for real-time updates
- [ ] Multi-model routing based on task type
- [ ] Performance benchmarking tools

## License

This project is part of the SwarmRouter educational platform. See the main repository for license details.