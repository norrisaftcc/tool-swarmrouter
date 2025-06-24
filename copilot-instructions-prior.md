# Copilot Instructions for SwarmRouter 🐝

## Project Overview

SwarmRouter (Project Waggle) is a distributed AI orchestration platform using a bee/hive metaphor where LLMs (llamas) are paired with bee metadata for collaborative development tasks. Philosophy: "Keep It Simple Swarmers."

## System Architecture

Three main components:

### 🏠 The HIVE - Central MCP Server
Streaming HTTP MCP (Model Context Protocol) server with FastAPI, implementing ring-based architecture:
- **Ring 0**: Core system (MCP, auth, database)
- **Ring 1**: Essential tools (architect, orchestrator)  
- **Ring 2**: Extended tools (chronicler, intelligence)
- **Ring 3**: External integrations (GitHub, Slack)
- **Ring 4**: UI/Visualization (Observatory)

### 🐝 The Swarm - Distributed Agent Network
AI agents deployed from HIVE with bee metadata choreography.

### 🔭 The Observatory - Real-time Dashboard
Streamlit dashboards for model activity visualization and bee dance patterns.

## 🐝 Bee-Llama Metaphor

Each LLM (llama) has a companion "bee" with metadata for choreographed collaboration:

**Dance Patterns**: Waggle (decomposition), Round (notifications), Scout (research), Tremble (errors), Converge (consensus), Disperse (parallel)

**Bee Metadata**:
```json
{
  "bee": {
    "id": "bee-7f3a9c",
    "llama": {"model": "gpt-4", "provider": "openai"},
    "role": {"type": "architect", "ring_level": 1},
    "dance": {"pattern": "waggle", "intensity": 0.8},
    "nectar": {"tokens_collected": 1523, "efficiency_ratio": 0.76}
  }
}
```

## Development Tools Suite

**🏗️ Architect Tools (Ring 1)**: `decompose`, `design_solution`, `review_architecture`
**🎯 Orchestrator Tools (Ring 1)**: `plan_sprint`, `distribute_work`, `find_blockers`
**📚 Chronicler Tools (Ring 2)**: `document_system`, `track_decisions`, `update_docs`
**🧠 Intelligence Tools (Ring 2)**: `analyze_code`, `suggest_improvements`, `predict_issues`

## Code Standards & MCP Development

**Formatting**: black (line length 88), isort (black profile), flake8, mypy
**Commands**: `black . && isort . && flake8 . && mypy src/`

**MCP Tool Example**:
```python
@mcp_tool
async def architect_decompose(task_description: str) -> TaskBreakdown:
    bee_metadata = await get_bee_for_task("architect", "decomposition")
    result = await process_with_bee(task_description, bee_metadata)
    await log_bee_dance("waggle", bee_metadata.id, result.intensity)
    return result
```

**Streaming Support**: All tools support streaming with `@mcp_tool(streaming=True)`

## Development Workflow

**Setup**: 
1. Clone repo, Python 3.9+ venv
2. `pip install -r requirements.txt -r requirements-dev.txt`

**Run HIVE**: `uvicorn src.hive.main:app --reload --port 8000`
**Run Observatory**: `streamlit run src.observatory/dashboard.py --server.port 8501`

**Testing**:
```bash
pytest                                    # All tests
pytest --cov=src/hive --cov-report=html  # With coverage
pytest tests/educational/ -v             # Educational examples
pytest tests/bee_choreography/ -v        # Bee dance patterns
```

**Linting**: `make dev-check` (black && isort && flake8 && pytest)
**Health**: `curl http://localhost:8000/health`

## Repository Structure

```
tool-swarmrouter/
├── src/
│   ├── hive/                    # 🏠 HIVE MCP Server
│   │   ├── main.py             # FastAPI application
│   │   ├── rings/              # Ring 0-4 architecture
│   │   ├── tools/              # Development tools
│   │   └── bee/                # 🐝 Bee metadata system
│   ├── observatory/            # 🔭 Dashboard
│   └── swarm/                  # 🐝 Agent Network
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── educational/            # Educational examples
│   └── bee_choreography/       # Dance pattern tests
├── docs/                       # Documentation
├── scripts/                    # Utilities
└── requirements*.txt           # Dependencies
```

## Development Guidelines

### Python Code & MCP Design
- **Idiomatic Python** with PEP 8, type hints, bee metadata integration
- **Clear MCP tool signatures** with Pydantic models and streaming support
- **Bee metadata tracking** in all tool responses with appropriate dance patterns
- **FastAPI integration** with HTTP streaming and OpenAPI documentation

### Documentation & Testing
- **Google-style docstrings** with bee metadata examples
- **Comprehensive tests** (>80% coverage) including bee choreography validation
- **Educational focus** - design as teaching tools with clear examples
- **MCP protocol compliance** testing and bee interaction validation

### Ring Architecture & Configuration
- **Ring security levels** (0: core, 1: essential, 2: extended, 3: external, 4: UI)
- **Environment variables** with bee/hive context and multiple profiles
- **Structured logging** with bee activity tracking for Observatory

## SwarmRouter-Specific Notes

### HIVE Development
- **MCP server is primary focus** - coordinates all bee activities
- **Token efficiency critical** - track nectar collection carefully
- **Streaming support** for real-time bee choreography
- **Educational platform** - demonstrate best practices

### Bee Choreography Implementation
- **Waggle**: Complex decomposition (architect tools)
- **Round**: Notifications and status
- **Scout**: Exploration activities
- **Tremble**: Error conditions
- **Converge**: Consensus building
- **Disperse**: Parallel execution

### Observatory Integration
- **Real-time visualization** of all bee activities and dance patterns
- **Token efficiency metrics** and nectar collection tracking
- **Educational dashboards** with debugging tools for bee interactions

## Development Roadmap

**Sprint 1-2**: Core HIVE server, MCP protocol, basic bee metadata, essential tools
**Sprint 3-4**: Complete tool suite, full choreography system, external integrations
**Sprint 5-6**: Performance optimization, monitoring, educational materials, deployment

## Documentation & Resources

**Internal Docs**: system-architecture.md, llama-bee-metadata.md, educational-materials/
**Development**: GitHub workflow guide, Observatory debugging, bee choreography patterns
**Core Principles**: MCP server first, educational focus, bee metaphor consistency, token efficiency, ring architecture

---

*🐝 SwarmRouter is both a powerful development platform and educational tool. Every component should serve both purposes while maintaining the delightful bee/hive metaphor.*