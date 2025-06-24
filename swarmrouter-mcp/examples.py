#!/usr/bin/env python3
"""
Example usage of the Minimal SwarmRouter MCP Server.

This demonstrates how to use the SwarmRouter programmatically
to delegate tasks and route them to appropriate AI models.
"""

import asyncio
import os
from minimal_mcp_server import MinimalSwarmRouter, MCPServer


async def basic_usage_example():
    """Basic usage example showing task delegation."""
    print("🐝 Basic SwarmRouter Usage Example")
    print("=" * 40)
    
    # Create a router instance
    router = MinimalSwarmRouter()
    
    # Example tasks of varying complexity
    tasks = [
        "Create a simple hello world function",
        "Design a scalable microservices architecture for e-commerce",
        "Find the best Python web frameworks for 2024"
    ]
    
    for task_desc in tasks:
        print(f"\nTask: {task_desc}")
        print("-" * 40)
        
        # Delegate the task
        task = await router.delegate_task(task_desc, max_tokens=5000)
        
        print(f"✅ Task ID: {task.task_id}")
        print(f"🎭 Dance Type: {task.dance_type.value}")
        print(f"🧠 Complexity: {task.complexity.value}")
        print(f"🐝 Bees: {len(task.bees)}")
        print(f"💰 Token Savings: {task.calculate_token_savings():.1f}%")
        
        # Show bee assignments
        for bee in task.bees:
            print(f"  • {bee.bee_id}: {bee.assigned_task[:50]}...")


async def mcp_server_example():
    """Example showing MCP server usage."""
    print("\n🛠️ MCP Server Example")
    print("=" * 40)
    
    server = MCPServer()
    
    # Simulate MCP requests
    requests = [
        {
            "id": 1,
            "method": "delegate_task",
            "params": {
                "description": "Debug authentication timeout issues",
                "max_tokens": 3000
            }
        },
        {
            "id": 2, 
            "method": "get_swarm_stats",
            "params": {}
        }
    ]
    
    for request in requests:
        print(f"\nRequest: {request['method']}")
        response = await server.process_request(request)
        
        if "result" in response:
            result = response["result"]
            if "task_id" in result:
                print(f"✅ Created task: {result['task_id']}")
                print(f"🎭 Dance: {result['dance_type']}")
                print(f"🐝 Bees: {result['bee_count']}")
            elif "total_tasks" in result:
                print(f"📊 Stats: {result['total_tasks']} tasks, {result['total_bees']} bees")
        else:
            print(f"❌ Error: {response.get('error', 'Unknown error')}")


async def anthropic_integration_example():
    """Example showing real Anthropic API integration if available."""
    print("\n🤖 Anthropic Integration Example")
    print("=" * 40)
    
    # Check if API key is available
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("ℹ️ No ANTHROPIC_API_KEY found - using simulated responses")
        print("   To test real API integration:")
        print("   1. Get an API key from https://console.anthropic.com/")
        print("   2. Set ANTHROPIC_API_KEY environment variable")
        print("   3. Re-run this example")
        return
    
    print("🚀 Using real Anthropic API for task execution")
    
    router = MinimalSwarmRouter()
    
    # Simple task that should work well with the API
    task = await router.delegate_task(
        "Explain the bee waggle dance in 2-3 sentences",
        max_tokens=1000
    )
    
    print(f"✅ Task completed: {task.task_id}")
    print(f"🎭 Dance type: {task.dance_type.value}")
    
    for bee in task.bees:
        if bee.result:
            print(f"\n🐝 {bee.bee_id} result:")
            print(f"   {bee.result}")
            print(f"   Tokens used: {bee.actual_tokens}")


async def main():
    """Run all examples."""
    print("🐝 SwarmRouter Minimal MVP - Usage Examples")
    print("=" * 50)
    
    await basic_usage_example()
    await mcp_server_example()
    await anthropic_integration_example()
    
    print("\n✨ Examples completed!")
    print("\nTry running the full demo with:")
    print("python minimal_mcp_server.py --demo")


if __name__ == "__main__":
    asyncio.run(main())