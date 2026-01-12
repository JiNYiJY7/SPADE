"""
Command-line entry point for the Smart Academic Planning Agent.

This module simulates how an intelligent agent:
- Loads task and availability data
- Evaluates task priorities
- Builds and updates a study plan
- Generates reminders
- Logs internal decision-making for transparency

It is designed as a CLI interface to demonstrate the full agent workflow.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime

from .memory import AgentMemory
from .behaviours.task_management import (
    add_tasks,
    set_free_slots,
    mark_progress,
)
from .behaviours.priority_evaluation import rank_tasks
from .behaviours.schedule_planning import build_plan
from .behaviours.rescheduling import reschedule
from .behaviours.reminder_management import generate_reminders


def load_input_json(file_path: Path) -> dict:
    """
    Load task and scheduling input data from a JSON file.

    This function exists to isolate file I/O logic from agent logic,
    making the system easier to test and extend (e.g. API or UI input).
    """

    return json.loads(file_path.read_text(encoding="utf-8"))


def display_ranked_tasks(prioritized_tasks) -> None:
    """
    Display tasks in priority order for inspection and debugging.

    This output allows users and evaluators to verify that
    the priority evaluation logic behaves as expected.
    """

    print("\n=== Ranked Tasks ===")
    for index, task in enumerate(prioritized_tasks, start=1):
        print(
            f"{index}. {task.title} | "
            f"due={task.due} | "
            f"importance={task.importance} | "
            f"remaining={task.remaining_minutes} min"
        )


def display_plan(execution_plan) -> None:
    """
    Display the generated study plan in a human-readable format.

    This function exists to bridge internal scheduling logic
    with user-facing output for validation and demonstration.
    """

    print("\n=== Study Plan ===")

    # Explicitly handle empty plans to avoid confusing output
    if not execution_plan.sessions:
        print("(No sessions scheduled)")
        return

    for session in execution_plan.sessions:
        print(
            f"{session.start} -> {session.end} | "
            f"{session.title} ({session.minutes} min)"
        )


def display_reminders(reminder_messages) -> None:
    """
    Display generated reminders.

    This output demonstrates how urgency-based logic
    translates into actionable user notifications.
    """

    print("\n=== Reminders ===")

    if not reminder_messages:
        print("(No reminders)")
        return

    for reminder in reminder_messages:
        print(reminder)


def display_agent_logs(memory: AgentMemory) -> None:
    """
    Display the agent's internal decision logs.

    Logs exist to provide transparency, traceability,
    and debugging insight into agent behaviour.
    """

    print("\n=== Agent Logs ===")
    for log_entry in memory.history:
        print(f"- {log_entry}")


def main() -> None:
    """
    Main execution function for the Smart Academic Planning Agent.

    This function orchestrates the entire agent lifecycle:
    - Input parsing
    - Memory initialization
    - Task loading
    - Planning and rescheduling
    - Output generation
    """

    # Argument parsing enables flexible simulation without code changes
    parser = argparse.ArgumentParser(
        description="Smart Academic Planning Agent (Simulated)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="",
        help="Path to input JSON file",
    )
    parser.add_argument(
        "--progress_task_id",
        type=str,
        default="",
        help="Task ID to update progress for",
    )
    parser.add_argument(
        "--progress_minutes",
        type=int,
        default=0,
        help="Minutes completed for progress update",
    )
    parser.add_argument(
        "--reschedule",
        action="store_true",
        help="Trigger rescheduling after progress update",
    )
    args = parser.parse_args()

    # Initialize agent memory to store tasks, plans, and logs
    memory = AgentMemory()

    # Capture current time once to keep all decisions consistent
    current_time = datetime.now()

    # Load input data either from file or built-in demo data
    if args.input:
        input_data = load_input_json(Path(args.input))
    else:
        # Default dataset allows the system to run without external files,
        # useful for demos, testing, and grading
        input_data = {
            "tasks": [
                {
                    "id": "A1",
                    "title": "NLP Assignment",
                    "due": "2026-01-05T23:59:00",
                    "est_minutes": 300,
                    "importance": 5,
                },
                {
                    "id": "Q1",
                    "title": "Quiz Revision",
                    "due": "2026-01-04T18:00:00",
                    "est_minutes": 120,
                    "importance": 4,
                },
            ],
            "free_slots": [
                {
                    "start": "2026-01-02T20:00:00",
                    "end": "2026-01-02T23:00:00",
                },
                {
                    "start": "2026-01-03T14:00:00",
                    "end": "2026-01-03T18:00:00",
                },
            ],
        }

    # Populate agent memory with tasks and availability
    add_tasks(memory, input_data["tasks"])
    set_free_slots(memory, input_data["free_slots"])

    # Initial planning phase: evaluate priorities, then schedule
    prioritized_tasks = rank_tasks(memory, current_time)
    execution_plan = build_plan(memory, prioritized_tasks, current_time)

    # Optional progress update simulates real-world user interaction
    if args.progress_task_id and args.progress_minutes > 0:
        mark_progress(
            memory,
            args.progress_task_id,
            args.progress_minutes,
        )

        # Rescheduling is optional to avoid unnecessary recomputation
        if args.reschedule:
            execution_plan = reschedule(memory, current_time)
            prioritized_tasks = rank_tasks(memory, current_time)

    # Output results for inspection and demonstration
    display_ranked_tasks(prioritized_tasks)
    display_plan(execution_plan)

    reminder_messages = generate_reminders(
        prioritized_tasks,
        current_time,
    )
    display_reminders(reminder_messages)
    display_agent_logs(memory)


# Entry-point guard ensures this script only runs when executed directly
if __name__ == "__main__":
    main()
