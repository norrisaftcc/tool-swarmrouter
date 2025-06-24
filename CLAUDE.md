# CLAUDE.md - SwarmRouter Project Context

## Project Overview

SwarmRouter (originally "Project Waggle") is a distributed AI orchestration platform that demonstrates efficient swarm intelligence for development tasks. The system uses a bee/hive metaphor where LLMs (llamas) are paired with bee metadata that choreographs their collaboration.

## Key Concepts

### 🐝 The Bee-Llama Metaphor
- Each LLM (llama) has a companion "bee" that carries metadata
- Bees perform different "dances" to communicate task types:
  - **Waggle dance**: Complex task decomposition
  - **Round dance**: Simple notifications
  - **Scout dance**: Exploration and research
  - **Tremble dance**: Error/issue alerts
  - **Converge dance**: Consensus building
  - **Disperse dance**: Parallel execution

### 🏗️ Ring Architecture
The HIVE uses a ring-based architecture inspired by CPU protection rings:
- **Ring 0**: Core system (MCP protocol, auth, database)
- **Ring 1**: Essential dev tools (architect, orchestrator)
- **Ring 2**: Extended tools (chronicler, intelligence)
- **Ring 3**: External integrations (GitHub, Slack)
- **Ring 4**: UI/Visualization (Observatory, dashboards)

### 📊 Token Efficiency
The project demonstrates significant token savings through delegation:
- Complex analysis tasks: 80-82% savings
- Planning/coordination: 65-70% savings
- Documentation generation: 60-67% savings
- Overall average: 73% token reduction

## Development Guidelines

### Code Style
- Follow FastAPI best practices for the HIVE server
- Use type hints throughout Python code
- Implement proper error handling with meaningful messages
- Write self-documenting code (minimize comments unless explaining "why")

### Testing
When implementing features, ensure:
- Unit test coverage >80%
- Integration tests for tool combinations
- Performance benchmarks for new tools
- Load testing for streaming connections

### Documentation
- Every new module needs comprehensive documentation
- Include examples and use cases
- Update architecture diagrams when adding rings/modules
- Create educational materials for student use

## Important Commands

### Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run linting
ruff check .
mypy .

# Start HIVE server
uvicorn hive.main:app --reload

# Start visualizer
streamlit run hive_visualizer/app.py
```

### Git Workflow
```bash
# Always create feature branches
git checkout -b feature/description

# Commit with conventional commits
git commit -m "feat(scope): description"

# Create PRs with detailed descriptions
gh pr create --title "feat: Title" --body "..."
```

## Project Structure

```
tool-swarmrouter/
├── docs/                    # All documentation
│   ├── inspiration/         # Reference materials
│   ├── *-task-decomposition.md
│   ├── *-architecture.md
│   └── *-module.md
├── hive/                    # Core HIVE server (future)
│   ├── rings/              # Ring modules
│   ├── tools/              # Tool implementations
│   └── main.py             # FastAPI app
├── hive_visualizer/         # Streamlit dashboard (future)
├── tests/                   # Test suite
└── CLAUDE.md               # This file
```

## Current State (as of last interaction)

### 📋 Persistent TODO List
**See `docs/TODOS.md` for the complete, persistent task list that survives session interruptions.**

### Completed
- Comprehensive documentation for HIVE architecture
- Task decomposition following Agile practices
- Ring-based modular system design
- HIVE Visualizer module specification
- Contributor guide module design
- GitHub workflow documentation for students
- Llama-bee metadata system

### In Progress
- PR #5: Documentation merge
- Issue #4: Task decomposition (closing with PR #5)

### Next Steps (Sprint 1)
1. Implement Ring 0 core infrastructure
2. Set up FastAPI project structure
3. Create MCP protocol handlers
4. Implement streaming HTTP/WebSocket support
5. Add basic authentication
6. **CRITICAL**: Implement persistent state management (see TODOS.md)

## Educational Focus

This project is designed to teach:
1. **Agile Development**: Sprint planning, task decomposition
2. **Open Source Contribution**: GitHub workflows, PR processes
3. **System Architecture**: Modular design, ring-based security
4. **AI Orchestration**: Efficient delegation patterns
5. **Collaborative Development**: Group contribution modes

## Key Design Decisions

1. **FastAPI over Flask**: Better async support, automatic OpenAPI docs
2. **Ring Architecture**: Allows progressive enhancement and security isolation
3. **Bee Metaphor**: Makes swarm coordination intuitive and visual
4. **Token Optimization**: Core metric for system efficiency
5. **Educational First**: Every feature should be learnable

## Useful Context for Future Sessions

### When implementing the HIVE server:
- Start with Ring 0 only, ensure stability
- Use Anthropic's MCP examples as reference
- Implement health checks and monitoring early
- Design for horizontal scaling from the start

### When building the visualizer:
- Use Streamlit for rapid prototyping
- Show real-time bee dances and token savings
- Include "tune in" feature to see agent conversations
- Make it engaging for demos

### When creating dev tools:
- Each tool should map to a specific bee dance
- Implement caching for repeated operations
- Use streaming for long-running tasks
- Provide clear progress indicators

## Model Selection Strategy (To Discuss)

Considerations for model routing:
- **architect:* tools**: Need strong reasoning (Claude/GPT-4)
- **orchestrator:* tools**: Planning capabilities (GPT-4)
- **chronicler:* tools**: Consistency important (GPT-3.5 sufficient)
- **intelligence:* tools**: Deep analysis (Claude preferred)

## Remember

- This is a teaching tool as much as a development platform
- Token efficiency proves the delegation concept
- The bee metaphor should be fun and educational
- Documentation is as important as code
- Students will use this to learn OSS contribution

---

*Last updated: During implementation of PR #5 - HIVE architecture documentation*