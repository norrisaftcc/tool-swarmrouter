"""
Data models for Shadow Clone Jutsu MCP server.

This module defines the core data structures for managing tasks and clones
using the Shadow Clone Jutsu coding motif. In this system:

- Tasks represent coding challenges or objectives that need to be completed
- Clones are specialized shadow copies that can execute specific types of work
- Each clone has unique abilities and can be deployed for different task types

The Shadow Clone Jutsu technique allows a ninja to create multiple copies of themselves
to work on different aspects of a problem simultaneously, similar to how we can
distribute coding tasks across multiple AI agents for efficient parallel processing.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class CloneType(str, Enum):
    """
    Types of shadow clones, each specialized for different coding tasks.
    
    These clone types are inspired by different ninja specializations and
    represent different AI agent capabilities:
    
    - ARCHITECT: High-level system design and architecture planning
    - IMPLEMENTER: Core coding and implementation tasks  
    - TESTER: Quality assurance and testing operations
    - DEBUGGER: Error detection and troubleshooting
    - OPTIMIZER: Performance tuning and code optimization
    - CHRONICLER: Documentation and knowledge management
    """
    
    ARCHITECT = "architect"
    IMPLEMENTER = "implementer" 
    TESTER = "tester"
    DEBUGGER = "debugger"
    OPTIMIZER = "optimizer"
    CHRONICLER = "chronicler"


class TaskPriority(str, Enum):
    """
    Priority levels for tasks in the ninja mission system.
    
    Based on traditional ninja mission rankings:
    - S_RANK: Legendary difficulty, highest priority
    - A_RANK: Elite level, high priority  
    - B_RANK: Journeyman level, medium priority
    - C_RANK: Apprentice level, low priority
    """
    
    S_RANK = "s_rank"  # Legendary
    A_RANK = "a_rank"  # Elite
    B_RANK = "b_rank"  # Journeyman  
    C_RANK = "c_rank"  # Apprentice


class TaskStatus(str, Enum):
    """Current status of a shadow clone mission."""
    
    PENDING = "pending"           # Mission briefing received
    CLONES_ASSIGNED = "clones_assigned"  # Shadow clones deployed
    IN_PROGRESS = "in_progress"   # Mission underway
    COMPLETED = "completed"       # Mission accomplished
    FAILED = "failed"            # Mission failed


class Clone(BaseModel):
    """
    Represents a shadow clone with specific abilities and current assignment.
    
    Each clone is a specialized copy created using the Shadow Clone Jutsu
    technique. Clones maintain their own identity and can work independently
    on assigned tasks while sharing knowledge with the original ninja.
    """
    
    clone_id: str = Field(
        default_factory=lambda: f"clone_{uuid.uuid4().hex[:8]}", 
        description="Unique identifier for this shadow clone"
    )
    clone_type: CloneType = Field(
        description="Specialization type of this clone"
    )
    name: str = Field(
        description="Display name for this clone"
    )
    current_task: Optional[str] = Field(
        default=None,
        description="Current task assigned to this clone"
    )
    chakra_level: int = Field(
        default=100,
        ge=0,
        le=100,
        description="Current chakra/energy level (0-100)"
    )
    experience_points: int = Field(
        default=0,
        ge=0,
        description="Accumulated experience from completed tasks"
    )
    specialties: List[str] = Field(
        default_factory=list,
        description="List of specific skills or technologies this clone excels at"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When this clone was created"
    )
    
    def is_available(self) -> bool:
        """Check if clone is available for new assignments."""
        return self.current_task is None and self.chakra_level > 10
    
    def assign_task(self, task_description: str) -> None:
        """Assign a task to this clone."""
        if not self.is_available():
            raise ValueError(f"Clone {self.clone_id} is not available for assignment")
        self.current_task = task_description
        
    def complete_task(self, experience_gained: int = 10) -> None:
        """Mark current task as complete and gain experience."""
        self.current_task = None
        self.experience_points += experience_gained
        self.chakra_level = min(100, self.chakra_level + 5)  # Rest restores chakra
    
    def get_rank(self) -> str:
        """Get the ninja rank based on experience points."""
        if self.experience_points >= 1000:
            return "Jōnin (Elite)"
        elif self.experience_points >= 500:
            return "Chūnin (Journeyman)"
        elif self.experience_points >= 100:
            return "Genin (Apprentice)"
        else:
            return "Academy Student"


class Task(BaseModel):
    """
    Represents a coding task/mission that can be assigned to shadow clones.
    
    Tasks in the Shadow Clone Jutsu system represent programming challenges
    that can be broken down and distributed among specialized clones for
    efficient parallel execution.
    """
    
    task_id: str = Field(
        default_factory=lambda: f"mission_{uuid.uuid4().hex}",
        description="Unique identifier for this task/mission"
    )
    title: str = Field(
        description="Brief title describing the task"
    )
    description: str = Field(
        description="Detailed description of what needs to be accomplished"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.B_RANK,
        description="Mission priority/difficulty rank"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status of the mission"
    )
    required_clone_types: List[CloneType] = Field(
        default_factory=list,
        description="Types of clones needed for this task"
    )
    assigned_clones: List[Clone] = Field(
        default_factory=list,
        description="Clones currently assigned to this task"
    )
    estimated_duration: Optional[int] = Field(
        default=None,
        description="Estimated duration in minutes"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Technology tags or categories (e.g., 'python', 'api', 'database')"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When this task was created"
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="When work on this task began"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="When this task was completed"
    )
    result: Optional[str] = Field(
        default=None,
        description="Final result or output from completing the task"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if the task failed"
    )
    
    def assign_clone(self, clone: Clone) -> None:
        """Assign a clone to work on this task."""
        if clone in self.assigned_clones:
            raise ValueError(f"Clone {clone.clone_id} is already assigned to this task")
        
        if not clone.is_available():
            raise ValueError(f"Clone {clone.clone_id} is not available for assignment")
        
        self.assigned_clones.append(clone)
        clone.assign_task(f"{self.title} ({self.task_id})")
        
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.CLONES_ASSIGNED
    
    def start_work(self) -> None:
        """Mark the task as started."""
        if not self.assigned_clones:
            raise ValueError("Cannot start task without assigned clones")
        
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete_task(self, result: str) -> None:
        """Mark the task as completed with the given result."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        
        # Complete task for all assigned clones
        for clone in self.assigned_clones:
            clone.complete_task()
    
    def fail_task(self, error: str) -> None:
        """Mark the task as failed with the given error."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error
        
        # Reset clones
        for clone in self.assigned_clones:
            clone.current_task = None
    
    def get_duration(self) -> Optional[int]:
        """Get actual duration in minutes if task is completed."""
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds() / 60)
        return None
    
    def to_summary(self) -> Dict[str, Any]:
        """Get a summary representation of this task."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority.value,
            "status": self.status.value,
            "clone_count": len(self.assigned_clones),
            "duration_minutes": self.get_duration(),
            "tags": self.tags
        }


class TaskRequest(BaseModel):
    """Request model for creating a new shadow clone task."""
    
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Brief title for the task"
    )
    description: str = Field(
        min_length=1,
        description="Detailed description of the task"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.B_RANK,
        description="Task priority level"
    )
    preferred_clone_types: Optional[List[CloneType]] = Field(
        default=None,
        description="Preferred types of clones for this task"
    )
    estimated_duration: Optional[int] = Field(
        default=None,
        gt=0,
        description="Estimated duration in minutes"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Technology or category tags"
    )


class TaskResponse(BaseModel):
    """Response model for task operations."""
    
    task_id: str = Field(description="Unique task identifier")
    message: str = Field(description="Response message")
    assigned_clones: int = Field(description="Number of clones assigned")
    estimated_completion: Optional[str] = Field(
        default=None,
        description="Estimated completion time"
    )


class ShadowCloneStatus(BaseModel):
    """Overall status of the shadow clone system."""
    
    total_clones: int = Field(description="Total number of active clones")
    available_clones: int = Field(description="Number of available clones")
    active_tasks: int = Field(description="Number of tasks in progress")
    completed_tasks: int = Field(description="Total completed tasks")
    total_experience: int = Field(description="Combined experience of all clones")
    system_uptime: str = Field(description="How long the system has been running")