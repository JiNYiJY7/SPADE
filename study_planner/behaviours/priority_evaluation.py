from __future__ import annotations
from datetime import datetime
from typing import List
from ..memory import AgentMemory
from ..models import Task
from ..utils.scoring import priority_score


def rank_tasks(memory: AgentMemory, now: datetime) -> List[Task]:
    ranked = sorted(
        memory.tasks.values(),
        key=lambda t: priority_score(t, now),
        reverse=True,
    )
    memory.log("Ranked tasks by priority score")
    return ranked
