"""Task delegation logic for SwarmRouter MCP server."""

import logging
from typing import Dict, List, Optional
from .models import DanceType, SwarmTask, BeeMetadata, TaskDelegationRequest, TaskStatus

logger = logging.getLogger(__name__)


class TaskDelegator:
    """
    Handles task delegation to the bee swarm.

    This class determines the optimal dance type for tasks and assigns
    appropriate bees to handle the work.
    """

    def __init__(self):
        self.tasks: Dict[str, SwarmTask] = {}
        self.dance_keywords = {
            DanceType.WAGGLE: [
                "complex",
                "decompose",
                "analyze",
                "multi-step",
                "elaborate",
                "comprehensive",
                "detailed",
                "break down",
                "architect",
            ],
            DanceType.ROUND: [
                "simple",
                "notify",
                "alert",
                "inform",
                "quick",
                "brief",
                "announcement",
                "update",
                "status",
            ],
            DanceType.SCOUT: [
                "research",
                "explore",
                "find",
                "discover",
                "investigate",
                "search",
                "locate",
                "identify",
                "survey",
            ],
            DanceType.TREMBLE: [
                "error",
                "issue",
                "problem",
                "fix",
                "debug",
                "troubleshoot",
                "resolve",
                "broken",
                "failed",
            ],
            DanceType.CONVERGE: [
                "consensus",
                "agree",
                "decide",
                "vote",
                "collaborate",
                "merge",
                "combine",
                "unify",
                "coordinate",
            ],
            DanceType.DISPERSE: [
                "parallel",
                "distribute",
                "split",
                "concurrent",
                "multiple",
                "simultaneous",
                "spread",
                "divide",
                "batch",
            ],
        }

    def determine_dance_type(self, task_description: str) -> DanceType:
        """
        Determine the optimal dance type based on task description.

        Uses keyword matching to identify the most appropriate coordination
        pattern for the given task.
        """
        task_lower = task_description.lower()

        # Count keyword matches for each dance type
        scores = {}
        for dance, keywords in self.dance_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            scores[dance] = score

        # Return dance with highest score, defaulting to WAGGLE for complex tasks
        best_dance = max(scores, key=scores.get)
        if scores[best_dance] == 0:
            logger.info("No keywords matched, defaulting to WAGGLE dance")
            return DanceType.WAGGLE

        logger.info(f"Selected {best_dance} dance based on task description")
        return best_dance

    def estimate_tokens_per_bee(
        self, total_tokens: int, num_subtasks: int, dance_type: DanceType
    ) -> int:
        """
        Estimate token allocation per bee based on dance type.

        Different dances have different efficiency patterns.
        """
        base_allocation = total_tokens // max(num_subtasks, 1)

        # Apply dance-specific efficiency multipliers
        efficiency_multipliers = {
            DanceType.WAGGLE: 0.3,  # 70% savings - complex decomposition
            DanceType.ROUND: 0.9,  # 10% savings - simple tasks
            DanceType.SCOUT: 0.5,  # 50% savings - focused research
            DanceType.TREMBLE: 0.7,  # 30% savings - error handling
            DanceType.CONVERGE: 0.4,  # 60% savings - shared consensus
            DanceType.DISPERSE: 0.25,  # 75% savings - parallel efficiency
        }

        multiplier = efficiency_multipliers.get(dance_type, 0.5)
        return int(base_allocation * multiplier)

    def create_bees_for_task(
        self, task: SwarmTask, subtasks: Optional[List[str]] = None
    ) -> List[BeeMetadata]:
        """
        Create bee metadata for task execution.

        Each bee represents an AI agent that will handle part of the task.
        """
        if not subtasks:
            # Generate default subtasks based on dance type
            subtasks = self.generate_default_subtasks(task.description, task.dance_type)

        bees = []
        tokens_per_bee = self.estimate_tokens_per_bee(
            task.max_tokens, len(subtasks), task.dance_type
        )

        for i, subtask in enumerate(subtasks):
            bee = BeeMetadata(
                dance_type=task.dance_type,
                assigned_task=subtask,
                estimated_tokens=tokens_per_bee,
                specialty=self.get_bee_specialty(task.dance_type),
            )
            bees.append(bee)
            logger.debug(f"Created {bee.bee_id} for subtask: {subtask}")

        return bees

    def generate_default_subtasks(
        self, description: str, dance_type: DanceType
    ) -> List[str]:
        """
        Generate default subtasks based on dance type.

        This is a simplified version - in production, you might use
        an AI model to decompose tasks.
        """
        subtask_templates = {
            DanceType.WAGGLE: [
                f"Analyze requirements for: {description}",
                "Design solution architecture",
                "Implement core functionality",
                "Create tests and documentation",
            ],
            DanceType.ROUND: [f"Execute: {description}"],
            DanceType.SCOUT: [
                f"Research existing solutions for: {description}",
                "Identify best practices",
                "Compile findings report",
            ],
            DanceType.TREMBLE: [
                f"Identify root cause of: {description}",
                "Develop fix or workaround",
                "Test and validate solution",
            ],
            DanceType.CONVERGE: [
                f"Gather perspectives on: {description}",
                "Synthesize different viewpoints",
                "Build consensus recommendation",
            ],
            DanceType.DISPERSE: [
                f"Parallel task 1: {description}",
                f"Parallel task 2: {description}",
                f"Parallel task 3: {description}",
            ],
        }

        return subtask_templates.get(dance_type, [f"Execute: {description}"])

    def get_bee_specialty(self, dance_type: DanceType) -> str:
        """Map dance types to bee specialties."""
        specialty_map = {
            DanceType.WAGGLE: "architect",
            DanceType.ROUND: "messenger",
            DanceType.SCOUT: "explorer",
            DanceType.TREMBLE: "debugger",
            DanceType.CONVERGE: "facilitator",
            DanceType.DISPERSE: "coordinator",
        }
        return specialty_map.get(dance_type, "generalist")

    def delegate_task(self, request: TaskDelegationRequest) -> SwarmTask:
        """
        Main method to delegate a task to the swarm.

        This creates a task, determines the optimal dance type,
        and assigns appropriate bees.
        """
        # Determine dance type
        dance_type = request.preferred_dance or self.determine_dance_type(
            request.description
        )

        # Create task
        task = SwarmTask(
            description=request.description,
            priority=request.priority,
            dance_type=dance_type,
            max_tokens=request.max_tokens,
        )

        # Create and assign bees
        bees = self.create_bees_for_task(task, request.subtasks)
        for bee in bees:
            task.assign_bee(bee)

        # Store task
        self.tasks[task.task_id] = task

        logger.info(
            f"Delegated task {task.task_id} with {len(bees)} bees "
            f"using {dance_type} dance"
        )

        return task

    def get_task_status(self, task_id: str) -> Optional[SwarmTask]:
        """Get the current status of a task."""
        return self.tasks.get(task_id)

    def get_swarm_statistics(self) -> Dict:
        """Get overall swarm performance statistics."""
        if not self.tasks:
            return {
                "total_tasks": 0,
                "active_tasks": 0,
                "completed_tasks": 0,
                "average_token_savings": 0,
                "total_bees_deployed": 0,
            }

        active_tasks = [
            t
            for t in self.tasks.values()
            if t.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]
        ]
        completed_tasks = [
            t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED
        ]

        avg_savings = 0
        if completed_tasks:
            savings = [t.calculate_token_savings() for t in completed_tasks]
            avg_savings = sum(savings) / len(savings)

        return {
            "total_tasks": len(self.tasks),
            "active_tasks": len(active_tasks),
            "completed_tasks": len(completed_tasks),
            "average_token_savings": round(avg_savings, 2),
            "total_bees_deployed": sum(
                len(t.assigned_bees) for t in self.tasks.values()
            ),
        }
