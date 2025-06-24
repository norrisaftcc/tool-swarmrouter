"""Tests for SwarmRouter data models."""

import pytest
from datetime import datetime
from src.models import (
    DanceType, TaskPriority, TaskStatus, BeeMetadata, 
    SwarmTask, TaskDelegationRequest, TaskDelegationResponse
)


class TestDanceType:
    """Test the DanceType enum."""
    
    def test_all_dance_types_exist(self):
        """Ensure all expected dance types are defined."""
        expected_dances = ["waggle", "round", "scout", "tremble", "converge", "disperse"]
        actual_dances = [dance.value for dance in DanceType]
        assert set(expected_dances) == set(actual_dances)
    
    def test_dance_type_from_string(self):
        """Test creating dance type from string."""
        assert DanceType("waggle") == DanceType.WAGGLE
        assert DanceType("round") == DanceType.ROUND
        
        with pytest.raises(ValueError):
            DanceType("invalid_dance")


class TestBeeMetadata:
    """Test the BeeMetadata model."""
    
    def test_bee_creation(self):
        """Test creating a bee with metadata."""
        bee = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            assigned_task="Implement authentication",
            estimated_tokens=1000
        )
        
        assert bee.bee_id.startswith("bee_")
        assert bee.dance_type == DanceType.WAGGLE
        assert bee.assigned_task == "Implement authentication"
        assert bee.estimated_tokens == 1000
        assert bee.actual_tokens is None
    
    def test_bee_efficiency_calculation(self):
        """Test token efficiency calculation."""
        bee = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            estimated_tokens=1000
        )
        
        # No actual tokens yet
        assert bee.calculate_efficiency() is None
        
        # Set actual tokens less than estimate (good efficiency)
        bee.actual_tokens = 700
        assert bee.calculate_efficiency() == 0.3  # 30% savings
        
        # Set actual tokens equal to estimate
        bee.actual_tokens = 1000
        assert bee.calculate_efficiency() == 0.0
        
        # Set actual tokens more than estimate (over budget)
        bee.actual_tokens = 1200
        assert bee.calculate_efficiency() == -0.2  # 20% over


class TestSwarmTask:
    """Test the SwarmTask model."""
    
    def test_task_creation(self):
        """Test creating a swarm task."""
        task = SwarmTask(
            description="Build user authentication",
            priority=TaskPriority.HIGH,
            dance_type=DanceType.WAGGLE,
            max_tokens=15000
        )
        
        assert task.task_id.startswith("task_")
        assert task.description == "Build user authentication"
        assert task.priority == TaskPriority.HIGH
        assert task.dance_type == DanceType.WAGGLE
        assert task.status == TaskStatus.PENDING
        assert task.max_tokens == 15000
        assert isinstance(task.created_at, datetime)
        assert len(task.assigned_bees) == 0
    
    def test_assign_bee(self):
        """Test assigning bees to a task."""
        task = SwarmTask(
            description="Test task",
            dance_type=DanceType.ROUND
        )
        
        bee1 = BeeMetadata(dance_type=DanceType.ROUND, estimated_tokens=100)
        bee2 = BeeMetadata(dance_type=DanceType.ROUND, estimated_tokens=150)
        
        # Assign first bee
        task.assign_bee(bee1)
        assert len(task.assigned_bees) == 1
        assert task.status == TaskStatus.ASSIGNED
        
        # Assign second bee
        task.assign_bee(bee2)
        assert len(task.assigned_bees) == 2
        assert task.status == TaskStatus.ASSIGNED
    
    def test_task_completion(self):
        """Test marking a task as complete."""
        task = SwarmTask(
            description="Test task",
            dance_type=DanceType.ROUND
        )
        
        result = "Task completed successfully"
        task.mark_complete(result)
        
        assert task.status == TaskStatus.COMPLETED
        assert task.result == result
        assert task.completed_at is not None
        assert task.error is None
    
    def test_task_failure(self):
        """Test marking a task as failed."""
        task = SwarmTask(
            description="Test task",
            dance_type=DanceType.ROUND
        )
        
        error = "Connection timeout"
        task.mark_failed(error)
        
        assert task.status == TaskStatus.FAILED
        assert task.error == error
        assert task.completed_at is not None
        assert task.result is None
    
    def test_token_savings_calculation(self):
        """Test calculating token savings."""
        task = SwarmTask(
            description="Complex task",
            dance_type=DanceType.WAGGLE,
            max_tokens=10000
        )
        
        # Add bees with actual token usage
        bee1 = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            estimated_tokens=3000,
            actual_tokens=2000
        )
        bee2 = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            estimated_tokens=3000,
            actual_tokens=1500
        )
        
        task.assign_bee(bee1)
        task.assign_bee(bee2)
        
        # Total actual: 2000 + 1500 = 3500
        # Max tokens: 10000
        # Savings: (10000 - 3500) / 10000 * 100 = 65%
        assert task.calculate_token_savings() == 65.0
        
        # Test with no actual tokens (uses estimates)
        bee3 = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            estimated_tokens=2000
        )
        task.assign_bee(bee3)
        
        # Total: 2000 + 1500 + 2000 = 5500
        # Savings: (10000 - 5500) / 10000 * 100 = 45%
        assert task.calculate_token_savings() == 45.0


class TestTaskDelegationModels:
    """Test request and response models."""
    
    def test_delegation_request(self):
        """Test task delegation request model."""
        request = TaskDelegationRequest(
            description="Build feature X",
            priority=TaskPriority.MEDIUM,
            max_tokens=5000,
            preferred_dance=DanceType.WAGGLE,
            subtasks=["Design API", "Implement logic", "Write tests"]
        )
        
        assert request.description == "Build feature X"
        assert request.priority == TaskPriority.MEDIUM
        assert request.max_tokens == 5000
        assert request.preferred_dance == DanceType.WAGGLE
        assert len(request.subtasks) == 3
    
    def test_delegation_request_defaults(self):
        """Test delegation request with defaults."""
        request = TaskDelegationRequest(description="Simple task")
        
        assert request.description == "Simple task"
        assert request.priority == TaskPriority.MEDIUM
        assert request.max_tokens == 10000
        assert request.preferred_dance is None
        assert request.subtasks is None
    
    def test_delegation_response(self):
        """Test task delegation response model."""
        response = TaskDelegationResponse(
            task_id="task_123",
            dance_type=DanceType.WAGGLE,
            assigned_bees=4,
            estimated_token_savings=73.5,
            message="Task delegated successfully"
        )
        
        assert response.task_id == "task_123"
        assert response.dance_type == DanceType.WAGGLE
        assert response.assigned_bees == 4
        assert response.estimated_token_savings == 73.5
        assert response.message == "Task delegated successfully"


class TestModelValidation:
    """Test model validation and error cases."""
    
    def test_bee_metadata_validation(self):
        """Test BeeMetadata validation."""
        # Valid bee
        bee = BeeMetadata(
            dance_type=DanceType.WAGGLE,
            estimated_tokens=100
        )
        assert bee.estimated_tokens > 0
        
        # Invalid: negative tokens
        with pytest.raises(ValueError):
            BeeMetadata(
                dance_type=DanceType.WAGGLE,
                estimated_tokens=-100
            )
    
    def test_swarm_task_validation(self):
        """Test SwarmTask validation."""
        # Valid task
        task = SwarmTask(
            description="Valid task",
            dance_type=DanceType.ROUND,
            max_tokens=1000
        )
        assert task.max_tokens > 0
        
        # Invalid: negative max tokens
        with pytest.raises(ValueError):
            SwarmTask(
                description="Invalid task",
                dance_type=DanceType.ROUND,
                max_tokens=-1000
            )
    
    def test_delegation_request_validation(self):
        """Test TaskDelegationRequest validation."""
        # Invalid: empty description
        with pytest.raises(ValueError):
            TaskDelegationRequest(description="")