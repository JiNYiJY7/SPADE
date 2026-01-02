from __future__ import annotations
from datetime import datetime
from ..memory import AgentMemory
from ..behaviours.priority_evaluation import rank_tasks
from ..behaviours.schedule_planning import build_plan


def reschedule(memory: AgentMemory, now: datetime):
    tasks_sorted = rank_tasks(memory, now)
    plan = build_plan(memory, tasks_sorted, now)
    memory.log("Rescheduling completed")
    return plan
