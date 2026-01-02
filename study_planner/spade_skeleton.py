"""
SPADE Skeleton (Framework Demonstration)

Goal:
- Provide a real SPADE-based class/inheritance skeleton that matches the Phase 2 architecture:
  Agent + multiple Behaviours + shared memory concept.
- This skeleton is designed for framework marking ("Use of Selected Framework").
- It DOES NOT require a live XMPP deployment for this phase.

How it works without XMPP:
- SPADE normally starts agents via XMPP. In many academic environments, XMPP setup is not required
  (or not available). Therefore, this file focuses on framework structure:
  - Agent subclass
  - Behaviour subclasses
  - setup() method that registers behaviours
  - (Optional) offline demonstration runner that does not call agent.start()

If your lecturer requires a real run:
- You can supply valid JID/password and an XMPP server, then enable the start() lines
  in the __main__ section.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

# Real SPADE imports (framework usage)
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour


# ---------------------------
# Shared Agent Memory (SPADE-style)
# ---------------------------

@dataclass
class SPADEAgentMemory:
    """
    Shared agent memory (internal state).
    Behaviours read/write here to simulate coordination.
    """
    tasks: Dict[str, dict] = field(default_factory=dict)
    free_slots: List[dict] = field(default_factory=list)
    plan: Optional[dict] = None
    logs: List[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        self.logs.append(msg)


# ---------------------------
# Behaviours (SPADE Behaviour subclasses)
# ---------------------------

class TaskManagementBehaviour(OneShotBehaviour):
    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("TaskManagementBehaviour: initialized (skeleton)")

        # Skeleton placeholder: Normally parse user input / JSON and store tasks
        # mem.tasks["A1"] = {...}
        # mem.free_slots = [...]
        # This phase focuses on framework structure, not full deployment.

        # Stop this OneShot behaviour
        await self.kill()


class PriorityEvaluationBehaviour(OneShotBehaviour):
    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("PriorityEvaluationBehaviour: ranked tasks (skeleton)")
        await self.kill()


class SchedulePlanningBehaviour(OneShotBehaviour):
    async def run(self):
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("SchedulePlanningBehaviour: generated plan (skeleton)")
        mem.plan = {"generated_at": datetime.now().isoformat(), "sessions": []}
        await self.kill()


class ReschedulingBehaviour(CyclicBehaviour):
    async def run(self):
        """
        CyclicBehaviour skeleton:
        In a real system, this would wait for updates (new tasks, progress, changed slots)
        and then trigger re-ranking + re-planning.
        """
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("ReschedulingBehaviour: waiting for changes (skeleton)")

        # Skeleton: do nothing, then sleep briefly and continue
        await self.sleep(2)


class ReminderManagementBehaviour(CyclicBehaviour):
    async def run(self):
        """
        CyclicBehaviour skeleton:
        In a real system, this would periodically check deadlines and output reminders.
        """
        mem: SPADEAgentMemory = self.agent.memory  # type: ignore[attr-defined]
        mem.log("ReminderManagementBehaviour: checking reminders (skeleton)")
        await self.sleep(2)


# ---------------------------
# SPADE Agent (real framework subclass)
# ---------------------------

class SmartAcademicPlanningAgent(Agent):
    """
    Real SPADE Agent subclass.
    Registers behaviours in setup() as per Phase 2 architecture.
    """

    def __init__(self, jid: str, password: str, **kwargs):
        super().__init__(jid, password, **kwargs)
        self.memory = SPADEAgentMemory()

    async def setup(self):
        # Register behaviours (Phase 2 mapping)
        self.memory.log("Agent setup: registering behaviours (SPADE skeleton)")

        self.add_behaviour(TaskManagementBehaviour())
        self.add_behaviour(PriorityEvaluationBehaviour())
        self.add_behaviour(SchedulePlanningBehaviour())

        self.add_behaviour(ReschedulingBehaviour())
        self.add_behaviour(ReminderManagementBehaviour())


# ---------------------------
# Offline Demonstration (No XMPP Required)
# ---------------------------

def offline_framework_demo() -> None:
    """
    Offline demo: verifies that classes can be instantiated and that the framework skeleton exists.
    Does NOT start XMPP connection.
    """
    print("=== SPADE Skeleton Offline Demo ===")
    print("This demo validates framework structure only (no XMPP start).")

    dummy_jid = "dummy@localhost"
    dummy_password = "dummy"

    agent = SmartAcademicPlanningAgent(dummy_jid, dummy_password)

    # We do not call agent.start() here (no XMPP). Instead we verify class creation.
    print("Agent class:", agent.__class__.__name__)
    print("Memory object:", agent.memory.__class__.__name__)
    print("Behaviours are registered in async setup() when started with SPADE runtime.")
    print("Offline demo completed successfully.")


if __name__ == "__main__":
    offline_framework_demo()

    # If you have a real XMPP server and credentials, you can enable this:
    #
    # import asyncio
    #
    # async def run_agent():
    #     agent = SmartAcademicPlanningAgent("your_jid@server", "your_password")
    #     await agent.start()
    #     await asyncio.sleep(10)
    #     await agent.stop()
    #
    # asyncio.run(run_agent())
