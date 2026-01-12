"""
SPADE Offline Demo Runner

Demonstrates Phase 3 intelligent agent implementation using SPADE framework.
Runs WITHOUT requiring XMPP infrastructure (simulated locally).

Purpose:
- Illustrates SPADE agent and behaviour usage in a controlled offline demo
- Provides a reproducible Phase 3 demonstration for academic evaluation
- Shows shared memory patterns, task scheduling, and monitoring behaviours

Usage:
    python -m study_planner.run_spade_demo [--input INPUT_JSON] [--progress]

Key Features:
- Offline demonstration (no XMPP credentials required)
- Behaviour execution order is shown explicitly for clarity
- Progress updates and rescheduling simulation included
- Full agent state displayed at the end
"""

from __future__ import annotations
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from .spade_agent import StudyPlannerAgent(Agent)
from .utils.time_utils import parse_iso


def load_input_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file containing tasks and free time slots.

    Why:
    - Separates I/O from agent logic for testability and clarity
    - Converts external input to a structured dictionary
    """
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


def get_default_input() -> Dict[str, Any]:
    """
    Provide default demo tasks and free slots when no input file is given.
    Why:
    - Ensures offline demo runs without external dependencies
    - Demonstrates a realistic academic scheduling scenario
    - Supports multiple task types and varying urgencies
    """
    return {
        "tasks": [
            {
                "id": "NLP-A1",
                "title": "NLP Assignment: Tokenization",
                "due": "2026-01-05T23:59:00",
                "est_minutes": 300,
                "importance": 5,
                "subject": "Natural Language Processing"
            },
            {
                "id": "QUIZ-Q1",
                "title": "Quiz: Linear Algebra Revision",
                "due": "2026-01-04T18:00:00",
                "est_minutes": 120,
                "importance": 4,
                "subject": "Mathematics"
            },
            {
                "id": "PROJ-P1",
                "title": "Project: Database Design",
                "due": "2026-01-08T23:59:00",
                "est_minutes": 480,
                "importance": 4,
                "subject": "Database Systems"
            },
            {
                "id": "READ-R1",
                "title": "Chapter 5-6 Reading: Data Structures",
                "due": "2026-01-06T23:59:00",
                "est_minutes": 180,
                "importance": 2,
                "subject": "Computer Science"
            }
        ],
        "free_slots": [
            {"start": "2026-01-02T20:00:00", "end": "2026-01-02T23:00:00"},
            {"start": "2026-01-03T14:00:00", "end": "2026-01-03T18:00:00"},
            {"start": "2026-01-03T20:00:00", "end": "2026-01-03T23:00:00"},
            {"start": "2026-01-04T10:00:00", "end": "2026-01-04T12:00:00"},
        ]
    }


async def run_agent_demo(
    input_data: Optional[Dict[str, Any]] = None,
    reference_time: Optional[datetime] = None,
    demo_progress: bool = False
) -> StudyPlannerAgent:
    """
    Run the StudyPlannerAgent in offline demo mode.

    Execution flow:
    1. Create the agent with input data
    2. Setup behaviours (OneShot + Cyclic)
    3. Execute behaviours sequentially for demonstration
    4. Optionally simulate progress updates and rescheduling
    5. Display final agent state

    Args:
        input_data: Dictionary with tasks and free slots
        reference_time: Base datetime for planning and scheduling
        demo_progress: If True, simulate task progress and rescheduling

    Returns:
        Configured StudyPlannerAgent
    """

    # Use default demo input if none provided
    if input_data is None:
        input_data = get_default_input()

    # Reference time ensures reproducibility of demo output
    if reference_time is None:
        reference_time = datetime.fromisoformat("2026-01-02T20:00:00")

    # Initialize SPADE agent with shared memory and input
    agent = StudyPlannerAgent(
        jid="planner@localhost",
        password="offline_demo",
        input_data=input_data,
        reference_time=reference_time
    )

    print("=" * 70)
    print("PHASE 3: SPADE-BASED INTELLIGENT AGENT DEMO")
    print("=" * 70)
    print(f"Reference Time: {reference_time}")
    print(f"Tasks to Process: {len(input_data['tasks'])}")
    print(f"Available Slots: {len(input_data['free_slots'])}")
    print("=" * 70)

    try:
        # Setup agent behaviours (initialization)
        await agent.setup()

        # Execute behaviours sequentially for offline demo clarity
        await _execute_behaviours_sequentially(agent)

        # Optional progress update simulation
        if demo_progress and agent.memory.tasks:
            print("\n" + "=" * 70)
            print("PROGRESS UPDATE SIMULATION")
            print("=" * 70)

            # Pick first task to simulate partial completion
            first_task_id = list(agent.memory.tasks.keys())[0]
            agent.mark_task_progress(first_task_id, 90)

            # Execute rescheduling behaviour after progress update
            await _execute_rescheduling(agent)

        # Display final agent state: tasks, plan, reminders, logs
        print("\n" + "=" * 70)
        print("AGENT FINAL STATE")
        print("=" * 70)
        _display_agent_state(agent)

        return agent

    except Exception as e:
        print(f"[ERROR] Demo execution failed: {e}")
        raise
    finally:
        # Attempt clean shutdown (ignore errors in demo mode)
        try:
            await agent.stop()
        except Exception:
            pass


async def _execute_behaviours_sequentially(agent: StudyPlannerAgent) -> None:
    """
    Execute registered behaviours sequentially for demo purposes.

    Why:
    - Real SPADE executes behaviours concurrently via event loop
    - Offline demo runs sequentially to show exact flow and cause-effect
    - Provides academic demonstration of OneShot vs Cyclic behaviours
    """

    print("\n[DEMO] Executing OneShot Behaviours (initialization phase)...")
    for behaviour in agent._behaviours:
        # Detect behaviour type via class inheritance chain
        parent_names = [c.__name__ for c in behaviour.__class__.__mro__[1:]]
        if 'OneShotBehaviour' in parent_names:
            try:
                await behaviour.run()
                await asyncio.sleep(0.1)  # yield control for readability
            except Exception as e:
                print(f"  Error in {behaviour.__class__.__name__}: {e}")

    print("\n[DEMO] Executing Cyclic Behaviours (monitoring phase)...")
    for behaviour in agent._behaviours:
        parent_names = [c.__name__ for c in behaviour.__class__.__mro__[1:]]
        if 'CyclicBehaviour' in parent_names:
            try:
                await behaviour.run()
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"  Error in {behaviour.__class__.__name__}: {e}")


async def _execute_rescheduling(agent: StudyPlannerAgent) -> None:
    """
    Execute rescheduling behaviour after progress update.

    Why:
    - Demonstrates dynamic adaptation of schedule
    - Shows agent can respond to state changes at runtime
    """
    print("\n[DEMO] Executing rescheduling after progress update...")
    for behaviour in agent._behaviours:
        if 'Rescheduling' in behaviour.__class__.__name__:
            await behaviour.run()
            break


def _display_agent_state(agent: StudyPlannerAgent) -> None:
    """
    Display full agent state for demo output.

    Shows:
    - Current tasks with status
    - Generated study plan
    - Active reminders
    - Agent activity log

    Why:
    - Provides transparency and traceability
    - Demonstrates correctness of behaviours and shared memory
    """
    memory = agent.memory

    print("\nCurrent Tasks:")
    if not memory.tasks:
        print("  (No tasks)")
    else:
        for task_id, task in sorted(memory.tasks.items()):
            status = "[DONE]" if task.remaining_minutes <= 0 else "[TODO]"
            print(f"  {status} [{task.importance}*] {task.title}")
            print(f"      Due: {task.due} | Remaining: {task.remaining_minutes} min")

    print("\nStudy Plan:")
    if not memory.plan or not memory.plan.sessions:
        print("  (No sessions scheduled)")
    else:
        print(f"  Generated: {memory.plan.generated_at}")
        for session in memory.plan.sessions:
            print(f"  • {session.start.strftime('%Y-%m-%d %H:%M')} - "
                  f"{session.end.strftime('%H:%M')} ({session.minutes}min)")
            print(f"    {session.title}")

    print("\nActive Reminders:")
    if not agent.current_reminders:
        print("  (No reminders)")
    else:
        for reminder in agent.current_reminders:
            print(f"  [!] {reminder}")

    print("\nAgent Activity Log:")
    if not memory.history:
        print("  (No activity)")
    else:
        for entry in memory.history:
            print(f"  • {entry}")


def main():
    """
    Entry point for SPADE offline demo.

    Demonstrates:
    - SPADE agent and behaviour registration
    - Shared memory usage
    - Offline execution for academic evaluation
    - Progress update and rescheduling simulation

    Why:
    - Encapsulates demo logic and argument parsing
    - Provides reproducible Phase 3 SPADE demonstration
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="SPADE Intelligent Agent Demo (Offline)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python -m study_planner.run_spade_demo\n"
               "  python -m study_planner.run_spade_demo --input tasks.json\n"
               "  python -m study_planner.run_spade_demo --progress\n"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="",
        help="Path to input JSON file with tasks and free slots"
    )

    parser.add_argument(
        "--progress",
        action="store_true",
        help="Simulate progress update and rescheduling"
    )

    args = parser.parse_args()

    # Load input data from file or use default demo dataset
    try:
        if args.input:
            input_data = load_input_json(args.input)
        else:
            input_data = get_default_input()
    except Exception as e:
        print(f"Error loading input: {e}")
        return

    # Run the SPADE agent demo
    try:
        asyncio.run(run_agent_demo(
            input_data=input_data,
            reference_time=datetime.fromisoformat("2026-01-02T20:00:00"),
            demo_progress=args.progress
        ))
    except KeyboardInterrupt:
        print("\n[Demo] Interrupted by user")
    except Exception as e:
        print(f"\n[Error] Demo failed: {e}")
        raise


if __name__ == "__main__":
    main()
