#!/usr/bin/env python3
"""
SwarmRouter MCP Client Example

This script demonstrates how to interact with the SwarmRouter MCP server,
showcasing task delegation, bee coordination, and token optimization patterns.

Usage:
    python client_example.py

Requirements:
    - SwarmRouter MCP server running
    - MCP client dependencies installed
"""

import asyncio
import json
import time
from typing import Dict, List, Any
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.server import delegate_task_impl, delegator
from src.models import DanceType, TaskPriority


class SwarmRouterClient:
    """
    Example client for interacting with SwarmRouter MCP server.

    This client demonstrates various patterns of task delegation
    and shows how to leverage the bee swarm metaphor for efficient
    AI task processing.
    """

    def __init__(self):
        """Initialize the client."""
        self.total_tasks_delegated = 0
        self.total_tokens_saved = 0

    async def delegate_task(
        self,
        description: str,
        task_type: str = None,
        priority: str = "medium",
        max_tokens: int = 10000,
        subtasks: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Delegate a task to the SwarmRouter server.

        Args:
            description: Task description
            task_type: Optional dance type override
            priority: Task priority (low, medium, high, critical)
            max_tokens: Maximum token budget
            subtasks: Optional custom subtasks

        Returns:
            Task delegation result
        """
        print(
            f"\n🐝 Delegating task: {description[:50]}{'...' if len(description) > 50 else ''}"
        )

        start_time = time.time()

        try:
            result = await delegate_task_impl(
                task_description=description,
                task_type=task_type,
                priority=priority,
                max_tokens=max_tokens,
                subtasks=subtasks,
            )

            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)

            if "error" in result:
                print(f"❌ Error: {result['error']}")
                return result

            # Track success metrics
            self.total_tasks_delegated += 1
            self.total_tokens_saved += result.get("estimated_token_savings", 0)

            # Display results
            print(f"✅ Task delegated successfully!")
            print(f"   📋 Task ID: {result['task_id']}")
            print(f"   🎭 Dance Type: {result['dance_type']}")
            print(f"   🐝 Assigned Bees: {result['assigned_bees']}")
            print(f"   💰 Token Savings: {result['estimated_token_savings']:.1f}%")
            print(f"   ⏱️  Response Time: {response_time}ms")
            print(f"   💬 Message: {result['message']}")

            return result

        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            return {"error": str(e)}

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a delegated task.

        Args:
            task_id: The task ID to check

        Returns:
            Task status information
        """
        print(f"\n📊 Checking status for task: {task_id}")

        try:
            task = delegator.get_task_status(task_id)

            if not task:
                print(f"❌ Task {task_id} not found")
                return {"error": f"Task {task_id} not found"}

            status_info = {
                "task_id": task.task_id,
                "status": task.status.value,
                "dance_type": task.dance_type.value,
                "assigned_bees": len(task.assigned_bees),
                "created_at": task.created_at.isoformat(),
                "completed_at": (
                    task.completed_at.isoformat() if task.completed_at else None
                ),
                "token_savings": task.calculate_token_savings(),
                "description": (
                    task.description[:100] + "..."
                    if len(task.description) > 100
                    else task.description
                ),
            }

            print(f"📈 Task Status:")
            print(f"   Status: {status_info['status']}")
            print(f"   Dance: {status_info['dance_type']}")
            print(f"   Bees: {status_info['assigned_bees']}")
            print(f"   Created: {status_info['created_at']}")
            if status_info["completed_at"]:
                print(f"   Completed: {status_info['completed_at']}")
            print(f"   Token Savings: {status_info['token_savings']:.1f}%")

            return status_info

        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            return {"error": str(e)}

    async def get_swarm_statistics(self) -> Dict[str, Any]:
        """
        Get overall swarm performance statistics.

        Returns:
            Swarm statistics
        """
        print(f"\n📊 Getting swarm statistics...")

        try:
            stats = delegator.get_swarm_statistics()

            print(f"🏆 Swarm Performance:")
            print(f"   Total Tasks: {stats['total_tasks']}")
            print(f"   Active Tasks: {stats['active_tasks']}")
            print(f"   Completed Tasks: {stats['completed_tasks']}")
            print(f"   Average Token Savings: {stats['average_token_savings']:.1f}%")
            print(f"   Total Bees Deployed: {stats['total_bees_deployed']}")

            return stats

        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            return {"error": str(e)}

    async def demonstrate_dance_types(self):
        """Demonstrate different bee dance types and their use cases."""
        print(f"\n{'='*60}")
        print(f"🎭 DEMONSTRATING BEE DANCE TYPES")
        print(f"{'='*60}")

        dance_examples = [
            {
                "dance": "waggle",
                "description": "Design and implement a comprehensive user authentication system with JWT tokens, password reset, and multi-factor authentication",
                "explanation": "Complex tasks requiring decomposition into multiple subtasks",
            },
            {
                "dance": "round",
                "description": "Send notification to all users about scheduled maintenance",
                "explanation": "Simple tasks that can be completed quickly",
            },
            {
                "dance": "scout",
                "description": "Research best practices for implementing microservices architecture",
                "explanation": "Exploration and research tasks",
            },
            {
                "dance": "tremble",
                "description": "Debug authentication timeout issues in production",
                "explanation": "Error handling and troubleshooting tasks",
            },
            {
                "dance": "converge",
                "description": "Build consensus on new API design among team members",
                "explanation": "Tasks requiring collaboration and agreement",
            },
            {
                "dance": "disperse",
                "description": "Process multiple data files in parallel for analysis",
                "explanation": "Tasks that can be parallelized efficiently",
            },
        ]

        for example in dance_examples:
            print(f"\n🎭 {example['dance'].upper()} DANCE")
            print(f"💡 Use case: {example['explanation']}")
            print(f"📝 Task: {example['description']}")

            result = await self.delegate_task(
                description=example["description"],
                task_type=example["dance"],
                max_tokens=12000,
            )

            if "error" not in result:
                print(
                    f"🎯 Expected bees for {example['dance']}: {result['assigned_bees']}"
                )
                print(f"🏆 Token efficiency: {result['estimated_token_savings']:.1f}%")

            await asyncio.sleep(0.5)  # Brief pause for readability

    async def demonstrate_priority_levels(self):
        """Demonstrate different task priority levels."""
        print(f"\n{'='*60}")
        print(f"⚡ DEMONSTRATING PRIORITY LEVELS")
        print(f"{'='*60}")

        priority_examples = [
            {
                "priority": "low",
                "description": "Update documentation with latest API changes",
                "explanation": "Non-urgent maintenance tasks",
            },
            {
                "priority": "medium",
                "description": "Implement new user preference settings",
                "explanation": "Standard feature development",
            },
            {
                "priority": "high",
                "description": "Optimize database queries for performance",
                "explanation": "Important performance improvements",
            },
            {
                "priority": "critical",
                "description": "Fix security vulnerability in authentication",
                "explanation": "Urgent security or production issues",
            },
        ]

        for example in priority_examples:
            print(f"\n⚡ {example['priority'].upper()} PRIORITY")
            print(f"💡 Use case: {example['explanation']}")

            result = await self.delegate_task(
                description=example["description"],
                priority=example["priority"],
                max_tokens=8000,
            )

            await asyncio.sleep(0.5)

    async def demonstrate_custom_subtasks(self):
        """Demonstrate using custom subtasks for fine-grained control."""
        print(f"\n{'='*60}")
        print(f"🔧 DEMONSTRATING CUSTOM SUBTASKS")
        print(f"{'='*60}")

        print(f"\n📋 Custom Subtask Decomposition")
        print(f"Instead of letting the swarm auto-generate subtasks,")
        print(f"you can provide your own for precise control.")

        custom_subtasks = [
            "Design the database schema for user profiles",
            "Implement REST API endpoints for CRUD operations",
            "Create React components for profile management UI",
            "Write comprehensive unit and integration tests",
            "Set up CI/CD pipeline for automated deployment",
        ]

        print(f"\n🎯 Custom subtasks:")
        for i, subtask in enumerate(custom_subtasks, 1):
            print(f"   {i}. {subtask}")

        result = await self.delegate_task(
            description="Build a complete user profile management system",
            subtasks=custom_subtasks,
            priority="high",
            max_tokens=15000,
        )

        if "error" not in result:
            task_id = result["task_id"]
            task = delegator.get_task_status(task_id)

            print(f"\n🐝 Bee assignments:")
            for i, bee in enumerate(task.assigned_bees, 1):
                print(f"   {bee.bee_id}: {bee.assigned_task}")

    async def demonstrate_token_optimization(self):
        """Demonstrate token optimization patterns."""
        print(f"\n{'='*60}")
        print(f"💰 DEMONSTRATING TOKEN OPTIMIZATION")
        print(f"{'='*60}")

        optimization_examples = [
            {
                "task": "Simple email template update",
                "tokens": 1000,
                "expected_savings": "10-20%",
            },
            {
                "task": "Complex e-commerce platform architecture with multiple microservices",
                "tokens": 20000,
                "expected_savings": "70-80%",
            },
            {
                "task": "Parallel analysis of customer data across multiple regions",
                "tokens": 15000,
                "expected_savings": "75%+",
            },
        ]

        savings_results = []

        for example in optimization_examples:
            print(f"\n💰 Token Optimization Test")
            print(f"📝 Task: {example['task']}")
            print(f"🎯 Budget: {example['tokens']} tokens")
            print(f"📈 Expected savings: {example['expected_savings']}")

            result = await self.delegate_task(
                description=example["task"], max_tokens=example["tokens"]
            )

            if "error" not in result:
                actual_savings = result["estimated_token_savings"]
                savings_results.append(actual_savings)
                print(f"✅ Actual savings: {actual_savings:.1f}%")

                # Calculate estimated cost reduction
                tokens_saved = int(example["tokens"] * actual_savings / 100)
                print(f"💵 Tokens saved: {tokens_saved}")

            await asyncio.sleep(0.5)

        if savings_results:
            avg_savings = sum(savings_results) / len(savings_results)
            print(f"\n🏆 Average token savings across examples: {avg_savings:.1f}%")

    async def run_comprehensive_demo(self):
        """Run a comprehensive demonstration of SwarmRouter capabilities."""
        print(f"🐝 SwarmRouter MCP Client Example")
        print(f"{'='*60}")
        print(f"This demonstration shows how to leverage bee swarm intelligence")
        print(f"for efficient AI task delegation and token optimization.")

        # Run all demonstrations
        await self.demonstrate_dance_types()
        await self.demonstrate_priority_levels()
        await self.demonstrate_custom_subtasks()
        await self.demonstrate_token_optimization()

        # Show final statistics
        print(f"\n{'='*60}")
        print(f"📊 FINAL STATISTICS")
        print(f"{'='*60}")

        await self.get_swarm_statistics()

        print(f"\n🎯 Client Session Summary:")
        print(f"   Tasks Delegated: {self.total_tasks_delegated}")
        if self.total_tasks_delegated > 0:
            avg_savings = self.total_tokens_saved / self.total_tasks_delegated
            print(f"   Average Token Savings: {avg_savings:.1f}%")

        print(f"\n✨ Demonstration completed successfully!")
        print(f"🔗 Next steps:")
        print(f"   1. Start the MCP server: mcp run src/server.py")
        print(f"   2. Integrate with your AI applications")
        print(f"   3. Monitor token savings and swarm performance")


async def interactive_mode():
    """Run interactive mode for hands-on exploration."""
    client = SwarmRouterClient()

    print(f"\n🎮 INTERACTIVE MODE")
    print(f"{'='*40}")
    print(f"Enter task descriptions to see SwarmRouter in action!")
    print(f"Commands: 'quit' to exit, 'stats' for statistics, 'help' for help")

    while True:
        try:
            user_input = input(f"\n🐝 Enter task description (or command): ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print(f"👋 Goodbye! Thanks for exploring SwarmRouter!")
                break
            elif user_input.lower() in ["stats", "statistics"]:
                await client.get_swarm_statistics()
            elif user_input.lower() in ["help", "h"]:
                print(f"\n📚 Available commands:")
                print(f"   - Enter any task description to delegate it")
                print(f"   - 'stats' - Show swarm statistics")
                print(f"   - 'quit' - Exit interactive mode")
                print(f"   - 'help' - Show this help message")
            elif user_input:
                await client.delegate_task(description=user_input, max_tokens=10000)
            else:
                print(f"❓ Please enter a task description or command")

        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye! Thanks for exploring SwarmRouter!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def quick_test():
    """Run a quick test of core functionality."""
    print(f"🚀 QUICK TEST")
    print(f"{'='*30}")

    client = SwarmRouterClient()

    # Test basic delegation
    result = await client.delegate_task(
        description="Create a simple REST API for managing user accounts",
        priority="medium",
        max_tokens=8000,
    )

    if "error" not in result:
        # Check status
        await client.get_task_status(result["task_id"])

    # Show statistics
    await client.get_swarm_statistics()

    print(f"\n✅ Quick test completed!")


def main():
    """Main entry point with different modes."""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "demo"

    print(f"🐝 SwarmRouter MCP Client Example")
    print(f"Version: 1.0.0")
    print(f"Mode: {mode}")

    if mode == "interactive":
        asyncio.run(interactive_mode())
    elif mode == "quick":
        asyncio.run(quick_test())
    else:
        # Default: comprehensive demo
        client = SwarmRouterClient()
        asyncio.run(client.run_comprehensive_demo())


if __name__ == "__main__":
    main()
