from __future__ import annotations
from typing import List, Dict, Any
from ..memory import AgentMemory
from ..models import Task, TimeSlot
from ..utils.time_utils import parse_iso


def add_tasks(
    memory: AgentMemory,
    task_payloads: List[Dict[str, Any]]
) -> None:
    """
    Load external task data into the agent's internal memory structure.

    This function exists to:
    - Convert raw task data (e.g. from UI, API, or file input)
      into strongly-typed Task objects
    - Apply default values where optional fields are missing
    - Centralize task initialization logic to avoid duplication
    """

    for task_payload in task_payloads:
        # Estimated duration represents the original expected effort.
        # It is required for scheduling and workload estimation.
        estimated_minutes = int(task_payload["est_minutes"])

        # Remaining time may not be provided initially.
        # Defaulting to estimated time ensures new tasks start unworked.
        remaining_minutes = int(
            task_payload.get("remaining_minutes", estimated_minutes)
        )

        # Create a Task domain object to enforce consistency,
        # validation, and clear ownership of task-related data
        task = Task(
            id=str(task_payload["id"]),
            title=str(task_payload["title"]),
            due=parse_iso(task_payload["due"]),
            est_minutes=estimated_minutes,
            remaining_minutes=remaining_minutes,
            importance=int(task_payload.get("importance", 3)),
            subject=task_payload.get("subject"),
        )

        # Store tasks by ID to allow fast lookup, updates,
        # and dependency handling in later stages
        memory.tasks[task.id] = task

    # Logging provides transparency for debugging and auditing
    memory.log(f"Loaded tasks: {len(task_payloads)}")


def set_free_slots(
    memory: AgentMemory,
    slot_payloads: List[Dict[str, Any]]
) -> None:
    """
    Define the user's available time slots for scheduling.

    This function exists to:
    - Translate raw time-slot input into TimeSlot objects
    - Ensure all scheduling operates on a consistent time format
    - Replace existing slots atomically to avoid partial updates
    """

    # Convert each raw slot into a TimeSlot object.
    # Using a list comprehension ensures a clean overwrite
    # rather than incremental mutation.
    memory.free_slots = [
        TimeSlot(
            start=parse_iso(slot_payload["start"]),
            end=parse_iso(slot_payload["end"])
        )
        for slot_payload in slot_payloads
    ]

    # Logging helps confirm that availability was successfully updated
    memory.log(f"Loaded free slots: {len(slot_payloads)}")


def mark_progress(
    memory: AgentMemory,
    task_id: str,
    minutes_completed: int
) -> None:
    """
    Update progress on a task by reducing its remaining workload.

    This function exists to:
    - Safely track user progress over time
    - Prevent remaining time from becoming negative
    - Keep task state consistent for future scheduling decisions
    """

    # Validate task existence early to fail fast and
    # avoid silent state corruption
    if task_id not in memory.tasks:
        raise KeyError(f"Task not found: {task_id}")

    task = memory.tasks[task_id]

    # Reduce remaining workload while ensuring it never drops below zero.
    # This prevents invalid states that could break scheduling logic.
    task.remaining_minutes = max(
        0,
        task.remaining_minutes - int(minutes_completed)
    )

    # Reassign task to memory to make the update explicit
    memory.tasks[task_id] = task

    # Logging supports traceability of user actions
    memory.log(
        f"Progress updated: {task_id} -{minutes_completed} min"
    )
