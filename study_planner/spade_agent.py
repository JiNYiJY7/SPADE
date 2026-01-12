"""
SPADE-based Smart Academic Planning Intelligent Agent

Phase 2 implementation using SPADE framework.
Demonstrates correct SPADE Agent and Behaviour usage without XMPP.

Architecture:
- Single StudyPlannerAgent (extends spade.agent.Agent)
- Five specialized behaviours (OneShotBehaviour and CyclicBehaviour)
- Shared internal memory (AgentMemory)
- Local message-based communication (simulated)
"""

from __future__ import annotations
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

# SPADE framework imports (with offline stubs if SPADE not installed)
try:
    from spade.agent import Agent
    from spade.behaviour import OneShotBehaviour, CyclicBehaviour
    SPADE_AVAILABLE = True
except ImportError:
    SPADE_AVAILABLE = False
    class Agent: pass
    class OneShotBehaviour: pass
    class CyclicBehaviour: pass

# Phase 2 logic imports
from .memory import AgentMemory
from .models import Task, TimeSlot, Plan, StudySession
from .behaviours.task_management import add_tasks, set_free_slots, mark_progress
from .behaviours.priority_evaluation import rank_tasks
from .behaviours.schedule_planning import build_plan
from .behaviours.rescheduling import reschedule_plan
from .behaviours.reminder_management import generate_reminders


# ============================================================================
# SPADE BEHAVIOURS
# ============================================================================

class TaskManagementBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour to initialize agent memory with tasks and free slots.

    Runs once at agent startup. Uses existing Phase 2 logic to populate shared memory.
    """

    async def run(self):
        """Load tasks and free slots into shared AgentMemory."""
        memory: AgentMemory = self.agent.memory
        input_data: Dict[str, Any] = self.agent.input_data

        memory.log("[TaskManagementBehaviour] Initializing tasks and free slots")

        # Delegate actual population to Phase 2 module
        add_tasks(memory, input_data.get("tasks", []))
        set_free_slots(memory, input_data.get("free_slots", []))

        memory.log("[TaskManagementBehaviour] Initialization complete")
        print(f"[AGENT] Loaded {len(memory.tasks)} tasks and {len(memory.free_slots)} free slots")


class PriorityEvaluationBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour to rank tasks by priority.

    Runs after TaskManagementBehaviour. Stores ranked tasks in agent state.
    """

    async def run(self):
        """Rank tasks by priority score using existing Phase 2 logic."""
        memory: AgentMemory = self.agent.memory
        current_time: datetime = self.agent.reference_time

        memory.log("[PriorityEvaluationBehaviour] Evaluating task priorities")
        ranked_tasks = rank_tasks(memory, current_time)

        # Store ranked tasks for downstream behaviours
        self.agent.ranked_tasks = ranked_tasks

        memory.log("[PriorityEvaluationBehaviour] Ranking complete")
        print(f"[AGENT] Ranked {len(ranked_tasks)} tasks")
        for index, task in enumerate(ranked_tasks[:3], 1):
            print(f"  {index}. {task.title} (importance={task.importance})")


class SchedulePlanningBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour to build an optimized study plan.

    Runs after PriorityEvaluationBehaviour. Populates agent memory plan.
    """

    async def run(self):
        """Generate optimized study plan."""
        memory: AgentMemory = self.agent.memory
        ranked_tasks = self.agent.ranked_tasks
        current_time: datetime = self.agent.reference_time

        memory.log("[SchedulePlanningBehaviour] Starting schedule planning")
        plan = build_plan(memory, ranked_tasks, current_time)

        memory.log("[SchedulePlanningBehaviour] Planning complete")
        print(f"[AGENT] Generated study plan with {len(plan.sessions)} sessions")
        for session in plan.sessions[:3]:
            print(f"  {session.start.strftime('%H:%M')} - {session.end.strftime('%H:%M')}: {session.title}")


class ReschedulingBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour that monitors progress and triggers rescheduling.

    In Phase 2 demo, rescheduling is triggered manually when task progress updates occur.
    """

    async def run(self):
        """Check for rescheduling trigger and update plan."""
        memory: AgentMemory = self.agent.memory
        current_time: datetime = self.agent.reference_time

        # Only reschedule if flagged
        if getattr(self.agent, 'trigger_reschedule', False):
            memory.log("[ReschedulingBehaviour] Triggering reschedule")
            reschedule(memory, current_time)
            self.agent.trigger_reschedule = False
            memory.log("[ReschedulingBehaviour] Rescheduling complete")
            print(f"[AGENT] Rescheduled study plan")


class ReminderManagementBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour to generate and update task reminders periodically.

    Uses Phase 2 logic to compute active reminders based on current task states.
    """

    async def run(self):
        """Compute reminders and store in agent state."""
        memory: AgentMemory = self.agent.memory
        current_time: datetime = self.agent.reference_time

        ranked_tasks = rank_tasks(memory, current_time)
        reminders = generate_reminders(ranked_tasks, current_time)

        self.agent.current_reminders = reminders
        if reminders:
            memory.log(f"[ReminderManagementBehaviour] Generated {len(reminders)} reminders")
            print(f"\n[REMINDERS] {len(reminders)} active reminders:")
            for reminder in reminders[:5]:
                print(f"  - {reminder}")


# ============================================================================
# SPADE AGENT
# ============================================================================

class StudyPlannerAgent(Agent):
    """
    Smart Academic Planning Intelligent Agent (SPADE-based).

    Behaviour-based design:
    - OneShotBehaviours for initialization (tasks, priorities, schedule)
    - CyclicBehaviours for monitoring (rescheduling, reminders)
    - Shared memory (AgentMemory) enables behaviours coordination

    Offline demo mode: runs without XMPP server.
    """

    def __init__(
        self,
        jid: str = "planner@localhost",
        password: str = "dummy_password",
        input_data: Optional[Dict[str, Any]] = None,
        reference_time: Optional[datetime] = None
    ):
        """
        Initialize agent state and offline demo configuration.
        """
        if SPADE_AVAILABLE:
            super().__init__(jid, password)
        else:
            object.__init__(self)

        # Shared state accessible by all behaviours
        self.memory = AgentMemory()

        # Input for task initialization
        self.input_data = input_data or {}

        # Reference datetime for scheduling and reminders
        self.reference_time = reference_time or datetime.now()

        # Behavioural state
        self.ranked_tasks: List[Task] = []
        self.current_reminders: List[str] = []
        self.trigger_reschedule: bool = False
        self._behaviours: List = []

    def add_behaviour(self, behaviour):
        """Attach behaviour to agent and keep local reference for offline demo."""
        behaviour.agent = self
        self._behaviours.append(behaviour)
        if SPADE_AVAILABLE and hasattr(super(), 'add_behaviour'):
            super().add_behaviour(behaviour)

    async def setup(self):
        """Register and initialize all behaviours in correct execution order."""
        print(f"\n[AGENT] Setting up StudyPlannerAgent")

        # OneShot: setup sequence
        self.add_behaviour(TaskManagementBehaviour())
        self.add_behaviour(PriorityEvaluationBehaviour())
        self.add_behaviour(SchedulePlanningBehaviour())

        # Cyclic: continuous monitoring
        self.add_behaviour(ReschedulingBehaviour())
        self.add_behaviour(ReminderManagementBehaviour())

        print(f"[AGENT] Agent setup complete: {len(self._behaviours)} behaviours registered\n")

    def mark_task_progress(self, task_id: str, minutes_done: int) -> None:
        """
        Public API: record work done on a task and flag rescheduling.

        Why:
        - Demonstrates dynamic plan adjustment
        - Triggers ReschedulingBehaviour
        """
        if task_id not in self.memory.tasks:
            print(f"[AGENT] Error: Task {task_id} not found")
            return

        mark_progress(self.memory, task_id, minutes_done)
        self.trigger_reschedule = True
        print(f"[AGENT] Progress recorded: {task_id} -{minutes_done}min")

    def get_plan(self) -> Optional[Plan]:
        """Return current study plan."""
        return self.memory.plan

    def get_reminders(self) -> List[str]:
        """Return current reminders."""
        return self.current_reminders

    async def stop(self):
        """Clean up SPADE agent resources if available."""
        if SPADE_AVAILABLE and hasattr(super(), 'stop'):
            await super().stop()
