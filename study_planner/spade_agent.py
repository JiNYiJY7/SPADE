"""
SPADE-based Smart Academic Planning Intelligent Agent

This module implements the Phase 2 design using SPADE framework.
It demonstrates correct usage of SPADE Agent and Behaviour classes
without requiring XMPP infrastructure (simulated locally).

Architecture:
- Single StudyPlannerAgent (extends spade.agent.Agent)
- Five specialized behaviours (OneShotBehaviour and CyclicBehaviour)
- Shared internal memory (AgentMemory)
- Local message-based communication (simulated)
"""

from __future__ import annotations
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# SPADE framework imports
try:
    from spade.agent import Agent
    from spade.behaviour import OneShotBehaviour, CyclicBehaviour
    from spade.message import Message
    from spade.template import Template
    SPADE_AVAILABLE = True
except ImportError:
    SPADE_AVAILABLE = False
    # Fallback stubs for development without SPADE installed
    class Agent:
        pass
    class OneShotBehaviour:
        pass
    class CyclicBehaviour:
        pass
    class Message:
        pass
    class Template:
        pass

# Import existing Phase 2 logic
from .memory import AgentMemory
from .models import Task, TimeSlot, Plan, StudySession
from .behaviours.task_management import add_tasks, set_free_slots, mark_progress
from .behaviours.priority_evaluation import rank_tasks
from .behaviours.schedule_planning import build_plan
from .behaviours.rescheduling import reschedule
from .behaviours.reminder_management import generate_reminders
from .utils.time_utils import parse_iso


# ============================================================================
# SPADE BEHAVIOURS - Each maps to Phase 2 behaviour modules
# ============================================================================

class TaskManagementBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour: Initializes agent memory with tasks and free slots.
    
    Calls: study_planner.behaviours.task_management functions
    Runs: Once at agent startup
    """
    
    async def run(self):
        """Load tasks and free slots from input data into shared memory."""
        # Access shared agent memory
        memory: AgentMemory = self.agent.memory
        input_data: Dict[str, Any] = self.agent.input_data
        
        memory.log("[TaskManagementBehaviour] Starting task initialization")
        
        # Delegate to existing Phase 2 logic
        add_tasks(memory, input_data.get("tasks", []))
        set_free_slots(memory, input_data.get("free_slots", []))
        
        memory.log("[TaskManagementBehaviour] Task initialization complete")
        print(f"[AGENT] Loaded {len(memory.tasks)} tasks and {len(memory.free_slots)} free slots")


class PriorityEvaluationBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour: Ranks tasks by priority score.
    
    Calls: study_planner.behaviours.priority_evaluation.rank_tasks
    Runs: After TaskManagementBehaviour
    """
    
    async def run(self):
        """Evaluate and rank tasks by priority."""
        memory: AgentMemory = self.agent.memory
        now: datetime = self.agent.reference_time
        
        memory.log("[PriorityEvaluationBehaviour] Starting priority evaluation")
        
        # Delegate to existing Phase 2 logic
        ranked_tasks = rank_tasks(memory, now)
        
        # Store ranked tasks for next behaviour
        self.agent.ranked_tasks = ranked_tasks
        
        memory.log("[PriorityEvaluationBehaviour] Priority evaluation complete")
        print(f"[AGENT] Ranked {len(ranked_tasks)} tasks by priority")
        for index, task in enumerate(ranked_tasks[:3], 1):
            print(f"  {index}. {task.title} (importance={task.importance})")


class SchedulePlanningBehaviour(OneShotBehaviour):
    """
    OneShotBehaviour: Generates an optimized study plan.
    
    Calls: study_planner.behaviours.schedule_planning.build_plan
    Runs: After PriorityEvaluationBehaviour
    """
    
    async def run(self):
        """Build an optimized study plan."""
        memory: AgentMemory = self.agent.memory
        ranked_tasks = self.agent.ranked_tasks
        now: datetime = self.agent.reference_time
        
        memory.log("[SchedulePlanningBehaviour] Starting schedule planning")
        
        # Delegate to existing Phase 2 logic
        plan = build_plan(memory, ranked_tasks, now)
        
        memory.log("[SchedulePlanningBehaviour] Schedule planning complete")
        print(f"[AGENT] Generated study plan with {len(plan.sessions)} sessions")
        for session in plan.sessions[:3]:
            print(f"  {session.start.strftime('%H:%M')} - {session.end.strftime('%H:%M')}: {session.title}")


class ReschedulingBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour: Monitors for changes and reschedules when needed.
    
    Calls: study_planner.behaviours.rescheduling.reschedule
    Runs: Periodically (can be triggered by progress updates)
    
    Simulated trigger: When progress is marked, reschedule is called.
    """
    
    async def run(self):
        """Check for rescheduling needs periodically."""
        memory: AgentMemory = self.agent.memory
        now: datetime = self.agent.reference_time
        
        # In production, this would check conditions and trigger reschedule
        # For demo, this is called manually when progress updates occur
        if hasattr(self.agent, 'trigger_reschedule') and self.agent.trigger_reschedule:
            memory.log("[ReschedulingBehaviour] Rescheduling triggered")
            
            # Delegate to existing Phase 2 logic
            plan = reschedule(memory, now)
            
            self.agent.trigger_reschedule = False
            memory.log("[ReschedulingBehaviour] Rescheduling complete")
            print(f"[AGENT] Rescheduled: {len(plan.sessions)} sessions updated")


class ReminderManagementBehaviour(CyclicBehaviour):
    """
    CyclicBehaviour: Generates and manages reminders for tasks.
    
    Calls: study_planner.behaviours.reminder_management.generate_reminders
    Runs: Periodically
    
    Simulated: Generates reminders based on current task state.
    """
    
    async def run(self):
        """Generate reminders for all active tasks."""
        memory: AgentMemory = self.agent.memory
        now: datetime = self.agent.reference_time
        
        # Rank tasks and generate reminders
        ranked_tasks = rank_tasks(memory, now)
        reminders = generate_reminders(ranked_tasks, now)
        
        # Store reminders in agent state
        self.agent.current_reminders = reminders
        
        if reminders:
            memory.log(f"[ReminderManagementBehaviour] Generated {len(reminders)} reminders")
            print(f"\n[REMINDERS] {len(reminders)} active reminders:")
            for reminder in reminders[:5]:
                print(f"  - {reminder}")


# ============================================================================
# SPADE AGENT - Main intelligent agent
# ============================================================================

class StudyPlannerAgent(Agent):
    """
    Smart Academic Planning Intelligent Agent (SPADE implementation).
    
    Single autonomous agent using a behaviour-based architecture.
    Manages academic tasks, priorities, scheduling, and reminders.
    
    Shared state:
    - memory: AgentMemory instance (stores tasks, plan, history)
    - ranked_tasks: Current task ranking
    - current_reminders: Active reminders
    
    Behaviours:
    1. TaskManagementBehaviour (OneShot) - Initialize tasks
    2. PriorityEvaluationBehaviour (OneShot) - Rank by priority
    3. SchedulePlanningBehaviour (OneShot) - Generate plan
    4. ReschedulingBehaviour (Cyclic) - Monitor and reschedule
    5. ReminderManagementBehaviour (Cyclic) - Generate reminders
    
    Design rationale:
    - OneShotBehaviour for one-time setup tasks
    - CyclicBehaviour for ongoing monitoring and updates
    - All behaviours access shared memory, enabling coordination
    - No XMPP required; runs locally for Phase 3 demo
    """
    
    def __init__(
        self,
        jid: str = "planner@localhost",
        password: str = "dummy_password",
        input_data: Optional[Dict[str, Any]] = None,
        reference_time: Optional[datetime] = None
    ):
        """
        Initialize the StudyPlannerAgent.
        
        Args:
            jid: SPADE JID (not used in offline mode)
            password: SPADE password (not used in offline mode)
            input_data: Dictionary with 'tasks' and 'free_slots'
            reference_time: Reference datetime for planning (default: now)
        """
        # Initialize parent class if SPADE is available
        if SPADE_AVAILABLE:
            super().__init__(jid, password)
        else:
            # Offline stub: initialize object directly
            object.__init__(self)
        
        # Shared memory: all behaviours access this
        self.memory = AgentMemory()
        
        # Input data for task initialization
        self.input_data = input_data or {}
        
        # Reference time for all scheduling decisions
        self.reference_time = reference_time or datetime.now()
        
        # Behavioural state
        self.ranked_tasks: List[Task] = []
        self.current_reminders: List[str] = []
        self.trigger_reschedule: bool = False
        
        # For offline mode: store behaviours
        self._behaviours: List = []
    
    def add_behaviour(self, behaviour):
        """Register a behaviour with this agent."""
        # Set agent reference on behaviour
        behaviour.agent = self
        self._behaviours.append(behaviour)
        if SPADE_AVAILABLE and hasattr(super(), 'add_behaviour'):
            super().add_behaviour(behaviour)
    
    async def setup(self):
        """
        SPADE lifecycle: Called when agent is started.
        
        Registers behaviours with execution order:
        1. TaskManagementBehaviour (setup phase)
        2. PriorityEvaluationBehaviour (after tasks loaded)
        3. SchedulePlanningBehaviour (after ranking)
        4. ReschedulingBehaviour (monitors continuously)
        5. ReminderManagementBehaviour (monitors continuously)
        """
        print(f"\n[AGENT] Setting up StudyPlannerAgent")
        
        # OneShot behaviours execute in sequence (in order of registration)
        self.add_behaviour(TaskManagementBehaviour())
        self.add_behaviour(PriorityEvaluationBehaviour())
        self.add_behaviour(SchedulePlanningBehaviour())
        
        # Cyclic behaviours run periodically
        self.add_behaviour(ReschedulingBehaviour())
        self.add_behaviour(ReminderManagementBehaviour())
        
        print(f"[AGENT] Agent setup complete: 5 behaviours registered\n")
    
    def mark_task_progress(self, task_id: str, minutes_done: int) -> None:
        """
        Public API: Mark progress on a task and trigger rescheduling.
        
        Args:
            task_id: ID of task to update
            minutes_done: Minutes of work completed
        """
        if task_id not in self.memory.tasks:
            print(f"[AGENT] Error: Task {task_id} not found")
            return
        
        mark_progress(self.memory, task_id, minutes_done)
        self.trigger_reschedule = True
        print(f"[AGENT] Progress recorded: {task_id} -{minutes_done}min")
    
    def get_plan(self) -> Optional[Plan]:
        """Get current study plan."""
        return self.memory.plan
    
    def get_reminders(self) -> List[str]:
        """Get current reminders."""
        return self.current_reminders
    
    async def stop(self):
        """SPADE lifecycle: Cleanup when agent stops."""
        if SPADE_AVAILABLE and hasattr(super(), 'stop'):
            await super().stop()
