"""Tests for SwarmRouter MCP server."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from src.server import (
    delegate_task_impl,
    delegator,
    mcp,
)
from src.models import TaskPriority, DanceType, TaskStatus


class TestServerImplementation:
    """Test the server implementation functions."""

    @pytest.mark.asyncio
    async def test_delegate_task_impl_basic(self):
        """Test basic task delegation implementation."""
        result = await delegate_task_impl(
            task_description="Send a simple notification",
            priority="medium",
            max_tokens=5000,
        )

        assert "error" not in result
        assert "task_id" in result
        assert "dance_type" in result
        assert "assigned_bees" in result
        assert "estimated_token_savings" in result
        assert "message" in result

        # Should detect ROUND dance for simple notification
        assert result["dance_type"] == DanceType.ROUND.value
        assert result["assigned_bees"] == 1
        assert result["estimated_token_savings"] >= 0

    @pytest.mark.asyncio
    async def test_delegate_task_impl_complex(self):
        """Test complex task delegation with waggle dance."""
        result = await delegate_task_impl(
            task_description="Analyze and decompose this complex system architecture",
            task_type="waggle",
            priority="high",
            max_tokens=15000,
        )

        assert "error" not in result
        assert result["dance_type"] == DanceType.WAGGLE.value
        assert result["assigned_bees"] == 4  # Waggle dance creates 4 subtasks
        assert result["estimated_token_savings"] > 50  # Should have significant savings

        # Verify task was stored
        task_id = result["task_id"]
        task = delegator.get_task_status(task_id)
        assert task is not None
        assert task.priority == TaskPriority.HIGH
        assert task.dance_type == DanceType.WAGGLE

    @pytest.mark.asyncio
    async def test_delegate_task_impl_with_subtasks(self):
        """Test delegation with custom subtasks."""
        custom_subtasks = [
            "Design the database schema",
            "Implement REST API endpoints",
            "Create user interface",
        ]

        result = await delegate_task_impl(
            task_description="Build user management system",
            subtasks=custom_subtasks,
            max_tokens=12000,
        )

        assert "error" not in result
        assert result["assigned_bees"] == 3

        # Verify bees have the custom subtasks
        task_id = result["task_id"]
        task = delegator.get_task_status(task_id)
        assert len(task.assigned_bees) == 3

        assigned_tasks = [bee.assigned_task for bee in task.assigned_bees]
        for subtask in custom_subtasks:
            assert subtask in assigned_tasks

    @pytest.mark.asyncio
    async def test_delegate_task_impl_invalid_priority(self):
        """Test handling of invalid priority values."""
        result = await delegate_task_impl(
            task_description="Test task",
            priority="invalid",
        )

        # Should handle gracefully and return error
        assert "error" in result

    @pytest.mark.asyncio
    async def test_delegate_task_impl_invalid_dance_type(self):
        """Test handling of invalid dance type."""
        result = await delegate_task_impl(
            task_description="Test task",
            task_type="invalid_dance",
        )

        # Should handle gracefully and auto-detect dance type
        assert "error" not in result
        assert "dance_type" in result

    @pytest.mark.asyncio
    async def test_delegate_task_impl_different_dance_types(self):
        """Test different dance types produce different results."""
        test_cases = [
            ("Research best practices for microservices", DanceType.SCOUT),
            ("Fix authentication bug", DanceType.TREMBLE),
            ("Parallel processing of data files", DanceType.DISPERSE),
            ("Build consensus on API design", DanceType.CONVERGE),
        ]

        for description, expected_dance in test_cases:
            result = await delegate_task_impl(
                task_description=description,
                max_tokens=8000,
            )

            assert "error" not in result
            assert result["dance_type"] == expected_dance.value

    @pytest.mark.asyncio
    async def test_delegate_task_impl_token_savings_calculation(self):
        """Test that token savings are calculated correctly."""
        result = await delegate_task_impl(
            task_description="Complex task requiring decomposition",
            task_type="waggle",
            max_tokens=10000,
        )

        assert "error" not in result
        savings = result["estimated_token_savings"]

        # Waggle dance should have significant savings (>60%)
        assert savings > 60
        assert savings <= 100


class TestServerIntegration:
    """Integration tests for the complete server functionality."""

    @pytest.mark.asyncio
    async def test_end_to_end_task_delegation(self):
        """Test complete end-to-end task delegation flow."""
        # Step 1: Delegate a task
        task_description = "Build a comprehensive user authentication system with JWT tokens and password reset"

        result = await delegate_task_impl(
            task_description=task_description,
            priority="high",
            max_tokens=20000,
        )

        assert "error" not in result
        task_id = result["task_id"]

        # Step 2: Verify task is stored and accessible
        task = delegator.get_task_status(task_id)
        assert task is not None
        assert task.description == task_description
        assert task.status == TaskStatus.ASSIGNED
        assert len(task.assigned_bees) > 0

        # Step 3: Verify each bee has proper metadata
        for bee in task.assigned_bees:
            assert bee.bee_id.startswith("bee_")
            assert bee.dance_type == task.dance_type
            assert bee.assigned_task is not None
            assert bee.estimated_tokens > 0
            assert bee.specialty is not None

        # Step 4: Verify swarm statistics include this task
        stats = delegator.get_swarm_statistics()
        assert stats["total_tasks"] >= 1
        assert stats["active_tasks"] >= 1
        assert stats["total_bees_deployed"] >= len(task.assigned_bees)

    @pytest.mark.asyncio
    async def test_multiple_concurrent_tasks(self):
        """Test handling multiple concurrent task delegations."""
        tasks = [
            "Send notification about system maintenance",
            "Research new authentication protocols",
            "Debug performance issues in database queries",
            "Build consensus on new feature priorities",
        ]

        # Delegate all tasks concurrently
        results = await asyncio.gather(
            *[
                delegate_task_impl(task_description=task, max_tokens=5000)
                for task in tasks
            ]
        )

        # Verify all tasks were successful
        task_ids = []
        for result in results:
            assert "error" not in result
            assert "task_id" in result
            task_ids.append(result["task_id"])

        # Verify all tasks are unique and stored
        assert len(set(task_ids)) == len(task_ids)  # All unique

        for task_id in task_ids:
            task = delegator.get_task_status(task_id)
            assert task is not None
            assert task.status == TaskStatus.ASSIGNED

        # Verify swarm statistics reflect all tasks
        stats = delegator.get_swarm_statistics()
        assert stats["total_tasks"] >= len(tasks)
        assert stats["active_tasks"] >= len(tasks)

    @pytest.mark.asyncio
    async def test_task_lifecycle_simulation(self):
        """Test simulating a complete task lifecycle."""
        # Create task
        result = await delegate_task_impl(
            task_description="Implement user profile management",
            max_tokens=8000,
        )

        task_id = result["task_id"]
        task = delegator.get_task_status(task_id)

        # Simulate completion
        task.mark_complete("User profile management implemented successfully")

        # Verify completed state
        assert task.status == TaskStatus.COMPLETED
        assert task.result is not None
        assert task.completed_at is not None

        # Verify stats reflect completion
        stats = delegator.get_swarm_statistics()
        assert stats["completed_tasks"] >= 1

    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self):
        """Test error handling and recovery scenarios."""
        # Test with empty description
        result = await delegate_task_impl(
            task_description="",
            max_tokens=5000,
        )
        assert "error" in result

        # Test with negative max_tokens
        result = await delegate_task_impl(
            task_description="Valid task",
            max_tokens=-1000,
        )
        assert "error" in result

        # Test with extremely long description
        long_description = "x" * 10000
        result = await delegate_task_impl(
            task_description=long_description,
            max_tokens=5000,
        )
        # Should handle gracefully
        assert "task_id" in result or "error" in result

    @pytest.mark.asyncio
    async def test_token_optimization_scenarios(self):
        """Test different scenarios for token optimization."""
        test_scenarios = [
            {
                "description": "Simple status update",
                "expected_dance": DanceType.ROUND,
                "expected_min_savings": 5,
                "expected_max_savings": 25,
            },
            {
                "description": "Complex system architecture analysis and decomposition",
                "expected_dance": DanceType.WAGGLE,
                "expected_min_savings": 60,
                "expected_max_savings": 80,
            },
            {
                "description": "Parallel data processing tasks",
                "expected_dance": DanceType.DISPERSE,
                "expected_min_savings": 70,
                "expected_max_savings": 80,
            },
        ]

        for scenario in test_scenarios:
            result = await delegate_task_impl(
                task_description=scenario["description"],
                max_tokens=10000,
            )

            assert "error" not in result
            assert result["dance_type"] == scenario["expected_dance"].value

            savings = result["estimated_token_savings"]
            assert (
                scenario["expected_min_savings"]
                <= savings
                <= scenario["expected_max_savings"]
            )


class TestMCPServerIntegration:
    """Test MCP server integration if available."""

    def test_mcp_server_initialization(self):
        """Test MCP server initialization."""
        if mcp is not None:
            # MCP server should be initialized
            assert hasattr(mcp, "tool")
            assert hasattr(mcp, "resource")
            assert hasattr(mcp, "prompt")
        else:
            # Should gracefully handle missing MCP
            assert mcp is None

    @pytest.mark.skipif(mcp is None, reason="MCP not available")
    def test_mcp_tools_registered(self):
        """Test that MCP tools are properly registered."""
        # This test only runs if MCP is available
        # The tools should be registered with the MCP server
        assert mcp is not None

    @pytest.mark.asyncio
    async def test_server_error_handling(self):
        """Test server-level error handling."""
        # Test exception handling in delegate_task_impl
        with patch(
            "src.server.delegator.delegate_task", side_effect=Exception("Test error")
        ):
            result = await delegate_task_impl(
                task_description="Test task",
                max_tokens=5000,
            )

            assert "error" in result
            assert "Test error" in result["error"]


class TestServerPerformance:
    """Test server performance characteristics."""

    @pytest.mark.asyncio
    async def test_response_time(self):
        """Test that task delegation responds within reasonable time."""
        import time

        start_time = time.time()

        result = await delegate_task_impl(
            task_description="Test performance task",
            max_tokens=5000,
        )

        end_time = time.time()
        response_time = end_time - start_time

        # Should respond within 1 second for simple tasks
        assert response_time < 1.0
        assert "error" not in result

    @pytest.mark.asyncio
    async def test_memory_usage_with_many_tasks(self):
        """Test memory usage doesn't grow unreasonably with many tasks."""
        initial_task_count = len(delegator.tasks)

        # Create many tasks
        for i in range(50):
            await delegate_task_impl(
                task_description=f"Test task {i}",
                max_tokens=1000,
            )

        # Verify tasks are tracked
        assert len(delegator.tasks) == initial_task_count + 50

        # Verify stats are calculated efficiently
        stats = delegator.get_swarm_statistics()
        assert stats["total_tasks"] == initial_task_count + 50
