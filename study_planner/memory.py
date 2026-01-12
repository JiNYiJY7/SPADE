from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .models import Task, TimeSlot, Plan


@dataclass
class AgentMemory:
    """
    Centralized state container for the intelligent planning agent.

    This class exists to:
    - Store all mutable agent state in one place
    - Enable clean separation between decision-making logic and data storage
    - Provide a shared memory that different agent behaviours can read from
      and write to without tight coupling

    Using a dataclass simplifies initialization, improves readability,
    and enforces a clear schema for agent state.
    """

    # Tasks are stored in a dictionary keyed by task ID to allow:
    # - Fast lookup and updates
    # - Clear task identity across the system
    # - Safe modification during rescheduling and progress tracking
    tasks: Dict[str, Task] = field(default_factory=dict)

    # Free time slots represent when the agent is allowed to schedule work.
    # A list is used to preserve chronological ordering and allow iteration.
    free_slots: List[TimeSlot] = field(default_factory=list)

    # The current execution plan is stored explicitly so that:
    # - It can be reused without recomputation
    # - Other components (UI, reminders, logs) can access it consistently
    plan: Optional[Plan] = None

    # History keeps a chronological log of agent decisions and actions.
    # This supports transparency, debugging, and academic evaluation.
    history: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        """
        Record a human-readable message describing an agent action or decision.

        This method exists to:
        - Provide traceability of the agent's internal reasoning
        - Support debugging and validation of agent behaviour
        - Enable explainabilit
