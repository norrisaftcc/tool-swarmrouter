"""Tests for task delegation logic."""

import pytest
from src.models import (
    DanceType, TaskPriority, TaskStatus, TaskDelegationRequest
)
from src.delegation import TaskDelegator


class TestTaskDelegator:
    """Test the TaskDelegator class."""
    
    @pytest.fixture
    def delegator(self):
        """Create a TaskDelegator instance for testing."""
        return TaskDelegator()
    
    def test_determine_dance_type_waggle(self, delegator):
        """Test identifying waggle dance for complex tasks."""
        descriptions = [
            "Analyze and decompose this complex system architecture",
            "Break down the requirements for a multi-step process",
            "Create a comprehensive analysis of the codebase"
        ]
        
        for desc in descriptions:
            dance = delegator.determine_dance_type(desc)
            assert dance == DanceType.WAGGLE
    
    def test_determine_dance_type_round(self, delegator):
        """Test identifying round dance for simple tasks."""
        descriptions = [
            "Send a simple notification to users",
            "Quick status update needed",
            "Brief announcement about maintenance"
        ]
        
        for desc in descriptions:
            dance = delegator.determine_dance_type(desc)
            assert dance == DanceType.ROUND
    
    def test_determine_dance_type_scout(self, delegator):
        """Test identifying scout dance for research tasks."""
        descriptions = [
            "Research best practices for microservices",
            "Explore new authentication methods",
            "Find and identify security vulnerabilities"
        ]
        
        for desc in descriptions:
            dance = delegator.determine_dance_type(desc)
            assert dance == DanceType.SCOUT
    
    def test_determine_dance_type_default(self, delegator):
        """Test default to waggle for ambiguous tasks."""
        description = "Do something with the code"
        dance = delegator.determine_dance_type(description)
        assert dance == DanceType.WAGGLE
    
    def test_estimate_tokens_per_bee(self, delegator):
        """Test token estimation for different dance types."""
        total_tokens = 10000
        num_subtasks = 4
        
        # Test waggle (30% of allocation = 70% savings)
        tokens = delegator.estimate_tokens_per_bee(
            total_tokens, num_subtasks, DanceType.WAGGLE
        )
        assert tokens == 750  # (10000/4) * 0.3
        
        # Test round (90% of allocation = 10% savings)
        tokens = delegator.estimate_tokens_per_bee(
            total_tokens, num_subtasks, DanceType.ROUND
        )
        assert tokens == 2250  # (10000/4) * 0.9
        
        # Test disperse (25% of allocation = 75% savings)
        tokens = delegator.estimate_tokens_per_bee(
            total_tokens, num_subtasks, DanceType.DISPERSE
        )
        assert tokens == 625  # (10000/4) * 0.25
    
    def test_generate_default_subtasks(self, delegator):
        """Test default subtask generation."""
        description = "Build authentication system"
        
        # Waggle dance should generate 4 subtasks
        subtasks = delegator.generate_default_subtasks(
            description, DanceType.WAGGLE
        )
        assert len(subtasks) == 4
        assert "Analyze requirements" in subtasks[0]
        assert "Design solution" in subtasks[1]
        
        # Round dance should generate 1 subtask
        subtasks = delegator.generate_default_subtasks(
            description, DanceType.ROUND
        )
        assert len(subtasks) == 1
        assert subtasks[0] == f"Execute: {description}"
        
        # Scout dance should generate 3 subtasks
        subtasks = delegator.generate_default_subtasks(
            description, DanceType.SCOUT
        )
        assert len(subtasks) == 3
        assert "Research existing solutions" in subtasks[0]
    
    def test_get_bee_specialty(self, delegator):
        """Test bee specialty assignment."""
        assert delegator.get_bee_specialty(DanceType.WAGGLE) == "architect"
        assert delegator.get_bee_specialty(DanceType.ROUND) == "messenger"
        assert delegator.get_bee_specialty(DanceType.SCOUT) == "explorer"
        assert delegator.get_bee_specialty(DanceType.TREMBLE) == "debugger"
        assert delegator.get_bee_specialty(DanceType.CONVERGE) == "facilitator"
        assert delegator.get_bee_specialty(DanceType.DISPERSE) == "coordinator"
    
    def test_create_bees_for_task(self, delegator):
        """Test bee creation for tasks."""
        from src.models import SwarmTask
        
        task = SwarmTask(
            description="Complex task",
            dance_type=DanceType.WAGGLE,
            max_tokens=10000
        )
        
        # Create bees with custom subtasks
        subtasks = ["Design", "Implement", "Test"]
        bees = delegator.create_bees_for_task(task, subtasks)
        
        assert len(bees) == 3
        assert all(bee.dance_type == DanceType.WAGGLE for bee in bees)
        assert bees[0].assigned_task == "Design"
        assert bees[1].assigned_task == "Implement"
        assert bees[2].assigned_task == "Test"
        assert all(bee.specialty == "architect" for bee in bees)
        
        # Test token allocation
        expected_tokens = int((10000/3) * 0.3)  # Account for integer conversion
        assert all(bee.estimated_tokens == expected_tokens for bee in bees)
    
    def test_delegate_task_simple(self, delegator):
        """Test delegating a simple task."""
        request = TaskDelegationRequest(
            description="Send notification about system update",
            priority=TaskPriority.LOW
        )
        
        task = delegator.delegate_task(request)
        
        assert task.task_id.startswith("task_")
        assert task.description == request.description
        assert task.priority == TaskPriority.LOW
        assert task.dance_type == DanceType.ROUND
        assert task.status == TaskStatus.ASSIGNED
        assert len(task.assigned_bees) == 1  # Round dance = 1 bee
        assert task.task_id in delegator.tasks
    
    def test_delegate_task_complex(self, delegator):
        """Test delegating a complex task with subtasks."""
        subtasks = [
            "Design database schema",
            "Implement API endpoints",
            "Create frontend components",
            "Write integration tests"
        ]
        
        request = TaskDelegationRequest(
            description="Build a complete user management system",
            priority=TaskPriority.HIGH,
            max_tokens=20000,
            preferred_dance=DanceType.WAGGLE,
            subtasks=subtasks
        )
        
        task = delegator.delegate_task(request)
        
        assert task.priority == TaskPriority.HIGH
        assert task.dance_type == DanceType.WAGGLE
        assert task.max_tokens == 20000
        assert len(task.assigned_bees) == 4
        
        # Check bee assignments
        for i, bee in enumerate(task.assigned_bees):
            assert bee.assigned_task == subtasks[i]
            assert bee.specialty == "architect"
    
    def test_get_task_status(self, delegator):
        """Test retrieving task status."""
        # Create a task
        request = TaskDelegationRequest(description="Test task")
        task = delegator.delegate_task(request)
        
        # Retrieve status
        retrieved = delegator.get_task_status(task.task_id)
        assert retrieved is not None
        assert retrieved.task_id == task.task_id
        assert retrieved.description == "Test task"
        
        # Non-existent task
        assert delegator.get_task_status("fake_id") is None
    
    def test_get_swarm_statistics_empty(self, delegator):
        """Test swarm statistics with no tasks."""
        stats = delegator.get_swarm_statistics()
        
        assert stats["total_tasks"] == 0
        assert stats["active_tasks"] == 0
        assert stats["completed_tasks"] == 0
        assert stats["average_token_savings"] == 0
        assert stats["total_bees_deployed"] == 0
    
    def test_get_swarm_statistics_with_tasks(self, delegator):
        """Test swarm statistics with multiple tasks."""
        # Create some tasks
        for i in range(3):
            request = TaskDelegationRequest(
                description=f"Task {i}",
                max_tokens=10000
            )
            task = delegator.delegate_task(request)
            
            # Complete one task
            if i == 0:
                task.mark_complete("Done")
                # Set actual tokens for savings calculation
                for bee in task.assigned_bees:
                    bee.actual_tokens = 500
        
        stats = delegator.get_swarm_statistics()
        
        assert stats["total_tasks"] == 3
        assert stats["active_tasks"] == 2  # 2 still assigned
        assert stats["completed_tasks"] == 1
        assert stats["average_token_savings"] > 0
        assert stats["total_bees_deployed"] > 0
    
    def test_dance_type_override(self, delegator):
        """Test overriding automatic dance type detection."""
        request = TaskDelegationRequest(
            description="This seems complex and needs decomposition",
            preferred_dance=DanceType.ROUND  # Override to simple
        )
        
        task = delegator.delegate_task(request)
        
        # Should use preferred dance, not detected
        assert task.dance_type == DanceType.ROUND
        assert len(task.assigned_bees) == 1  # Round = 1 bee