from __future__ import annotations
from datetime import datetime
from ..memory import AgentMemory
from ..models import Plan
from ..utils.scheduler import plan_sessions


def build_plan(memory: AgentMemory, tasks_sorted, now: datetime) -> Plan:
    plan = plan_sessions(tasks_sorted=tasks_sorted, free_slots=memory.free_slots, now=now)
    memory.plan = plan
    memory.log(f"Generated plan with {len(plan.sessions)} sessions")
    return plan
