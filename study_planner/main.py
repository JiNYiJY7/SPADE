from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import datetime

from .memory import AgentMemory
from .behaviours.task_management import add_tasks, set_free_slots, mark_progress
from .behaviours.priority_evaluation import rank_tasks
from .behaviours.schedule_planning import build_plan
from .behaviours.rescheduling import reschedule
from .behaviours.reminder_management import generate_reminders


def load_input_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def print_ranked(tasks_sorted):
    print("\n=== Ranked Tasks ===")
    for index, task in enumerate(tasks_sorted, 1):
        print(f"{index}. {task.title} | due={task.due} | importance={task.importance} | remaining={task.remaining_minutes}min")


def print_plan(plan):
    print("\n=== Study Plan ===")
    if not plan.sessions:
        print("(No sessions scheduled)")
        return
    for session in plan.sessions:
        print(f"{session.start} -> {session.end} | {session.title} ({session.minutes} min)")


def print_reminders(reminders):
    print("\n=== Reminders ===")
    if not reminders:
        print("(No reminders)")
        return
    for reminder in reminders:
        print(reminder)


def print_logs(memory: AgentMemory):
    print("\n=== Agent Logs ===")
    for line in memory.history:
        print(f"- {line}")


def main():
    parser = argparse.ArgumentParser(description="Smart Academic Planning Agent (Simulated)")
    parser.add_argument("--input", type=str, default="", help="Path to input JSON")
    parser.add_argument("--progress_task_id", type=str, default="", help="Task ID to mark progress")
    parser.add_argument("--progress_minutes", type=int, default=0, help="Minutes completed for progress update")
    parser.add_argument("--reschedule", action="store_true", help="Trigger rescheduling after updates")
    args = parser.parse_args()

    memory = AgentMemory()
    now = datetime.now()

    # Load data
    if args.input:
        data = load_input_json(Path(args.input))
    else:
        # Default demo data
        data = {
            "tasks": [
                {"id": "A1", "title": "NLP Assignment", "due": "2026-01-05T23:59:00", "est_minutes": 300, "importance": 5},
                {"id": "Q1", "title": "Quiz Revision", "due": "2026-01-04T18:00:00", "est_minutes": 120, "importance": 4},
            ],
            "free_slots": [
                {"start": "2026-01-02T20:00:00", "end": "2026-01-02T23:00:00"},
                {"start": "2026-01-03T14:00:00", "end": "2026-01-03T18:00:00"},
            ],
        }

    add_tasks(memory, data["tasks"])
    set_free_slots(memory, data["free_slots"])

    # Initial plan
    tasks_sorted = rank_tasks(memory, now)
    plan = build_plan(memory, tasks_sorted, now)

    # Optional progress update
    if args.progress_task_id and args.progress_minutes > 0:
        mark_progress(memory, args.progress_task_id, args.progress_minutes)
        if args.reschedule:
            plan = reschedule(memory, now)
            tasks_sorted = rank_tasks(memory, now)

    # Output
    print_ranked(tasks_sorted)
    print_plan(plan)
    reminders = generate_reminders(tasks_sorted, now)
    print_reminders(reminders)
    print_logs(memory)


if __name__ == "__main__":
    main()
