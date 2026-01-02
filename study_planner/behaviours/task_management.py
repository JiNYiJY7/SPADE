from __future__ import annotations
from typing import List, Dict, Any
from ..memory import AgentMemory
from ..models import Task, TimeSlot
from ..utils.time_utils import parse_iso


def add_tasks(memory: AgentMemory, tasks: List[Dict[str, Any]]) -> None:
    for t in tasks:
        est = int(t["est_minutes"])
        remaining = int(t.get("remaining_minutes", est))

        task = Task(
            id=str(t["id"]),
            title=str(t["title"]),
            due=parse_iso(t["due"]),
            est_minutes=est,
            remaining_minutes=remaining,
            importance=int(t.get("importance", 3)),
            subject=t.get("subject"),
        )
        memory.tasks[task.id] = task
    memory.log(f"Loaded tasks: {len(tasks)}")


def set_free_slots(memory: AgentMemory, slots: List[Dict[str, Any]]) -> None:
    memory.free_slots = [
        TimeSlot(start=parse_iso(s["start"]), end=parse_iso(s["end"])) for s in slots
    ]
    memory.log(f"Loaded free slots: {len(slots)}")


def mark_progress(memory: AgentMemory, task_id: str, minutes_done: int) -> None:
    if task_id not in memory.tasks:
        raise KeyError(f"Task not found: {task_id}")

    task = memory.tasks[task_id]
    task.remaining_minutes = max(0, task.remaining_minutes - int(minutes_done))
    memory.tasks[task_id] = task
    memory.log(f"Progress updated: {task_id} -{minutes_done} min")
