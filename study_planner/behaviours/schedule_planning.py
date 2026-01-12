from __future__ import annotations
from datetime import datetime
from ..memory import AgentMemory
from ..models import Plan
from ..utils.scheduler import plan_sessions


def build_execution_plan(
    memory: AgentMemory,
    prioritized_tasks,
    current_time: datetime
) -> Plan:
    """
    Construct a structured execution plan by assigning prioritized tasks
    into the user's available free time slots.

    This function exists to translate abstract task priorities into
    a concrete, time-based schedule that the system can execute or display.
    It acts as the bridge between task evaluation (what should be done)
    and scheduling (when it should be done).
    """

    # Generate a schedule by fitting the most important tasks first
    # into available free slots. This ensures urgent tasks are not
    # pushed out by less important ones.
    execution_plan = plan_sessions(
        tasks_sorted=prioritized_tasks,
        free_slots=memory.free_slots,
        current_time=current_time
    )

    # Store the generated plan in memory so that it can be reused
    # by other system components without recomputation
    memory.plan = execution_plan

    # Log the outcome to support debugging, monitoring,
    # and transparency of system decisions
    memory.log(
        f"Generated plan with {len(execution_plan.sessions)} sessions"
    )

    # Return the finalized plan for downstream use
    return execution_plan
