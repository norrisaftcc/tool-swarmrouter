#!/usr/bin/env python3
"""
SwarmRouter MCP Server - Main server implementation.

This server demonstrates task delegation using the bee/hive metaphor,
where AI agents (llamas) are coordinated by bee metadata to efficiently
handle complex tasks.
"""

import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # Fallback for development without mcp installed
    print("Warning: mcp package not installed. Install with: pip install 'mcp[cli]'")
    FastMCP = None

# Handle both relative and absolute imports for flexibility
try:
    from .models import (
        TaskDelegationRequest, TaskDelegationResponse,
        DanceType, TaskPriority
    )
    from .delegation import TaskDelegator
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from models import (
        TaskDelegationRequest, TaskDelegationResponse,
        DanceType, TaskPriority
    )
    from delegation import TaskDelegator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
if FastMCP:
    mcp = FastMCP(
        name=os.getenv("MCP_SERVER_NAME", "SwarmRouter"),
        version=os.getenv("MCP_SERVER_VERSION", "0.1.0")
    )
else:
    mcp = None
    logger.warning("Running without MCP server (development mode)")

# Initialize task delegator
delegator = TaskDelegator()


# Tool implementations
async def delegate_task_impl(
    task_description: str,
    task_type: Optional[str] = None,
    priority: str = "medium",
    max_tokens: int = 10000,
    subtasks: Optional[list[str]] = None
) -> Dict:
    """Implementation of the delegate_task tool."""
    try:
        # Parse priority
        priority_enum = TaskPriority(priority.lower())
        
        # Parse dance type if provided
        dance_type = None
        if task_type:
            try:
                dance_type = DanceType(task_type.lower())
            except ValueError:
                logger.warning(f"Invalid dance type '{task_type}', using auto-detection")
        
        # Create delegation request
        request = TaskDelegationRequest(
            description=task_description,
            priority=priority_enum,
            max_tokens=max_tokens,
            preferred_dance=dance_type,
            subtasks=subtasks
        )
        
        # Delegate to swarm
        task = delegator.delegate_task(request)
        
        # Create response
        response = TaskDelegationResponse(
            task_id=task.task_id,
            dance_type=task.dance_type,
            assigned_bees=len(task.assigned_bees),
            estimated_token_savings=task.calculate_token_savings(),
            message=f"Task delegated to {len(task.assigned_bees)} bees using {task.dance_type.value} dance"
        )
        
        return response.model_dump()
        
    except Exception as e:
        logger.error(f"Error delegating task: {e}", exc_info=True)
        return {"error": str(e)}


# MCP Tool decorator (only if MCP is available)
if mcp:
    @mcp.tool()
    async def delegate_task(
        task_description: str,
        task_type: Optional[str] = None,
        priority: str = "medium",
        max_tokens: int = 10000,
        subtasks: Optional[list[str]] = None
    ) -> Dict:
        """
        Delegate a task to the bee swarm for efficient execution.
        
        The swarm will analyze the task and assign appropriate bees using
        coordination patterns inspired by real bee behavior.
        
        Args:
            task_description: Description of the task to delegate
            task_type: Type of bee dance (waggle, round, scout, tremble, converge, disperse)
            priority: Task priority (low, medium, high, critical)
            max_tokens: Maximum token budget for the task
            subtasks: Optional list of subtasks (auto-generated if not provided)
        
        Returns:
            Task delegation result with ID and swarm assignment details
        """
        return await delegate_task_impl(
            task_description, task_type, priority, max_tokens, subtasks
        )
    
    @mcp.tool()
    async def get_task_status(task_id: str) -> Dict:
        """
        Get the current status of a delegated task.
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            Current task status and assigned bee information
        """
        task = delegator.get_task_status(task_id)
        if not task:
            return {"error": f"Task {task_id} not found"}
        
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "dance_type": task.dance_type.value,
            "assigned_bees": len(task.assigned_bees),
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "token_savings": task.calculate_token_savings()
        }
    
    @mcp.resource("swarm://status")
    async def get_swarm_status() -> Dict:
        """Get overall swarm status and statistics."""
        return delegator.get_swarm_statistics()
    
    @mcp.resource("swarm://tasks")
    async def list_tasks() -> list[Dict]:
        """List all tasks in the swarm."""
        tasks = []
        for task in delegator.tasks.values():
            tasks.append({
                "task_id": task.task_id,
                "description": task.description[:100] + "..." if len(task.description) > 100 else task.description,
                "status": task.status.value,
                "dance_type": task.dance_type.value,
                "priority": task.priority.value,
                "bee_count": len(task.assigned_bees)
            })
        return tasks
    
    @mcp.prompt()
    def analyze_task_for_delegation(task_description: str) -> str:
        """
        Analyze a task to determine the best delegation strategy.
        
        This prompt helps determine which bee dance type would be most
        appropriate for the given task.
        """
        return f"""Analyze the following task and suggest the best bee dance type for delegation:

Task: {task_description}

Consider these dance types and their purposes:
- WAGGLE: Complex tasks requiring decomposition (70%+ token savings)
- ROUND: Simple notifications or updates (10-20% token savings)  
- SCOUT: Research and exploration tasks (50% token savings)
- TREMBLE: Error handling and debugging (30% token savings)
- CONVERGE: Consensus building among agents (60% token savings)
- DISPERSE: Parallel independent tasks (75% token savings)

Analyze the task for:
1. Complexity level
2. Need for decomposition
3. Parallelization potential
4. Type of cognitive work required

Suggest the optimal dance type and explain why."""


# Standalone functions for testing without MCP
async def test_server():
    """Test the server functionality without MCP."""
    logger.info("Testing SwarmRouter server...")
    
    # Test task delegation
    result = await delegate_task_impl(
        task_description="Build a user authentication system with JWT tokens",
        task_type="waggle",
        priority="high",
        max_tokens=15000
    )
    
    logger.info(f"Delegation result: {result}")
    
    # Get status
    if "task_id" in result:
        task = delegator.get_task_status(result["task_id"])
        logger.info(f"Task status: {task.status.value}")
        logger.info(f"Assigned bees: {len(task.assigned_bees)}")
        for i, bee in enumerate(task.assigned_bees):
            logger.info(f"  Bee {i+1}: {bee.bee_id} - {bee.assigned_task}")
    
    # Get swarm stats
    stats = delegator.get_swarm_statistics()
    logger.info(f"Swarm statistics: {stats}")


if __name__ == "__main__":
    if not mcp:
        # Run test mode if MCP not available
        import asyncio
        asyncio.run(test_server())
    else:
        logger.info("SwarmRouter MCP server ready. Use 'mcp run server.py' to start.")