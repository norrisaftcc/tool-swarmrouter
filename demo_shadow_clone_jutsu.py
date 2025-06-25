#!/usr/bin/env python3
"""
Shadow Clone Jutsu Server Demonstration Script

This script demonstrates the key features of the Shadow Clone Jutsu MCP server
by running through various scenarios and showing the API responses.

Run this script to see the Shadow Clone Jutsu technique in action!
"""

import asyncio
import json
from datetime import datetime
from src.models import CloneType, TaskPriority, TaskRequest
from src.server import shadow_system, app


async def demonstrate_shadow_clone_jutsu():
    """Demonstrate the Shadow Clone Jutsu server capabilities."""
    
    print("🥷" + "="*60 + "🥷")
    print("    SHADOW CLONE JUTSU MCP SERVER DEMONSTRATION")
    print("🥷" + "="*60 + "🥷")
    print()
    
    # 1. Show initial system status
    print("1️⃣  INITIAL DOJO STATUS")
    print("-" * 40)
    status = shadow_system.get_system_status()
    print(f"Total Clones: {status.total_clones}")
    print(f"Available Clones: {status.available_clones}")
    print(f"Active Tasks: {status.active_tasks}")
    print(f"System Uptime: {status.system_uptime}")
    print()
    
    # 2. Show available clones
    print("2️⃣  ACTIVE SHADOW CLONES")
    print("-" * 40)
    for clone in shadow_system.clones.values():
        print(f"🔸 {clone.name} ({clone.clone_type.value})")
        print(f"   Rank: {clone.get_rank()}")
        print(f"   Chakra: {clone.chakra_level}/100")
        print(f"   Specialties: {', '.join(clone.specialties)}")
        print(f"   Available: {'✅' if clone.is_available() else '❌'}")
        print()
    
    # 3. Create some sample tasks
    print("3️⃣  CREATING SHADOW CLONE MISSIONS")
    print("-" * 40)
    
    sample_tasks = [
        {
            "title": "Build User Authentication API",
            "description": "Create a JWT-based authentication system with registration, login, and password reset functionality",
            "priority": TaskPriority.A_RANK,
            "estimated_duration": 120,
            "tags": ["authentication", "jwt", "api", "security"]
        },
        {
            "title": "Implement Database Models",
            "description": "Design and implement SQLAlchemy models for user management system",
            "priority": TaskPriority.B_RANK,
            "estimated_duration": 60,
            "tags": ["database", "sqlalchemy", "models"]
        },
        {
            "title": "Create Unit Tests",
            "description": "Write comprehensive unit tests for the authentication system",
            "priority": TaskPriority.B_RANK,
            "estimated_duration": 90,
            "tags": ["testing", "pytest", "unit-tests"]
        }
    ]
    
    created_tasks = []
    for task_data in sample_tasks:
        # Create task request
        task_request = TaskRequest(**task_data)
        
        print(f"📝 Creating mission: {task_request.title}")
        print(f"   Priority: {task_request.priority.value}")
        print(f"   Estimated duration: {task_request.estimated_duration} minutes")
        
        # Create task using the server logic
        from src.server import Task
        task = Task(
            title=task_request.title,
            description=task_request.description,
            priority=task_request.priority,
            estimated_duration=task_request.estimated_duration,
            tags=task_request.tags
        )
        
        # Assign available clone
        available_clones = shadow_system.get_available_clones()
        if available_clones:
            clone_to_assign = available_clones[0]
            task.assign_clone(clone_to_assign)
            task.start_work()
            shadow_system.tasks[task.task_id] = task
            created_tasks.append(task)
            
            print(f"   ✅ Assigned to: {clone_to_assign.name}")
            print(f"   🆔 Task ID: {task.task_id}")
        else:
            print("   ❌ No available clones!")
        print()
    
    # 4. Show updated system status
    print("4️⃣  UPDATED DOJO STATUS")
    print("-" * 40)
    status = shadow_system.get_system_status()
    print(f"Total Clones: {status.total_clones}")
    print(f"Available Clones: {status.available_clones}")
    print(f"Active Tasks: {status.active_tasks}")
    print(f"Total Experience: {status.total_experience}")
    print()
    
    # 5. Show task details
    print("5️⃣  ACTIVE MISSIONS")
    print("-" * 40)
    for task in created_tasks:
        print(f"🎯 {task.title}")
        print(f"   Status: {task.status.value}")
        print(f"   Priority: {task.priority.value}")
        print(f"   Assigned clones: {len(task.assigned_clones)}")
        for clone in task.assigned_clones:
            print(f"     - {clone.name} ({clone.clone_type.value})")
        print()
    
    # 6. Complete a task to show experience gain
    if created_tasks:
        print("6️⃣  COMPLETING A MISSION")
        print("-" * 40)
        task_to_complete = created_tasks[0]
        print(f"📋 Completing: {task_to_complete.title}")
        
        # Complete the task
        result = "Authentication API successfully implemented with JWT tokens, user registration, login endpoints, and secure password hashing."
        task_to_complete.complete_task(result)
        
        print(f"   ✅ Status: {task_to_complete.status.value}")
        print(f"   📊 Result: {task_to_complete.result[:80]}...")
        print(f"   ⏱️  Duration: {task_to_complete.get_duration()} minutes")
        
        # Show clone experience gain
        for clone in task_to_complete.assigned_clones:
            print(f"   🎖️  {clone.name} gained experience!")
            print(f"       Experience: {clone.experience_points} points")
            print(f"       Rank: {clone.get_rank()}")
        print()
    
    # 7. Final status
    print("7️⃣  FINAL DOJO STATUS")
    print("-" * 40)
    status = shadow_system.get_system_status()
    print(f"Total Clones: {status.total_clones}")
    print(f"Available Clones: {status.available_clones}")
    print(f"Active Tasks: {status.active_tasks}")
    print(f"Completed Tasks: {status.completed_tasks}")
    print(f"Total Experience: {status.total_experience}")
    print()
    
    print("🥷" + "="*60 + "🥷")
    print("  SHADOW CLONE JUTSU DEMONSTRATION COMPLETE!")
    print("  The ninja dojo is ready for real missions! 🎯")
    print("🥷" + "="*60 + "🥷")


if __name__ == "__main__":
    print("Starting Shadow Clone Jutsu Demonstration...")
    print("This shows the core functionality without starting the web server.\n")
    
    asyncio.run(demonstrate_shadow_clone_jutsu())
    
    print("\n🚀 To start the full web server, run:")
    print("   python3 -m src.server")
    print("\n📚 Then visit http://localhost:8000/docs for the full API documentation!")