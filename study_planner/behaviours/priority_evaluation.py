"""
Task prioritization module.

This module provides functionality to rank tasks based on a computed
priority score. The ranking is used by the scheduling system to decide
which tasks should be planned first when time and resources are limited.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from ..memory import AgentMemory
from ..models import Task
from ..utils.scoring import priority_score


def rank_tasks(memory: AgentMemory, current_time: datetime) -> List[Task]:
    """
    Rank tasks by priority score in descending order.

    This function evaluates all tasks stored in the agent's memory and
    orders them so that the most urgent and important tasks appear first.
    The ranking is time-aware, meaning the current time influences the
    urgency calculation (e.g., approaching deadlines).

    Args:
        memory (AgentMemory):
            The agent's memory containing all tracked tasks.
        current_time (datetime):
            The current time used to compute time-sensitive priority scores.

    Returns:
        List[Task]:
            A list of tasks sorted from highest to lowest priority.
    """

    # Sorting tasks ensures that downstream planning logic can simply
    # iterate from the top of the list, always selecting the most
    # valuable task first without re-evaluating priorities.
    ranked_tasks = sorted(
        memory.tasks.values(),
        key=lambda task: priority_score(task, current_time),
        reverse=True,  # Highest priority first to support greedy scheduling
    )

    # Logging this step improves traceability and debugging, making it
    # easier to verify that task prioritization occurred as expected.
    memory.log("Ranked tasks by priority score")

    return ranked_tasks
