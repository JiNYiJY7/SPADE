from __future__ import annotations
from typing import List, Dict, Any
from ..memory import AgentMemory
from ..models import Task, TimeSlot
from ..utils.time_utils import parse_iso


def add_tasks(memory: AgentMemory, tasks: List[Dict[str, Any]]) -> None:
    for task_data in tasks:
        estimated_minutes = int(task_data["est_minutes"])
        remaining_minutes = int(task_data.get("remaining_minutes", estimated_minutes))

        task = Task(
            id=str(task_data["id"]),
            title=str(task_data["title"]),
            due=parse_iso(task_data["due"]),
            est_minutes=estimated_minutes,
            remaining_minutes=remaining_minutes,
            importance=int(task_data.get("importance", 3)),
            subject=task_data.get("subject"),
        )
        memory.tasks[task.id] = task
    memory.log(f"Loaded tasks: {len(tasks)}")


def set_free_slots(memory: AgentMemory, slots: List[Dict[str, Any]]) -> None:
    memory.free_slots = [
        TimeSlot(start=parse_iso(slot_data["start"]), end=parse_iso(slot_data["end"])) for slot_data in slots
    ]
    memory.log(f"Loaded free slots: {len(slots)}")


def mark_progress(memory: AgentMemory, task_id: str, minutes_done: int) -> None:
    if task_id not in memory.tasks:
        raise KeyError(f"Task not found: {task_id}")

    task = memory.tasks[task_id]
    task.remaining_minutes = max(0, task.remaining_minutes - int(minutes_done))
    memory.tasks[task_id] = task
    memory.log(f"Progress updated: {task_id} -{minutes_done} min")
