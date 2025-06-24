#!/usr/bin/env python3
"""
Queen Bee Coordination Example

Demonstrates how a Sonnet "queen bee" can coordinate multiple Haiku "worker bees"
for efficient task execution with significant token savings.

This pattern shows:
- Sonnet analyzing and decomposing complex tasks
- Multiple Haiku instances handling simple subtasks in parallel
- Token optimization through intelligent task distribution
"""

import asyncio
import os
from typing import List, Dict
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import json
import time

load_dotenv()

# Initialize Anthropic client
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class QueenBee:
    """Sonnet-powered queen bee that coordinates the swarm."""
    
    def __init__(self):
        self.model = "claude-3-5-sonnet-20241022"
        self.total_tokens_used = 0
    
    async def analyze_and_decompose(self, task: str) -> Dict:
        """Use Sonnet to analyze task complexity and create subtasks."""
        prompt = f"""You are a queen bee coordinating a swarm of worker bees.
        
Analyze this task and decompose it into simple subtasks that can be handled by worker bees:

Task: {task}

Provide a JSON response with:
{{
    "dance_type": "waggle|round|scout|tremble|converge|disperse",
    "complexity_score": 1-10,
    "subtasks": [
        {{"id": 1, "description": "...", "estimated_tokens": 100}},
        ...
    ],
    "coordination_strategy": "parallel|sequential|converge"
}}

Each subtask should be simple enough for a Haiku model to handle efficiently.
Aim for maximum parallelization where possible."""

        response = await client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        self.total_tokens_used += response.usage.input_tokens + response.usage.output_tokens
        
        # Parse JSON from response
        content = response.content[0].text
        try:
            # Find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            return json.loads(json_str)
        except:
            # Fallback if JSON parsing fails
            return {
                "dance_type": "waggle",
                "complexity_score": 5,
                "subtasks": [{"id": 1, "description": task, "estimated_tokens": 500}],
                "coordination_strategy": "parallel"
            }


class WorkerBee:
    """Haiku-powered worker bee for simple tasks."""
    
    def __init__(self, bee_id: str):
        self.bee_id = bee_id
        self.model = "claude-3-haiku-20240307"
        self.tokens_used = 0
    
    async def execute_task(self, subtask: Dict) -> Dict:
        """Execute a simple subtask using Haiku."""
        prompt = f"""You are a worker bee. Complete this simple task concisely:

{subtask['description']}

Provide a brief, direct response."""

        start_time = time.time()
        
        response = await client.messages.create(
            model=self.model,
            max_tokens=subtask.get('estimated_tokens', 200),
            messages=[{"role": "user", "content": prompt}]
        )
        
        execution_time = time.time() - start_time
        self.tokens_used = response.usage.input_tokens + response.usage.output_tokens
        
        return {
            "bee_id": self.bee_id,
            "subtask_id": subtask['id'],
            "result": response.content[0].text,
            "tokens_used": self.tokens_used,
            "execution_time": execution_time
        }


class SwarmCoordinator:
    """Orchestrates the queen bee and worker bees."""
    
    def __init__(self):
        self.queen = QueenBee()
        self.results = []
    
    async def execute_with_swarm(self, task: str) -> Dict:
        """Execute a task using the swarm pattern."""
        print(f"🐝 Queen Bee analyzing task: {task}")
        
        # Queen bee decomposes the task
        decomposition = await self.queen.analyze_and_decompose(task)
        
        print(f"\n👑 Queen Bee Decision:")
        print(f"  Dance Type: {decomposition['dance_type']}")
        print(f"  Complexity: {decomposition['complexity_score']}/10")
        print(f"  Strategy: {decomposition['coordination_strategy']}")
        print(f"  Subtasks: {len(decomposition['subtasks'])}")
        
        # Create worker bees
        worker_bees = [
            WorkerBee(f"bee_{i+1}") 
            for i in range(len(decomposition['subtasks']))
        ]
        
        # Execute based on strategy
        if decomposition['coordination_strategy'] == 'parallel':
            results = await self._execute_parallel(worker_bees, decomposition['subtasks'])
        elif decomposition['coordination_strategy'] == 'sequential':
            results = await self._execute_sequential(worker_bees, decomposition['subtasks'])
        else:  # converge
            results = await self._execute_converge(worker_bees, decomposition['subtasks'])
        
        # Calculate token savings
        total_worker_tokens = sum(r['tokens_used'] for r in results)
        total_tokens = self.queen.total_tokens_used + total_worker_tokens
        
        # Estimate direct approach tokens (usually 3-4x for complex tasks)
        estimated_direct_tokens = total_tokens * 3.5
        savings_percentage = ((estimated_direct_tokens - total_tokens) / estimated_direct_tokens) * 100
        
        return {
            "task": task,
            "decomposition": decomposition,
            "results": results,
            "token_usage": {
                "queen_tokens": self.queen.total_tokens_used,
                "worker_tokens": total_worker_tokens,
                "total_tokens": total_tokens,
                "estimated_direct_tokens": int(estimated_direct_tokens),
                "savings_percentage": round(savings_percentage, 2)
            }
        }
    
    async def _execute_parallel(self, bees: List[WorkerBee], subtasks: List[Dict]) -> List[Dict]:
        """Execute subtasks in parallel."""
        print("\n🔄 Executing subtasks in parallel...")
        
        tasks = [
            bee.execute_task(subtask) 
            for bee, subtask in zip(bees, subtasks)
        ]
        
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f"  ✅ {result['bee_id']} completed (tokens: {result['tokens_used']})")
        
        return results
    
    async def _execute_sequential(self, bees: List[WorkerBee], subtasks: List[Dict]) -> List[Dict]:
        """Execute subtasks sequentially."""
        print("\n📝 Executing subtasks sequentially...")
        
        results = []
        for bee, subtask in zip(bees, subtasks):
            result = await bee.execute_task(subtask)
            results.append(result)
            print(f"  ✅ {result['bee_id']} completed (tokens: {result['tokens_used']})")
        
        return results
    
    async def _execute_converge(self, bees: List[WorkerBee], subtasks: List[Dict]) -> List[Dict]:
        """Execute subtasks and converge results."""
        print("\n🤝 Executing with convergence pattern...")
        
        # First, execute all subtasks in parallel
        initial_results = await self._execute_parallel(bees, subtasks)
        
        # Then use queen bee to synthesize
        synthesis_prompt = f"Synthesize these results into a cohesive response:\n"
        for r in initial_results:
            synthesis_prompt += f"\n{r['result']}\n"
        
        synthesis = await self.queen.analyze_and_decompose(synthesis_prompt)
        
        return initial_results + [{"synthesis": synthesis}]


async def demonstrate_swarm_patterns():
    """Demonstrate different swarm coordination patterns."""
    
    examples = [
        {
            "name": "Complex Development Task",
            "task": "Design and implement a real-time chat application with user authentication, message history, and typing indicators"
        },
        {
            "name": "Research Task",
            "task": "Research the best practices for implementing microservices architecture, including service discovery, load balancing, and fault tolerance"
        },
        {
            "name": "Simple Notification",
            "task": "Send a notification to users about scheduled maintenance"
        }
    ]
    
    coordinator = SwarmCoordinator()
    
    for example in examples:
        print(f"\n{'='*60}")
        print(f"📋 Example: {example['name']}")
        print(f"{'='*60}")
        
        result = await coordinator.execute_with_swarm(example['task'])
        
        print(f"\n📊 Token Usage Summary:")
        print(f"  Queen Bee (Sonnet): {result['token_usage']['queen_tokens']} tokens")
        print(f"  Worker Bees (Haiku): {result['token_usage']['worker_tokens']} tokens")
        print(f"  Total Used: {result['token_usage']['total_tokens']} tokens")
        print(f"  Estimated Direct: {result['token_usage']['estimated_direct_tokens']} tokens")
        print(f"  💰 Savings: {result['token_usage']['savings_percentage']}%")
        
        print(f"\n📝 Results Preview:")
        for i, r in enumerate(result['results'][:3]):  # Show first 3 results
            if 'result' in r:
                preview = r['result'][:100] + "..." if len(r['result']) > 100 else r['result']
                print(f"  {r.get('bee_id', f'Result {i+1}')}: {preview}")
        
        # Brief pause between examples
        await asyncio.sleep(1)


async def test_queen_bee_coordination():
    """Simple test of queen bee coordination."""
    print("🐝 Testing Queen Bee Coordination Pattern\n")
    
    coordinator = SwarmCoordinator()
    
    # Test with a moderately complex task
    task = "Create a Python function that validates email addresses, handles edge cases, and includes unit tests"
    
    result = await coordinator.execute_with_swarm(task)
    
    print(f"\n✨ Task Completed!")
    print(f"Token Savings: {result['token_usage']['savings_percentage']}%")
    print(f"Strategy Used: {result['decomposition']['coordination_strategy']}")


if __name__ == "__main__":
    print("🐝 SwarmRouter - Queen Bee Coordination Example\n")
    print("This example demonstrates how a Sonnet 'queen bee' coordinates")
    print("multiple Haiku 'worker bees' for efficient task execution.\n")
    
    # Run the demonstration
    asyncio.run(demonstrate_swarm_patterns())
    
    # Uncomment for a simple test
    # asyncio.run(test_queen_bee_coordination())