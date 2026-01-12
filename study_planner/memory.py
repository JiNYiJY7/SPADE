"""
Agent Memory Module

Holds the internal state of the StudyPlannerAgent.
Behaviours read/write to this memory to coordinate tasks, scheduling, and reminders.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .models import Task, Plan

@dataclass
class AgentMemory:
    """
    Shared memory for the StudyPlannerAgent.
    
    Attributes:
        tasks: Dictionary mapping task IDs to Task objects.
        free_slots: List of available TimeSlots for scheduling.
        plan: Optional Plan object representing the current study plan.
        history: List of log messages for tracking agent actions.
    """
    tasks: Dict[str, Task] = field(default_factory=dict)
    free_slots: List = field(default_factory=list)
    plan: Optional[Plan] = None
    history: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        """
        Append a message to the agent's history log.

        Why:
        - Behaviours use this to record actions and decisions.
        - Provides a timeline of operations for debugging or display.
        
        Args:
            message: String describing the action or event.
        """
        self.history.append(message)
