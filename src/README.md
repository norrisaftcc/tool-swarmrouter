# Shadow Clone Jutsu MCP Server

A FastAPI-based server implementing the Shadow Clone Jutsu technique for distributed coding task management.

## 🥷 Overview

This server uses the Shadow Clone Jutsu motif to create specialized AI agents (clones) that can work on different coding tasks simultaneously. Each clone has unique abilities and gains experience over time.

## 🚀 Quick Start

### Start the Server
```bash
cd /path/to/tool-swarmrouter
python3 -m src.server
```

The server will start on `http://localhost:8000`

### Try the Demo
```bash
python3 demo_shadow_clone_jutsu.py
```

## 📋 Features

### Shadow Clones
- **Architect**: System design and architecture planning
- **Implementer**: Core coding and implementation  
- **Tester**: Quality assurance and testing
- **Debugger**: Error detection and troubleshooting
- **Optimizer**: Performance tuning
- **Chronicler**: Documentation management

### Task Management
- Create coding missions with ninja rank priorities (S_RANK to C_RANK)
- Automatic clone assignment based on specializations
- Experience and chakra system for clone progression
- Real-time task monitoring and status tracking

## 🎯 API Endpoints

- `GET /` - Welcome message with Shadow Clone Jutsu overview
- `GET /status` - System status and statistics
- `GET /clones` - List all active shadow clones
- `GET /clones/{id}` - Get specific clone details
- `POST /tasks` - Create new coding missions
- `GET /tasks` - List all tasks/missions
- `GET /tasks/{id}` - Get specific task details
- `POST /tasks/{id}/complete` - Mark task as completed

## 📚 Documentation

- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## 🏗️ Architecture

### Models (`models.py`)
- **Clone**: Represents shadow clones with specializations and experience
- **Task**: Coding missions with status tracking and clone assignments
- Full Pydantic validation with type hints

### Server (`server.py`)
- FastAPI application with RESTful endpoints
- Automatic shadow clone initialization
- Task delegation and management logic
- Comprehensive error handling

## 🎮 Example Usage

```python
# Create a new task
import requests

response = requests.post("http://localhost:8000/tasks", json={
    "title": "Build Authentication System",
    "description": "Create JWT-based auth with registration and login",
    "priority": "a_rank",
    "estimated_duration": 120,
    "tags": ["authentication", "jwt", "security"]
})

print(response.json())
# Returns task_id and assigned clone information
```

## 🥋 Philosophy

*"Code like a ninja, debug like a sage, deploy like the wind!"*

The Shadow Clone Jutsu technique teaches us that complex problems can be solved more efficiently through specialized parallel execution, where each clone contributes their unique expertise to the overall mission.

## 🔮 Future Expansions

The system is designed for easy extension:
- Additional clone types (e.g., DevOps, Security, Frontend)
- Advanced task scheduling algorithms
- Clone collaboration patterns
- Experience-based auto-optimization
- Integration with external AI providers

---

**Ready for your first ninja mission? Start the server and visit `/docs` to explore the full API!** 🥷✨