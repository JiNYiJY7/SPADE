from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .models import Task, TimeSlot, Plan


@dataclass
class AgentMemory:
    tasks: Dict[str, Task] = field(default_factory=dict)
    free_slots: List[TimeSlot] = field(default_factory=list)
    plan: Optional[Plan] = None
    history: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.history.append(message)
