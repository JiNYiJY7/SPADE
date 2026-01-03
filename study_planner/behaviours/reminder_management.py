from __future__ import annotations
from datetime import datetime
from typing import List
from ..models import Task


def reminder_level(hours_left: float) -> str:
    if hours_left <= 6:
        return "HIGH (every 30-60 min)"
    if hours_left <= 24:
        return "MEDIUM (every 2-3 hours)"
    if hours_left <= 72:
        return "LOW (daily)"
    return "INFO (every few days)"


def generate_reminders(tasks_sorted: List[Task], now: datetime) -> List[str]:
    reminders = []
    for task in tasks_sorted:
        if task.remaining_minutes <= 0:
            continue
        hours_left = (task.due - now).total_seconds() / 3600.0
        reminder_level_str = reminder_level(hours_left)
        reminders.append(
            f"[{reminder_level_str}] {task.title} | due in {hours_left:.1f}h | remaining {task.remaining_minutes}min"
        )
    return reminders
