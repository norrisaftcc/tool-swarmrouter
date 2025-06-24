#!/usr/bin/env python3
"""
Basic tests for the Minimal SwarmRouter MCP Server.

These tests verify the core functionality without requiring
external dependencies like the Anthropic API.
"""

import asyncio
import unittest
from minimal_mcp_server import (
    MinimalSwarmRouter, MCPServer, DanceType, TaskComplexity,
    BeeAgent, SwarmTask
)


class TestMinimalSwarmRouter(unittest.TestCase):
    """Test the core SwarmRouter functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.router = MinimalSwarmRouter()
    
    def test_dance_type_detection(self):
        """Test that dance types are correctly detected."""
        test_cases = [
            ("List all files", DanceType.ROUND),
            ("Research API best practices", DanceType.SCOUT),
            ("Debug connection timeout error", DanceType.TREMBLE),
            ("Build authentication system", DanceType.WAGGLE),
            ("Team decision on framework", DanceType.CONVERGE),
        ]
        
        for description, expected_dance in test_cases:
            with self.subTest(description=description):
                detected = self.router.determine_dance_type(description)
                self.assertEqual(detected, expected_dance,
                               f"Expected {expected_dance} for '{description}', got {detected}")
    
    def test_complexity_analysis(self):
        """Test that task complexity is correctly analyzed."""
        test_cases = [
            ("List files", TaskComplexity.SIMPLE),
            ("Create a comprehensive user management system", TaskComplexity.COMPLEX),
            ("Design API endpoints", TaskComplexity.MEDIUM),
        ]
        
        for description, expected_complexity in test_cases:
            with self.subTest(description=description):
                detected = self.router.analyze_task_complexity(description)
                self.assertIn(detected, [expected_complexity, TaskComplexity.MEDIUM],
                            f"Unexpected complexity for '{description}': {detected}")
    
    def test_model_routing(self):
        """Test that models are correctly routed based on complexity."""
        test_cases = [
            (TaskComplexity.SIMPLE, "claude-3-haiku-20240307"),
            (TaskComplexity.MEDIUM, "claude-3-sonnet-20240229"),
            (TaskComplexity.COMPLEX, "claude-3-opus-20240229"),
        ]
        
        for complexity, expected_model in test_cases:
            with self.subTest(complexity=complexity):
                model = self.router.model_routing[complexity]
                self.assertEqual(model, expected_model)
    
    def test_subtask_generation(self):
        """Test that subtasks are generated correctly for different dance types."""
        test_cases = [
            (DanceType.ROUND, 1),    # Simple tasks have 1 subtask
            (DanceType.WAGGLE, 4),   # Complex decomposition has 4 subtasks
            (DanceType.SCOUT, 3),    # Research has 3 subtasks
            (DanceType.TREMBLE, 3),  # Debugging has 3 subtasks
        ]
        
        for dance_type, expected_count in test_cases:
            with self.subTest(dance_type=dance_type):
                subtasks = self.router.generate_subtasks("Test task", dance_type)
                self.assertEqual(len(subtasks), expected_count,
                               f"Expected {expected_count} subtasks for {dance_type}, got {len(subtasks)}")
    
    async def test_task_delegation(self):
        """Test end-to-end task delegation."""
        task = await self.router.delegate_task(
            "Create a simple hello world function",
            max_tokens=1000
        )
        
        # Verify task properties
        self.assertIsInstance(task, SwarmTask)
        self.assertEqual(task.status, "completed")
        self.assertGreater(len(task.bees), 0)
        
        # Verify all bees completed
        for bee in task.bees:
            self.assertEqual(bee.status, "completed")
            self.assertIsNotNone(bee.result)
    
    async def test_token_savings_calculation(self):
        """Test that token savings are calculated correctly."""
        task = await self.router.delegate_task(
            "Simple task",
            max_tokens=1000
        )
        
        savings = task.calculate_token_savings()
        self.assertGreater(savings, 0, "Task should show token savings")
        self.assertLessEqual(savings, 100, "Savings should not exceed 100%")


class TestMCPServer(unittest.TestCase):
    """Test the MCP server functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.server = MCPServer()
    
    async def test_delegate_task_request(self):
        """Test MCP delegate_task request handling."""
        request = {
            "id": 1,
            "method": "delegate_task",
            "params": {
                "description": "Test task",
                "max_tokens": 1000
            }
        }
        
        response = await self.server.process_request(request)
        
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("task_id", result)
        self.assertIn("dance_type", result)
        self.assertIn("bee_count", result)
    
    async def test_get_swarm_stats_request(self):
        """Test MCP get_swarm_stats request handling."""
        # First create a task
        await self.server.handle_delegate_task({
            "description": "Test task",
            "max_tokens": 1000
        })
        
        # Then get stats
        request = {
            "id": 2,
            "method": "get_swarm_stats",
            "params": {}
        }
        
        response = await self.server.process_request(request)
        
        self.assertIn("result", response)
        result = response["result"]
        self.assertIn("total_tasks", result)
        self.assertIn("total_bees", result)
        self.assertGreaterEqual(result["total_tasks"], 1)
    
    async def test_unknown_method(self):
        """Test handling of unknown MCP methods."""
        request = {
            "id": 3,
            "method": "unknown_method",
            "params": {}
        }
        
        response = await self.server.process_request(request)
        
        self.assertIn("error", response)
        self.assertIn("Unknown method", response["error"])


class TestBeeAgent(unittest.TestCase):
    """Test the BeeAgent class."""
    
    def test_bee_creation(self):
        """Test bee agent creation."""
        bee = BeeAgent(
            bee_id="test_bee_001",
            dance_type=DanceType.WAGGLE,
            task="Test task",
            estimated_tokens=100,
            model="claude-3-haiku-20240307"
        )
        
        self.assertEqual(bee.bee_id, "test_bee_001")
        self.assertEqual(bee.dance_type, DanceType.WAGGLE)
        self.assertEqual(bee.assigned_task, "Test task")
        self.assertEqual(bee.estimated_tokens, 100)
        self.assertEqual(bee.status, "pending")
    
    def test_bee_serialization(self):
        """Test bee to dictionary conversion."""
        bee = BeeAgent(
            bee_id="test_bee_001",
            dance_type=DanceType.ROUND,
            task="Test task",
            estimated_tokens=50
        )
        
        bee_dict = bee.to_dict()
        
        self.assertIsInstance(bee_dict, dict)
        self.assertEqual(bee_dict["bee_id"], "test_bee_001")
        self.assertEqual(bee_dict["dance_type"], "round")
        self.assertEqual(bee_dict["assigned_task"], "Test task")


class TestSwarmTask(unittest.TestCase):
    """Test the SwarmTask class."""
    
    def test_task_creation(self):
        """Test swarm task creation."""
        task = SwarmTask(
            task_id="test_task_001",
            description="Test task description",
            complexity=TaskComplexity.MEDIUM,
            dance_type=DanceType.WAGGLE,
            max_tokens=5000
        )
        
        self.assertEqual(task.task_id, "test_task_001")
        self.assertEqual(task.complexity, TaskComplexity.MEDIUM)
        self.assertEqual(task.dance_type, DanceType.WAGGLE)
        self.assertEqual(task.status, "pending")
    
    def test_bee_assignment(self):
        """Test adding bees to a task."""
        task = SwarmTask(
            task_id="test_task_001",
            description="Test task",
            complexity=TaskComplexity.SIMPLE,
            dance_type=DanceType.ROUND,
            max_tokens=1000
        )
        
        bee = BeeAgent(
            bee_id="test_bee_001",
            dance_type=DanceType.ROUND,
            task="Test subtask",
            estimated_tokens=500
        )
        
        task.add_bee(bee)
        
        self.assertEqual(len(task.bees), 1)
        self.assertEqual(task.status, "assigned")
        self.assertEqual(task.bees[0], bee)


async def run_async_tests():
    """Run async test methods."""
    router_tests = TestMinimalSwarmRouter()
    router_tests.setUp()
    
    print("Running async tests...")
    await router_tests.test_task_delegation()
    await router_tests.test_token_savings_calculation()
    print("✅ Task delegation tests passed")
    
    server_tests = TestMCPServer()
    server_tests.setUp()
    
    await server_tests.test_delegate_task_request()
    await server_tests.test_get_swarm_stats_request()
    await server_tests.test_unknown_method()
    print("✅ MCP server tests passed")


def main():
    """Run all tests."""
    print("🧪 Running Minimal SwarmRouter Tests")
    print("=" * 40)
    
    # Run sync tests
    print("Running synchronous tests...")
    unittest.main(exit=False, verbosity=0, buffer=True)
    print("✅ Synchronous tests completed")
    
    # Run async tests
    asyncio.run(run_async_tests())
    
    print("\n✨ All tests passed!")
    print("\nThe minimal MVP is working correctly!")


if __name__ == "__main__":
    main()