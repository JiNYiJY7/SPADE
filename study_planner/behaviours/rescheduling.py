from __future__ import annotations
from datetime import datetime
from ..memory import AgentMemory
from ..behaviours.priority_evaluation import rank_tasks
from ..behaviours.schedule_planning import build_plan


def reschedule_plan(memory: AgentMemory, current_time: datetime):
    """
    Recompute the user's schedule based on updated task priorities and time context.

    This function exists to handle dynamic changes in the system such as:
    - Tasks being added, removed, or updated
    - Progress being made on existing tasks
    - Time passing, which affects task urgency

    Instead of modifying the schedule incrementally, the system recalculates
    the entire plan to ensure global optimality and consistency.
    """

    # Rank tasks first so that scheduling decisions are made
    # using the most up-to-date urgency and importance information
    prioritized_tasks = rank_tasks(memory, current_time)

    # Build a new schedule using the prioritized tasks and
    # the user's available free time slots
    new_plan = build_plan(memory, prioritized_tasks, current_time)

    # Log rescheduling activity for traceability and debugging
    memory.log("Rescheduling completed")

    # Return the newly generated plan so it can be displayed or executed
    return new_plan
