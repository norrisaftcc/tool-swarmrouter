# Copilot Instructions for SwarmRouter 🐝

## Project Overview

SwarmRouter (Project Waggle) is a distributed AI orchestration platform that enables coordinated swarm intelligence for development tasks. The system uses a bee/hive metaphor where LLMs (llamas) are paired with bee metadata that choreographs their collaboration. The core philosophy is "Keep It Simple Swarmers" while building an intelligent development ecosystem.

## System Architecture

SwarmRouter consists of three main components:

### 🏠 The HIVE - Central MCP Server
A remotely deployed streaming HTTP MCP (Model Context Protocol) server with development tools exposed via FastAPI, serving as the central coordination hub. The HIVE implements a ring-based architecture:

- **Ring 0**: Core system (MCP protocol, auth, database)
- **Ring 1**: Essential dev tools (architect, orchestrator)  
- **Ring 2**: Extended tools (chronicler, intelligence)
- **Ring 3**: External integrations (GitHub, Slack)
- **Ring 4**: UI/Visualization (Observatory, dashboards)

### 🐝 The Swarm - Distributed Agent Network
Deployed from the HIVE, utilizing the main server's services to spawn and coordinate multiple AI models with bee metadata for task choreography.

### 🔭 The Observatory - Real-time Dashboard
Python-based dashboards (Streamlit) for real-time visualization of model activities with activity word clouds and bee dance patterns.

## 🐝 Bee-Llama Metaphor

Each LLM (llama) has a companion "bee" that carries metadata and choreographs collaboration:

- **Waggle dance**: Complex task decomposition
- **Round dance**: Simple notifications  
- **Scout dance**: Exploration and research
- **Tremble dance**: Error/issue alerts
- **Converge dance**: Consensus building
- **Disperse dance**: Parallel execution

### Bee Metadata Structure
```json
{
  "bee": {
    "id": "bee-7f3a9c",
    "llama": {
      "model": "gpt-4",
      "provider": "openai",
      "temperature": 0.7
    },
    "role": {
      "type": "architect",
      "specialization": "decomposition",
      "ring_level": 1
    },
    "dance": {
      "pattern": "waggle",
      "intensity": 0.8,
      "direction": "task_breakdown"
    },
    "nectar": {
      "tokens_collected": 1523,
      "tokens_saved": 4821,
      "efficiency_ratio": 0.76
    }
  }
}
```

## Development Tools Suite

The HIVE provides four categories of development tools:

### 🏗️ Architect Tools (Ring 1)
- `architect:decompose` - Break down complex development tasks
- `architect:design_solution` - Create technical designs
- `architect:review_architecture` - Evaluate system designs

### 🎯 Orchestrator Tools (Ring 1) 
- `orchestrator:plan_sprint` - Create development sprints
- `orchestrator:distribute_work` - Assign tasks to team members
- `orchestrator:find_blockers` - Identify project impediments

### 📚 Chronicler Tools (Ring 2)
- `chronicler:document_system` - Generate technical documentation
- `chronicler:track_decisions` - Record architectural decisions
- `chronicler:update_docs` - Maintain documentation currency

### 🧠 Intelligence Tools (Ring 2)
- `intelligence:analyze_code` - Code quality analysis
- `intelligence:suggest_improvements` - Optimization recommendations
- `intelligence:predict_issues` - Proactive problem identification

## Code Formatting Standards

### Required Tools
- **black**: Code formatter with line length of 88 characters
- **isort**: Import statement organizer with black compatibility
- **flake8**: Linting for code quality
- **mypy**: Type checking for bee metadata and MCP interfaces

### Configuration
```bash
# Format code
black --line-length 88 .
isort --profile black .

# Lint and type check
flake8 --max-line-length 88 --extend-ignore E203,W503 .
mypy src/ --ignore-missing-imports
```

## MCP Server Development

### Core MCP Implementation
The HIVE server implements the Model Context Protocol (MCP) for standardized tool communication:

```python
# Example MCP tool implementation
@mcp_tool
async def architect_decompose(task_description: str, complexity_level: int = 1) -> TaskBreakdown:
    """Decompose a development task into manageable subtasks.
    
    Args:
        task_description: Description of the task to decompose
        complexity_level: Complexity level (1-5)
        
    Returns:
        TaskBreakdown with subtasks and bee assignments
    """
    bee_metadata = await get_bee_for_task("architect", "decomposition")
    result = await process_with_bee(task_description, bee_metadata)
    await log_bee_dance("waggle", bee_metadata.id, result.intensity)
    return result
```

### Streaming Support
All MCP tools support streaming for real-time feedback:

```python
@mcp_tool(streaming=True)
async def orchestrator_plan_sprint(requirements: List[str]) -> AsyncIterator[SprintUpdate]:
    """Stream sprint planning updates as they're generated."""
    async for update in generate_sprint_plan(requirements):
        yield SprintUpdate(
            step=update.step,
            progress=update.progress,
            bee_activity=update.bee_metadata
        )
```

## Development Workflow

### Getting Started
1. Clone the repository
2. Set up a Python virtual environment (Python 3.9+ recommended)
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install -r requirements-dev.txt`
5. Review the system architecture documentation in `docs/`

### Running the HIVE Server
```bash
# Development MCP server with auto-reload
uvicorn src.hive.main:app --reload --host 0.0.0.0 --port 8000

# Run with bee metadata logging
ENABLE_BEE_LOGGING=true uvicorn src.hive.main:app --reload

# Production HIVE deployment
uvicorn src.hive.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Running the Observatory
```bash
# Start the visualization dashboard
streamlit run src/observatory/dashboard.py --server.port 8501

# View bee activity in real-time
streamlit run src/observatory/bee_monitor.py
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage for HIVE components
pytest --cov=src/hive --cov=src/observatory --cov-report=html

# Test specific components
pytest tests/unit/hive/           # HIVE server tests
pytest tests/unit/observatory/    # Observatory tests
pytest tests/integration/mcp/     # MCP protocol tests
pytest tests/integration/bee/     # Bee metadata tests

# Test development tools
pytest tests/tools/architect/     # Architect tools
pytest tests/tools/orchestrator/  # Orchestrator tools
pytest tests/tools/chronicler/    # Chronicler tools
pytest tests/tools/intelligence/  # Intelligence tools
```

### Educational Testing
SwarmRouter serves as a teaching platform, so include pedagogical test examples:

```bash
# Run example-driven tests for students
pytest tests/educational/ --verbose

# Test bee dance pattern recognition
pytest tests/bee_choreography/ -v

# Validate token efficiency demonstrations
pytest tests/token_efficiency/ -v
```

### Linting and Code Quality
```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting (CI pipeline) 
black --check src/ tests/
isort --check-only src/ tests/

# Lint code with bee-specific rules
flake8 src/ tests/
mypy src/ --ignore-missing-imports

# Validate MCP tool signatures
python scripts/validate_mcp_tools.py

# Check bee metadata schemas
python scripts/validate_bee_schemas.py
```

### Health Checks
```bash
# Quick development check with bee validation
make dev-check  # black && isort && flake8 && pytest && bee-validate

# Full CI pipeline with MCP compliance check
make ci-check

# HIVE server health check
curl http://localhost:8000/health

# Observatory health check
curl http://localhost:8501/health
```

## Repository Structure

```
tool-swarmrouter/
├── src/
│   ├── hive/                    # 🏠 HIVE MCP Server
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── mcp_server.py       # MCP protocol implementation
│   │   ├── rings/              # Ring-based architecture
│   │   │   ├── ring0/          # Core system (auth, database)
│   │   │   ├── ring1/          # Essential tools (architect, orchestrator)
│   │   │   ├── ring2/          # Extended tools (chronicler, intelligence)
│   │   │   ├── ring3/          # External integrations
│   │   │   └── ring4/          # UI components
│   │   ├── tools/              # Development tool implementations
│   │   │   ├── architect/      # Task decomposition tools
│   │   │   ├── orchestrator/   # Project management tools
│   │   │   ├── chronicler/     # Documentation tools  
│   │   │   └── intelligence/   # Analysis tools
│   │   ├── bee/                # 🐝 Bee metadata system
│   │   │   ├── metadata.py     # Bee metadata models
│   │   │   ├── choreography.py # Dance pattern management
│   │   │   └── efficiency.py   # Token efficiency tracking
│   │   ├── models/             # Pydantic models and schemas
│   │   ├── services/           # Business logic services
│   │   └── config/             # Configuration management
│   ├── observatory/            # 🔭 Real-time Dashboard
│   │   ├── dashboard.py        # Main Streamlit dashboard
│   │   ├── bee_monitor.py      # Bee activity visualization
│   │   ├── hive_visualizer.py  # Ring topology rendering
│   │   └── components/         # Dashboard components
│   └── swarm/                  # 🐝 Distributed Agent Network
│       ├── agents/             # Individual AI agents
│       ├── coordination/       # Swarm coordination logic
│       └── deployment/         # Agent deployment scripts
├── tests/
│   ├── unit/
│   │   ├── hive/              # HIVE server tests
│   │   ├── observatory/       # Observatory tests
│   │   └── swarm/             # Swarm tests
│   ├── integration/
│   │   ├── mcp/               # MCP protocol integration tests
│   │   ├── bee/               # Bee choreography tests
│   │   └── e2e/               # End-to-end workflow tests
│   ├── tools/                 # Development tool tests
│   │   ├── architect/         # Architect tool tests
│   │   ├── orchestrator/      # Orchestrator tool tests
│   │   ├── chronicler/        # Chronicler tool tests
│   │   └── intelligence/      # Intelligence tool tests
│   ├── educational/           # 📚 Educational test examples
│   ├── bee_choreography/      # Bee dance pattern tests
│   └── fixtures/              # Test data and fixtures
├── docs/                      # 📖 Documentation
│   ├── system-architecture.md # System design documentation
│   ├── development-task-decomposition.md
│   ├── llama-bee-metadata.md  # Bee metadata specification
│   ├── sprint-roadmap.md      # Development roadmap
│   ├── github-workflow-guide.md
│   ├── educational-materials/ # Teaching resources
│   └── inspiration/           # MCP usage patterns
├── scripts/                   # Utility and deployment scripts
│   ├── validate_mcp_tools.py  # MCP tool validation
│   ├── validate_bee_schemas.py # Bee metadata validation
│   └── deploy_hive.py         # HIVE deployment script
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── pyproject.toml            # Python project configuration
├── Dockerfile                # HIVE container configuration
├── docker-compose.yml        # Full system deployment
├── .env.example              # Environment configuration template
└── README.md                 # Project documentation
```

## Development Guidelines

### Python Code Style
- Write **idiomatic Python** following PEP 8 standards
- Use type hints for all function signatures, especially MCP tool interfaces
- Implement bee metadata consistently across all components
- Prefer composition over inheritance for bee choreography
- Use descriptive variable and function names that reflect the bee/hive metaphor
- Keep functions focused and single-purpose for tool modularity

### MCP Tool Design
- Design **clear MCP tool signatures** with explicit parameter types
- Use Pydantic models for all tool request/response schemas  
- Follow MCP protocol standards for tool registration and invocation
- Implement streaming support for long-running operations
- Provide comprehensive tool documentation with examples
- Include bee metadata in all tool responses for choreography tracking

### Bee Metadata Integration
- **Always include bee metadata** in tool responses and logging
- Track token efficiency (nectar collection) for all operations
- Implement appropriate dance patterns for different tool types:
  - **Waggle dance** for complex decomposition tasks
  - **Round dance** for simple status updates
  - **Scout dance** for research and discovery
  - **Tremble dance** for error conditions
- Log bee activity for Observatory visualization
- Maintain bee lineage and collaboration history

### FastAPI Integration
- Use FastAPI as the web framework for the HIVE server
- Implement proper HTTP streaming for MCP protocol compliance
- Provide OpenAPI documentation for all endpoints
- Include bee metadata in HTTP response headers where appropriate
- Implement proper error handling with bee dance error patterns

### Documentation
- Write **comprehensive docstrings** using Google style
- Include bee metadata examples in all tool documentation
- Document dance patterns and their appropriate usage
- Keep architectural decision records (ADRs) updated
- Include educational examples for students learning the system
- Document token efficiency patterns and best practices

### Logging and Monitoring
- Implement **structured logging** with bee metadata integration
- Use appropriate log levels with bee dance context
- Log bee choreography patterns for Observatory visualization
- Include correlation IDs for request tracing across the swarm
- Track performance metrics and token efficiency
- Implement bee activity monitoring for real-time dashboards

### Educational Focus
- Design components as **teaching tools** for software development
- Include comprehensive examples and educational materials
- Implement clear separation of concerns for pedagogical clarity
- Provide debugging tools that visualize bee interactions
- Create learning progressions from simple to complex patterns
- Document common anti-patterns and how to avoid them

### Ring-Based Architecture
- Design components according to **ring security levels**:
  - **Ring 0**: Core system components (authentication, database, MCP protocol)
  - **Ring 1**: Essential development tools (architect, orchestrator)
  - **Ring 2**: Extended tools (chronicler, intelligence)
  - **Ring 3**: External integrations (GitHub, Slack, other APIs)
  - **Ring 4**: User interfaces and visualization (Observatory)
- Implement proper access controls between rings
- Design for horizontal scaling within each ring
- Maintain clear separation of concerns between rings

### Testing Strategy
- Write **comprehensive tests** for all MCP tools and bee interactions
- Test bee metadata consistency across tool invocations
- Include integration tests for complete bee choreography cycles
- Test error handling with appropriate dance patterns
- Maintain >80% test coverage for HIVE server and development tools
- Include educational test examples for student learning
- Test token efficiency tracking and nectar accumulation
- Validate MCP protocol compliance

### Configuration Management
- Use environment variables for runtime configuration
- Provide sensible defaults for development environments
- Support multiple deployment profiles (dev, staging, prod, educational)
- Validate configuration at HIVE startup
- Document all configuration options with bee/hive context
- Include bee metadata configuration (dance patterns, token tracking)
- Configure Observatory visualization settings

## SwarmRouter-Specific Implementation Notes

### HIVE Server Development
- The **MCP server is the primary focus** - it coordinates all bee activities
- Implement proper streaming support for real-time bee choreography
- Design tools to be **both functional and educational**
- Each development tool should demonstrate best practices
- Token efficiency is critical - track nectar collection carefully
- The HIVE should gracefully handle bee failures and reassignment

### Bee Choreography Patterns
- **Waggle dance**: Use for complex task decomposition (architect tools)
- **Round dance**: Use for simple notifications and status updates
- **Scout dance**: Use for exploration and research activities
- **Tremble dance**: Use for error conditions and alerts
- **Converge dance**: Use for consensus building across multiple bees
- **Disperse dance**: Use for parallel task execution

### Observatory Integration
- All bee activities should be **visible in the Observatory**
- Implement real-time bee dance visualization
- Track token efficiency metrics and display nectar collection
- Provide educational dashboards for students
- Include debugging tools for bee interaction analysis
- Support "tune in" features to observe agent conversations

### Educational Platform Requirements
- This is a **teaching tool as much as a development platform**
- Include comprehensive examples for students learning OSS contribution
- Document all patterns and anti-patterns clearly
- Provide scaffolding for different skill levels
- Token efficiency should prove the delegation concept
- The bee metaphor should be fun and educational
- Create clear learning progressions from simple to complex

## Development Roadmap Integration

Follow the sprint-based development approach:

### Sprint 1-2: Foundation
- Implement core HIVE server with MCP protocol
- Set up basic bee metadata system
- Create essential development tools (architect, orchestrator)
- Establish Observatory foundation

### Sprint 3-4: Enhanced Tools
- Complete chronicler and intelligence tools
- Implement full bee choreography system
- Add external integrations (GitHub, etc.)
- Enhance Observatory visualizations

### Sprint 5-6: Production Readiness
- Optimize performance and token efficiency
- Implement comprehensive monitoring
- Complete educational materials and examples
- Prepare for deployment and scaling

## Documentation Updates and Maintenance

When making changes to SwarmRouter:
- **Update system architecture documentation** in `docs/system-architecture.md`
- **Refresh MCP tool specifications** if tool interfaces change
- **Update bee metadata schemas** when dance patterns evolve
- **Maintain educational materials** in `docs/educational-materials/`
- **Update this copilot-instructions.md** if development practices change
- **Keep Observatory documentation current** for visualization features
- **Document any new environment variables** or configuration options
- **Update the sprint roadmap** based on development progress
- **Maintain ADRs** (Architectural Decision Records) for major choices
- **Update student workflow guides** for educational use

## Getting Help and Resources

### Internal Documentation
- Check **system architecture docs** for design decisions
- Review **llama-bee metadata documentation** for bee integration
- Consult **development task decomposition** for sprint planning
- Reference **educational materials** for student examples

### Development Support  
- Follow established **bee choreography patterns** in the codebase
- Use the **Observatory dashboard** to debug bee interactions
- Check **GitHub workflow guide** for contribution processes
- Review **instructor quick patterns** for educational use cases

### Core Principles
- **MCP server first** - everything flows through the HIVE
- **Educational focus** - design for learning and teaching
- **Bee metaphor consistency** - maintain the choreography model
- **Token efficiency** - always track and optimize nectar collection
- **Ring architecture** - respect security boundaries and separation of concerns
- **Documentation as code** - keep docs current with implementation
- When in doubt, prioritize **simplicity and educational value**

---

*🐝 Remember: SwarmRouter is both a powerful development platform and an educational tool. Every component should serve both purposes effectively while maintaining the delightful bee/hive metaphor that makes learning fun and intuitive.*