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
    for t in tasks_sorted:
        if t.remaining_minutes <= 0:
            continue
        hours_left = (t.due - now).total_seconds() / 3600.0
        lvl = reminder_level(hours_left)
        reminders.append(
            f"[{lvl}] {t.title} | due in {hours_left:.1f}h | remaining {t.remaining_minutes}min"
        )
    return reminders
