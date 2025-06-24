# GitHub Issue: [HIVE-MVP-1] Implement Basic MCP Server for Task Delegation

## Title
[HIVE-MVP-1] Implement Basic MCP Server for Task Delegation

## Description

Create a minimal viable MCP (Model Context Protocol) server that demonstrates the core SwarmRouter concept: delegating tasks to a swarm of models. This MVP will serve as a learning tool and foundation for the full HIVE system.

## Background

The SwarmRouter project uses a bee/hive metaphor where LLMs (llamas) are paired with bee metadata that choreographs their collaboration. This MVP will implement the most basic form of this concept - accepting tasks and delegating them to appropriate models.

## Acceptance Criteria

- [ ] Basic MCP server running with FastMCP
- [ ] Single tool: `delegate_task` that accepts task descriptions
- [ ] Task routing based on simple heuristics (complexity detection)
- [ ] Return task ID and assigned "bee" metadata
- [ ] Proper error handling and logging
- [ ] Environment-based API key management
- [ ] Unit tests with >80% coverage
- [ ] Integration test demonstrating task delegation
- [ ] README with setup and usage instructions
- [ ] Example client script showing how to use the server

## Technical Requirements

### Core Functionality
- Use FastMCP for rapid development
- Implement basic bee dance types (waggle for complex, round for simple)
- Track delegated tasks in memory (no persistence needed for MVP)
- Calculate estimated token savings

### Code Structure
```
swarmrouter-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── models.py          # Task and Bee data models
│   └── delegation.py      # Task delegation logic
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   └── test_delegation.py
├── examples/
│   └── client_example.py
├── requirements.txt
├── README.md
└── .env.example
```

## User Stories

As a developer, I want to:
1. Send a task description to the MCP server
2. Receive back a task ID and assigned bee metadata
3. Understand which "dance type" was selected and why
4. See estimated token savings from delegation

## Definition of Done

- [ ] Code follows project style guidelines (type hints, docstrings)
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] PR has been reviewed
- [ ] Example client successfully delegates a task
- [ ] No hardcoded secrets or API keys

## Notes

- This is an MVP - focus on demonstrating the concept clearly
- Excellent documentation is crucial as this will be used for learning
- The code should be simple enough for students to understand
- Include comments explaining the bee/hive metaphor

## Labels
`enhancement`, `mvp`, `ring-0`, `good-first-issue`, `documentation`

## Milestone
Sprint 1: Foundation

## Assignee
@norrisaftcc (or current developer)

## Related Issues
- Relates to #4 (Task Decomposition)
- Implements first part of HIVE-2.1.3 (MCP Protocol handlers)

## Resources
- [MCP Documentation](https://github.com/modelcontextprotocol/)
- [FastMCP Examples](https://github.com/modelcontextprotocol/servers)
- [SwarmRouter Architecture Docs](../hive-ring-architecture.md)