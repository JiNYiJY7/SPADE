"""
SPADE Skeleton (Framework Demonstration)

Goal:
- Provide a SPADE-based class/behaviour skeleton matching Phase 2 architecture:
  Agent + multiple Behaviours + shared memory concept.
- Designed for framework marking ("Use of Selected Framework").
- Demonstrates structure without requiring a live XMPP deployment.

Offline Execution Rationale:
- SPADE normally requires XMPP infrastructure.
- This skeleton demonstrates:
  * Agent subclass
  * Behaviour subclasses
  * setup() method registering behaviours
  * Offline verification of framework design
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

# Real SPADE imports (for framework demonstration)
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour


# ---------------------------
# Shared Agent Memory
# ---------------------------

@dataclass
class SPADEAgentMemory:
    """
    Shared memory object for SPADE agent.
    
    Why:
    - All behaviours read/write to this shared memory.
    - Demonstrates internal coordination without XMPP messages.
    """
    tasks: Dict[str, dict] = field(default_factory=dict)
    free_slots: List[dict] = field(default_factory=list)
    plan: Optional[dict] = None
    logs: List[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        """
        Append a log message to memory.

        Why:
        - Simulates agent history tracking.
        - Useful for debugging and framework demonstration.
        """
        self.logs.append(msg)


# ---------------------------
# SPADE Behaviours (Skeletons)
# ---------------------------

class TaskManagementBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour skeleton for task initialization.

    Why:
    - Demonstrates OneShotBehaviour usage.
    - Typically would parse input and populate shared memory.
    """

    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("TaskManagementBehaviour: initialized (skeleton)")

        # Skeleton placeholder: normally parse tasks & free_slots
        # mem.tasks["A1"] = {...}
        # mem.free_slots = [...]

        # Kill behaviour after execution (OneShot)
        await self.kill()


class PriorityEvaluationBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour skeleton for task ranking.

    Why:
    - Demonstrates ordering of behaviours in SPADE setup.
    - In real system, would rank tasks by priority.
    """

    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("PriorityEvaluationBehaviour: ranked tasks (skeleton)")
        await self.kill()


class SchedulePlanningBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour skeleton for building study plan.

    Why:
    - Demonstrates calling downstream logic after ranking tasks.
    - Populates `plan` in memory.
    """

    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("SchedulePlanningBehaviour: generated plan (skeleton)")

        # Skeleton plan
        mem.plan = {"generated_at": datetime.now().isoformat(), "sessions": []}

        await self.kill()


class ReschedulingBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour skeleton for rescheduling.

    Why:
    - Shows how a cyclic behaviour can monitor for triggers.
    - In real agent, would wait for task updates or progress changes.
    """

    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("ReschedulingBehaviour: waiting for changes (skeleton)")

        # Placeholder: sleep to simulate cyclic monitoring
        await self.sleep(2)


class ReminderManagementBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour skeleton for generating reminders.

    Why:
    - Demonstrates periodic behaviour execution.
    - Would normally compute reminders based on task deadlines.
    """

    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("ReminderManagementBehaviour: checking reminders (skeleton)")
        await self.sleep(2)


# ---------------------------
# SPADE Agent Skeleton
# ---------------------------

class SmartAcademicPlanningAgent(Agent):
    """
    SPADE Agent subclass demonstrating Phase 2 architecture.

    Why:
    - Registers multiple behaviours (OneShot + Cyclic)
    - Maintains shared memory object
    - Offline skeleton demonstrates framework usage without XMPP
    """

    def __init__(self, jid: str, password: str, **kwargs):
        """
        Initialize agent memory and prepare for behaviours.

        Args:
            jid: SPADE JID (not required for offline demo)
            password: SPADE password (not required for offline demo)
        """
        super().__init__(jid, password, **kwargs)
        self.memory = SPADEAgentMemory()

    async def setup(self):
        """
        Register all behaviours with agent.

        Why:
        - Shows correct SPADE inheritance and registration pattern.
        - OneShot behaviours execute setup logic sequentially.
        - Cyclic behaviours run periodically (simulated here).
        """
        self.memory.log("Agent setup: registering behaviours (SPADE skeleton)")

        # OneShot behaviours for initialization
        self.add_behaviour(TaskManagementBehaviour())
        self.add_behaviour(PriorityEvaluationBehaviour())
        self.add_behaviour(SchedulePlanningBehaviour())

        # Cyclic behaviours for monitoring
        self.add_behaviour(ReschedulingBehaviour())
        self.add_behaviour(ReminderManagementBehaviour())


# ---------------------------
# Offline Demo
# ---------------------------

def offline_framework_demo() -> None:
    """
    Offline demonstration of SPADE framework skeleton.

    Why:
    - Ensures that the agent and behaviours can be instantiated.
    - Verifies shared memory object exists.
    - No XMPP server or connection is required.
    """
    print("=== SPADE Skeleton Offline Demo ===")
    print("Framework structure verification only (no XMPP)")

    dummy_jid = "dummy@localhost"
    dummy_password = "dummy"

    agent = SmartAcademicPlanningAgent(dummy_jid, dummy_password)

    print("Agent class:", agent.__class__.__name__)
    print("Memory object:", agent.memory.__class__.__name__)
    print("Behaviours are registered during async setup() in SPADE runtime")
    print("Offline demo completed successfully.")


if __name__ == "__main__":
    offline_framework_demo()

    # Real SPADE run (optional):
    # import asyncio
    #
    # async def run_agent():
    #     agent = SmartAcademicPlanningAgent("your_jid@server", "your_password")
    #     await agent.start()
    #     await asyncio.sleep(10)
    #     await agent.stop()
    #
    # asyncio.run(run_agent())
