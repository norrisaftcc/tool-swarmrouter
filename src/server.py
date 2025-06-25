"""
Shadow Clone Jutsu FastAPI Server

This server implements the Shadow Clone Jutsu technique for distributed coding tasks.
Like a ninja creating shadow clones to tackle multiple objectives simultaneously,
this system creates specialized AI agents (clones) to handle different aspects
of programming challenges.

The Shadow Clone Jutsu server provides endpoints for:
- Managing shadow clones with different specializations
- Creating and assigning coding tasks/missions  
- Monitoring task progress and clone performance
- Coordinating parallel execution of complex projects

Each clone maintains its own chakra level (energy) and gains experience as it
completes tasks, making the system more efficient over time.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uuid

# Import our Shadow Clone Jutsu models
from .models import (
    Clone,
    Task,
    CloneType,
    TaskPriority,
    TaskStatus,
    TaskRequest,
    TaskResponse,
    ShadowCloneStatus
)


class ShadowCloneJutsuServer:
    """
    Main server class for managing the Shadow Clone Jutsu system.
    
    This class maintains the state of all active clones and tasks,
    providing the core functionality for the ninja coding dojo.
    """
    
    def __init__(self):
        """Initialize the Shadow Clone Jutsu system."""
        self.clones: Dict[str, Clone] = {}
        self.tasks: Dict[str, Task] = {}
        self.start_time = datetime.now()
        
        # Create initial shadow clones for demonstration
        self._create_initial_clones()
    
    def _create_initial_clones(self):
        """Create the initial set of shadow clones for the dojo."""
        initial_clones = [
            {
                "clone_type": CloneType.ARCHITECT,
                "name": "Kage-Bunshin Alpha",
                "specialties": ["system_design", "microservices", "architecture_patterns"]
            },
            {
                "clone_type": CloneType.IMPLEMENTER,
                "name": "Kage-Bunshin Beta", 
                "specialties": ["python", "javascript", "api_development"]
            },
            {
                "clone_type": CloneType.TESTER,
                "name": "Kage-Bunshin Gamma",
                "specialties": ["pytest", "integration_testing", "qa_automation"]
            },
            {
                "clone_type": CloneType.DEBUGGER,
                "name": "Kage-Bunshin Delta",
                "specialties": ["error_analysis", "performance_debugging", "troubleshooting"]
            }
        ]
        
        for clone_config in initial_clones:
            clone = Clone(**clone_config)
            self.clones[clone.clone_id] = clone
    
    def get_available_clones(self) -> List[Clone]:
        """Get all clones that are available for assignment."""
        return [clone for clone in self.clones.values() if clone.is_available()]
    
    def get_system_status(self) -> ShadowCloneStatus:
        """Get the current status of the Shadow Clone Jutsu system."""
        available_clones = len(self.get_available_clones())
        active_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        total_experience = sum(clone.experience_points for clone in self.clones.values())
        
        uptime = datetime.now() - self.start_time
        uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
        
        return ShadowCloneStatus(
            total_clones=len(self.clones),
            available_clones=available_clones,
            active_tasks=active_tasks,
            completed_tasks=completed_tasks,
            total_experience=total_experience,
            system_uptime=uptime_str
        )


# Initialize the Shadow Clone Jutsu system
shadow_system = ShadowCloneJutsuServer()

# Create FastAPI application
app = FastAPI(
    title="Shadow Clone Jutsu MCP Server",
    description="A FastAPI server for managing coding tasks using the Shadow Clone Jutsu technique",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/")
async def root():
    """
    Welcome endpoint for the Shadow Clone Jutsu server.
    
    Returns a welcome message introducing the Shadow Clone Jutsu coding technique
    and providing an overview of the server's capabilities.
    """
    return {
        "message": "🥷 Welcome to the Shadow Clone Jutsu MCP Server! 🥷",
        "description": (
            "Harness the power of the Shadow Clone Jutsu to tackle your coding challenges! "
            "Create specialized ninja clones to work on different aspects of your projects "
            "simultaneously. Each clone brings unique skills and grows stronger with experience."
        ),
        "technique": {
            "name": "Kage Bunshin no Jutsu (Shadow Clone Technique)",
            "purpose": "Parallel execution of coding tasks through specialized AI agents",
            "philosophy": "Many hands make light work - even if they're shadow hands!"
        },
        "available_endpoints": {
            "/clones": "Manage your shadow clones",
            "/tasks": "Create and monitor coding missions", 
            "/status": "Check the dojo status",
            "/docs": "Full API documentation"
        },
        "dojo_motto": "Code like a ninja, debug like a sage, deploy like the wind! 🌪️",
        "current_time": datetime.now().isoformat(),
        "system_status": "Active and ready for missions"
    }


@app.get("/status", response_model=ShadowCloneStatus)
async def get_status():
    """
    Get the current status of the Shadow Clone Jutsu system.
    
    Returns information about active clones, tasks in progress,
    and overall system performance metrics.
    """
    return shadow_system.get_system_status()


@app.get("/clones")
async def list_clones():
    """
    List all active shadow clones and their current status.
    
    Shows each clone's specialization, availability, chakra level,
    and current assignment if any.
    """
    clones_info = []
    for clone in shadow_system.clones.values():
        clone_info = {
            "clone_id": clone.clone_id,
            "name": clone.name,
            "type": clone.clone_type.value,
            "rank": clone.get_rank(),
            "chakra_level": clone.chakra_level,
            "experience_points": clone.experience_points,
            "specialties": clone.specialties,
            "available": clone.is_available(),
            "current_task": clone.current_task,
            "created_at": clone.created_at.isoformat()
        }
        clones_info.append(clone_info)
    
    return {
        "message": "Active shadow clones in the dojo",
        "total_clones": len(clones_info),
        "available_clones": len([c for c in clones_info if c["available"]]),
        "clones": clones_info
    }


@app.get("/clones/{clone_id}")
async def get_clone(clone_id: str):
    """
    Get detailed information about a specific shadow clone.
    
    Args:
        clone_id: The unique identifier of the clone
        
    Returns:
        Detailed information about the requested clone
    """
    if clone_id not in shadow_system.clones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clone with ID {clone_id} not found in the dojo"
        )
    
    clone = shadow_system.clones[clone_id]
    return {
        "clone_id": clone.clone_id,
        "name": clone.name,
        "type": clone.clone_type.value,
        "rank": clone.get_rank(),
        "chakra_level": clone.chakra_level,
        "experience_points": clone.experience_points,
        "specialties": clone.specialties,
        "available": clone.is_available(),
        "current_task": clone.current_task,
        "created_at": clone.created_at.isoformat()
    }


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task_request: TaskRequest):
    """
    Create a new coding task and assign appropriate shadow clones.
    
    The system will automatically select the best clones based on the
    task requirements and clone specializations.
    
    Args:
        task_request: Details of the task to be created
        
    Returns:
        Information about the created task and assigned clones
    """
    # Create the task
    task = Task(
        title=task_request.title,
        description=task_request.description,
        priority=task_request.priority,
        estimated_duration=task_request.estimated_duration,
        tags=task_request.tags
    )
    
    # Auto-assign clones if none specified
    if not task_request.preferred_clone_types:
        # Simple assignment logic - assign one clone of each available type
        available_clones = shadow_system.get_available_clones()
        if not available_clones:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No shadow clones available for assignment. All are currently on missions."
            )
        
        # Assign the first available clone (can be enhanced with better logic)
        clone_to_assign = available_clones[0]
        task.assign_clone(clone_to_assign)
    else:
        # Assign specific clone types as requested
        for preferred_type in task_request.preferred_clone_types:
            available_clones_of_type = [
                clone for clone in shadow_system.get_available_clones()
                if clone.clone_type == preferred_type
            ]
            if available_clones_of_type:
                task.assign_clone(available_clones_of_type[0])
    
    if not task.assigned_clones:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to assign any clones to this task. Check clone availability."
        )
    
    # Store the task
    shadow_system.tasks[task.task_id] = task
    
    # Start the task immediately for demonstration
    task.start_work()
    
    return TaskResponse(
        task_id=task.task_id,
        message=f"Mission '{task.title}' has been assigned to {len(task.assigned_clones)} shadow clone(s)",
        assigned_clones=len(task.assigned_clones),
        estimated_completion=(
            (datetime.now() + timedelta(minutes=task.estimated_duration)).isoformat()
            if task.estimated_duration else None
        )
    )


@app.get("/tasks")
async def list_tasks():
    """
    List all tasks/missions in the system.
    
    Shows current status, assigned clones, and progress for each task.
    """
    tasks_info = []
    for task in shadow_system.tasks.values():
        task_info = task.to_summary()
        task_info.update({
            "description": task.description[:100] + "..." if len(task.description) > 100 else task.description,
            "assigned_clone_names": [clone.name for clone in task.assigned_clones],
            "created_at": task.created_at.isoformat()
        })
        tasks_info.append(task_info)
    
    return {
        "message": "Current missions in the dojo",
        "total_tasks": len(tasks_info),
        "active_tasks": len([t for t in tasks_info if t["status"] == "in_progress"]),
        "tasks": tasks_info
    }


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """
    Get detailed information about a specific task.
    
    Args:
        task_id: The unique identifier of the task
        
    Returns:
        Detailed information about the requested task
    """
    if task_id not in shadow_system.tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {task_id} not found in the dojo"
        )
    
    task = shadow_system.tasks[task_id]
    return {
        "task_id": task.task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "status": task.status.value,
        "assigned_clones": [
            {
                "clone_id": clone.clone_id,
                "name": clone.name,
                "type": clone.clone_type.value
            }
            for clone in task.assigned_clones
        ],
        "estimated_duration": task.estimated_duration,
        "actual_duration": task.get_duration(),
        "tags": task.tags,
        "created_at": task.created_at.isoformat(),
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "result": task.result,
        "error_message": task.error_message
    }


@app.post("/tasks/{task_id}/complete")
async def complete_task(task_id: str, result: Dict[str, Any]):
    """
    Mark a task as completed with the given result.
    
    Args:
        task_id: The unique identifier of the task
        result: The completion result data
        
    Returns:
        Confirmation of task completion
    """
    if task_id not in shadow_system.tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with ID {task_id} not found"
        )
    
    task = shadow_system.tasks[task_id]
    if task.status != TaskStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mission {task_id} is not in progress and cannot be completed"
        )
    
    result_text = result.get("result", "Task completed successfully")
    task.complete_task(result_text)
    
    return {
        "message": f"Mission '{task.title}' has been completed successfully!",
        "task_id": task_id,
        "completion_time": task.completed_at.isoformat(),
        "assigned_clones": [clone.name for clone in task.assigned_clones],
        "experience_gained": "All assigned clones gained experience points"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring the server status."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "dojo_operational": True,
        "message": "The Shadow Clone Jutsu dojo is operating at full capacity! 🥷"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("🥷 Starting Shadow Clone Jutsu MCP Server...")
    print("🎯 Navigate to http://localhost:8000 for the welcome message")
    print("📚 API documentation available at http://localhost:8000/docs")
    print("🔍 Alternative docs at http://localhost:8000/redoc")
    
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )