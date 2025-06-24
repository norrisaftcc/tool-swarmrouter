"""Data models for SwarmRouter MCP server using the bee/hive metaphor."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class DanceType(str, Enum):
    """
    Types of bee dances that represent different task coordination patterns.
    
    Based on real bee behavior:
    - WAGGLE: Complex tasks requiring decomposition (like bees indicating distant food)
    - ROUND: Simple notifications or alerts (like bees indicating nearby resources)
    - SCOUT: Exploration and research tasks (like scout bees finding new locations)
    - TREMBLE: Error handling or issue alerts (like bees signaling problems)
    - CONVERGE: Consensus building among multiple agents (like swarm decisions)
    - DISPERSE: Parallel task execution (like foraging in multiple directions)
    """
    WAGGLE = "waggle"
    ROUND = "round"
    SCOUT = "scout"
    TREMBLE = "tremble"
    CONVERGE = "converge"
    DISPERSE = "disperse"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class BeeMetadata(BaseModel):
    """
    Metadata for a bee (agent) in the swarm.
    
    Each bee carries information about its assigned task and capabilities,
    similar to how real bees carry information about food sources.
    """
    bee_id: str = Field(default_factory=lambda: f"bee_{uuid.uuid4().hex[:8]}")
    dance_type: DanceType
    assigned_task: Optional[str] = None
    estimated_tokens: int = Field(gt=0)
    actual_tokens: Optional[int] = None
    specialty: Optional[str] = None  # e.g., "architect", "chronicler", "scout"
    
    def calculate_efficiency(self) -> Optional[float]:
        """Calculate token efficiency if actual tokens are known."""
        if self.actual_tokens is None:
            return None
        return (self.estimated_tokens - self.actual_tokens) / self.estimated_tokens


class SwarmTask(BaseModel):
    """
    Represents a task to be executed by the swarm.
    
    Tasks are delegated to bees based on their dance type and the nature
    of the work required.
    """
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex}")
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    dance_type: DanceType
    status: TaskStatus = TaskStatus.PENDING
    max_tokens: int = Field(default=10000, gt=0)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    assigned_bees: List[BeeMetadata] = Field(default_factory=list)
    result: Optional[str] = None
    error: Optional[str] = None
    
    def assign_bee(self, bee: BeeMetadata) -> None:
        """Assign a bee to this task."""
        self.assigned_bees.append(bee)
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.ASSIGNED
    
    def mark_complete(self, result: str) -> None:
        """Mark task as completed with result."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
    
    def mark_failed(self, error: str) -> None:
        """Mark task as failed with error."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
    
    def calculate_token_savings(self) -> float:
        """Calculate estimated token savings from delegation."""
        total_actual = sum(
            bee.actual_tokens or bee.estimated_tokens 
            for bee in self.assigned_bees
        )
        if total_actual >= self.max_tokens:
            return 0.0
        return (self.max_tokens - total_actual) / self.max_tokens * 100


class TaskDelegationRequest(BaseModel):
    """Request model for delegating a task."""
    description: str = Field(..., min_length=1)
    priority: TaskPriority = TaskPriority.MEDIUM
    max_tokens: int = Field(default=10000, gt=0)
    preferred_dance: Optional[DanceType] = None
    subtasks: Optional[List[str]] = None


class TaskDelegationResponse(BaseModel):
    """Response model for task delegation."""
    task_id: str
    dance_type: DanceType
    assigned_bees: int
    estimated_token_savings: float
    message: str