"""
Data models for the Shadow Clone Jutsu MCP Server.

This module defines the core data structures used in the Shadow Clone Jutsu
task delegation system, drawing inspiration from the Naruto ninja world.

The Shadow Clone Jutsu (Kage Bunshin no Jutsu) is a ninja technique that creates
physical copies of the user. Each clone can act independently and when dismissed,
their memories and experiences return to the original. This serves as a perfect
metaphor for distributed task execution in project management:

- Original Ninja = Project Manager/Main Process
- Shadow Clones = Specialized workers/subtasks  
- Jutsu Techniques = Task types and execution strategies
- Chakra = Computational resources/token budget
- Mission = Overall project or task to complete
- Clone Specializations = Different skill sets for different task types
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import uuid


class CloneType(str, Enum):
    """
    Types of shadow clones specialized for different kinds of tasks.
    
    Each clone type represents a different specialization, similar to how
    different ninja have different specialties and jutsu techniques:
    
    - ARCHITECT: Planning and design clones (like strategic ninja)
    - RESEARCHER: Information gathering clones (like scout ninja) 
    - IMPLEMENTER: Code/content creation clones (like craftsman ninja)
    - REVIEWER: Quality assurance clones (like sensory ninja)
    - MESSENGER: Communication and reporting clones (like messenger ninja)
    - DEBUGGER: Problem-solving clones (like medical ninja)
    """
    
    ARCHITECT = "architect"      # Design and planning specialist
    RESEARCHER = "researcher"    # Information gathering specialist  
    IMPLEMENTER = "implementer"  # Creation and building specialist
    REVIEWER = "reviewer"        # Quality control specialist
    MESSENGER = "messenger"      # Communication specialist
    DEBUGGER = "debugger"        # Problem-solving specialist


class TaskPriority(str, Enum):
    """Task priority levels using ninja mission rankings."""
    
    D_RANK = "d_rank"        # Simple, low-priority tasks
    C_RANK = "c_rank"        # Standard tasks
    B_RANK = "b_rank"        # Important tasks  
    A_RANK = "a_rank"        # High-priority tasks
    S_RANK = "s_rank"        # Critical, top-priority tasks


class TaskStatus(str, Enum):
    """Task execution status tracking."""
    
    PENDING = "pending"           # Task created but not yet assigned
    ASSIGNED = "assigned"         # Clones assigned but not started
    IN_PROGRESS = "in_progress"   # Clones actively working
    COMPLETED = "completed"       # Task successfully finished
    FAILED = "failed"            # Task failed to complete
    CANCELLED = "cancelled"       # Task was cancelled


class Clone(BaseModel):
    """
    Represents a shadow clone created to handle a specific task.
    
    In the Shadow Clone Jutsu, each clone is an independent copy of the original
    ninja with the same skills and knowledge. In our system, each clone represents
    a specialized worker focused on a particular aspect of a larger task.
    
    Attributes:
        clone_id: Unique identifier for this clone
        clone_type: Specialization of this clone
        assigned_task: Specific task or subtask assigned to this clone
        chakra_allocation: Resource/token budget allocated to this clone
        status: Current status of the clone's work
        created_at: When this clone was created
        completed_at: When this clone finished its task (if completed)
        result: The output or result produced by this clone
        efficiency_rating: How efficiently this clone used its resources (0.0-1.0)
    """
    
    clone_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clone_type: CloneType
    assigned_task: str = Field(..., min_length=1, description="The specific task assigned to this clone")
    chakra_allocation: int = Field(..., gt=0, description="Token/resource budget for this clone")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    efficiency_rating: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    @validator('efficiency_rating')
    def validate_efficiency(cls, v):
        """Ensure efficiency rating is between 0.0 and 1.0."""
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError("Efficiency rating must be between 0.0 and 1.0")
        return v
    
    def complete_task(self, result: str, efficiency: float = 0.8) -> None:
        """
        Mark this clone's task as completed with results.
        
        Args:
            result: The output or result produced by the clone
            efficiency: How efficiently the clone used its chakra (0.0-1.0)
        """
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.result = result
        self.efficiency_rating = efficiency
    
    def fail_task(self, error_message: str) -> None:
        """
        Mark this clone's task as failed with error details.
        
        Args:
            error_message: Description of what went wrong
        """
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)
        self.result = f"FAILED: {error_message}"
        self.efficiency_rating = 0.0


class Task(BaseModel):
    """
    Represents a mission or task that can be delegated to shadow clones.
    
    In the ninja world, missions are assigned to teams or individuals based on
    their complexity and importance. Similarly, our tasks are analyzed and
    broken down into subtasks that can be distributed among specialized clones.
    
    Attributes:
        task_id: Unique identifier for this task/mission
        description: Detailed description of what needs to be accomplished
        priority: Mission rank (D through S rank)
        total_chakra_budget: Total resources available for this task
        assigned_clones: List of clones working on this task
        status: Current status of the overall task
        created_at: When this task was created
        completed_at: When this task was finished (if completed)
        estimated_completion_time: Estimated time to complete (in minutes)
        actual_completion_time: Actual time taken (in minutes)
        success_rate: Percentage of subtasks completed successfully
    """
    
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str = Field(..., min_length=1, description="Description of the task/mission")
    priority: TaskPriority = Field(default=TaskPriority.C_RANK)
    total_chakra_budget: int = Field(..., gt=0, description="Total token/resource budget")
    assigned_clones: List[Clone] = Field(default_factory=list)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    estimated_completion_time: Optional[int] = Field(None, gt=0, description="Estimated minutes to complete")
    actual_completion_time: Optional[int] = None
    success_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    @validator('total_chakra_budget')
    def validate_chakra_budget(cls, v):
        """Ensure chakra budget is positive."""
        if v <= 0:
            raise ValueError("Chakra budget must be greater than 0")
        return v
    
    def assign_clone(self, clone: Clone) -> None:
        """
        Assign a clone to work on this task.
        
        Args:
            clone: The clone to assign to this task
        """
        self.assigned_clones.append(clone)
        clone.status = TaskStatus.ASSIGNED
        
        # Update task status if this is the first clone
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.ASSIGNED
    
    def start_execution(self) -> None:
        """Mark the task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
        for clone in self.assigned_clones:
            if clone.status == TaskStatus.ASSIGNED:
                clone.status = TaskStatus.IN_PROGRESS
    
    def calculate_success_rate(self) -> float:
        """Calculate the percentage of clones that completed successfully."""
        if not self.assigned_clones:
            return 0.0
        
        completed_successfully = sum(
            1 for clone in self.assigned_clones 
            if clone.status == TaskStatus.COMPLETED
        )
        return completed_successfully / len(self.assigned_clones)
    
    def calculate_efficiency(self) -> float:
        """Calculate average efficiency across all clones."""
        if not self.assigned_clones:
            return 0.0
        
        efficiencies = [
            clone.efficiency_rating for clone in self.assigned_clones
            if clone.efficiency_rating is not None
        ]
        
        if not efficiencies:
            return 0.0
        
        return sum(efficiencies) / len(efficiencies)
    
    def check_completion(self) -> bool:
        """
        Check if the task is complete and update status accordingly.
        
        Returns:
            True if task is complete, False otherwise
        """
        if not self.assigned_clones:
            return False
        
        # Check if all clones are done (either completed or failed)
        all_done = all(
            clone.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
            for clone in self.assigned_clones
        )
        
        if all_done:
            self.success_rate = self.calculate_success_rate()
            self.completed_at = datetime.now(timezone.utc)
            
            # Calculate actual completion time
            if self.created_at:
                duration = self.completed_at - self.created_at
                self.actual_completion_time = int(duration.total_seconds() / 60)
            
            # Determine if task succeeded or failed based on success rate
            if self.success_rate >= 0.5:  # At least 50% of clones succeeded
                self.status = TaskStatus.COMPLETED
            else:
                self.status = TaskStatus.FAILED
            
            return True
        
        return False


class TaskDelegationRequest(BaseModel):
    """
    Request model for delegating a task to shadow clones.
    
    This represents a request to create shadow clones and delegate work,
    similar to how a ninja leader would assign a mission to their team.
    """
    
    description: str = Field(..., min_length=1, description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.C_RANK)
    chakra_budget: int = Field(default=1000, gt=0, description="Total token budget")
    requested_clone_types: Optional[List[CloneType]] = Field(
        default=None, 
        description="Specific clone types requested (auto-detected if not provided)"
    )
    max_clones: int = Field(default=5, gt=0, le=20, description="Maximum number of clones to create")
    estimated_time: Optional[int] = Field(None, gt=0, description="Estimated completion time in minutes")


class TaskDelegationResponse(BaseModel):
    """
    Response model for task delegation results.
    
    Contains information about the created task and assigned clones,
    similar to a mission briefing in the ninja world.
    """
    
    task_id: str
    message: str
    created_clones: int
    clone_details: List[Dict[str, Any]]
    estimated_token_savings: int
    estimated_completion_time: Optional[int]
    jutsu_technique: str = Field(
        default="Multi Shadow Clone Jutsu", 
        description="The technique used for delegation"
    )