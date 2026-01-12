from __future__ import annotations
from datetime import datetime
from typing import List
from ..memory import AgentMemory
from ..models import Task
from ..utils.scoring import priority_score


def rank_tasks(memory: AgentMemory, current_time: datetime) -> List[Task]:
    """
    Rank tasks based on their priority score.

    The priority score is calculated using task attributes
    (e.g. importance, deadline, remaining time) and the current time.
    Tasks with higher scores are ranked first.
    """

    # Sort tasks stored in memory by priority score (highest first)
    ranked = sorted(
        memory.tasks.values(),
        key=lambda task: priority_score(task, current_time),
        reverse=True,
    )

    # Log ranking activity for tracking and debugging
    memory.log("Ranked tasks by priority score")

    # Return the ranked list of tasks
    return ranked
